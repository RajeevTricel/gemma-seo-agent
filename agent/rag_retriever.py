from pathlib import Path
import re
from typing import List, Dict


RAG_DIR = Path("rag")


ROUTE_RULES = {
    "rag/seo/technical_seo_runbook.md": [
        "noindex", "robots", "robots.txt", "canonical", "canonicals",
        "sitemap", "redirect", "redirects", "404", "500", "crawl",
        "indexation", "indexed", "blocked", "internal links", "duplicate title",
        "duplicate meta", "javascript rendering", "js rendering"
    ],
    "rag/seo/programmatic_seo_safety.md": [
        "programmatic", "pseo", "location pages", "city pages",
        "service area pages", "generated pages", "ai pages",
        "same copy", "duplicate templates", "doorway", "thin pages",
        "scale pages", "5000", "5,000", "thousands of pages"
    ],
    "rag/seo/pagespeed_priority_guide.md": [
        "pagespeed", "page speed", "core web vitals", "cwv",
        "lcp", "inp", "cls", "slow", "performance", "load time",
        "hero image", "unused javascript", "render blocking", "cache",
        "caching", "third-party scripts"
    ],
    "rag/seo/gsc_ga4_diagnosis.md": [
        "gsc", "search console", "ga4", "analytics",
        "clicks", "impressions", "ctr", "average position",
        "position", "rankings", "traffic dropped", "sessions",
        "organic sessions", "landing pages", "queries", "query"
    ],
    "rag/marketing/cro_content_refresh.md": [
        "cro", "conversion", "conversions", "leads", "form submissions",
        "cta", "trust signals", "value proposition", "content refresh",
        "service page", "not converting", "copy", "landing page",
        "case studies", "testimonials"
    ],
}


def load_markdown_docs(rag_dir: Path = RAG_DIR) -> List[Dict[str, str]]:
    docs = []

    for path in rag_dir.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        docs.append({
            "path": str(path),
            "title": path.stem.replace("_", " ").title(),
            "content": text
        })

    return docs


def tokenize(text: str) -> set:
    return set(re.findall(r"[a-zA-Z0-9]+", text.lower()))


def keyword_route_score(query: str, doc_path: str) -> int:
    query_lower = query.lower()
    route_terms = ROUTE_RULES.get(doc_path, [])

    score = 0

    for term in route_terms:
        if term in query_lower:
            score += 10

    # Strong domain-specific boosts so the primary SEO topic wins
    pagespeed_terms = ["pagespeed", "page speed", "core web vitals", "cwv", "lcp", "inp", "cls", "slow", "load time"]
    technical_terms = ["noindex", "robots", "robots.txt", "canonical", "sitemap", "redirect", "crawl", "indexation"]
    pseo_terms = ["programmatic", "pseo", "location pages", "city pages", "same copy", "doorway", "thin pages", "5,000", "5000"]
    gsc_terms = ["gsc", "search console", "clicks", "impressions", "ctr", "average position", "queries"]
    cro_terms = ["conversion", "conversions", "leads", "cta", "not convert", "form submissions"]

    if doc_path == "rag/seo/pagespeed_priority_guide.md" and any(t in query_lower for t in pagespeed_terms):
        score += 25

    if doc_path == "rag/seo/technical_seo_runbook.md" and any(t in query_lower for t in technical_terms):
        score += 25

    if doc_path == "rag/seo/programmatic_seo_safety.md" and any(t in query_lower for t in pseo_terms):
        score += 25

    if doc_path == "rag/seo/gsc_ga4_diagnosis.md" and any(t in query_lower for t in gsc_terms):
        score += 25

    if doc_path == "rag/marketing/cro_content_refresh.md" and any(t in query_lower for t in cro_terms):
        score += 15

    return score


def overlap_score(query: str, doc_text: str) -> int:
    query_terms = tokenize(query)
    doc_terms = tokenize(doc_text)

    overlap = query_terms.intersection(doc_terms)
    return len(overlap)


def score_doc(query: str, doc: Dict[str, str]) -> int:
    route_score = keyword_route_score(query, doc["path"])
    text_score = overlap_score(query, doc["content"] + " " + doc["title"])

    return route_score + text_score


def retrieve_context(query: str, top_k: int = 2) -> List[Dict[str, str]]:
    docs = load_markdown_docs()

    scored = []
    for doc in docs:
        score = score_doc(query, doc)
        scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)

    results = []
    for score, doc in scored[:top_k]:
        if score > 0:
            results.append({
                "path": doc["path"],
                "title": doc["title"],
                "score": score,
                "content": doc["content"]
            })

    return results


def build_context_block(query: str, top_k: int = 2, max_chars: int = 2500) -> str:
    results = retrieve_context(query, top_k=top_k)

    if not results:
        return "No relevant RAG context found."

    parts = []

    for item in results:
        content = item["content"][:max_chars]

        parts.append(
            f"Source: {item['path']}\n"
            f"Title: {item['title']}\n"
            f"Relevance score: {item['score']}\n"
            f"Relevant guidance:\n{content}"
        )

    return "\n\n---\n\n".join(parts)


if __name__ == "__main__":
    test_queries = [
        "Can we generate 5,000 location pages with the same copy?",
        "The crawl says 20 important pages are noindex. What should we do first?",
        "The PageSpeed score is low but conversions are up. Should we still fix it?",
        "Clicks dropped 30%, impressions stayed stable, and CTR dropped. What does this mean?",
        "This service page ranks but does not convert. What should we change?"
    ]

    for query in test_queries:
        print("=" * 80)
        print("QUERY:", query)
        print("-" * 80)
        results = retrieve_context(query, top_k=2)

        for result in results:
            print(f"{result['path']} | score={result['score']}")

        print()
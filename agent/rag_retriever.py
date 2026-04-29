from pathlib import Path
import re
from typing import List, Dict


RAG_DIR = Path("rag")


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


def score_doc(query: str, doc_text: str) -> int:
    query_terms = tokenize(query)
    doc_terms = tokenize(doc_text)

    overlap = query_terms.intersection(doc_terms)
    return len(overlap)


def retrieve_context(query: str, top_k: int = 3) -> List[Dict[str, str]]:
    docs = load_markdown_docs()

    scored = []
    for doc in docs:
        score = score_doc(query, doc["content"] + " " + doc["title"])
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


def build_context_block(query: str, top_k: int = 3, max_chars: int = 3500) -> str:
    results = retrieve_context(query, top_k=top_k)

    if not results:
        return "No relevant RAG context found."

    parts = []

    for item in results:
        content = item["content"][:max_chars]

        parts.append(
            f"Source: {item['path']}\n"
            f"Title: {item['title']}\n"
            f"Relevant guidance:\n{content}"
        )

    return "\n\n---\n\n".join(parts)


if __name__ == "__main__":
    query = "Can we generate 5000 location pages with the same copy?"
    context = build_context_block(query)
    print(context)
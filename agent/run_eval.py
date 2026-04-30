import json
from agent.seo_agent import load_model, seo_agent, has_all_headings


EVAL_PATH = "data/eval_prompts.jsonl"


def load_eval_prompts(path=EVAL_PATH):
    prompts = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                prompts.append(json.loads(line))

    return prompts

def section_lengths_ok(response: str, max_words_per_section: int = 60) -> bool:
    sections = ["Diagnosis:", "Evidence:", "Priority:", "Fix:", "Next action:"]
    
    for i, heading in enumerate(sections):
        start = response.find(heading)
        if start == -1:
            return False

        end = len(response)
        if i + 1 < len(sections):
            next_heading = response.find(sections[i + 1])
            if next_heading != -1:
                end = next_heading

        section_text = response[start:end]
        word_count = len(section_text.split())

        if word_count > max_words_per_section:
            return False

    return True


def has_bad_phrases(response: str) -> bool:
    bad_patterns = [
        "Positionand",
        "AvgPositionchange",
        "innoindexed",
        "guaranteed ranking",
        "rank #1",
        "exact cause",
        "definitely caused by Google",
    ]

    response_lower = response.lower()

    return any(pattern.lower() in response_lower for pattern in bad_patterns)


def quality_check(response: str) -> tuple[bool, list[str]]:
    issues = []

    if not has_all_headings(response):
        issues.append("missing required headings")

    if not section_lengths_ok(response):
        issues.append("section too long")

    if has_bad_phrases(response):
        issues.append("bad or malformed phrase detected")

    return len(issues) == 0, issues


def main():
    prompts = load_eval_prompts()

    print(f"Loaded {len(prompts)} eval prompts")

    model, tokenizer = load_model()

    passed = 0
    failed = 0

    for i, item in enumerate(prompts, start=1):
        prompt = item["prompt"]
        category = item.get("category", "unknown")

        print("=" * 80)
        print(f"Eval {i} | Category: {category}")
        print(f"Prompt: {prompt}")
        print("-" * 80)

        response = seo_agent(model, tokenizer, prompt, use_rag=True)

        print(response)

        ok, issues = quality_check(response)

        if ok:
            print("Result: ✅ PASS")
            passed += 1
        else:
            print("Result: ❌ FAIL")
            print("Issues:", ", ".join(issues))
            failed += 1

    print("=" * 80)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")


if __name__ == "__main__":
    main()
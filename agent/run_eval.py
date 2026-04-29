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

        if has_all_headings(response):
            print("Result: ✅ PASS")
            passed += 1
        else:
            print("Result: ❌ FAIL")
            failed += 1

    print("=" * 80)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")


if __name__ == "__main__":
    main()
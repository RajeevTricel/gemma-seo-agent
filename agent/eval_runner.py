import json
import re
from pathlib import Path

REQUIRED_HEADINGS = [
    "Diagnosis:",
    "Evidence:",
    "Priority:",
    "Fix:",
    "Next action:",
]


def normalize_headings(text: str) -> str:
    text = text.strip()
    replacements = {
        r"Diagnosis\s*:": "Diagnosis:",
        r"Evidence\s*:": "Evidence:",
        r"Priority\s*:": "Priority:",
        r"Fix\s*:": "Fix:",
        r"Next action\s*:": "Next action:",
        r"Next action\s*\n": "Next action:\n",
    }

    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text


def check_headings(response: str) -> dict:
    response = normalize_headings(response)

    result = {
        "has_all_headings": all(h in response for h in REQUIRED_HEADINGS),
        "missing_headings": [h for h in REQUIRED_HEADINGS if h not in response],
        "duplicate_headings": [h for h in REQUIRED_HEADINGS if response.count(h) > 1],
    }

    return result


def load_eval_prompts(path: str = "data/eval_prompts.jsonl") -> list[dict]:
    prompts = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                prompts.append(json.loads(line))

    return prompts


def main():
    prompts = load_eval_prompts()

    print(f"Loaded {len(prompts)} eval prompts")
    print("This script currently validates eval file structure only.")
    print("Model inference evaluation should be run from the inference notebook.")

    for i, item in enumerate(prompts, start=1):
        assert "prompt" in item, f"Line {i}: missing prompt"
        assert "category" in item, f"Line {i}: missing category"
        assert "expected_headings" in item, f"Line {i}: missing expected_headings"

    print("✅ eval_prompts.jsonl structure is valid")


if __name__ == "__main__":
    main()
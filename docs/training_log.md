# Training Log

## Run 1 — Pipeline test
- Dataset: 3 examples
- Model: google/gemma-4-E2B-it
- Method: QLoRA/LoRA
- Result: Training worked, but output repeated "HereHereHere"
- Conclusion: Pipeline valid, dataset too small

## Run 2 — Clean 30-example dataset
- Dataset: data/train.jsonl
- Examples: 30
- Model: google/gemma-4-E2B-it
- Method: QLoRA/LoRA
- Result: Output improved and avoided repetition
- Issues:
  - Does not always follow required headings
  - Sometimes gives too much framework text
  - Missing-data prompts need stronger examples
- Next step:
  - Add Batch 3 examples
  - Target total: 100 examples
  - Improve strict format following:
    Diagnosis:
    Evidence:
    Priority:
    Fix:
    Next action:
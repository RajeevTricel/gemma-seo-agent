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

## Run 3 — 100-example strict-format dataset

- Dataset: data/train.jsonl
- Examples: 100
- Model: google/gemma-4-E2B-it
- Method: QLoRA / LoRA
- Steps: 100
- Training loss: dropped from ~4.70 to ~1.71
- Adapter pushed to Hugging Face:
  - RajeevSK25/gemma4-e2b-seo-lora
- Result:
  - Strong improvement over 3-example and 30-example runs
  - Can produce SEO/marketing answers with required headings under stricter prompting
- Remaining issues:
  - Sometimes stops after Evidence without scaffolded prompting
  - PageSpeed vs conversion tradeoff examples need more coverage
  - Some outputs are too long or slightly messy
  - Needs more concise examples
- Status:
  - Saved as v2-100-test milestone, not final
- Next step:
  - Batch 4 to expand dataset to 300 examples
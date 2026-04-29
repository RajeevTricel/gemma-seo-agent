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

## Run 4 — v3 300-example adapter

- Dataset: `data/train.jsonl`
- Examples: 300
- Model: `google/gemma-4-E2B-it`
- Method: QLoRA / LoRA
- Steps: 300
- Final training loss: ~1.247
- Runtime: ~6 min 55 sec
- Hugging Face repo: `RajeevSK25/gemma4-e2b-seo-lora-v3-300`

### What improved

- Stronger five-heading response format.
- Better PageSpeed vs conversion/business tradeoff reasoning.
- Better missing-data handling.
- Better programmatic SEO safety reasoning.
- Better technical SEO/indexation prioritisation.
- Less repetition than earlier runs.

### Evaluation results

Passed:
- “The PageSpeed score is low but conversions are up. Should we still fix it?”
- “Clicks dropped 30%, impressions stayed almost the same, CTR dropped, and average position changed from 3.8 to 4.1. What does this mean?”
- “We don’t have GSC access. Diagnose the ranking drop anyway.”
- “The crawl says 20 important pages are noindex. What should we do first?”

Partially failed:
- “Can we generate 5,000 location pages with the same copy?”

### Remaining issues

- Sometimes over-explains Diagnosis/Evidence and runs out before `Priority`, `Fix`, or `Next action`.
- Programmatic SEO prompts still need more concise safety examples.
- Some outputs continue with extra text after the first complete answer.
- Inference cleanup is still needed to keep only the first complete five-heading answer.

### Current status

`v3-300` is the best current adapter and should be saved as a milestone, but it is not final.

### Next step

Create Batch 5 with 100 focused examples targeting:
- strict five-heading completion
- one short sentence per heading
- programmatic SEO safety
- technical SEO/indexation cases
- missing-data prompts that still complete all headings
- PageSpeed/business tradeoff in concise format

Target next model: `v4-400`.
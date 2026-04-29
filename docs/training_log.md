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


## Run 5 — v4 400-example adapter

- Dataset: `data/train.jsonl`
- Examples: 400
- Model: `google/gemma-4-E2B-it`
- Platform: Kaggle T4 x2
- Method: QLoRA / LoRA
- Steps: 200
- Final training loss: ~1.31
- Hugging Face repo: `RajeevSK25/gemma4-e2b-seo-lora-v4-400`

### What improved

- Stronger completion of all five required headings.
- Better programmatic SEO safety responses.
- Better technical SEO/noindex responses.
- Better missing-data handling when GSC is unavailable.
- Better PageSpeed vs conversion/business tradeoff handling.
- More concise outputs than v3.

### Evaluation results

Passed:
- “Can we generate 5,000 location pages with the same copy?”
- “The crawl says 20 important pages are noindex. What should we do first?”
- “We don’t have GSC access. Diagnose the ranking drop anyway.”
- “The PageSpeed score is low but conversions are up. Should we still fix it?”

### Important inference note

After training, one test initially produced random repeated tokens. Setting the model to evaluation mode, disabling gradient checkpointing, and enabling cache fixed the generation behaviour.

Recommended inference setup:
- `trainer.model.eval()`
- `trainer.model.gradient_checkpointing_disable()`
- `trainer.model.config.use_cache = True`
- Use deterministic generation with `do_sample=False`
- Use heading normalisation/cleanup in the inference layer

### Current status

`v4-400` is the best current adapter and can be used as the main milestone model.

### Next step

Create an inference notebook/script that loads the Hugging Face adapter fresh and applies the production prompt + cleanup function.

## Inference notebook — v4 adapter

- Notebook: `notebooks/03_inference_gemma_seo_lora.ipynb`
- Adapter: `RajeevSK25/gemma4-e2b-seo-lora-v4-400`
- Purpose: Load base Gemma E2B + v4 LoRA adapter without retraining.
- Result: Production wrapper successfully controls output format.
- Important inference controls:
  - deterministic generation with `do_sample=False`
  - short-section prompt
  - heading normalisation
  - retry if required headings are missing
  - cleanup for repeated assistant/system continuations
- Passed previous failure prompts:
  - noindex technical SEO prompt
  - missing GSC access prompt

## RAG inference update

- Connected `agent/rag_retriever.py` to the v4 inference notebook.
- The assistant now retrieves relevant markdown guidance before generating.
- Initial tests passed heading checks for:
  - programmatic SEO/location-page safety
  - noindex technical SEO
  - PageSpeed vs conversion tradeoff
  - GSC/CTR interpretation
- Known issue:
  - simple keyword retrieval can sometimes inject slightly broad or imperfect context.
- Next retrieval improvement:
  - add keyword routing so noindex/canonical/robots prompts prefer `technical_seo_runbook.md`
  - location/programmatic prompts prefer `programmatic_seo_safety.md`
  - PageSpeed prompts prefer `pagespeed_priority_guide.md`
  - GSC/GA4 prompts prefer `gsc_ga4_diagnosis.md`

## Fresh inference verification — v4 + RAG

- Verified that `google/gemma-4-E2B-it` can be loaded fresh with adapter `RajeevSK25/gemma4-e2b-seo-lora-v4-400`.
- Verified that RAG context from `agent/rag_retriever.py` is injected before generation.
- Tested:
  - programmatic SEO/location-page safety
  - noindex technical SEO
  - PageSpeed vs conversion tradeoff
- All tests passed the required heading format:
  - Diagnosis
  - Evidence
  - Priority
  - Fix
  - Next action
- Current status: full training → adapter push → fresh inference → RAG flow is working.
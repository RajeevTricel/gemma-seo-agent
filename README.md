# Gemma SEO Agent

A cloud-only Gemma-based SEO and marketing assistant trained with QLoRA/LoRA.

## Current best model

- Base model: `google/gemma-4-E2B-it`
- Current adapter: `RajeevSK25/gemma4-e2b-seo-lora-v4-400`
- Training dataset: `data/train.jsonl`
- Examples: 400
- Status: working v4 milestone

## What the assistant does

The assistant gives evidence-led SEO and marketing recommendations using this strict format:

Diagnosis:
Evidence:
Priority:
Fix:
Next action:

It is trained to handle:
- SEO ranking drops
- GSC/GA4 interpretation
- PageSpeed/Core Web Vitals tradeoffs
- technical SEO and indexation issues
- programmatic SEO safety
- WooCommerce/Elementor SEO
- missing-data handling
- practical prioritisation by business impact

## Important notebooks

- `notebooks/01_finetune_gemma_qlora.ipynb`  
  Original Colab training notebook.

- `notebooks/02_train_gemma_kaggle_v4_400.ipynb`  
  Kaggle training notebook for the v4 400-example adapter.

- `notebooks/03_inference_gemma_seo_lora.ipynb`  
  Loads the Hugging Face adapter and tests inference without retraining.

## Current limitation

The model works best with the production inference wrapper. The wrapper:
- forces the five required headings
- keeps answers short
- normalises heading formatting
- cleans repeated model/system continuations
- retries if headings are missing

## Next development phase

The next phase is to build an agent layer around the model:
- add RAG documents
- add tool-calling schemas
- add evaluation prompts
- eventually connect APIs such as PageSpeed, GSC, GA4, and crawl data
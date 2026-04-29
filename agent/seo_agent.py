import argparse
import re
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

try:
    from agent.rag_retriever import build_context_block
except ImportError:
    from rag_retriever import build_context_block


BASE_MODEL_ID = "google/gemma-4-E2B-it"
ADAPTER_ID = "RajeevSK25/gemma4-e2b-seo-lora-v4-400"


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


def clean_first_complete_answer(text: str) -> str:
    text = normalize_headings(text)

    stop_markers = [
        "\nsystem\n",
        "\nmodel\n",
        "\ntype\n",
        "\nevidence\n",
        "\npriority\n",
        "\nfix\n",
        "\nnext action\n",
        "<start_of_turn>model",
        "<end_of_turn>",
    ]

    for marker in stop_markers:
        if marker in text:
            text = text.split(marker)[0].strip()

    second_diag = text.find("\nDiagnosis:", 5)
    if second_diag != -1:
        text = text[:second_diag].strip()

    return normalize_headings(text)


def has_all_headings(response: str) -> bool:
    required = ["Diagnosis:", "Evidence:", "Priority:", "Fix:", "Next action:"]
    return all(heading in response for heading in required)


def load_model():
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(ADAPTER_ID)

    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_ID,
        quantization_config=bnb_config,
        device_map="auto",
        dtype=torch.float16,
        trust_remote_code=True,
    )

    model = PeftModel.from_pretrained(base_model, ADAPTER_ID)

    model.eval()

    try:
        model.gradient_checkpointing_disable()
    except Exception:
        pass

    try:
        model.config.use_cache = True
    except Exception:
        pass

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    return model, tokenizer


def generate_response(model, tokenizer, messages, max_new_tokens: int = 220) -> str:
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            repetition_penalty=1.3,
            no_repeat_ngram_size=6,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )

    new_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
    raw_response = tokenizer.decode(new_tokens, skip_special_tokens=True)

    return clean_first_complete_answer(raw_response)


def seo_agent(model, tokenizer, user_prompt: str, use_rag: bool = True) -> str:
    rag_context = (
        build_context_block(user_prompt, top_k=2, max_chars=2000)
        if use_rag
        else "RAG disabled."
    )

    system_prompt = f"""You are an evidence-led SEO and marketing assistant.

Use the RAG context below as reference guidance when relevant.
Do not quote it blindly. Apply it to the user's situation.

RAG context:
{rag_context}

You must answer using exactly five headings:
Diagnosis:
Evidence:
Priority:
Fix:
Next action:

Hard rules:
- Each heading must be one short sentence only.
- Evidence must mention maximum 5 missing or provided evidence points.
- Do not create long comma-separated lists.
- Do not add extra sections.
- Stop after Next action.
- Do not mention paid ads, display ads, ad copy, ROAS, or non-organic channels unless the user provides paid-channel data.
- If data is missing, say what is missing but still complete all five headings.
- Prioritise by business impact."""

    forced_user_prompt = f"""{user_prompt}

Return exactly this format only:
Diagnosis: one short sentence.
Evidence: one short sentence with maximum 5 evidence points.
Priority: one short sentence.
Fix: one short sentence.
Next action: one short sentence.

Do not write anything after Next action."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": forced_user_prompt},
    ]

    response = generate_response(model, tokenizer, messages, max_new_tokens=220)

    if not has_all_headings(response):
        retry_prompt = f"""{user_prompt}

Complete every line below. Do not skip any line.

Diagnosis:
Evidence:
Priority:
Fix:
Next action:

Rules:
- Fill each line with one short sentence.
- Do not list more than 5 items.
- Stop after Next action."""

        retry_messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": retry_prompt},
        ]

        response = generate_response(model, tokenizer, retry_messages, max_new_tokens=260)

    return response


def main():
    parser = argparse.ArgumentParser(description="Run the Gemma SEO LoRA agent from terminal.")
    parser.add_argument("prompt", type=str, help="SEO/marketing question to answer.")
    parser.add_argument("--no-rag", action="store_true", help="Disable RAG context retrieval.")

    args = parser.parse_args()

    model, tokenizer = load_model()
    response = seo_agent(model, tokenizer, args.prompt, use_rag=not args.no_rag)

    print(response)


if __name__ == "__main__":
    main()
"""
Structured JSON output experiment (E4) for the SAMSum project.

Generates a machine-readable summary (summary + action_items) for each
baseline dialogue, parses and validates it against SUMMARY_SCHEMA, and
demonstrates recovery when the model returns invalid JSON:
  1. extract + parse + validate the first response
  2. on failure, issue one corrective repair prompt and re-validate
  3. if still invalid, fall back to a stub flagged for human review

A deliberately malformed string is also run through the validator so the
validation/error-handling path is demonstrated independently of the model.
"""

import json
import time
from pathlib import Path

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from prompts import structured_json_prompt
from structured_schema import parse_and_validate, validate_output


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

BASELINE_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "baseline_smoke_test"
    / "baseline_outputs.json"
)

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "structured_output"

MAX_NEW_TOKENS = 256

SYSTEM_PROMPT = (
    "You are a conversation summarization assistant. "
    "Return only valid JSON when asked."
)


# --------------------------------------------------
# LOAD EXISTING BASELINE EXAMPLES
# --------------------------------------------------

def load_baseline_examples(file_path):

    if not file_path.exists():
        raise FileNotFoundError(f"Baseline file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list) or not records:
        raise ValueError("Baseline JSON must contain a non-empty list.")

    return records


# --------------------------------------------------
# LOAD THE MODEL
# --------------------------------------------------

def load_model():

    print("\nLoading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    print("Loading model on CPU...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True,
    )
    model.eval()

    print("Model loaded successfully.")
    return tokenizer, model


# --------------------------------------------------
# GENERATION
# --------------------------------------------------

def generate(messages, tokenizer, model):
    """Greedy generation from a chat-message list. Returns raw text."""

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.inference_mode():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    new_tokens = output_ids[0, inputs["input_ids"].shape[1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


def generate_structured(dialogue, tokenizer, model):
    """Generate a structured output for one dialogue with recovery.

    Returns a result dict capturing the raw output, parse/validation
    outcome, whether a repair retry was needed and whether it succeeded,
    and the final object used (parsed or fallback stub).
    """

    user_prompt = structured_json_prompt(dialogue)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    start = time.time()
    raw_output = generate(messages, tokenizer, model)

    first = parse_and_validate(raw_output)

    recovered = False
    repair_attempted = False
    repair_raw = None
    final = first

    # Recovery: one corrective retry when the first response is invalid.
    if not (first["parse_ok"] and first["schema_valid"]):
        repair_attempted = True

        repair_messages = messages + [
            {"role": "assistant", "content": raw_output},
            {
                "role": "user",
                "content": (
                    "Your previous output was not valid JSON matching the "
                    "required schema. Return only a corrected JSON object "
                    "with string \"summary\" and a \"action_items\" list of "
                    "objects (owner, task, optional due). No other text."
                ),
            },
        ]

        repair_raw = generate(repair_messages, tokenizer, model)
        second = parse_and_validate(repair_raw)

        if second["parse_ok"] and second["schema_valid"]:
            recovered = True
            final = second

    # Fallback stub when both attempts fail, flagged for human review.
    used_fallback = not (final["parse_ok"] and final["schema_valid"])
    if used_fallback:
        final_object = {
            "summary": raw_output,
            "action_items": [],
            "_needs_review": True,
        }
    else:
        final_object = final["parsed"]

    return {
        "raw_output": raw_output,
        "extracted_json": first["extracted_json"],
        "parse_ok": first["parse_ok"],
        "schema_valid": first["schema_valid"],
        "validation_errors": first["errors"],
        "repair_attempted": repair_attempted,
        "repair_raw_output": repair_raw,
        "recovered": recovered,
        "used_fallback": used_fallback,
        "final_object": final_object,
        "generation_seconds": round(time.time() - start, 3),
    }


# --------------------------------------------------
# DELIBERATE INVALID CASE (no model needed)
# --------------------------------------------------

def deliberate_invalid_case():
    """Run a known-malformed payload through the validator for evidence."""

    malformed_raw = '{"summary": "Missing action_items field and trailing comma",}'
    result = parse_and_validate(malformed_raw)

    # Also show a parse-OK but schema-invalid object.
    schema_bad = {"summary": "ok", "action_items": "not-a-list"}
    schema_valid, schema_errors = validate_output(schema_bad)

    return {
        "case": "deliberate_invalid",
        "malformed_raw": malformed_raw,
        "parse_ok": result["parse_ok"],
        "schema_valid_of_malformed": result["schema_valid"],
        "parse_errors": result["errors"],
        "schema_bad_object": schema_bad,
        "schema_bad_valid": schema_valid,
        "schema_bad_errors": schema_errors,
    }


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("=" * 60)
    print("SAMSum STRUCTURED JSON OUTPUT EXPERIMENT (E4)")
    print("=" * 60)

    records = load_baseline_examples(BASELINE_FILE)
    print(f"Baseline examples loaded: {len(records)}")

    tokenizer, model = load_model()

    results = []

    for record in records:
        sample_id = str(record["sample_id"])
        dialogue = str(record["dialogue"])

        print("\n" + "-" * 60)
        print(f"Sample ID: {sample_id}")

        outcome = generate_structured(dialogue, tokenizer, model)

        print(f"parse_ok={outcome['parse_ok']} "
              f"schema_valid={outcome['schema_valid']} "
              f"recovered={outcome['recovered']} "
              f"used_fallback={outcome['used_fallback']}")

        results.append({
            "sample_id": sample_id,
            "dialogue": dialogue,
            "reference_summary": record.get("reference_summary"),
            **outcome,
            "model_name": MODEL_NAME,
            "max_new_tokens": MAX_NEW_TOKENS,
        })

    invalid_case = deliberate_invalid_case()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    json_path = OUTPUT_DIR / "structured_outputs.json"
    json_path.write_text(
        json.dumps(
            {"results": results, "deliberate_invalid_case": invalid_case},
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    # Compact per-sample log for the report.
    log_rows = [
        {
            "sample_id": r["sample_id"],
            "parse_ok": r["parse_ok"],
            "schema_valid": r["schema_valid"],
            "repair_attempted": r["repair_attempted"],
            "recovered": r["recovered"],
            "used_fallback": r["used_fallback"],
            "num_action_items": len(
                r["final_object"].get("action_items", [])
            ),
            "generation_seconds": r["generation_seconds"],
        }
        for r in results
    ]
    log_df = pd.DataFrame(log_rows)
    log_path = OUTPUT_DIR / "structured_output_log.csv"
    log_df.to_csv(log_path, index=False, encoding="utf-8")

    print("\n" + "=" * 60)
    print("STRUCTURED OUTPUT EXPERIMENT COMPLETE")
    print("=" * 60)
    print(f"Samples processed: {len(results)}")
    print(f"First-attempt valid: {sum(r['schema_valid'] for r in results)}")
    print(f"Recovered via repair: {sum(r['recovered'] for r in results)}")
    print(f"Fell back to stub: {sum(r['used_fallback'] for r in results)}")
    print("\nDeliberate invalid case -> "
          f"parse_ok={invalid_case['parse_ok']}, "
          f"schema_bad_valid={invalid_case['schema_bad_valid']}")
    print(f"JSON results: {json_path}")
    print(f"CSV log: {log_path}")
    print("\n" + log_df.to_string(index=False))


if __name__ == "__main__":
    main()

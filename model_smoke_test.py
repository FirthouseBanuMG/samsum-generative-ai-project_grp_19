# Run a baseline smoke test for a conversational summarization model.

# The script loads selected SAMSum training examples, generates summaries
# using a pretrained causal language model, and saves the outputs along
# with experiment metadata.

# This test verifies pipeline functionality and is not intended to measure
# summarization quality or benchmark model performance.

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Model configuration and input/output paths for the baseline experiment.
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
MANIFEST_PATH = Path("data/processed/baseline_sample_manifest.json")
TRAIN_PATH = Path("data/processed/samsum-train-processed.csv")
OUTPUT_DIR = Path("outputs/baseline_smoke_test")

# Define the summarization instructions passed to the model.
SYSTEM_PROMPT = (
    "Summarize the conversation accurately in one or two sentences. "
    "Include important decisions and action items. Do not invent information."
)

# Limit the summary length and use deterministic greedy decoding.
MAX_NEW_TOKENS = 100
DO_SAMPLE = False

def main():
# Confirm that all required input files exist before processing.
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Manifest not found: {MANIFEST_PATH}")
    if not TRAIN_PATH.exists():
        raise FileNotFoundError(f"Processed training data not found: {TRAIN_PATH}")

# Load the sample manifest and ensure that only training examples are selected.
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    if manifest.get("dataset_split") != "train":
        raise ValueError("Safety check failed: manifest dataset_split must be 'train'.")

    examples = manifest.get("examples", [])
    if not examples:
        raise ValueError("Manifest contains no selected examples.")

    df = pd.read_csv(TRAIN_PATH, dtype={"id": str})
    df["id"] = df["id"].astype(str)

    selected_ids = [str(item["id"]) for item in examples]
    if len(selected_ids) != len(set(selected_ids)):
        raise ValueError("Manifest contains duplicate sample IDs.")

    indexed = df.set_index("id", drop=False)
    missing_ids = [sample_id for sample_id in selected_ids if sample_id not in indexed.index]
    if missing_ids:
        raise ValueError(f"Selected IDs not found in processed training data: {missing_ids}")

    print("PyTorch:", torch.__version__)
    print("CUDA available:", torch.cuda.is_available())
    print("Dataset split: train")
    print("Selected IDs:", selected_ids)
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    print("Loading model on CPU...")
    load_start = time.time()
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True
    )
    model.eval()
    model_load_seconds = time.time() - load_start
    print(f"Model loaded in {model_load_seconds / 60:.2f} minutes")

    results = []
    total_generation_seconds = 0.0

    for item in examples:
        sample_id = str(item["id"])
        row = indexed.loc[sample_id]
        dialogue = str(row["dialogue"])
        reference = str(row["summary"])

# Build the system and user messages for the selected conversation.
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Summarize this conversation:\n{dialogue}"
            }
        ]

# Apply the model-specific chat template to format the input prompt.
        prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
# Convert the formatted prompt into token IDs for model inference.
        inputs = tokenizer(prompt, return_tensors="pt")

        print(f"\nGenerating summary for {sample_id}...")
        generation_start = time.time()

# Generate the summary without tracking gradients to reduce inference overhead.
        with torch.inference_mode():
            output_ids = model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=DO_SAMPLE
            )
        generation_seconds = time.time() - generation_start
        total_generation_seconds += generation_seconds

# Remove the input prompt tokens so that only the generated summary is decoded.
        new_tokens = output_ids[0][inputs["input_ids"].shape[1]:]
        generated_summary = tokenizer.decode(
            new_tokens,
            skip_special_tokens=True
        ).strip()

        result = {
            "sample_id": sample_id,
            "dataset_split": "train",
            "dialogue": dialogue,
            "rendered_prompt": prompt,
            "reference_summary": reference,
            "generated_summary": generated_summary,
            "selection_category": item.get("category"),
            "selection_reason": item.get("selection_reason"),
            "generation_seconds": round(generation_seconds, 3)
        }
        results.append(result)

        print("Reference:", reference)
        print("Generated:", generated_summary)
        print(f"Generation time: {generation_seconds:.1f} seconds")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    run_metadata = {
        "experiment": "initial_baseline_smoke_test",
        "run_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "model_name": MODEL_NAME,
        "dataset_split": "train",
        "sample_ids": selected_ids,
        "system_prompt": SYSTEM_PROMPT,
        "decoding": {
            "do_sample": DO_SAMPLE,
            "max_new_tokens": MAX_NEW_TOKENS,
            "temperature": None,
            "top_k": None,
            "top_p": None,
            "note": "Greedy decoding; sampling parameters are not applied."
        },
        "device": "cpu",
        "torch_version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "model_load_seconds": round(model_load_seconds, 3),
        "total_generation_seconds": round(total_generation_seconds, 3),
        "purpose": "Qualitative pipeline verification only, not a performance estimate."
    }

    results_path = OUTPUT_DIR / "baseline_outputs.json"
    metadata_path = OUTPUT_DIR / "run_metadata.json"

    results_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    metadata_path.write_text(
        json.dumps(run_metadata, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print("\n=== BASELINE SMOKE TEST COMPLETE ===")
    print("Results:", results_path)
    print("Metadata:", metadata_path)
    print("Examples generated:", len(results))
    print("This is qualitative smoke-test evidence, not an evaluation score.")

if __name__ == "__main__":
    main()

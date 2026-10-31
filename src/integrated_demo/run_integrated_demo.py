"""Run the integrated workflow for one processed training-split sample ID.

This demo reuses the project's structured-generation recovery, JSON Schema
validator, coverage warning, and allowlisted application-level validation tool.
Run with ``python -m integrated_demo.run_integrated_demo --sample-id <id>``.
"""

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

from project_paths import PROJECT_ROOT
from structured_output.run_structured_output import (
    MODEL_NAME,
    generate_structured,
    load_model,
)
from integrated_demo.presentation import (
    format_final_response_for_review,
    format_summary_for_review,
)
from tool_calling.run_tool_calling import (
    TOOL_NAME,
    execute_tool_call,
    generate_final_response,
)


TRAIN_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "samsum-train-processed.csv"
)
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "integrated_demo" / "demo_result.json"


def load_dialogue(sample_id: str) -> str:
    """Load a single dialogue by ID from the processed training split."""
    if not TRAIN_FILE.is_file():
        raise FileNotFoundError(
            f"Processed training data not found: {TRAIN_FILE}. "
            "Follow the dataset setup guide before running this demo."
        )

    frame = pd.read_csv(TRAIN_FILE, dtype={"id": str})
    required = {"id", "dialogue"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Training data is missing columns: {sorted(missing)}")

    matches = frame.loc[frame["id"] == sample_id, "dialogue"]
    if matches.empty:
        raise ValueError(f"Sample ID {sample_id!r} was not found in training data.")

    dialogue = matches.iloc[0]
    if not isinstance(dialogue, str) or not dialogue.strip():
        raise ValueError(f"Sample ID {sample_id!r} has an empty dialogue.")
    return dialogue


def run_demo(
    sample_id: str | None = None,
    *,
    dialogue: str | None = None,
    device: str = "cpu",
    save_input: bool = False,
) -> dict:
    """Generate, validate, and save a summary from a training example or text."""
    if dialogue is not None:
        if sample_id is not None:
            raise ValueError("Provide either sample_id or dialogue, not both.")
        if not isinstance(dialogue, str) or not dialogue.strip():
            raise ValueError("Dialogue must be non-empty.")
        dataset_split = "user_supplied"
    else:
        if sample_id is None:
            raise ValueError("A training sample ID or dialogue is required.")
        dialogue = load_dialogue(sample_id)
        dataset_split = "train"

    tokenizer, model = load_model(device)
    outcome = generate_structured(dialogue, tokenizer, model)
    coverage_flags = outcome["commitment_coverage_flags"]

    record = {
        "sample_id": sample_id,
        "dataset_split": dataset_split,
        "model": MODEL_NAME,
        "dialogue": (
            dialogue if dataset_split == "train" or save_input else None
        ),
        "dialogue_sha256": (
            None
            if dataset_split == "train"
            else hashlib.sha256(dialogue.encode("utf-8")).hexdigest()
        ),
        "generation": outcome,
        "human_review_required": True,
        "commitment_coverage_check": {
            "type": "narrow_heuristic",
            "flags": coverage_flags,
        },
        "tool_request": None,
        "tool_result": None,
    }

    if outcome["schema_valid"] and not outcome["used_fallback"]:
        request = {
            "tool_name": TOOL_NAME,
            "arguments": {"output": outcome["final_object"]},
        }
        record["tool_request"] = request
        record["tool_result"] = execute_tool_call(request)
        if record["tool_result"]["valid"]:
            raw_request = json.dumps(request, ensure_ascii=False)
            record["final_response"] = generate_final_response(
                dialogue,
                raw_request,
                record["tool_result"],
                tokenizer,
                model,
            )
            if coverage_flags:
                record["final_response"] += (
                    "\n\nCompleteness review required: "
                    + " ".join(coverage_flags)
                )
            record["final_response_status"] = (
                "generated_after_valid_tool_result_with_coverage_warning"
                if coverage_flags
                else "generated_after_valid_tool_result"
            )
        else:
            record["final_response"] = None
            record["final_response_status"] = (
                "blocked_tool_validation_failed"
            )
    else:
        record["tool_error"] = (
            "Generated output did not pass JSON Schema validation; "
            "the tool was not invoked."
        )
        record["final_response"] = None
        record["final_response_status"] = "blocked_structured_output_invalid"

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(record, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group()
    inputs.add_argument(
        "--sample-id",
        help="Training-split dialogue ID (default: 13818513).",
    )
    inputs.add_argument("--dialogue", help="Summarize this supplied dialogue.")
    inputs.add_argument(
        "--dialogue-file",
        type=Path,
        help="Read a dialogue from this UTF-8 text file.",
    )
    parser.add_argument(
        "--device",
        choices=("cpu", "cuda", "auto"),
        default="cpu",
        help="Inference device (default: cpu; use cuda when available).",
    )
    parser.add_argument(
        "--save-input",
        action="store_true",
        help="Include a user-supplied dialogue in the saved result file.",
    )
    args = parser.parse_args()

    if args.dialogue_file is not None:
        if not args.dialogue_file.is_file():
            raise FileNotFoundError(
                f"Dialogue file not found: {args.dialogue_file}"
            )
        supplied_dialogue = args.dialogue_file.read_text(encoding="utf-8")
        result = run_demo(
            dialogue=supplied_dialogue,
            device=args.device,
            save_input=args.save_input,
        )
    elif args.dialogue is not None:
        result = run_demo(
            dialogue=args.dialogue,
            device=args.device,
            save_input=args.save_input,
        )
    else:
        sample_id = args.sample_id or "13818513"
        result = run_demo(sample_id=str(sample_id), device=args.device)

    generation = result["generation"]
    if result["sample_id"] is None:
        print("Input: user-supplied dialogue")
    else:
        print(f"Sample: {result['sample_id']} (train split)")
    print(f"Model: {result['model']}")
    print(
        format_summary_for_review(
            generation["final_object"],
            schema_valid=generation["schema_valid"],
            used_fallback=generation["used_fallback"],
            validation_errors=generation["validation_errors"],
            coverage_flags=generation["commitment_coverage_flags"],
        )
    )
    if result["tool_result"] is not None:
        tool_status = "passed" if result["tool_result"]["valid"] else "failed"
        print(f"\nTool validation: {tool_status}")
    if result["final_response"] is not None:
        print()
        print(format_final_response_for_review(result["final_response"]))
    print(
        "\nMachine-readable evidence saved to: "
        f"{OUTPUT_FILE.relative_to(PROJECT_ROOT)}"
    )

    if result["tool_result"] is not None and not result["tool_result"]["valid"]:
        raise RuntimeError(
            "The integrated demo's validation tool reported an invalid result."
        )
    if result["tool_result"] is None:
        raise RuntimeError(
            "No valid structured result was produced; inspect the saved "
            "generation/recovery diagnostics before treating the run as successful."
        )


if __name__ == "__main__":
    main()

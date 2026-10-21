# Assignment-to-Evidence Matrix

**Project:** SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction
**Group:** 19
**Purpose:** Track every major assignment requirement against its implementation, evidence, and verification status.

## Status definitions

- **Planned:** Not yet implemented.
- **In Progress:** Work has started but is incomplete.
- **Implemented:** An artifact or code exists.
- **Tested:** Evidence confirms the intended behavior.
- **Blocked:** Progress depends on an unresolved issue.

A requirement must not be marked Tested based only on a plan or an unverified code file.

## Requirement Matrix

| ID | Requirement | Planned implementation/evidence | Verification method | Current status |
|---|---|---|---|---|
| R01 | Dataset analysis and preprocessing | Data-quality report, preprocessing script, metadata, exclusion log | Check row counts, columns, exclusions, and validation output | Tested for documented checks |
| R02 | Sample selection | Document representative development examples and selection rationale | Verify IDs, selection method, and rationale are recorded | Planned |
| R03 | Compare at least three generative model families covered in the course | Model-family comparison table and experiment logs | Verify model identity, family, configuration, outputs, and limitations | Planned |
| R04 | Explain LLM architecture, tokenization, and autoregressive generation | Report section with technical explanation and tokenizer observations | Check report coverage and factual consistency | Planned |
| R05 | Pretrained causal LM baseline with at least three outputs | Baseline experiment and retained output examples | Inspect at least three generated outputs and their configurations | In Progress |
| R06 | Zero-shot prompting | Reusable prompt template and experiment log | Verify prompt and generated output are saved | Planned |
| R07 | Few-shot prompting | Example-based prompt template and experiment log | Verify examples, prompt, and output are saved | Planned |
| R08 | Role/context prompting | Role/context template and experiment log | Verify context, prompt, and output are saved | Planned |
| R09 | Constraint-based prompting | Constrained output template and experiment log | Verify constraints and resulting output are saved | Planned |
| R10 | Greedy versus sampling comparison | Controlled decoding experiment (`src/run_decoding_experiments.py`, `outputs/decoding_experiments/`) | Compare outputs and configurations for the same inputs | Implemented |
| R11 | Temperature, top-k, and top-p | Decoding configurations and observations (`src/run_decoding_experiments.py`, variability summary) | Verify supported settings, actual values, and output differences | Implemented |
| R12 | Prompting versus RAG versus fine-tuning versus PEFT | Conceptual comparison in report | Check coverage, trade-offs, and project-specific justification | Planned |
| R13 | JSON Schema validation | JSON Schema, parser/validator, valid and invalid test cases (`src/structured_schema.py`, `src/run_structured_output.py`, `src/test_structured_schema.py`, `outputs/structured_output/`) | Execute validation tests and retain results | Implemented |
| R14 | Callable tool/function demonstration | Tool definition, invocation example, and result | Demonstrate invocation and verify arguments/results | Planned |
| R15 | Reusable parameterized prompt | Prompt template with configurable fields | Test multiple inputs without rewriting the template | Planned |
| R16 | At least four evaluation criteria | Evaluation protocol and results table | Confirm four or more criteria are defined and results recorded | Planned |
| R17 | At least three failure cases | Failure log with input, output, failure type, and analysis | Inspect at least three concrete documented cases | Planned |
| R18 | Responsible-use controls | Privacy, uncertainty, unsupported claims, and human-review guidance | Check controls are documented and relevant behaviors tested where possible | Planned |
| R19 | Integrated notebook/demo | Runnable end-to-end notebook or demo | Run from documented setup and test representative cases | Planned |
| R20 | Report, 10–15 pages excluding appendices/references | Final report and references | Verify page count and requirement coverage | Planned |
| R21 | Dataset and preprocessing notes | Data-quality report and preprocessing metadata | Verify paths, counts, exclusions, and procedures are documented | Implemented |
| R22 | Prompt and decoding logs | Versioned experiment records and generated outputs | Reproduce selected experiments from recorded configurations | Planned |
| R23 | Presentation, 8–10 minutes | Slide deck and speaking plan | Rehearse and time the presentation | Planned |
| R24 | Individual contribution statements | Contribution record from each group member | Confirm all required statements are included | Planned |

## Evidence Rules

1. Link each requirement to the exact file, notebook section, experiment record, test, or report section once available.
2. Record actual results, not expected results.
3. Keep generated outputs and their prompt/model/decoding configurations together.
4. Document negative results and failures rather than omitting them.
5. Do not use the final test split to tune prompts or select models.
6. Update this matrix whenever a requirement's status changes.

## Evidence Path Register

Fill in the actual paths as the artifacts are created.

| Artifact | Path | Status |
|---|---|---|
| High-level architecture | documents/03_Implementation_and_Experiments/01_High_Level_Architecture.md | Implemented |
| Master phase plan | documents/03_Implementation_and_Experiments/02_Master_Phase_Plan.md | Implemented |
| Assignment-to-evidence matrix | documents/03_Implementation_and_Experiments/03_Assignment_to_Evidence_Matrix.md | In Progress |
| Data-quality report | documents/03_Implementation_and_Experiments/Data_Quality_Report.md | Implemented |
| Baseline experiment outputs | To be assigned | Planned |
| Prompt experiment logs | To be assigned | Planned |
| JSON Schema and validation tests | src/structured_schema.py, src/test_structured_schema.py, outputs/structured_output/ | Implemented |
| Decoding comparison experiment | src/run_decoding_experiments.py, outputs/decoding_experiments/ | Implemented |
| Integrated notebook/demo | To be assigned | Planned |
| Final report and slides | To be assigned | Planned |

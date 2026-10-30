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
| R01 | Dataset analysis and preprocessing | Data-quality report, preprocessing script, metadata, exclusion log, processed-split leakage check, raw integrity check | Check reported source/version, license disclosure, row counts, exclusions, split overlap, hashes, and validation output | Kaggle page/version 1 recorded; its license is Unknown, so the report makes no redistribution claim and dataset files are not included. Exact downloaded archive/upstream version is unverified. Processed splits passed row/content checks and zero ID/exact-pair overlap on 28 Oct; raw hashes match the local 16 Oct baseline, which cannot establish earlier integrity or upstream authenticity |
| R02 | Sample selection | Baseline manifest and model-comparison sample manifest | Verify IDs, split, selection method, and rationale | Implemented; baseline examples are documented; 50-test-sample protocol must be described accurately |
| R03 | Compare at least three generative model families covered in the course | Conceptual VAE/GAN/autoregressive Transformer comparison in report; empirical Qwen/FLAN-T5/DistilBART comparison and evidence | Check conceptual comparison, tested model configurations, outputs, limitations, and avoid unsupported claims about lecture coverage | User directed use of standard generative-AI families after confirming the CS1 session title; comparison is complete, but specific lecture coverage is not independently verified |
| R04 | Explain LLM architecture, tokenization, and autoregressive generation | `documents/Final_Assignment_Report.md`, Section 4 | Review technical explanation and relation to project workflow | Reviewed against the implemented Qwen flow; the report explains tokenization, causal attention, next-token generation, and decoding |
| R05 | Pretrained causal LM baseline with at least three outputs | `outputs/baseline_smoke_test/` and run metadata | Inspect three generated outputs and settings | Tested; qualitative smoke test only |
| R06 | Zero-shot prompting | `src/prompting/prompts.py`, prompt outputs and evaluation files | Verify prompt and output are retained | Tested |
| R07 | Few-shot prompting | `src/prompting/prompts.py`, prompt outputs and evaluation files | Verify example, prompt, and output are retained | Tested |
| R08 | Role/context prompting | `src/prompting/prompts.py`, prompt outputs and evaluation files | Verify context, prompt, and output are retained | Tested |
| R09 | Constraint-based prompting | `src/prompting/prompts.py`, prompt outputs and evaluation files | Verify constraints and output are retained | Tested |
| R10 | Greedy versus sampling comparison | `src/generation/run_decoding_experiments.py`, `outputs/decoding_experiments/` | Compare outputs and configurations for identical inputs | Tested; saved outputs and variability summary exist |
| R11 | Temperature, top-k, and top-p | Decoding configurations and variability summary | Verify actual values and output differences | Tested |
| R12 | Prompting versus RAG versus fine-tuning versus PEFT | `documents/Final_Assignment_Report.md`, Section 8 | Check trade-offs and project-specific justification | Reviewed; prompting is justified for dialogue-grounded summarization and the project's CPU/data constraints; RAG and training trade-offs are documented |
| R13 | JSON Schema validation | Schema includes summary, key points, decisions, and action items; runner, tests, and `outputs/structured_output/` | Execute positive/negative validation tests and inspect outputs for all required fields | Tested; schema/recovery tests pass; the structured runner flags a narrow class of explicit-commitment omissions, but does not prove general factuality or completeness |
| R14 | Callable tool/function demonstration | `src/tool_calling/run_tool_calling.py`, tests, saved demonstration | Verify invocation, tool result, and model follow-up | Tested end-to-end on CPU; saved evidence includes generated final response; application-level JSON protocol, not native model-specific tool calling |
| R15 | Reusable parameterized prompt | `src/prompting/prompts.py` and prompt experiment runner | Build prompts for input dialogues without rewriting template | Tested |
| R16 | At least four evaluation criteria | `outputs/evaluation/prompt_evaluation.csv`; concise/detailed ROUGE and length comparison under `outputs/summary_detail_comparison/` | Confirm criteria, scores, method, and limitations | Implemented; rubric comparison n=3 per style and concise/detailed lexical comparison n=3; conclusions are exploratory |
| R17 | At least three failure cases | Experiment log and `documents/Final_Assignment_Report.md`, Section 11 | Inspect input/output, failure, impact, and mitigation | Documented with concrete examples; qualitative cases are not a failure-rate estimate |
| R18 | Responsible-use controls | Final report Section 12, prompt constraints, validator, review flags | Verify controls are relevant and tested where applicable | Partially implemented/documented; human review remains required |
| R19 | Integrated notebook/demo | `notebooks/01_integrated_demo.ipynb`, `src/integrated_demo/run_integrated_demo.py`, `outputs/integrated_demo/demo_result.json` | Run end-to-end with local model/data; inspect saved result, factuality warning, and final response | CLI and notebook rerun on CPU using the project environment; model still omits the explicit commitment, now caught by a narrow heuristic and shown as a review warning; factual completion remains human-reviewed |
| R20 | Report, 10–15 pages excluding appendices/references | `documents/Final_Assignment_Report.md` | Render, check required page count, citations, and complete assignment coverage | Rendered with Pandoc/Microsoft Word on 29 Oct: 14 pages total, 11-page body excluding references/appendices. Evidence and citation consistency reviewed; recheck if final submission formatting changes |
| R21 | Dataset and preprocessing notes | Data-quality report, dataset guide, processed metadata | Verify paths, counts, exclusions, and procedures | Implemented |
| R22 | Prompt and decoding logs | Prompt/decoding result files and run configurations | Reproduce selected experiments from recorded configurations | Dataset validation/preprocessing/leakage checks and integrated CPU CLI rerun passed on 28 Oct; no new model comparison was run on the already-used test subset |
| R23 | Presentation, 8–10 minutes | `documents/Assignment_1_Presentation.pptx`, `documents/Assignment_1_Presentation_Slides.md`, `documents/Assignment_1_Presentation_Draft.md` | Assign speakers, review deck, rehearse and time | 10-slide deck generated; slide allocations total 8:25 and a one-minute demo gives a 9:25 target. Speaker split is proposed; team rehearsal and actual timing remain |
| R24 | Individual contribution statements | `documents/Individual_Contribution_Statements_Template.md` | Confirm every required statement is completed and approved by its member | Simplified template is ready: each member writes a short, accurate contribution statement, confirms it, and dates it. Member input is still required |
| R25 | SAMSum-specific concise versus detailed prompting | `src/prompting/run_summary_detail_comparison.py`, `outputs/summary_detail_comparison/` | Compare outputs on fixed dialogues with the same model and decoding settings | Tested on 3 training examples; detailed summaries are longer; lexical and factual limits documented |

## Evidence Rules

1. Link each requirement to the exact file, notebook section, experiment record, test, or report section once available.
2. Record actual results, not expected results.
3. Keep generated outputs and their prompt/model/decoding configurations together.
4. Document negative results and failures rather than omitting them.
5. Do not tune against or claim a pristine holdout from the 50-sample test subset already used for model comparison.
6. Update this matrix whenever a requirement's status changes.

## Evidence Path Register

Fill in the actual paths as the artifacts are created.

| Artifact | Path | Status |
|---|---|---|
| High-level architecture | documents/03_Implementation_and_Experiments/01_High_Level_Architecture.md | Implemented |
| Master phase plan | documents/03_Implementation_and_Experiments/02_Master_Phase_Plan.md | Implemented |
| Assignment-to-evidence matrix | documents/03_Implementation_and_Experiments/03_Assignment_to_Evidence_Matrix.md | Updated |
| Data-quality report | documents/03_Implementation_and_Experiments/Data_Quality_Report.md | Implemented |
| Baseline experiment outputs | outputs/baseline_smoke_test/ | Tested |
| Prompt experiment logs | outputs/prompt_experiments/, outputs/evaluation/ | Tested; small sample |
| Concise-versus-detailed comparison | src/prompting/run_summary_detail_comparison.py, outputs/summary_detail_comparison/ | Tested on the same 3 training examples with fixed model/decoding |
| Model-family comparison | outputs/model_comparison_50_samples/, documents/03_Implementation_and_Experiments/05_Model_Family_Comparison/ | Implemented; architecture-family limitation documented |
| JSON Schema and validation tests | src/structured_output/schema.py, tests/test_structured_schema.py, outputs/structured_output/ | Tested |
| Tool/function demonstration | src/tool_calling/run_tool_calling.py, tests/test_tool_calling.py, outputs/tool_calling/ | End-to-end round-trip run and saved final response; factual review still required |
| Decoding comparison experiment | src/generation/run_decoding_experiments.py, outputs/decoding_experiments/ | Tested |
| Integrated notebook/demo | notebooks/01_integrated_demo.ipynb, src/integrated_demo/run_integrated_demo.py | Notebook and CLI executed; follow-up response saved; factual omission documented |
| Final report | documents/Final_Assignment_Report.md | Content/evidence and citation review complete; current render is 14 pages total with an 11-page body; final team approval remains |
| Presentation | documents/Assignment_1_Presentation_Draft.md | Slide outline and proposed speaker/demo plan ready; team confirmation and rehearsal pending |
| Contribution statements | documents/Individual_Contribution_Statements_Template.md | Simplified template ready; short member statements and confirmations pending |

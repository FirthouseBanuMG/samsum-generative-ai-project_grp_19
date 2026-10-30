# SAMSum Major Project — Master Project Plan

**Group:** 19  
**Project:** SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction  
**Course:** PCAM* ZG516 — Applied Generative AI  
**Status reviewed:** 31 October 2026
**Original submission deadline:** 25 October 2026 (passed)

## 1. Purpose and scope

This plan describes the project's current scope, implementation status, evidence, and remaining closeout work. It is updated to reflect completed implementation and saved experiment results, rather than the earlier proposed schedule.

The project is an educational prototype that uses pretrained generative models to summarize messenger-style conversations and extract key points, decisions, and action items into structured JSON. It is not a production or authoritative record system. Model outputs require human review.

The primary runtime uses the pretrained `Qwen/Qwen2.5-1.5B-Instruct` model. The project performs inference only; it does not train or fine-tune model parameters.

## 2. Current system and data policy

### Application flow

1. The integrated CLI reads a dialogue by sample ID from the processed SAMSum training split; it does not currently accept arbitrary dialogue text.
2. Build the structured prompt and generate output with the pretrained Qwen model.
3. Parse and validate the JSON against the project schema; retry invalid output once and flag fallback output.
4. Run a narrow commitment-coverage heuristic. It flags a limited pattern of possible omissions; it neither repairs output nor guarantees completeness.
5. Send schema-valid output to the allowlisted `validate_summary_output` function.
6. On valid tool output, return the result to the model for a final response. Invalid tool output blocks the follow-up.
7. Require human review against the original dialogue.

Tool invocation is an application-level JSON protocol, not native model-specific tool-call parsing. JSON Schema verifies structure, not factual accuracy.

### Data handling

- Keep raw CSVs unchanged in `data/raw/`. Read them for audit, profiling, integrity checks, and preprocessing only.
- Write cleaned/validated copies to `data/processed/`; use processed data for model workflows.
- The audited raw row counts were 14,732 train, 818 validation, and 819 test. One blank-dialogue training row is excluded and logged. Processed counts are 14,731, 818, and 819.
- Processed data validation and cross-split ID/exact dialogue-summary pair checks passed with zero overlaps. These checks do not prove the absence of semantic near-duplicates.
- The team reports the Kaggle dataset page as its source (version 1). Kaggle lists the license as **Unknown**. Cite that recorded information, do not claim redistribution rights, and do not include dataset files in the repository or submission.

## 3. Completed implementation and evidence

| Workstream | Current status and evidence | Limitation to report |
|---|---|---|
| Project setup and architecture | Windows/Python 3.13 environment, package layout under `src/`, setup guide, architecture and phase plan in place | CPU-only inference can be slow |
| Dataset audit and preprocessing | Raw/processed separation, validation, profiling, integrity check, exclusion log, and processed split leakage checks recorded | Local hashes only verify against the recorded local baseline, not upstream authenticity; Kaggle license is Unknown |
| Baseline generation | Three Qwen generations from processed training examples saved with settings | Qualitative smoke-test examples, not a population accuracy estimate |
| Prompt engineering | Zero-shot, few-shot, role/context, and constraint prompts implemented and compared; concise/detailed prompting also compared | Manual prompt ratings use n=3 and are exploratory |
| Decoding | Greedy and sampling configurations, including temperature, top-p, and top-k, run and logged | Sampling can add unsupported details; recorded CPU timings are machine-specific |
| Model comparison | Three model configurations evaluated on the same 50 processed test dialogues; details in [Model Family Comparison](../Implementation_and_Experiments/Model_Family_Comparison/README.md) | These results are comparative/selection evidence, not an untouched final holdout; input formats differ |
| Structured output | JSON Schema for summary, key points, decisions, and action items; parser, one repair attempt, fallback path, tests, and saved outputs | Schema validity does not establish semantic accuracy or completeness |
| Tool/function workflow | Allowlisted validation function, tests, saved tool-result round trip and model follow-up | Application-level JSON protocol, not native model tool calling |
| Integrated application | CLI and notebook run on CPU; saved output includes final response and a commitment-coverage warning | The heuristic is narrow and warns without repairing the omission |
| Current verification | Raw integrity, processed-dataset validation, split leakage, and offline test suite rerun on 31 October 2026 | 45 automated tests passed; read-only data checks do not prove semantic near-duplicate absence or model factuality |
| Evaluation and failure analysis | ROUGE comparison, human prompt criteria, and concrete qualitative failure cases recorded | Small samples; ROUGE is reference overlap, not factuality; no large-scale human factuality study |
| Report and presentation | Technical report, 10-slide deck, speaker notes, and simplified contribution template prepared | Team contribution confirmations and actual rehearsal are still required |

## 4. Model comparison on 50 test examples

### What was run

The saved comparison uses **50 unique examples from `data/processed/samsum-test-processed.csv`**, selected with **seed 42**, excluding pilot IDs `13818513`, `13681000`, and `13728094`. It generated **150 outputs total**: one per model for each of the 50 dialogues.

The three tested configurations were:

- `Qwen/Qwen2.5-1.5B-Instruct` with a constraint-based prompt.
- `google/flan-t5-base` with a constraint-based prompt.
- `sshleifer/distilbart-cnn-12-6` with dialogue-only input.

The recorded run used CPU, greedy decoding (`do_sample=False`, `num_beams=1`), maximum input length 1,024 tokens, and maximum output length 100 new tokens.

| Model | Samples | ROUGE-1 F1 | ROUGE-2 F1 | ROUGE-L F1 | Mean seconds/sample |
|---|---:|---:|---:|---:|---:|
| Qwen2.5-1.5B-Instruct | 50 | 0.220521 | 0.072396 | 0.158634 | 21.68958 |
| FLAN-T5-base | 50 | 0.514008 | 0.248225 | 0.429139 | 0.63586 |
| DistilBART-CNN-12-6 | 50 | 0.265467 | 0.098079 | 0.199712 | 1.38020 |

On this selected sample, FLAN-T5-base achieved the highest ROUGE values and lowest recorded mean generation time. ROUGE measures lexical overlap with reference summaries; it does not establish factual support, action-item correctness, or overall usefulness. Timing is specific to the recorded hardware and software.

### How to interpret the 50-example comparison

The 50 examples **came from the test split and were used for model comparison/selection**. Therefore:

- Report the numbers as a **50-example comparative model experiment**, not as a pristine final test or untouched holdout result.
- Do not continue tuning prompts, models, or settings against these same 50 examples.
- Do not claim that the comparison isolates model architecture: Qwen and FLAN-T5 use a constraint-based prompt, while DistilBART receives dialogue-only input.
- Do not claim that the three empirical systems represent three distinct generative architecture families. They represent one causal LM and two encoder-decoder systems.
- The experiment remains valuable evidence of implementation and observed comparative behavior, with its protocol and limitations disclosed.

Evidence includes the saved metrics and sample manifest under `outputs/model_comparison_50_samples/`, and the detailed methodology and outputs under `documents/Implementation_and_Experiments/Model_Family_Comparison/`. The experiment runner is `src/evaluation/run_model_family_comparison_50.py`. Do not rerun it as a new independent test after seeing these results.

## 5. Assignment coverage

The saved artifacts and report cover the main technical requirements:

- SAMSum dataset description, audit, preprocessing, and split-use disclosure.
- Pretrained causal-LM baseline with at least three examples.
- Four prompt styles and decoding comparisons.
- Conceptual VAE, GAN, and autoregressive Transformer comparison, distinguished from the empirical model comparison.
- Prompting versus RAG, full fine-tuning, and PEFT discussion.
- Structured JSON output and validation.
- Allowlisted application-level tool/function demonstration.
- Evaluation criteria, saved metrics, and concrete failure analysis.
- Integrated notebook and CLI.
- Responsible-use and human-review limitations.

The assignment evidence matrix maps each requirement to its evidence and status: [Assignment-to-Evidence Matrix](../Implementation_and_Experiments/03_Assignment_to_Evidence_Matrix.md).

## 6. Verification and deliverables

Recorded verification (latest checks on 31 October 2026 unless otherwise dated):

- 45 automated tests passed with `.\.venv\Scripts\python.exe -m pytest -q`.
- Raw dataset hash verification, processed data validation, and cross-split ID/exact-pair checks passed. Raw hashes match the local 16 October baseline; this does not authenticate upstream provenance.
- The integrated CLI/notebook model-backed example is saved in `outputs/integrated_demo/`. The 31 October offline test/data verification did not perform a fresh model inference run.
- The report last rendered on 29 October to 14 pages total, with an 11-page body excluding references and appendices. Re-render after any content/layout changes.
- The presentation deck contains 10 slides. Its planned slide timings total about 8 minutes 25 seconds; the proposed one-minute demo brings the target to about 9 minutes 25 seconds. The group has not yet recorded an actual timed rehearsal.

Run the application from the repository root in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m integrated_demo.run_integrated_demo --sample-id 13818513
```

Run the automated tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests
```

The complete current Windows software and dataset instructions are in [Environment Setup and Run Guide](../Environment_Setup/Prerequisites_and_Environment_Setup.md).

## 7. Current closeout actions

These items require team or course participation and cannot be truthfully completed from repository artifacts alone:

1. Each of the four members writes a short, accurate contribution statement, confirms it, and adds the date using the [contribution template](../Individual_Contribution_Statements_Template.md).
2. The group confirms the proposed speakers and presentation split, rehearses the slides plus demo, and records the actual duration. Target 8–10 minutes; the current estimate is about 9:25.
3. The group reviews final formatting and ensures the submitted report/deck match the verified evidence and limitations.
4. Submit via the course process. The original deadline was 25 October 2026; no submission confirmation is recorded in this repository.

## 8. Project controls and risks

| Risk | Control |
|---|---|
| Unsupported or omitted claims | Compare generated summaries and actions with their source dialogue; treat model output as a draft |
| Schema validity mistaken for truth | State clearly that schema validation is structural only |
| Commitment heuristic mistaken for complete coverage | Describe it as a narrow warning that does not repair output or prove completeness |
| Test-split result presented as independent holdout | Disclose the 50-example test usage and avoid further tuning on that subset |
| Dataset license assumed to permit sharing | State Kaggle's Unknown license and do not redistribute dataset files |
| CPU runtime is slow | Run one dialogue at a time; model generation is separate from the offline test suite |
| Private dialogue data mishandled in future use | Obtain authorization, minimize retained text, and apply appropriate access controls |

## 9. Core references

- Original assignment brief: `../Reference_Material/Original_Group_Major_Project_Assignment_Brief.md`.
- Dataset source, Kaggle version/license note, expected files, checksums, and preprocessing: `../Implementation_and_Experiments/05_Dataset_Acquisition_and_Reproducibility.md`.
- Technical report and bibliography: `../Final_Assignment_Report.md`.
- Model comparison protocol and results: `../Implementation_and_Experiments/Model_Family_Comparison/README.md`.
- Experiment history and decisions: `../Implementation_and_Experiments/04_Experiment_and_Decision_Log.md`.

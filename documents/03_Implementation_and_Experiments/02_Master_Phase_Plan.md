# SAMSum Major Project — Master Phase Plan

**Group:** 19
**Project:** SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction
**Submission deadline:** 25 October 2026
**Internal feature freeze:** 21 October 2026
**Planning status:** Baseline and data-quality work completed; remaining items require evidence-based verification.

## 1. Execution Rules

1. Work through phases in order unless a documented dependency justifies a change.
2. Complete one small step at a time and verify its output before proceeding.
3. Update this plan and relevant evidence documents after each meaningful milestone.
4. Do not mark a task complete without a file, test, experiment result, or other verifiable evidence.
5. Use training and validation data for development decisions; reserve the test split for final evaluation.
6. Prioritize assignment requirements and a runnable end-to-end demo over optional enhancements.
7. Record individual group-member contributions for the final submission.

## 2. Phase Plan

| Phase | Scope | Expected deliverables | Completion criteria | Target |
|---|---|---|---|---|
| 1. Project control and architecture | Architecture, phase plan, requirement-to-evidence mapping | Architecture document, this plan, assignment matrix | All assignment requirements mapped to tasks and evidence | 16 Oct |
| 2. Dataset and preprocessing | Dataset audit, exclusions, leakage checks, length profiles, reproducible preprocessing | Raw/processed data notes, scripts, metadata, validation evidence | Processed splits pass documented checks; raw files preserved | 16 Oct |
| 3. Baseline generation | Run pretrained causal LM on at least three representative dialogues | Baseline script/notebook, configurations, saved outputs | Three or more outputs retained and inspected; limitations recorded | 17 Oct |
| 4. Prompt engineering | Zero-shot, few-shot, role/context, and constraint-based prompts | Reusable prompt templates, experiment log | Controlled comparison with representative outputs and observations | 18 Oct |
| 5. Decoding and model-family comparison | Greedy versus sampling; temperature, top-k/top-p; at least three course-covered model families | Experiment configurations, comparison table, technical justification | Feasible comparisons completed or limitations explicitly evidenced | 19 Oct |
| 6. Structured output and tool demo | Output contract, JSON Schema validation, callable tool/function demo, parameterized prompt | Schema, parser/validator, tests, tool demonstration | Valid and invalid outputs tested; tool behavior demonstrated | 19 Oct |
| 7. Evaluation and failure analysis | At least four evaluation criteria and at least three failure cases | Evaluation script/results, failure log, error analysis | Results and limitations are reproducible and supported by evidence | 20 Oct |
| 8. Integrated notebook/demo | Connect input, prompt, model, validation, structured results and display | Runnable notebook or demo, setup instructions | End-to-end happy path and representative failures tested | 20 Oct |
| 9. Report and presentation | Write report, prepare slides, document individual contributions | 10–15-page report, 8–10-minute presentation, contribution statements | Every required deliverable is present and cross-checked | 20 Oct |
| 10. Final verification and buffer | Clean execution, final test-split evaluation, repository review, presentation rehearsal | Final evidence, release checklist | Notebook/demo runs; report and artifacts are complete | Feature freeze 21 Oct; buffer 22–24 Oct |
| 11. Submission | Submit required artifacts | Final submission package | Submission confirmed before deadline | 25 Oct |

## 3. Current Status — Evidence Available

### Completed or evidenced

- Project folders and Python environment established.
- Raw SAMSum train, validation, and test CSVs audited.
- One training record with a missing dialogue identified and logged for exclusion.
- Raw split ID and exact dialogue-summary overlap checks completed.
- Character-length and Qwen tokenizer-length profiles generated.
- Processed CSVs, exclusion log, and preprocessing metadata generated.
- Independent processed-dataset validation passed.
- Raw CSV SHA-256 baseline recorded and later verification passed.
- Qwen2.5-1.5B-Instruct CPU smoke test succeeded.
- Data-quality report created and incrementally updated.
- High-level architecture document created.

### Still to verify or complete

- Assignment-to-evidence matrix.
- Three or more retained baseline outputs.
- Four prompt-style experiments.
- Decoding strategy experiments and model-family comparison.
- JSON Schema validation and callable tool/function demonstration.
- Reusable parameterized prompt.
- At least four evaluation criteria and three failure cases.
- Integrated runnable notebook/demo.
- Final report, presentation, and individual contribution statements.
- Final end-to-end and test-split evaluation.

## 4. Risk and Scope Controls

- CPU-only execution may constrain the size and number of models. Select feasible pretrained models and document any limitation; do not claim a comparison was completed if it was not.
- Keep experiments small initially, then expand only when the runtime and evidence justify it.
- Avoid spending time on repeated dataset checks after the established checks pass, unless a new issue is discovered.
- Do not claim that generated summaries or extracted action items are correct without evaluation.
- Keep optional enhancements subordinate to mandatory assignment deliverables.

## 5. Phase Exit Record

For each phase, record:

- Date completed
- Files or outputs produced
- Commands/tests/experiments executed
- Observed results
- Known limitations
- Remaining follow-up work

**Status labels:** Planned, In Progress, Implemented, Tested, Blocked.

## 6. Detailed Execution Roadmap

This section expands the high-level phase plan into ordered tasks. Existing artifacts must be inspected before creating replacements. A task is complete only when its acceptance criteria have supporting evidence.

### Phase 3 — Baseline Generation

**Objective:** Establish a reproducible baseline using the existing pretrained Qwen2.5-1.5B-Instruct model.

| Step | Task | Expected evidence | Acceptance criteria |
|---|---|---|---|
| 3.1 | Inspect existing model smoke-test script and its outputs | Script and output inventory | Identify what already works and what is missing |
| 3.2 | Select at least three representative SAMSum examples from development data | Example IDs and selection rationale | Inputs and reference summaries are recorded |
| 3.3 | Implement or adapt a baseline generation script | Reusable baseline script | Script loads the model, generates outputs, and handles inference consistently |
| 3.4 | Save baseline outputs and configurations | Experiment log and generated outputs | At least three outputs are retained with model, prompt, and decoding settings |
| 3.5 | Inspect output quality and runtime | Baseline observations | Record factual errors, omissions, runtime, and limitations |
| 3.6 | Update documentation and requirement matrix | Updated report and matrix | Evidence paths and truthful status are recorded |

**Exit criteria:** Three or more reproducible baseline outputs are available and inspected.

### Phase 4 — Reusable Prompt Engineering

**Objective:** Implement reusable, parameterized prompts and compare the four required prompt styles.

| Step | Task | Expected evidence | Acceptance criteria |
|---|---|---|---|
| 4.1 | Define the output contract | Documented output fields | Summary, key points, decisions, and action items are specified |
| 4.2 | Implement a reusable prompt builder | Module under src/prompts | Dialogue and prompt settings can be supplied without rewriting the template |
| 4.3 | Implement zero-shot prompting | Template and saved outputs | Runs successfully on selected examples |
| 4.4 | Implement few-shot prompting | Template, examples, and saved outputs | Demonstrations are explicitly included and documented |
| 4.5 | Implement role/context prompting | Template and saved outputs | Role and task context are explicit |
| 4.6 | Implement constraint-based prompting | Template and saved outputs | Output structure and constraints are explicit |
| 4.7 | Run controlled prompt comparisons | Prompt experiment log | Inputs and relevant settings are recorded consistently |
| 4.8 | Analyze differences and update documentation | Comparison table and observations | Conclusions are based on observed outputs, not assumptions |

**Exit criteria:** All four prompt styles are implemented and compared, with reusable templates and recorded outputs.

### Phase 5 — Decoding and Model-Family Comparison

**Objective:** Investigate generation settings and compare at least three generative model families covered in the course.

| Step | Task | Expected evidence | Acceptance criteria |
|---|---|---|---|
| 5.1 | Explain causal LM architecture, tokenization, and autoregressive generation | Technical report section | Explanations match the models and tokenizer actually used |
| 5.2 | Define feasible model-family candidates | Model selection table | Family, model, constraints, and rationale are documented |
| 5.3 | Implement greedy decoding comparison | Configuration and outputs | Greedy outputs are recorded for fixed inputs |
| 5.4 | Implement sampling comparison | Configuration and outputs | Sampling outputs are recorded for comparable inputs |
| 5.5 | Compare temperature, top-k, and top-p | Decoding experiment log | Supported settings and actual values are recorded |
| 5.6 | Compare feasible model families | Model comparison table | At least three course-covered families are addressed with evidence or clearly documented feasibility limitations |
| 5.7 | Compare prompting, RAG, fine-tuning, and PEFT conceptually | Report section | Trade-offs and project-specific justification are included |

**Exit criteria:** Required comparisons are evidenced; infeasible experiments have explicit technical justification and are not misrepresented as completed.

### Phase 6 — Structured Outputs and Tool Use

**Objective:** Make model outputs machine-readable, validate them, and demonstrate callable tool/function use.

| Step | Task | Expected evidence | Acceptance criteria |
|---|---|---|---|
| 6.1 | Finalize the structured output schema | Schema file | Required fields and types are defined |
| 6.2 | Implement output parsing and JSON Schema validation | Parser and validator | Valid output passes; invalid output is rejected or handled |
| 6.3 | Add positive and negative validation tests | Automated tests and results | Tests cover valid, malformed, and schema-invalid outputs |
| 6.4 | Implement a callable tool/function demonstration | Tool definition and invocation example | Arguments, invocation, and result are demonstrable |
| 6.5 | Test missing, unsupported, or uncertain information | Test cases and observations | Unsupported assignees, deadlines, or decisions are not silently invented |
| 6.6 | Document the implementation | Updated matrix and experiment notes | File paths and test evidence are recorded |

**Exit criteria:** Structured output validation and the callable tool/function demonstration work in verified test cases.

### Phase 7 — Evaluation and Failure Analysis

**Objective:** Evaluate quality systematically and analyze concrete failures.

| Step | Task | Expected evidence | Acceptance criteria |
|---|---|---|---|
| 7.1 | Select at least four evaluation criteria | Evaluation protocol | Each criterion has a definition and evaluation method |
| 7.2 | Define the development evaluation sample | Sample manifest | Selection method and IDs are recorded |
| 7.3 | Implement or document evaluation procedures | Evaluation script or rubric | Procedure can be repeated |
| 7.4 | Evaluate selected prompts and configurations | Results table | Actual results and settings are recorded |
| 7.5 | Document at least three failure cases | Failure log | Each case contains input, output, failure type, and analysis |
| 7.6 | Record limitations and conclusions | Evaluation report section | Claims are proportional to the available evidence |

**Exit criteria:** At least four criteria and three concrete failure cases are documented with supporting evidence.

### Phase 8 — Integrated Notebook or Demo

**Objective:** Demonstrate the complete conversation summarization workflow.

| Step | Task | Expected evidence | Acceptance criteria |
|---|---|---|---|
| 8.1 | Define the end-to-end execution flow | Notebook outline or demo plan | Components and data flow are explicit |
| 8.2 | Connect input, prompt builder, and model | Runnable integration | A conversation reaches the generation step |
| 8.3 | Connect parsing and schema validation | Integration tests | Invalid outputs are handled |
| 8.4 | Display summary, key points, decisions, and action items | Example results | Output is readable and consistent with the schema |
| 8.5 | Demonstrate prompt parameter changes | Multiple demo runs | Different settings can be selected without rewriting the prompt |
| 8.6 | Add responsible-use guidance and limitations | Demo notes or UI text | Uncertainty and human-review needs are communicated |
| 8.7 | Run an end-to-end verification | Test record | Successful and representative failure paths are checked |

**Exit criteria:** A documented, runnable end-to-end demonstration is available.

### Phase 9 — Report and Presentation

**Objective:** Assemble all evidence into the required deliverables.

| Step | Task | Expected evidence | Acceptance criteria |
|---|---|---|---|
| 9.1 | Draft the report from verified evidence | Report draft | Covers methodology, architecture, experiments, results, and limitations |
| 9.2 | Include architecture and experiment results | Diagrams, tables, examples | Claims link to actual evidence |
| 9.3 | Check report length | Page-count check | 10–15 pages excluding appendices and references |
| 9.4 | Prepare presentation | Slide deck | Covers the problem, design, experiments, findings, failures, and demo |
| 9.5 | Rehearse presentation | Timing and rehearsal notes | Fits 8–10 minutes |
| 9.6 | Collect individual contribution statements | Contribution record | Each group member's contribution is documented |
| 9.7 | Cross-check assignment requirements | Updated evidence matrix | Every mandatory requirement has evidence or an explicitly documented unresolved gap |

**Exit criteria:** The report, presentation, and contribution statements are ready for final review.

### Phase 10 — Final Verification and Buffer

**Target:** Feature freeze on 21 October 2026; buffer from 22–24 October 2026.

1. Verify repository paths and required deliverables.
2. Run automated tests and the integrated demo from the documented environment.
3. Perform final evaluation on the reserved test split; do not use its results to tune prompts or choose models.
4. Check JSON validation, tool demonstration, and representative failure cases.
5. Confirm report length, references, figures, and presentation timing.
6. Record known limitations and unresolved issues.
7. Fix submission-blocking defects first; avoid optional enhancements after feature freeze.

**Exit criteria:** All mandatory deliverables have been checked and remaining limitations are documented.

### Phase 11 — Submission

**Deadline:** 25 October 2026.

1. Verify the final report, runnable notebook/demo, dataset/preprocessing notes, prompt and decoding logs, JSON schema, tool demonstration, presentation, and individual contribution statements.
2. Confirm that required files are accessible and paths are correct.
3. Submit through the required course process.
4. Record submission confirmation.

**Exit criteria:** Required deliverables are submitted before the deadline.

## 7. Cross-Phase Documentation Rules

After each meaningful task:

- Record the date and task completed.
- Record commands, tests, or experiments actually executed.
- Identify output files and evidence paths.
- Record actual observations, failures, and limitations.
- Update the assignment-to-evidence matrix status.
- Do not mark a phase complete until its exit criteria are satisfied.

## 8. Immediate Next Action

Inspect the existing `model_smoke_test.py` and any available output artifacts. Do not create a duplicate baseline script until the existing implementation and evidence have been reviewed.

### Phase 3 — Existing Smoke-Test Review

**Review date:** 16 October 2026
**File inspected:** `model_smoke_test.py`

**Existing capabilities confirmed by code inspection:**
- Loads `Qwen/Qwen2.5-1.5B-Instruct` using Transformers.
- Runs inference on CPU and uses `torch.inference_mode()`.
- Constructs a chat prompt using the tokenizer's chat template.
- Generates one summary using greedy decoding (`do_sample=False`).
- Reports model loading and generation time.

**Gaps identified:**
- The conversation is hard-coded rather than selected from the processed SAMSum dataset.
- Only one output is generated.
- The output and run configuration are printed but not saved as experiment artifacts.
- The script does not compare the generated summary with the dataset reference summary.
- The script is a smoke test, not a complete baseline evaluation.

**Decision:** Reuse the existing model-loading and generation approach where appropriate. Extend or adapt it for the baseline experiment only after reviewing the processed dataset and choosing representative development examples. Avoid duplicating model-loading code unnecessarily.

**Status:** Code review completed; baseline experiment extension remains planned.

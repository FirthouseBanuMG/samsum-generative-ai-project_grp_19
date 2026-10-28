# SAMSum Major Project — Master Phase Plan

**Group:** 19
**Project:** SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction
**Original submission deadline:** 25 October 2026
**Internal feature freeze:** 21 October 2026
**Status reviewed:** 29 October 2026
**Planning status:** Core implementation, evidence review, report citation/consistency review, and presentation materials are present. Remaining work is final rendering, member confirmation, rehearsal, and course submission; see phase statuses below.

## 1. Execution Rules

1. Work through phases in order unless a documented dependency justifies a change.
2. Complete one small step at a time and verify its output before proceeding.
3. Update this plan and relevant evidence documents after each meaningful milestone.
4. Do not mark a task complete without a file, test, experiment result, or other verifiable evidence.
5. Use training and validation data for development decisions. The 50-sample test subset has already been used for model comparison; do not continue tuning against it or claim it as an untouched holdout.
6. Prioritize assignment requirements and a runnable end-to-end demo over optional enhancements.
7. Record individual group-member contributions for the final submission.

## 2. Phase Plan

| Phase | Implementation work | Deliverables / acceptance evidence | Status as of 29 Oct 2026 |
|---|---|---|---|
| 1. Project control and architecture | Define the system, requirements, package structure, and verification plan | Architecture, phase plan, evidence matrix | **Complete.** Architecture now represents the verified implementation and offline/runtime flows. |
| 2. Dataset and preprocessing | Audit raw splits, preserve raw files, create processed splits, validate and check overlap | Scripts, metadata, exclusion log, split checks | **Complete with a disclosed use limitation.** Raw integrity matches the recorded local baseline; processed splits validate with zero shared IDs/exact pairs. Kaggle lists the license as Unknown; the report records this and does not claim redistribution rights. |
| 3. Baseline generation | Generate and inspect at least three pretrained causal-LM examples | Saved outputs and run settings | **Complete.** Three qualitative training examples retained; factual errors/omissions documented. |
| 4. Prompt engineering | Implement and compare four prompt strategies; compare concise and detailed prompting | Reusable templates, logs, outputs, comparison | **Complete with limitation.** Four strategies and length styles compared; prompt rating sample is n=3 and exploratory. |
| 5. Decoding and model-family comparison | Compare greedy/sampling settings and feasible model configurations; explain model families | Decoding outputs, model metrics, architecture discussion | **Complete with limitations.** Qwen, FLAN-T5, and DistilBART compared on 50 test examples; test subset is not a pristine holdout and input formats differ. Standard VAE/GAN/autoregressive Transformer conceptual families are used without claiming verified lecture coverage. |
| 6. Structured output and tool demo | Generate JSON; parse, validate, recover; demonstrate allowlisted function round trip | Schema, runner, tests, saved tool evidence | **Complete.** Application-level JSON tool protocol tested; it is not native model tool calling. |
| 7. Evaluation and failure analysis | Apply criteria and document concrete failure examples | Scores, metrics, failure analysis, caveats | **Complete with limitations.** Evidence and failures documented; small qualitative samples do not establish general accuracy. |
| 8. Integrated notebook/demo | Connect processed input, generation, coverage warning, tool, final response | Executed notebook, CLI, saved demo output | **Complete with limitation.** CLI and notebook rerun on CPU. The model still omits an explicit commitment; a narrow heuristic warns but does not repair it. |
| 9. Report and presentation | Prepare report, slide deck, and contribution forms | 10–15-page report body, 10-slide deck, four-member contribution template | **Mostly complete.** Report evidence/citations were reviewed; latest render is 14 pages total with an 11-page body. Slide outline, proposed speaker split, and demo plan are ready; member confirmations and actual rehearsal/timing remain. |
| 10. Final verification and closeout | Run tests/data checks/demo; verify report/deck and limitations | Test results, data checks, rendered page count, review checklist | **Mostly complete.** 39 tests pass; data pipeline and notebook/CLI were rerun; current report render meets the 10–15-page body requirement. Final team review remains. |
| 11. Submission | Package and submit through course process | Submission confirmation | **Pending / team-owned.** Original deadline was 25 Oct 2026; no submission confirmation is recorded here. |

## 3. Current Status — Evidence Available

### Completed or evidenced

- Project folders and Python environment established.
- Raw SAMSum train, validation, and test CSVs audited.
- One training record with a missing dialogue identified and logged for exclusion.
- Raw split ID and exact dialogue-summary overlap checks completed; processed split ID and exact-pair leakage audit also passes.
- Character-length and Qwen tokenizer-length profiles generated.
- Processed CSVs, exclusion log, and preprocessing metadata generated.
- Independent processed-dataset validation passed.
- Raw CSV SHA-256 baseline recorded and later verification passed; Kaggle source page and version 1 recorded, but Kaggle lists the license as Unknown.
- Qwen2.5-1.5B-Instruct CPU smoke test succeeded.
- Data-quality report created and incrementally updated.
- High-level architecture and visual PNG updated to show the actual raw/processed, experiment, and integrated-runtime flows.
- Four prompt styles and decoding settings have saved experiment outputs.
- Three model configurations have a 50-sample comparison with saved metrics.
- Structured JSON output, schema tests, and an application-level tool demonstration have saved evidence.
- The tool result is returned to the model for a final response; success and validation-failure paths have offline tests, and the model-backed run is saved under `outputs/tool_calling/`.
- Integrated notebook and CLI completed a fresh CPU run; the narrow commitment warning is included in the output saved under `outputs/integrated_demo/`.
- Python modules are grouped directly under `src/` by responsibility, tests are under top-level `tests/`, and runnable commands use those package modules.
- Assignment report renders to 14 pages total (11-page body excluding references/appendices); a 10-slide presentation deck and simplified four-member contribution template are present.

### Still to verify or complete for submission

- Use the Kaggle source/version/license information already recorded; the license is Unknown, so do not claim redistribution rights or include dataset files in the submission.
- Each member must review, complete, and personally confirm their contribution statement.
- Assign presentation portions/speakers; rehearse and record actual duration (planned slide timing: 8:25).
- Complete final team approval and submit through the course process; no submission confirmation is recorded here.

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

### Phase 1 — Project Control and Architecture

**Objective:** Establish project scope, repository conventions, traceability, and an architecture that matches the actual implementation.

| Step | Task | Evidence / acceptance |
|---|---|---|
| 1.1 | Read the assignment brief and identify technical and submission requirements | Requirements are represented in the evidence matrix |
| 1.2 | Establish repository layout, Python environment, and run/test conventions | Modules have clear responsibility-based locations; documented commands work |
| 1.3 | Draw the data-preparation, experiment, and integrated-runtime flows | Mermaid and PNG diagrams describe the same verified architecture |
| 1.4 | Define project constraints and evidence rules | Raw/processed boundary, no-training scope, output limitations, and verification expectations are explicit |

**Exit criteria:** Architecture, phase plan, and evidence matrix correspond to the repository and observed behavior.

**Status:** Complete. The architecture text and PNG were reconciled with the implemented data and model paths on 28 October 2026.

### Phase 2 — Dataset Audit and Preprocessing

**Objective:** Preserve raw data, produce validated processed splits, and record provenance and data-use limits.

| Step | Task | Evidence / acceptance |
|---|---|---|
| 2.1 | Validate raw split structure, IDs, missing text, and row counts | `data_processing.validate_dataset` output reviewed |
| 2.2 | Profile dialogue/summary lengths and model-tokenizer lengths | Profiling output recorded for each split |
| 2.3 | Verify raw files against the recorded local SHA-256 baseline | Hash check passes; its historical-baseline limitation is documented |
| 2.4 | Preprocess into separate processed files and log exclusions | Raw files stay unchanged; invalid training row and reason are logged |
| 2.5 | Independently validate processed splits and check cross-split IDs/exact pairs | All processed split assertions pass; overlap counts are zero |
| 2.6 | Record source and license information without inferring redistribution rights | Kaggle page/version 1 recorded; Unknown license and missing archive provenance disclosed |

**Exit criteria:** Processed splits pass validation, raw files remain separate, and provenance/licensing limitations are explicit.

**Status:** Data checks and preprocessing complete. Kaggle source/version are recorded; the Unknown license is disclosed and no redistribution permission is claimed.

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

**Status:** Complete. Three Qwen outputs from processed training examples are saved with settings; qualitative omissions and unsupported claims are documented. This is a pipeline smoke test, not a population-level accuracy estimate.

### Phase 4 — Reusable Prompt Engineering

**Objective:** Implement reusable, parameterized prompts and compare the four required prompt styles.

| Step | Task | Expected evidence | Acceptance criteria |
|---|---|---|---|
| 4.1 | Define the output contract | Documented output fields | Summary, key points, decisions, and action items are specified |
| 4.2 | Implement a reusable prompt builder | `src/prompting/prompts.py` | Dialogue and prompt settings can be supplied without rewriting the template |
| 4.3 | Implement zero-shot prompting | Template and saved outputs | Runs successfully on selected examples |
| 4.4 | Implement few-shot prompting | Template, examples, and saved outputs | Demonstrations are explicitly included and documented |
| 4.5 | Implement role/context prompting | Template and saved outputs | Role and task context are explicit |
| 4.6 | Implement constraint-based prompting | Template and saved outputs | Output structure and constraints are explicit |
| 4.7 | Run controlled prompt comparisons | Prompt experiment log | Inputs and relevant settings are recorded consistently |
| 4.8 | Analyze differences and update documentation | Comparison table and observations | Conclusions are based on observed outputs, not assumptions |

**Exit criteria:** All four prompt styles are implemented and compared, with reusable templates and recorded outputs.

**Status:** Complete with a small-sample limitation. The four prompt strategies and concise-versus-detailed comparison have saved outputs; human rubric comparisons use n=3.

### Phase 5 — Decoding and Model-Family Comparison

**Objective:** Investigate generation settings, compare feasible model configurations, and provide a conceptual comparison of standard generative-model families without claiming unverified lecture coverage.

| Step | Task | Expected evidence | Acceptance criteria |
|---|---|---|---|
| 5.1 | Explain causal LM architecture, tokenization, and autoregressive generation | Technical report section | Explanations match the models and tokenizer actually used |
| 5.2 | Define feasible model-family candidates | Model selection table | Family, model, constraints, and rationale are documented |
| 5.3 | Implement greedy decoding comparison | Configuration and outputs | Greedy outputs are recorded for fixed inputs |
| 5.4 | Implement sampling comparison | Configuration and outputs | Sampling outputs are recorded for comparable inputs |
| 5.5 | Compare temperature, top-k, and top-p | Decoding experiment log | Supported settings and actual values are recorded |
| 5.6 | Compare feasible model configurations and conceptual families | Model comparison table and report | Three tested systems are compared; conceptual VAE/GAN/autoregressive Transformer comparison is clearly distinguished from empirical architectures |
| 5.7 | Compare prompting, RAG, fine-tuning, and PEFT conceptually | Report section | Trade-offs and project-specific justification are included |

**Exit criteria:** Required comparisons are evidenced; infeasible experiments have explicit technical justification and are not misrepresented as completed.

**Status:** Complete with limitations. The 50-sample test-split comparison is comparative evidence, not an untouched holdout; tested systems cover causal and encoder-decoder architectures, not three distinct empirical families.

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

**Status:** Tested. The JSON-schema validator, allowlisted tool, model follow-up after the tool result, and blocked-invalid-result path are implemented; the round-trip evidence is saved in `outputs/tool_calling/tool_calling_demo.json`. This uses an application-level JSON protocol, not native model-specific tool-call parsing.

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

**Status:** Complete with limitations. Evaluation tables and qualitative failures are documented; small samples do not establish general model accuracy.

### Phase 8 — Integrated Notebook or Demo

**Objective:** Demonstrate the complete conversation summarization workflow, including the tool result and final model response.

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

**Status:** Tested on CPU using the notebook and CLI with training sample `13818513`. The model still omits an explicit delivery commitment despite the prompt instruction; a narrow heuristic now emits a review warning but does not repair output or prove completeness.

### Package Organization Follow-up

The Python source is grouped directly under `src/` (`data_processing`, `baseline`, `prompting`, `generation`, `evaluation`, `structured_output`, `tool_calling`, and `application`) with no extra project-named package directory. All test modules live in top-level `tests/`. Internal imports use these package paths and shared project-root constants; current run and test commands are documented in the README. Editable installation and the Python test suite were verified.

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

**Status:** Mostly complete. The report renders to 14 pages total (11-page body excluding references/appendices); evidence/citation review is done. The 10-slide deck and simplified contribution template exist. Member statements and rehearsal remain.

### Phase 10 — Final Verification and Buffer

**Target:** Feature freeze on 21 October 2026; buffer from 22–24 October 2026.

1. Verify repository paths and required deliverables.
2. Run automated tests and the integrated demo from the documented environment.
3. Do not run further tuning or claim a pristine final holdout on the 50-sample test subset already used for model comparison; report the existing results as comparative evidence.
4. Check JSON validation, tool demonstration, and representative failure cases.
5. Confirm report length, references, figures, and presentation timing.
6. Record known limitations and unresolved issues.
7. Fix submission-blocking defects first; avoid optional enhancements after feature freeze.

**Exit criteria:** All mandatory deliverables have been checked and remaining limitations are documented.

**Status:** Software and artifact checks are substantially complete: 39 tests pass, data checks pass, notebook/CLI were executed, and the current report render is 14 pages total with an 11-page body. Member confirmation, rehearsal, and submission confirmation remain.

### Phase 11 — Submission

**Original deadline:** 25 October 2026 (passed).

1. Verify the final report, runnable notebook/demo, dataset/preprocessing notes, prompt and decoding logs, JSON schema, tool demonstration, presentation, and individual contribution statements.
2. Confirm that required files are accessible and paths are correct.
3. Submit through the required course process.
4. Record submission confirmation.

**Exit criteria:** Required deliverables are submitted through the course process and confirmation is recorded.

**Status:** No submission confirmation is recorded in this project workspace.

## 7. Cross-Phase Documentation Rules

After each meaningful task:

- Record the date and task completed.
- Record commands, tests, or experiments actually executed.
- Identify output files and evidence paths.
- Record actual observations, failures, and limitations.
- Update the assignment-to-evidence matrix status.
- Do not mark a phase complete until its exit criteria are satisfied.

## 8. Current Closeout Actions

These are human/team-owned actions rather than unfinished implementation phases:

1. Keep final submission formatting consistent with the verified 13-page render (11-page body).
2. Have each member write a short, accurate contribution statement, confirm it, and add the date.
3. Confirm the proposed speaker split; rehearse and record an 8–10-minute presentation including the demo.
4. Submit the required materials through the course process and save the submission confirmation.

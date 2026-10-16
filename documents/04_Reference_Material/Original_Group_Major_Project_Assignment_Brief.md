**BIRLA INSTITUTE OF TECHNOLOGY & SCIENCE, PILANI
Work Integrated Learning Programmes Division
PCAM\* ZG516 – APPLIED GENERATIVE AI
GROUP MAJOR PROJECT / ASSIGNMENT – 1
Integrated Generative-AI Application: From LLM Foundations to Reliable Prompted Systems**

| **Course** | PCAM\* ZG516 – Applied Generative AI |
|----|----|
| **Coverage** | CS1–CS5 + ELS 1 |
| **Assignment Type** | Group Major Project / Work Integrated Learning Assignment |
| **Maximum Marks** | 20 |
| **Project Team** | As per approved group allocation |
| **Dataset Choice** | ONE dataset from five approved datasets |
| **Submission** | Technical report + Colab notebook/code + demonstration + contribution statement |

# 1. Broad Major Project Description

The objective of this major group project is to design, implement and critically evaluate a small,
domain-oriented Generative-AI application using an open dataset and a pretrained language model.
The project should demonstrate the complete learning journey covered in the first five contact sessions:
understanding generative models, understanding LLM architecture and autoregressive generation, selecting an
adaptation strategy, engineering effective prompts, controlling generation, and producing structured/tool-assisted
outputs.

The project is not intended to train a large language model from scratch. Instead, students are expected to
treat a pretrained LLM as the foundation of an application and investigate how prompt design, context,
decoding controls and lightweight adaptation choices affect application behaviour.

Each group must select ONE approved dataset and build a meaningful application around it. The final system
should include a clearly defined user problem, dataset analysis, model/prompt design, controlled generation,
structured output, at least one tool/function interface, and evidence-based evaluation.

# 2. Project Theme

Build a small Generative-AI application that converts a real-world information or language task into a reliable LLM workflow. The application should answer a user need rather than simply demonstrate that an LLM can generate text.

# 3. Approved Dataset Options – Select ONE

| **Option** | **Dataset** | **Suggested Project Domain** | **Core Task** | **Typical Project Output** |
|----|----|----|----|----|
| D1 | BANKING77 | Banking / customer service assistant | Intent understanding + response generation | Intent + response + optional action |
| D2 | DailyDialog | Conversational assistant | Context-aware dialogue generation | Context + response + dialogue analysis |
| D3 | SAMSum | Meeting/conversation summarization | Abstractive summarization | Structured summary + action items |
| D4 | AG News | News intelligence assistant | Topic classification + explanation | Category + explanation + key information |
| D5 | SQuAD | Question-answering assistant | Context-grounded QA | Answer + evidence/context + confidence |

Dataset selection rule: each group selects one dataset. A maximum of five groups may select the same dataset. Selection should be registered with the instructor on a first-confirmed basis. Groups using the same dataset must still develop distinct application designs, prompts, experiments and analysis.

# 4. Major Project Requirements

**1. Problem Definition:** Define the target user, problem, application scenario, expected input and expected output. State why a Generative-AI/LLM solution is appropriate.

**2. Dataset Understanding:** Describe the selected dataset, relevant fields, sample size used, representative examples, data preparation and the subset used for experiments.

**3. Generative Model Analysis:** Compare at least three generative-model families covered in CS1 and justify why an LLM/causal language model is appropriate for the selected application.

**4. LLM Architecture:** Explain tokenization, embeddings, Transformer/attention, language-modelling head and the autoregressive generation process in the context of the project.

**5. Baseline System:** Implement a baseline using a pretrained Hugging Face causal language model and a simple prompt.

**6. Prompt Engineering:** Develop and compare zero-shot, few-shot, role/context-based and constraint-based prompts.

**7. Decoding Study:** Compare greedy decoding with sampling using temperature and at least one of top-k/top-p. Analyse output quality and variability.

**8. Adaptation Decision:** Compare prompting, RAG and fine-tuning/PEFT. Explain which is most appropriate for the project and why. Actual fine-tuning is optional unless approved.

**9. Structured Output:** Design a machine-readable output schema. Demonstrate structured JSON or an equivalent validated format.

**10. Tool / Function Calling:** Design at least one useful function/tool for the application. Define its input and output schema and demonstrate one representative invocation or simulation.

**11. Programmatic Prompting:** Create a reusable prompt template and demonstrate parameterized/programmatic generation.

**12. Evaluation:** Evaluate the system using at least four criteria appropriate to the application and include failure/error analysis.

**13. Responsible Use:** Identify likely hallucination, misuse, privacy, data leakage or reliability risks relevant to the chosen application and propose practical controls.

# 5. Minimum Technical Workflow

- Dataset → preprocessing/sample selection → prompt/input construction

- Prompt → tokenizer → pretrained LLM → autoregressive generation

- Generation → decoding control → response

- Response → structured-output validation

- User request → LLM → tool/function decision → tool result → final response

- Evaluation dataset → baseline vs improved prompt/system → comparative analysis

# 6. Required Experiments

| **Experiment** | **Minimum requirement** | **Evidence** | **Purpose** |
|----|----|----|----|
| E1 – Baseline | One simple prompt | At least 3 outputs | Establish baseline |
| E2 – Prompt comparison | At least 4 prompt variants | Comparison table | Study prompt engineering |
| E3 – Decoding | Greedy + temperature + top-k/top-p | Output examples | Study generation control |
| E4 – Structured output | One schema + validation | JSON examples | Reliable machine-readable response |
| E5 – Tool/function | At least one function | Schema + invocation | Demonstrate tool-assisted workflow |
| E6 – Failure analysis | At least 3 failure cases | Analysis table | Understand limitations |
| E7 – Final system | Integrated workflow | Notebook/demo | Demonstrate complete application |

# 7. Application-Specific Expectations

**BANKING77:** Build an assistant that identifies customer intent and generates a safe response. Tool examples may include simulated transaction-status lookup, card-blocking request or branch lookup. Do not use real banking credentials/data.

**DailyDialog:** Build a context-aware conversational assistant. Study how the amount of dialogue context and prompt structure affects response relevance and consistency.

**SAMSum:** Build a meeting/conversation summarizer that produces a structured summary, key points, decisions and action items. Compare concise and detailed prompting.

**AG News:** Build a news-intelligence assistant that identifies the news category and generates a concise explanation or structured insight. Compare zero-shot and few-shot prompting.

**SQuAD:** Build a context-grounded question-answering assistant. Require the model to answer only from supplied context and analyse cases where the answer is unavailable or uncertain.

# 8. What Students Should NOT Do

- Do not train a large LLM from scratch.

- Do not submit only screenshots of ChatGPT/LLM conversations.

- Do not use prompts without explaining why they were designed.

- Do not claim model accuracy without an evaluation procedure.

- Do not expose real personal, financial, medical or confidential information.

- Do not treat generated text as automatically correct.

- Do not make later course modules such as diffusion/image generation or multimodal generation mandatory for this assignment.

# 9. Deliverables

- Technical report: approximately 10–15 pages excluding appendix/references.

- Working Google Colab notebook or equivalent executable implementation.

- Dataset description and preprocessing record.

- Prompt experiment log containing baseline and improved prompts.

- Decoding comparison table.

- Structured-output schema and sample validated outputs.

- Tool/function-calling specification and demonstration.

- Evaluation and failure-analysis table.

- 8–10 minute group demonstration/presentation.

- Individual contribution statement signed/confirmed by every member.

# 10. Suggested Report Structure

1.  Title page and group/member details

2.  1\. Abstract

3.  2\. Problem statement and motivation

4.  3\. Dataset description and preparation

5.  4\. Generative-model and LLM architecture analysis

6.  5\. Proposed application architecture

7.  6\. Baseline LLM implementation

8.  7\. Prompt-engineering experiments

9.  8\. Decoding experiments

10. 9\. Adaptation strategy: prompting vs RAG vs PEFT

11. 10\. Structured output and tool/function calling

12. 11\. Evaluation and results

13. 12\. Failure analysis and responsible-use considerations

14. 13\. Limitations

15. 14\. Conclusion and future work

16. References

17. Appendix: prompts, schemas, code/output samples

# 11. Assessment Rubric – 20 Marks

| **Component** | **Assessment focus** | **Marks** |
|----|----|----|
| Problem + dataset analysis | Problem clarity, dataset understanding, preprocessing and application relevance | 2 |
| LLM/generative-model understanding | CS1–CS3 concepts, architecture, autoregressive generation and decoding | 3 |
| Prompt engineering | Quality and systematic comparison of prompt strategies | 3 |
| Adaptation strategy | Prompting vs RAG vs PEFT reasoning and technical justification | 2 |
| Structured output + tool calling | Schema, validation and function/tool workflow | 3 |
| Implementation | Working Colab/notebook and reproducibility | 3 |
| Evaluation + failure analysis | Evidence, comparison, errors/hallucination analysis | 2 |
| Report + demonstration + contribution | Technical communication and individual contribution | 2 |

# 12. Course Outcome Alignment

| **CO** | **Project evidence** | **Coverage** |
|----|----|----|
| CO1 | Generative-model landscape, LLM architecture and generation | Strong |
| CO2 | Prompt engineering, structured outputs, templating and tool/function calling | Strong |
| CO3 | End-to-end LLM application design | Strong |
| CO4 | Failure analysis, safe/appropriate use and reliability considerations | Moderate |

# 13. Group Allocation

| **Group** | **Members** |
|----|----|
| 1 | SUNIDHI SHARMA; SAAKSHI; SHAH JESAL KIRIT PRADNYANA; NIDHI SHARMA |
| 2 | ABIJITH M G; SHUBHRA KHARE; AVINASH KUMAR BARNWAL; SUDHIR KUMAR |
| 3 | MD TANWEER ANWAR; DEBMALLYA CHAKRABORTY; AMIT KUMAR KAUSHIK; KARTHIKEYAN B |
| 4 | YELLAMELLI BAPURAJU; GADDE CHARAN; P VISHALA; AKKIRAJU CHAKRITHA |
| 5 | SANTOSH S; UGRAPPAGARI CHANDRASEKHAR REDDY; SHARAVANAN C; POOJA MISHRA |
| 6 | SUNEIIL SINGHH; VENKATAKRISHNA BHAT K; MOPURI NAGARAJU; D ASRITHA |
| 7 | NARKHEDE HARSHAL SANJAY; PARBALKAR PRANIL RAMESH RASHMI; DOLSY NARANG; BOROLE OM RAM |
| 8 | GM CHANDRA KISHORE; CHINTAPATLAWAR ADARSH SANTOSH; FIROS M; VIJAYA KUMAR NALLA |
| 9 | SNEHALATHA M; KARTHIK K; S. BHAGAT SINGH; PAVANI A RAMESH BABU |
| 10 | BHALLAMUDI VENKATA SRINIVAS KIRAN; SOURAV KUMAR; CHETAN RAGHAV; ANISHA PRAKASH DALSANIA |
| 11 | NAVNEET KASHYAP; BIJU K.; KAMMADANAM SOWMYA; PARVEEN KUMAR |
| 12 | AKSHAYA B; SAGAR S; VIVEK KUMAR DATTA; NIKHIL AGARWAL |
| 13 | KARTIKEY RANA; KALANGI PRAMOD; GEETHA M; MOHAMMED NADEEMODDIN MOIZODDIN |
| 14 | NARAYAN PRASAD; ASWATHI ANANDRAJ; ANKITA DUBEY; BUVANESWARI E |
| 15 | VENKATA SRINIVASA RAO TUNUGUNTLA; ANIL KUMAR REDDY K; TAKKARS BHAVANI; NISHA PALANISAMY |
| 16 | KOTA VAMSI KRISHNA; ABHISHEK SEKHAR; BIKRAM KUMAR SWAIN |
| 17 | SRINIVASAN N S; SABARINATH R; HARIHARAN E; SAHANA R |
| 18 | PRATYUSHA Y N; SHAH RONAK YOGESHKUMAR; EDWIN JUDE; SRIKANTH AMITI |
| 19 | CHAUDHARI GANESH GOVIND; RAMNIWASH KUMAR; SONAL GUPTA; FIRTHOUSE BANU M G |
| 20 | SNEHALATA MUNDHE; POONAM LAXMAN KESARKAR; HIROLE SHWETA KALLAPPA; VINAY VISHNUDAS RAKHUNDE |
| 21 | GANESH K; ROHIT KHANDELWAL; MEKHLA SEN; SANCHIKA |
| 22 | NANDHALURU KISHORE; VISHRUTH M; SATYA PRAKASH; SHRUTI DUBEY |
| 23 | GIRISH M; BHOOMIKA BATHLA; TENDOLKAR MOHIT NARENDRA NEHA; RAO SHRAVAN HARSHA JAYSHREE |
| 24 | MANASA RAAJHESH; KAPIL CHHABRA; TARUNKUMAR S; SOLANKI MITUL |
| 25 | LAVANYA G V (Individual) |

# 14. Final Student Instruction

Treat this as a major integrated project, not as a collection of independent exercises. Every design decision must be supported by an experiment, observation or technical justification. All members must be able to explain the complete workflow during the demonstration.

**End of Group Major Project / Assignment – 1**

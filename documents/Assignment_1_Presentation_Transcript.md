# Assignment 1 Presentation Transcript — Approximately 10 Minutes

**Project:** SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction
**Course:** PCAM* ZG516 — Applied Generative AI
**Group 19:** CHAUDHARI GANESH GOVIND; RAMNIWASH KUMAR; SONAL GUPTA; FIRTHOUSE BANU M G

This script follows the nine presentation slides. It should take about 9 minutes 45 seconds, including the one-minute demo. The speaker split below is a proposal; please confirm it with the group and rehearse with the slides.

## 0:00–1:50 — CHAUDHARI GANESH GOVIND

### Slide 1 — The problem

Good morning. We are Group 19. Our project is about summarizing conversations and finding action items in them.

In a chat, a decision or promise can be spread across several messages. It can take time to find it again. A summary can help, but the model might miss a promise or say someone agreed to something when they did not.

We built a system that reads a conversation and produces a short summary, key points, decisions, and action items. It is a first draft for a person to check. It should not be treated as the final source of truth.

### Slide 2 — Dataset and preparation

We used SAMSum. It contains chat-style conversations and summaries written by people. Each example has an ID, a conversation, and its reference summary.

After processing the data, we had 14,731 training examples, 818 validation examples, and 819 test examples. One training example had no conversation text, so we left it out of the processed data and recorded that decision.

We obtained the dataset from a Kaggle listing. Its license is marked “Unknown,” so we have not included the data files in our repository or claimed permission to redistribute them.

We also used 50 examples from the test split to compare models. Because we looked at those results, they are not a fresh, untouched final test. I’ll hand over to Ramniwash to explain the models and how they generate text.

## 1:50–3:50 — RAMNIWASH KUMAR

### Slide 3 — Generative-model choices

The project discusses three model types: variational autoencoders, or VAEs; generative adversarial networks, or GANs; and autoregressive Transformers. These are different ways to generate data.

For our model tests, we used Qwen2.5-1.5B-Instruct, FLAN-T5-base, and DistilBART-CNN. These are pretrained models; we did not train them or fine-tune them for this project.

There is a difference between the types we discuss and the systems we tested. Qwen generates text one token at a time using earlier text. FLAN-T5 and DistilBART use an encoder and a decoder. So our experiments compare three models, but they do not test all three model types mentioned on the slide.

We used Qwen in the final demo because it follows instructions and can produce the JSON format our application expects.

### Slide 4 — How generation works

The model first turns the conversation and the prompt into tokens. You can think of tokens as pieces of words. It uses those tokens as context and predicts what token should come next.

With greedy decoding, it picks the most likely next token. With sampling, settings such as temperature, top-k, and top-p affect which token it picks. It repeats this process until the answer is finished.

This explains how the model writes a response, but it does not check whether the response is true. It can still miss a promise or mistake a suggestion for a decision. Sonal will explain the tests we ran.

## 3:50–6:10 — SONAL GUPTA

### Slide 5 — Prompt and decoding experiments

We tried four ways of writing the prompt: zero-shot, few-shot, role or context-based, and constraint-based. We looked at relevance, whether important details were included, factual consistency, and how reliably the model followed the requested format.

In our manual review of three examples, few-shot prompting had the highest average score. That is a small test. It does not prove that few-shot prompting is always better.

We also compared greedy decoding with three sampling settings. Sampling gave us more varied answers, but some answers included details that were not in the conversation. So more variety did not always mean a better summary.

### Slide 6 — Model comparison

We compared the three models on the same 50 test conversations using ROUGE scores. ROUGE checks how much the generated summary’s wording overlaps with the human-written reference summary.

FLAN-T5 scored 0.514 for ROUGE-1, 0.248 for ROUGE-2, and 0.429 for ROUGE-L. DistilBART scored 0.265, 0.098, and 0.200. Qwen scored 0.221, 0.072, and 0.159.

These scores tell us about word overlap. They do not tell us whether every statement is true or whether every action item is correct. The models also did not receive exactly the same input: Qwen and FLAN-T5 received a prompt with constraints, while DistilBART received just the conversation. So this is a comparison of the tested setups, not a fair test of model architecture alone. And, as mentioned, these 50 examples are not an untouched final test.

Firthouse will explain how the application checks the model’s output.

## 6:10–7:25 — FIRTHOUSE BANU M G

### Slide 7 — Structured output and tool

The model is asked to return a summary, key points, decisions, and action items. An action item can include who owns it, what needs to be done, and a due date if one was mentioned.

The application checks whether the response is valid JSON and has the fields we expect. If it is not valid, the application asks the model to try one more time. If that still fails, it keeps a flagged fallback for review.

When the output passes the checks, the application sends it to an allowlisted validation function. If the function accepts it, the model uses that result to write the final response. These checks confirm the structure, not whether the content is true.

We also have a small check for some missed commitments. It can show a warning, but it cannot fix the summary. Ramniwash will show an example.

## 7:25–8:25 — RAMNIWASH KUMAR

### One-minute demo

This is a saved example from the training data. In the conversation, Amanda says she baked cookies and will bring some the next day. Jerry accepts.

The model’s JSON is in the right format, but it misses Amanda’s promise in the action items. Our check notices this example and shows a warning. It does not add the missing promise to the answer.

So the output can pass the format check and still miss something important. That is why we need to compare it with the original conversation.

**Show:** the conversation, generated result, validation result, and warning. Use the saved result at `outputs/integrated_demo/demo_result.json` if live generation is slow.

## 8:25–9:45 — FIRTHOUSE BANU M G

### Slide 8 — Failures and safeguards

We saw other mistakes too. Sometimes a suggestion was written as if it were a firm decision. Sometimes the model added details that were not in the chat. A response can also have valid JSON and still contain a wrong action item.

We use prompts and format checks to reduce some of these problems. The application limits which validation function can run, and it shows warnings when certain problems are found. These checks do not guarantee a correct or complete summary. A person still needs to check important details against the conversation.

If this kind of system were used with private chats, the team would also need permission to use them and safeguards for handling that data.

### Slide 9 — Conclusion

We built the summarization workflow and tested different prompts, decoding settings, and models. Our results are useful for comparing the versions we tested, but they have limits: the prompt review used only three examples, the model inputs differed, and 50 examples from the test split were used in the comparison.

The main point is simple: a summary that looks correct or has valid JSON can still be wrong. This system should help a person, not make decisions for them.

Thank you. We’re ready for your questions.

## Rehearsal checklist

- Confirm the speaker assignments with the group.
- Keep the demo to about one minute; use the saved result if needed.
- Rehearse with the slides and check the actual time.
- Speak at a comfortable pace. The timings are estimates, not a completed rehearsal.

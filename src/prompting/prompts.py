"""
Prompt templates for the SAMSum conversation summarization project.

Strategies:
1. Zero-shot prompting
2. Few-shot prompting
3. Role/context-based prompting
4. Constraint-based prompting
"""


def zero_shot_prompt(dialogue: str) -> str:
    """Summarize without providing an example."""

    return f"""
Summarize the following conversation.

Capture the main event, important information,
decisions, and agreed actions.

Conversation:
{dialogue}

Summary:
""".strip()


def few_shot_prompt(dialogue: str) -> str:
    """Summarize using one example."""

    return f"""
Summarize conversations by identifying the main
event and important information.

Example:

Conversation:
Amanda: I baked cookies. Do you want some?
Jerry: Sure!
Amanda: I'll bring you tomorrow :-)

Summary:
Amanda baked cookies and will bring some to Jerry tomorrow.

Now summarize the following conversation.

Conversation:
{dialogue}

Summary:
""".strip()


def role_based_prompt(dialogue: str) -> str:
    """Summarize with a specific role and context."""

    return f"""
You are a careful conversation summarization assistant.

Identify:
- The people involved
- The main topic or event
- Important decisions or intentions
- Actions that participants explicitly agree to take

Write a concise summary in natural language.

Use only information supported by the conversation.
Do not invent details.

Conversation:
{dialogue}

Summary:
""".strip()


def constraint_based_prompt(dialogue: str) -> str:
    """Summarize using explicit constraints."""

    return f"""
Summarize the conversation using these rules:

1. Use only facts explicitly supported by the dialogue.
2. Do not invent events, intentions, or decisions.
3. Distinguish suggestions from decisions or commitments.
4. Preserve important names, events, and actions.
5. Do not add information absent from the conversation.
6. If an intention is uncertain, keep it uncertain.
7. Write approximately 1-3 sentences.
8. Return only the summary.

Conversation:
{dialogue}

Summary:
""".strip()


def structured_json_prompt(dialogue: str) -> str:
    """Summarize and return a machine-readable JSON object.

    The model is asked to return a JSON object matching the structured
    output schema. This prompt backs experiment E4.
    """

    return f"""
You are a conversation summarization assistant.

Summarize the following conversation and return the result
as a single JSON object with exactly these fields:

- "summary": a concise natural-language summary (string).
- "key_points": a list of important facts from the conversation (strings).
- "decisions": a list of decisions explicitly made in the conversation (strings).
- "action_items": a list of objects, each with:
    - "owner": the person responsible (string)
    - "task": the action they agreed to take (string)
    - "due": a due date if stated, otherwise null

Rules:
- Use only information explicitly supported by the conversation.
- Read every speaker turn before drafting. Do not skip a short final turn.
- Capture explicit future commitments, including who committed to the action
  and when, in the summary and action_items. For example, include an action
  when a speaker says "I will" or "I'll" do something and the statement is
  not tentative.
- Leave action_items empty only when no participant explicitly commits to a
  future action. Do not turn suggestions, questions, or tentative plans into
  commitments.
- If there are no key points or decisions, use an empty list.
- Keep suggestions and tentative intentions out of "decisions".
- Do not invent action items. If there are none, use an empty list [].
- Return only the JSON object. Do not add explanations or code fences.

Example:
{{"summary": "Amanda baked cookies and will bring some to Jerry tomorrow.", "key_points": ["Jerry accepts Amanda's offer of cookies."], "decisions": ["Amanda will bring cookies to Jerry tomorrow."], "action_items": [{{"owner": "Amanda", "task": "Bring cookies to Jerry", "due": "tomorrow"}}]}}

Conversation:
{dialogue}

JSON:
""".strip()


def concise_summary_prompt(dialogue: str) -> str:
    """Request a concise summary while preserving essential supported facts."""
    return _summary_detail_prompt(
        dialogue,
        length_instruction=(
            "Write exactly one concise sentence. Include the main event "
            "and any explicit decision or agreed action."
        ),
    )


def detailed_summary_prompt(dialogue: str) -> str:
    """Request a detailed summary of salient supported conversation facts."""
    return _summary_detail_prompt(
        dialogue,
        length_instruction=(
            "Write 3-5 concise sentences. Cover the main event, important "
            "key points, explicit decisions, and agreed actions. Do not "
            "repeat the same information."
        ),
    )


def _summary_detail_prompt(dialogue: str, length_instruction: str) -> str:
    """Build the shared prompt while varying only the requested detail level."""
    if not isinstance(dialogue, str) or not dialogue.strip():
        raise ValueError("Dialogue must be a non-empty string.")

    return f"""
Summarize the following conversation.

{length_instruction}
Use only facts supported by the dialogue. Distinguish suggestions and
uncertain intentions from decisions or commitments. Do not invent details.
Return only the summary.

Conversation:
{dialogue}

Summary:
""".strip()


SUMMARY_DETAIL_PROMPTS = {
    "concise": concise_summary_prompt,
    "detailed": detailed_summary_prompt,
}


def build_summary_detail_prompt(style: str, dialogue: str) -> str:
    """Build a concise or detailed summary prompt for a dialogue."""
    if style not in SUMMARY_DETAIL_PROMPTS:
        available = ", ".join(SUMMARY_DETAIL_PROMPTS)
        raise ValueError(
            f"Unknown summary detail style: {style}. Available: {available}"
        )
    return SUMMARY_DETAIL_PROMPTS[style](dialogue)


PROMPT_FUNCTIONS = {
    "zero_shot": zero_shot_prompt,
    "few_shot": few_shot_prompt,
    "role_based": role_based_prompt,
    "constraint_based": constraint_based_prompt,
}


def build_prompt(strategy: str, dialogue: str) -> str:
    """Build a prompt using the requested strategy."""

    if not isinstance(dialogue, str) or not dialogue.strip():
        raise ValueError("Dialogue must be a non-empty string.")

    if strategy not in PROMPT_FUNCTIONS:
        available = ", ".join(PROMPT_FUNCTIONS.keys())
        raise ValueError(
            f"Unknown strategy: {strategy}. Available: {available}"
        )

    return PROMPT_FUNCTIONS[strategy](dialogue)

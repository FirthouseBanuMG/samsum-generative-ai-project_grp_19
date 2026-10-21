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

    The model is asked to return only a JSON object matching the
    structured-output schema (a summary string and an action_items
    array). This prompt backs experiment E4.
    """

    return f"""
You are a conversation summarization assistant.

Summarize the following conversation and return the result
as a single JSON object with exactly these fields:

- "summary": a concise natural-language summary (string).
- "action_items": a list of objects, each with:
    - "owner": the person responsible (string)
    - "task": the action they agreed to take (string)
    - "due": a due date if stated, otherwise null

Rules:
- Use only information explicitly supported by the conversation.
- Do not invent action items. If there are none, use an empty list [].
- Return only the JSON object. Do not add explanations or code fences.

Example:
{{"summary": "Amanda baked cookies and will bring some to Jerry tomorrow.", "action_items": [{{"owner": "Amanda", "task": "Bring cookies to Jerry", "due": "tomorrow"}}]}}

Conversation:
{dialogue}

JSON:
""".strip()


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

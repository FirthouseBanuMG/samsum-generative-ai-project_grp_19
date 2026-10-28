"""Heuristic checks for omitted explicit first-person commitments."""

import re


_COMMITMENT_PATTERN = re.compile(
    r"\b(?:I['’]ll|I will)\s+(?!not\b)(?P<verb>[a-z]+)\b",
    re.IGNORECASE,
)
_TENTATIVE_PATTERN = re.compile(
    r"\b(?:maybe|perhaps|might|could|would|should|think)\b",
    re.IGNORECASE,
)


def find_unrepresented_commitments(dialogue: str, output: dict) -> list[str]:
    """Flag clear first-person future commitments missing from action items.

    This deliberately narrow heuristic is a review aid, not a factuality
    validator. It recognizes direct "I'll"/"I will" statements only.
    """
    action_items = output.get("action_items", [])
    if not isinstance(action_items, list):
        return []

    flags = []
    for line in dialogue.splitlines():
        speaker, separator, utterance = line.partition(":")
        if not separator:
            continue

        match = _COMMITMENT_PATTERN.search(utterance)
        if not match:
            continue

        prefix = utterance[:match.start()]
        if _TENTATIVE_PATTERN.search(prefix):
            continue

        verb = match.group("verb").casefold()
        represented = any(
            isinstance(item, dict)
            and str(item.get("owner", "")).strip().casefold()
            == speaker.strip().casefold()
            and re.search(
                rf"\b{re.escape(verb)}\b",
                str(item.get("task", "")),
                re.IGNORECASE,
            )
            for item in action_items
        )
        if not represented:
            flags.append(
                f"{speaker.strip()} made an explicit first-person "
                f"commitment ({utterance.strip()!r}) with no matching "
                "owner/action verb in action_items."
            )

    return flags

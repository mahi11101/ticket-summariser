"""Turn a long support thread into a short CRM note.

Uses Claude through the Anthropic API when ANTHROPIC_API_KEY is set.
Without a key it falls back to a simple rule-based summary, so it always runs.

Usage: python summarise.py thread.txt
"""
import json
import os
import re
import sys
import urllib.request

PROMPT = """Summarise this support thread as a CRM note with exactly these lines:
Issue: <one sentence>
Customer impact: <one sentence>
Done so far: <one sentence>
Next step: <owner and action>
Sentiment: <positive / neutral / frustrated>

Thread:
"""


def with_llm(text, key):
    body = json.dumps({
        "model": os.environ.get("MODEL", "claude-haiku-5-5"),
        "max_tokens": 300,
        "messages": [{"role": "user", "content": PROMPT + text}],
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages", data=body,
        headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                 "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["content"][0]["text"].strip()


FRUSTRATED = re.compile(r"\b(still|again|urgent|unacceptable|frustrat\w*|escalat\w*|third time)\b", re.I)


def fallback(text):
    msgs = [m.strip() for m in re.split(r"\n(?=\w[\w .]*:)", text.strip()) if m.strip()]
    customer = [m for m in msgs if m.lower().startswith("customer")]
    agent = [m for m in msgs if not m.lower().startswith("customer")]
    first = lambda m: re.split(r"(?<=[.!?])\s", m.split(":", 1)[-1].strip())[0]
    longest = lambda m: max(re.split(r"(?<=[.!?])\s", m.split(":", 1)[-1].strip()), key=len)
    hits = len(FRUSTRATED.findall(" ".join(customer)))
    return "\n".join([
        f"Issue: {first(customer[0]) if customer else 'Unknown'}",
        f"Customer impact: {first(customer[-1]) if customer else 'Unknown'}",
        f"Done so far: {longest(agent[-1]) if agent else 'No reply yet'}",
        "Next step: Agent to confirm the fix with the customer",
        f"Sentiment: {'frustrated' if hits >= 2 else 'neutral'}",
        f"({len(msgs)} messages summarised)",
    ])


def summarise(text):
    key = os.environ.get("ANTHROPIC_API_KEY")
    return with_llm(text, key) if key else fallback(text)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "sample_thread.txt"
    with open(path) as f:
        print(summarise(f.read()))

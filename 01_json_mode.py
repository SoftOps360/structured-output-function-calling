"""Structured Output 1 — Reliable JSON. Force the model to return JSON your code can parse,
by turning on JSON mode AND describing the exact shape you want."""
import json
from _llm import client, MODEL

alert = "CRITICAL: db-01 disk at 96%, mysql refusing writes since 03:14 UTC."

resp = client.chat.completions.create(
    model=MODEL,
    response_format={"type": "json_object"},          # <-- forces valid JSON
    messages=[
        {"role": "system", "content": "You turn ops alerts into JSON. Return only JSON."},
        {"role": "user", "content":
            f"Alert: {alert}\n"
            'Return {"severity": "P1|P2|P3", "service": "", "problem": "", "action": ""}.'},
    ],
)

data = json.loads(resp.choices[0].message.content)   # a real Python dict now
print(data)
print("→ route as:", data["severity"], "| service:", data["service"])

"""Structured Output 2 — Validate with a schema. JSON mode gives you JSON;
Pydantic guarantees it's the RIGHT shape (typed & validated) before your code trusts it.
This is the production-grade way — never act on unvalidated model output."""
import json
from pydantic import BaseModel, ValidationError
from _llm import client, MODEL


class Incident(BaseModel):
    severity: str
    service: str
    problem: str
    action: str


alert = "CRITICAL: db-01 disk at 96%, mysql refusing writes since 03:14 UTC."

resp = client.chat.completions.create(
    model=MODEL,
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": "Return only JSON with the requested fields."},
        {"role": "user", "content":
            f"Alert: {alert}\n"
            'Return {"severity": "", "service": "", "problem": "", "action": ""}.'},
    ],
)

raw = resp.choices[0].message.content
try:
    incident = Incident.model_validate_json(raw)     # parse + validate in one step
    print(incident)
    print("✅ safe to use →", incident.service, "|", incident.action)
except ValidationError as e:
    print("⚠️ model returned bad data, don't trust it:\n", e)

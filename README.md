# AI for DevOps — Ep 4: Structured Output & Function Calling

Part of **SoftOps 360 · AI for DevOps (Hands-On)**.

So far the AI gives you **text**. To put AI into real automation, you need two things: output your code can **trust** (structured + validated), and a way for the model to **use your tools**. This episode delivers both — and the tool-calling loop here is the exact foundation of the **on-call agent** in the next series.

## What you run
| File | Concept | Ops example |
|---|---|---|
| `01_json_mode.py` | Reliable JSON | turn an alert into `{severity, service, problem, action}` |
| `02_schema_pydantic.py` | **Validate** with a schema | never act on unvalidated model output — Pydantic guarantees the shape |
| `03_function_calling.py` | Give the model **tools** | it decides to call `get_service_status(nginx)` |
| `04_tool_loop.py` | **Close the loop** (a tiny agent) | model asks → your code runs it → model answers |

## Setup (free)
1. Free Groq key: https://console.groq.com/keys
2. `pip install -r requirements.txt`  *(adds `pydantic`)*
3. Copy `.env.example` → `.env`, paste your key
4. `python 01_json_mode.py`  (then `02…`, `03…`, `04…`)

## The mental model of function calling
1. You **describe** tools (name · what they do · inputs) to the model.
2. The model returns a **structured tool call** — which function, what arguments.
3. **Your code** runs it (the model never touches your systems).
4. You feed the **result** back; the model gives a final, grounded answer.

That 4-step loop *is* an agent. Everything in the S3 on-call agent is this, repeated.

## The big lessons
- **Never trust raw model output in automation** — validate it (Pydantic) before acting.
- **The LLM decides, your code does** — the separation that keeps AI ops safe and controllable.
- Tool descriptions are just prompts — good descriptions = reliable tool use.

## Misconceptions cleared
- "The AI runs my commands." — No; it only *requests* a call; your code executes it.
- "JSON mode = valid data." — It guarantees valid JSON, not the *right* JSON. Validate the shape.

## Next → Ep 5: Choosing Your Model
Closed vs open, cost/speed/quality, and when to use which.

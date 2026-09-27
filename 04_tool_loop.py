"""Function Calling 2 — Close the loop (a tiny agent!):
   model asks for a tool  →  YOUR code runs it  →  feed the result back  →  model answers.
This exact loop is the heart of the on-call agent we build in the next series."""
import json
from _llm import client, MODEL


# --- your real ops functions (mocked here so it runs anywhere) ---
def get_service_status(service):
    return "inactive (dead)" if service == "myapp" else "active (running)"


TOOLS_IMPL = {"get_service_status": get_service_status}

tools = [{"type": "function", "function": {
    "name": "get_service_status",
    "description": "Check whether a systemd service is active.",
    "parameters": {"type": "object",
        "properties": {"service": {"type": "string"}}, "required": ["service"]}}}]

messages = [{"role": "user",
             "content": "The site is down. Is the myapp backend running? If not, tell me what to do."}]

# 1) the model decides to call a tool
resp = client.chat.completions.create(model=MODEL, messages=messages, tools=tools, tool_choice="auto")
msg = resp.choices[0].message
messages.append(msg)                        # keep the model's tool-call turn in history

# 2) run each requested tool, feed results back as role="tool"
for tc in (msg.tool_calls or []):
    args = json.loads(tc.function.arguments)
    result = TOOLS_IMPL[tc.function.name](**args)
    print(f"[ran {tc.function.name}({args}) -> {result}]")
    messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

# 3) the model gives its final, grounded answer
final = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
print("\nAI:", final.choices[0].message.content)

"""Function Calling 1 — Give the model TOOLS. You describe each tool (name + what it does +
its inputs). The model reads them and returns a STRUCTURED call: which function, what args.
The model never runs anything — YOUR code does. This is exactly how agents act."""
import json
from _llm import client, MODEL

# Describe the tools the model is allowed to use.
tools = [
    {"type": "function", "function": {
        "name": "get_service_status",
        "description": "Check whether a systemd service is active.",
        "parameters": {"type": "object",
            "properties": {"service": {"type": "string", "description": "e.g. nginx"}},
            "required": ["service"]}}},
    {"type": "function", "function": {
        "name": "get_disk_usage",
        "description": "Get disk usage percent for a host.",
        "parameters": {"type": "object",
            "properties": {"host": {"type": "string"}},
            "required": ["host"]}}},
]

resp = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "Is nginx running on the web box?"}],
    tools=tools,
    tool_choice="auto",     # let the model decide if/which tool to call
)

msg = resp.choices[0].message
if msg.tool_calls:
    for tc in msg.tool_calls:
        print("🔧 the model wants to call:", tc.function.name)
        print("   with arguments:", json.loads(tc.function.arguments))
else:
    print("no tool call; direct answer:", msg.content)

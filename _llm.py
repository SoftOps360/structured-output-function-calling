"""Shared client + helper. Exposes `client` and `MODEL` for the low-level calls
(JSON mode, tools) used in this episode, plus the simple ask() from before."""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1")
MODEL = "openai/gpt-oss-120b"   # if this errors, check console.groq.com/docs/models


def ask(prompt, system=None):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    return client.chat.completions.create(model=MODEL, messages=messages).choices[0].message.content

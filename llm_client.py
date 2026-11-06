#Author: Ben Prishtina
#Class: CAP 6938: AI Knowledge

import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:4b"

#Send a prompt to the locally hosted LLM.
#Returns:
#    str: The model's response.
def ask_llm(prompt, json_mode=False, json_schema=None, temperature=None):

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "think": False
    }

    if json_schema is not None:
        payload["format"] = json_schema
    elif json_mode:
        payload["format"] = "json"

    if temperature is not None:
        payload["options"] = {
            "temperature": temperature
        }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    content = response.json()["message"]["content"]

    if "</think>" in content:
        content = content.split("</think>", 1)[1].strip()

    return content


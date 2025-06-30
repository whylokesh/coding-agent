# agent/context.py

import os
import json
from datetime import datetime
from typing import List

LOG_DIR = "agent/logs"
os.makedirs(LOG_DIR, exist_ok=True)

def _get_log_path(session_id: str) -> str:
    return os.path.join(LOG_DIR, f"{session_id}.jsonl")

def save_message(session_id: str, message: dict):
    path = _get_log_path(session_id)
    with open(path, "a") as f:
        f.write(json.dumps(message) + "\n")

def load_history(session_id: str, max_messages: int = 30) -> List[dict]:
    path = _get_log_path(session_id)
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        lines = f.readlines()
    messages = [json.loads(line) for line in lines]
    return messages[-max_messages:]  # Keep recent ones only

def build_chat_history(session_id: str, user_prompt: str) -> List[dict]:
    history = load_history(session_id)
    history.append({
        "role": "user",
        "content": user_prompt,
        "timestamp": datetime.utcnow().isoformat()
    })
    return history

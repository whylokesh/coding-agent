import os
import json
from openai import OpenAI
from agent.tools import run_shell, write_file, read_file, execute_python
from agent.context import build_chat_history, save_message

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "run_shell",
            "description": "Runs a shell command inside the container.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string"}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Writes content to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_python",
            "description": "Executes a Python script.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string"}
                },
                "required": ["code"]
            }
        }
    }
]

SYSTEM_PROMPT = """
You are CodingAgent, a helpful developer agent that can write code, execute it, run shell commands, and manage files.
Use the tools provided to complete tasks inside a secure container.
"""

def run_coding_agent(user_prompt: str, model: str = "gpt-4o", session_id: str = "default") -> str:
    raw_history = build_chat_history(session_id, user_prompt)

    messages = []
    tool_call_lookup = {}

    for msg in raw_history:
        role = msg.get("role")

        if role == "tool":
            # Must match a previous assistant message with tool_calls
            if "tool_call_id" in msg and msg["tool_call_id"] in tool_call_lookup:
                messages.append({
                    "role": "tool",
                    "tool_call_id": msg["tool_call_id"],
                    "name": msg["name"],
                    "content": msg["content"]
                })
        elif role == "assistant" and "tool_calls" in msg:
            tool_calls = msg["tool_calls"]
            for call in tool_calls:
                tool_call_lookup[call["id"]] = True

            messages.append({
                "role": "assistant",
                "tool_calls": tool_calls
            })
        elif role in ["user", "assistant"] and "content" in msg:
            messages.append({
                "role": role,
                "content": msg["content"]
            })

    while True:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message
        msg_data = message.model_dump(exclude_unset=True)
        save_message(session_id, msg_data)

        # Append assistant response to message list
        if "tool_calls" in msg_data:
            messages.append({
                "role": "assistant",
                "tool_calls": msg_data["tool_calls"]
            })
        else:
            messages.append({
                "role": "assistant",
                "content": msg_data.get("content", "")
            })

        if hasattr(message, "tool_calls") and message.tool_calls:
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                if tool_name == "run_shell":
                    result = run_shell(**args)
                elif tool_name == "write_file":
                    result = write_file(**args)
                elif tool_name == "read_file":
                    result = read_file(**args)
                elif tool_name == "execute_python":
                    result = execute_python(**args)
                else:
                    result = f"[Unknown tool: {tool_name}]"

                tool_msg = {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": result
                }

                save_message(session_id, tool_msg)
                messages.append(tool_msg)

        elif message.content:
            return message.content

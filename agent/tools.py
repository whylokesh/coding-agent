# agent/tools.py
import subprocess
import os

def run_shell(command: str) -> str:
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return f"[Error running shell command]: {e}"

def write_file(path: str, content: str) -> str:
    try:
        with open(path, "w") as f:
            f.write(content)
        return f"[✅] Wrote to file: {path}"
    except Exception as e:
        return f"[❌] Failed to write to {path}: {e}"

def read_file(path: str) -> str:
    if os.path.exists(path):
        return open(path, "r").read()
    else:
        return f"[❌] File not found: {path}"

def execute_python(code: str) -> str:
    try:
        with open("temp_code.py", "w") as f:
            f.write(code)
        result = subprocess.run("python3 temp_code.py", shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return f"[❌] Python execution error: {e}"

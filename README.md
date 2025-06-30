Absolutely! Here's a clean, professional `README.md` for your **Coding Agent** project based on everything we've built so far — including FastAPI orchestration, OpenAI tool use, noVNC GUI access, and persistent sessions:

---

````markdown
# 🧠 Coding Agent

A containerized developer assistant that writes, executes, and updates code through OpenAI's function calling. It supports shell commands, file I/O, Python code execution, persistent memory via sessions, and a browser-accessible GUI terminal using noVNC.

## ✨ Features

- ✅ GPT-4o-based coding agent with OpenAI tool-calling
- ✅ FastAPI backend with job-based orchestration
- ✅ Session-based memory persistence (`.jsonl` logs)
- ✅ Execute shell commands, Python code, and manage files
- ✅ GUI terminal via noVNC + Fluxbox + x11vnc
- ✅ Dockerized environment with Node.js and Python
- ✅ File browsing & editing via integrated GUI

---

## 🚀 Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/whylokesh/coding-agent.git
cd coding-agent
````

### 2. Add your `.env`

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxx
```

### 3. Build and run with Docker Compose

```bash
docker-compose up --build
```

### 4. Access the app

| Component                | URL                                                              |
| ------------------------ | ---------------------------------------------------------------- |
| 🧠 API (FastAPI)         | [http://localhost:8000](http://localhost:8000)                   |
| 🖥️ GUI Terminal (noVNC) | [http://localhost:6080/vnc.html](http://localhost:6080/vnc.html) |
| 🔐 Password              | `password`                                                       |

---

## 📦 API Endpoints

### `POST /schedule`

Schedule a new coding task.

**Request:**

```json
{
  "prompt": "Create a simple Node.js server using Express."
}
```

**Response:**

```json
{
  "job_id": "1b3d8f26-b...",
  "session_id": "a4998816-..."
}
```

---

### `GET /status/{job_id}`

Fetch status and result of a scheduled task.

**Response:**

```json
{
  "status": "completed",
  "result": "Your Node.js server has been created..."
}
```

---

## 🧰 Tools Supported

| Tool             | Description                               |
| ---------------- | ----------------------------------------- |
| `run_shell`      | Executes shell commands                   |
| `write_file`     | Writes content to a file                  |
| `read_file`      | Reads contents of a file                  |
| `execute_python` | Runs a Python script inside the container |

---

## 🗂️ Project Structure

```
coding-agent/
├── api/
│   └── orchestrator.py   # FastAPI backend
├── agent/
│   ├── agent.py          # Core tool logic
│   ├── context.py        # Session handling (chat logs)
│   ├── tools.py          # Tool implementations
│   └── logs/             # Session `.jsonl` history
├── entrypoint.sh         # Starts GUI + FastAPI
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 💡 Future Ideas

* [ ] Add long-term memory (`context.py` with pruning)
* [ ] Add orchestration via k8s/Firecracker VMs
* [ ] Add more tools (`install_package`, `test_code`)
* [ ] Upload/download files via API

---

## 🛠️ Tech Stack

* **OpenAI GPT-4o** + Tool Calling
* **FastAPI** for orchestration
* **Docker** + `docker-compose`
* **noVNC**, **Fluxbox**, **x11vnc** for web-based GUI
* **Python 3.11**, **Node.js 18**

---

## 🧑‍💻 Author

Built by \[Lokesh Jha]. Inspired by the dream of giving AI real developer superpowers.

---

## 📜 License

MIT License — free to modify and use.

```

---

Let me know if you'd like a minimal version, screenshots, or badges (build passing, license, etc.) added.
```

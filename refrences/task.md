# Task

Build a basic coding agent with sandboxing and an orchestration layer. You can use any programming language, models, and tools (e.g. Cursor). Limit time spent to 1–2 hours. You'll be judged on architecture, scalability, security, reliability, and context management. No need to write tests unless absolutely necessary. Copy-paste Dockerfiles, setup scripts, etc. is fine.

### Tools to Provide

1. **Shell** – Execute shell commands. Think about security isolation. 
2. **Code Execution** – Run TypeScript, Python, etc. with context management. You can use Jupyter for this.
3. **xdot** – GUI control via xdot.
4. **Filesystem** – Create, edit, move files, etc.

### Container

Create a Docker image that sets up:

- Display server
- xdot
- Live VNC
- Jupyter notebook and development tools

You should be able to view the agent running inside the container via novnc link locally. 

### Context Management

Agent must work beyond 1M token limit. Design a way to persist and recall context intelligently using pruning, file-based state, or a novel approach. 

---

## Orchestration Layer

Build a simple orchestration server with 2 endpoints:

1. `POST /schedule`
    
    Accepts a plain-text task like “Build me a todo app in React”, returns a job ID. Spins up a Firecracker VM (with your agent container) in the background to complete the task.
    
2. `GET /status/:id`
    
    Returns the status. When the job is complete, it provides a download link to the generated project folder. 
    

Bonus: if you can write k8 or nomad job to scale this since this should be horizontally doable depending on how you create this.

---

### Notes

- You don’t need to support all cases. Focus on areas we care about. We are evaluating what you prioritize or ship since startups do not always have bandwidth to do everything.
- Share your solution via GitHub, ZIP, deployed endpoint, or any way you like.
- We will discuss the approach and extension in technical interview. No white-boarding, leetcode, etc.

---

### Submission

Send an Email to [founders@runable.com](mailto:founders@runable.com) and do CC [team@runable.com](mailto:team@runable.com)











Now we can go in two directions:

    🧠 Add context.py to enable memory beyond 1M tokens (via pruning, local file memory)

    ☁️ Orchestrate multiple agents using k8s / Firecracker VMs / Nomad (for scale)

    ⚒️ Add more smart tools: like install_package, test_code, etc.
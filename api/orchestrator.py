import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from agent.agent import run_coding_agent

app = FastAPI()
jobs = {}

class TaskRequest(BaseModel):
    prompt: str
    session_id: Optional[str] = None  # 👈 Optional field to reuse sessions

@app.post("/schedule")
def schedule_task(req: TaskRequest):
    job_id = str(uuid.uuid4())
    session_id = req.session_id or str(uuid.uuid4())  # 👈 Use provided session_id or generate new

    jobs[job_id] = {
        "status": "running",
        "result": None,
        "prompt": req.prompt,
        "session_id": session_id
    }

    try:
        result = run_coding_agent(req.prompt, session_id=session_id)
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = result
    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["result"] = str(e)

    return {"job_id": job_id, "session_id": session_id}

@app.get("/status/{job_id}")
def get_status(job_id: str):
    if job_id not in jobs:
        return {"error": "Job ID not found"}

    return {
        "status": jobs[job_id]["status"],
        "result": jobs[job_id]["result"],
        "session_id": jobs[job_id]["session_id"]
    }

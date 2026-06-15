import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
import asyncio
import json

app = FastAPI(title="OpenManus API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskRequest(BaseModel):
    prompt: str
    max_steps: int = 20


@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    html_path = Path(__file__).parent / "static" / "index.html"
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text())
    return HTMLResponse(content="<h1>OpenManus API is running</h1><p>UI not found.</p>")


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}


@app.post("/run")
async def run_task(request: TaskRequest):
    async def generate():
        try:
            from app.agent.manus import Manus
            agent = await Manus.create()
            yield json.dumps({"type": "status", "content": "Agent started..."}) + "\n"
            result = await agent.run(request.prompt)
            steps_taken = len(getattr(agent.memory, "messages", []))
            await agent.cleanup()
            yield json.dumps({"type": "result", "content": str(result), "steps": steps_taken}) + "\n"
        except Exception as e:
            yield json.dumps({"type": "error", "content": str(e)}) + "\n"

    return StreamingResponse(generate(), media_type="application/x-ndjson")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)

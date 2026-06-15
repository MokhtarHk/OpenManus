import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.agent.manus import Manus

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

class TaskResponse(BaseModel):
    result: str
    steps_taken: int

@app.get("/")
async def health():
    return {"status": "ok", "service": "OpenManus"}

@app.get("/health")
async def healthcheck():
    return {"status": "ok"}

@app.post("/run", response_model=TaskResponse)
async def run_task(request: TaskRequest):
    try:
        agent = await Manus.create()
        result = await agent.run(request.prompt)
        steps_taken = len(getattr(agent.memory, "messages", []))
        return TaskResponse(result=str(result), steps_taken=steps_taken)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)

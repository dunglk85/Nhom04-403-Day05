from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import json

from agent import run_agent
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

app = FastAPI(title="XanhSM Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store (key = session_id)
sessions: dict[str, list[BaseMessage]] = {}


class ChatRequest(BaseModel):
    session_id: str = "default"
    message: str


class ChatResponse(BaseModel):
    reply: str
    session_id: str


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    messages = sessions.get(req.session_id, [])
    reply, updated = run_agent(req.message, messages)
    sessions[req.session_id] = updated
    return ChatResponse(reply=reply, session_id=req.session_id)


@app.delete("/chat/{session_id}")
async def clear_session(session_id: str):
    sessions.pop(session_id, None)
    return {"status": "cleared"}


@app.get("/health")
async def health():
    return {"status": "ok"}

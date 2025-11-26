# Run: uvicorn api:app --host 127.0.0.1 --port 8000

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import uuid
import json
import time
from fastapi.middleware.cors import CORSMiddleware

from rag.rag_query_engine_safe import ask

app = FastAPI(title="Medical RAG API (fixed)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SESSIONS: Dict[str, List[Dict[str, Any]]] = {}

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    developer_mode: bool = False
    stream: bool = False

class NewSessionResponse(BaseModel):
    session_id: str

class ClearMemoryRequest(BaseModel):
    session_id: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/new_session", response_model=NewSessionResponse)
async def new_session():
    sid = "sess_" + uuid.uuid4().hex[:12]
    SESSIONS[sid] = []
    return {"session_id": sid}

@app.post("/clear_memory")
async def clear_memory(req: ClearMemoryRequest):
    sid = req.session_id
    if not sid or sid not in SESSIONS:
        return JSONResponse({"ok": False, "detail": "invalid session_id"}, status_code=400)
    SESSIONS[sid] = []
    return {"ok": True}

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    sid = req.session_id or ("sess_" + uuid.uuid4().hex[:12])
    if sid not in SESSIONS:
        SESSIONS[sid] = []

    if not req.message or not req.message.strip():
        return JSONResponse({"error": "message cannot be empty"}, status_code=422)

    SESSIONS[sid].append({"role": "user", "content": req.message})

    try:
        resp = ask(req.message)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

    answer = resp.get("answer") if isinstance(resp, dict) else str(resp)
    meta = resp.get("meta") if isinstance(resp, dict) else {}

    SESSIONS[sid].append({"role": "assistant", "content": answer, "meta": meta})

    if req.stream:
        def gen():
            text = answer or ""
            words = text.split()
            buf = []
            for i, w in enumerate(words, 1):
                buf.append(w)
                if i % 12 == 0:
                    yield json.dumps({"type": "partial", "text": " ".join(buf)}) + "\n"
                    buf = []
                    time.sleep(0.02)
            if buf:
                yield json.dumps({"type": "partial", "text": " ".join(buf)}) + "\n"
            yield json.dumps({"type": "meta", "meta": meta}) + "\n"
        return StreamingResponse(gen(), media_type="text/event-stream")

    return {"answer": answer, "meta": meta, "session_id": sid}

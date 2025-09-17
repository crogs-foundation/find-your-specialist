import os
from pathlib import Path

import uvicorn
from dotenv import dotenv_values
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from src.pipeline import ApiModel, LocalModel, RAGPipeline
from src.utils import load_json

CONFIG = dotenv_values(".env")
DEBUG = bool(os.environ.get("DEBUG"))
CONTEXT_PATH = Path("./prompts.json")
if not CONTEXT_PATH.exists():
    raise RuntimeError(f"Context '{CONTEXT_PATH}' does not exist")
RAG_PIPELINE = RAGPipeline(load_json(CONTEXT_PATH))


app = FastAPI()


# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (update for production)
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/specialists")
async def get_indexers_list():
    return RAG_PIPELINE.available_specialists


@app.get("/models")
async def get_llm_list():
    return RAG_PIPELINE.available_models


@app.get("/chat")
async def chat(prompt: str, model: ApiModel | LocalModel, specialist: str):
    try:
        return StreamingResponse(
            RAG_PIPELINE.request(prompt, model, specialist),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(CONFIG["BACKEND_PORT"] or 8000),
        reload=DEBUG,
        log_level="info" if DEBUG else "warning",
    )

import os
import time
import json
import uuid
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from typing import List, Dict, Any

from schemas import ChatCompletionRequest, ChatCompletionResponse, ChatCompletionResponseChoice, Message, ChatCompletionChunk, ChatCompletionChunkChoice, ChatCompletionChunkDelta
from inference import InferenceManager, get_model_path

# Load environment variables
load_dotenv()

MODEL_REPO = os.getenv("MODEL_ID", "litert-community/gemma-4-E2B-it-litert-lm")
MODEL_FILE = os.getenv("MODEL_FILE", "gemma-4-E2B-it.litertlm")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8080))

app = FastAPI(
    title="LiteBridge API",
    description="""
LiteBridge, Google'ın ultra hızlı **LiteRT** (TFLite) motorunu OpenAI uyumlu bir API üzerinden sunan hafif bir köprüdür.
Bu API sayesinde yerelde çalışan modelleri Cursor, Zed veya Aider gibi OpenAI API bekleyen tüm araçlarla kullanabilirsiniz.

### Temel Özellikler
*   **OpenAI Uyumluluğu:** `/v1/chat/completions` endpoint'i ile tam uyumlu.
*   **Streaming Desteği:** Tokens-by-token yanıt alma (SSE).
*   **Otomatik Model Yönetimi:** Eksik modelleri otomatik indirme.
*   **Hafif ve Hızlı:** Düşük kaynak tüketimi için optimize.
""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Global Inference Manager (Single model architecture)
manager = None

@app.on_event("startup")
async def startup_event():
    global manager
    model_path = get_model_path(model_repo=MODEL_REPO, model_file=MODEL_FILE)
    
    if not model_path:
        print(f"Model not found. Attempting to download '{MODEL_REPO}'...")
        from download_model import download_model
        success = download_model(MODEL_REPO)
        if success:
            model_path = get_model_path(model_repo=MODEL_REPO, model_file=MODEL_FILE)
        else:
            print(f"ERROR: Failed to download model '{MODEL_REPO}'.")
            return

    if model_path:
        print(f"Initializing LiteBridge with model: {model_path}")
        manager = InferenceManager(model_path)
        manager.load()
    else:
        print("ERROR: Inference Manager could not be initialized.")

@app.get("/v1/models", tags=["Models"], summary="Mevcut modelleri listele")
async def list_models():
    """LiteBridge üzerinde yüklü olan ve aktif edilebilen modelleri döner."""
    return {
        "object": "list",
        "data": [
            {
                "id": MODEL_REPO,
                "object": "model",
                "created": int(time.time()),
                "owned_by": "litert-community"
            }
        ]
    }

@app.post("/v1/chat/completions", tags=["Chat"], summary="Sohbet tamamlaması oluştur")
async def chat_completions(request: ChatCompletionRequest):
    """
    OpenAI uyumlu sohbet tamamlama endpoint'i. 
    Hem senkron hem de streaming (akış) modunda yanıt dönebilir.
    """
    if not manager:
        raise HTTPException(status_code=503, detail="Model not loaded. Check server logs.")

    request_id = f"chatcmpl-{uuid.uuid4()}"
    created_time = int(time.time())

    if request.stream:
        async def stream_generator():
            # Initial role chunk
            role_chunk = ChatCompletionChunk(
                id=request_id,
                created=created_time,
                model=request.model,
                choices=[ChatCompletionChunkChoice(
                    index=0,
                    delta=ChatCompletionChunkDelta(role="assistant"),
                    finish_reason=None
                )]
            )
            yield f"data: {role_chunk.model_dump_json(exclude_none=True)}\n\n"

            # Content chunks
            for chunk in manager.generate_stream(request.messages):
                for item in chunk.get("content", []):
                    if item.get("type") == "text":
                        content = item.get("text", "")
                        if content:
                            content_chunk = ChatCompletionChunk(
                                id=request_id,
                                created=created_time,
                                model=request.model,
                                choices=[ChatCompletionChunkChoice(
                                    index=0,
                                    delta=ChatCompletionChunkDelta(content=content),
                                    finish_reason=None
                                )]
                            )
                            yield f"data: {content_chunk.model_dump_json(exclude_none=True)}\n\n"

            # Final finish_reason chunk
            final_chunk = ChatCompletionChunk(
                id=request_id,
                created=created_time,
                model=request.model,
                choices=[ChatCompletionChunkChoice(
                    index=0,
                    delta=ChatCompletionChunkDelta(),
                    finish_reason="stop"
                )]
            )
            yield f"data: {final_chunk.model_dump_json(exclude_none=True)}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(stream_generator(), media_type="text/event-stream")
    else:
        answer = manager.generate(request.messages)
        return ChatCompletionResponse(
            id=request_id,
            created=created_time,
            model=request.model,
            choices=[ChatCompletionResponseChoice(
                index=0,
                message=Message(role="assistant", content=answer),
                finish_reason="stop"
            )],
            usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0} # Usage info could be added if supported
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)

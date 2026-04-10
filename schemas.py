from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict, Any

class Message(BaseModel):
    role: str = Field(..., description="Mesajı gönderen rol: 'system', 'user' veya 'assistant'.", example="user")
    content: str = Field(..., description="Mesajın metin içeriği.", example="Merhaba, nasılsın?")
    name: Optional[str] = Field(None, description="Mesajı gönderen için opsiyonel bir isim.")

class ChatCompletionRequest(BaseModel):
    model: str = Field(..., description="Kullanılacak modelin ID'si.", example="gemma-4-E2B-it")
    messages: List[Message] = Field(..., description="Sohbet geçmişini temsil eden mesaj listesi.")
    stream: Optional[bool] = Field(False, description="Yanıtın streaming (SSE) olarak dönüp dönmeyeceği.")
    temperature: Optional[float] = Field(1.0, description="Yaratıcılık seviyesi (0.0 - 2.0).", example=0.7)
    top_p: Optional[float] = Field(1.0, description="Nucleus sampling eşiği.")
    max_tokens: Optional[int] = Field(None, description="Üretilecek maksimum token sayısı.")
    stop: Optional[Union[str, List[str]]] = Field(None, description="Üretimi durduracak anahtar kelimeler.")

class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: Message
    finish_reason: Optional[str] = "stop"

class ChatCompletionResponse(BaseModel):
    id: str = Field(..., description="Yanıtın benzersiz ID'si.")
    object: str = "chat.completion"
    created: int = Field(..., description="Yanıtın oluşturulduğu zaman (Unix timestamp).")
    model: str = Field(..., description="Kullanılan modelin adı.")
    choices: List[ChatCompletionResponseChoice]
    usage: Optional[Dict[str, int]] = Field(None, description="Token kullanım bilgileri.")

class ChatCompletionChunkDelta(BaseModel):
    role: Optional[str] = None
    content: Optional[str] = None

class ChatCompletionChunkChoice(BaseModel):
    index: int
    delta: ChatCompletionChunkDelta
    finish_reason: Optional[str] = None

class ChatCompletionChunk(BaseModel):
    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: List[ChatCompletionChunkChoice]

from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict, Any

class ToolCallFunction(BaseModel):
    name: str
    arguments: str

class ToolCall(BaseModel):
    id: str
    type: str = "function"
    function: ToolCallFunction

class Message(BaseModel):
    role: str = Field(..., description="Mesajı gönderen rol: 'system', 'user', 'assistant' veya 'tool'.", example="user")
    content: Optional[str] = Field(None, description="Mesajın metin içeriği.", example="Merhaba, nasılsın?")
    name: Optional[str] = Field(None, description="Mesajı gönderen için opsiyonel bir isim.")
    tool_calls: Optional[List[ToolCall]] = Field(None, description="Modelin çağırmak istediği araçlar.")
    tool_call_id: Optional[str] = Field(None, description="Yanıtlanan aracın ID'si ('tool' rolü için).")

class ToolFunctionDefinition(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

class Tool(BaseModel):
    type: str = "function"
    function: ToolFunctionDefinition

class ChatCompletionRequest(BaseModel):
    model: str = Field(..., description="Kullanılacak modelin ID'si.", example="gemma-4-E2B-it")
    messages: List[Message] = Field(..., description="Sohbet geçmişini temsil eden mesaj listesi.")
    stream: Optional[bool] = Field(False, description="Yanıtın streaming (SSE) olarak dönüp dönmeyeceği.")
    temperature: Optional[float] = Field(1.0, description="Yaratıcılık seviyesi (0.0 - 2.0).", example=0.7)
    top_p: Optional[float] = Field(1.0, description="Nucleus sampling eşiği.")
    max_tokens: Optional[int] = Field(None, description="Üretilecek maksimum token sayısı.")
    stop: Optional[Union[str, List[str]]] = Field(None, description="Üretimi durduracak anahtar kelimeler.")
    tools: Optional[List[Tool]] = Field(None, description="Modelin çağırabileceği araçların listesi.")
    tool_choice: Optional[Union[str, Dict[str, Any]]] = Field(None, description="Hangi aracın çağrılacağını kontrol eder ('none', 'auto' veya spesifik fonksiyon).")

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

class ChunkToolCallFunction(BaseModel):
    name: Optional[str] = None
    arguments: Optional[str] = None

class ChunkToolCall(BaseModel):
    index: int
    id: Optional[str] = None
    type: Optional[str] = "function"
    function: ChunkToolCallFunction

class ChatCompletionChunkDelta(BaseModel):
    role: Optional[str] = None
    content: Optional[str] = None
    tool_calls: Optional[List[ChunkToolCall]] = None

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

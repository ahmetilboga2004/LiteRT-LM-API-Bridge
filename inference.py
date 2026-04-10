import litert_lm
from pathlib import Path
import os
import time
from typing import Generator, List, Dict, Any

class InferenceManager:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.engine = None
        
        # Log seviyesini ayarla
        litert_lm.set_min_log_severity(litert_lm.LogSeverity.ERROR)
        
    def load(self):
        if self.engine is None:
            print(f"Loading LiteRT-LM engine from: {self.model_path}")
            # .litertlm dosyasıysa direkt yolu ver, dizinse dizin yolunu ver
            self.engine = litert_lm.Engine(self.model_path)
        return self

    def __enter__(self):
        return self.load()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.engine:
            self.engine.__exit__(exc_type, exc_val, exc_tb)
            self.engine = None

    def create_conversation(self):
        if not self.engine:
            self.load()
        return self.engine.create_conversation()

    def generate_stream(self, messages: List[Dict[str, str]]) -> Generator[Dict[str, Any], None, None]:
        """
        OpenAI formatındaki mesaj listesini alır ve streaming yanıt döner.
        Stateless çalışmak için her seferinde yeni bir conversation açar ve geçmişi besler.
        """
        with self.create_conversation() as conversation:
            # Geçmiş mesajları besle (son mesaj hariç)
            for msg in messages[:-1]:
                content = msg.content if hasattr(msg, "content") else msg.get("content", "")
                role = msg.role if hasattr(msg, "role") else msg.get("role", "user")
                # LiteRT-LM şu an ağırlıklı olarak user prompt'u bekliyor.
                # Sistem mesajı veya asistan mesajları için uygun formatlama gerekebilir.
                # Şimdilik direkt gönderiyoruz.
                for _ in conversation.send_message_async(content):
                    pass # Yanıtı tüket ama kullanma
            
            # Son mesajı gönder ve yanıtı stream et
            last_message = messages[-1].content if messages else ""
            for chunk in conversation.send_message_async(last_message):
                yield chunk

    def generate(self, messages: List[Dict[str, str]]) -> str:
        """Non-streaming yanıt döner."""
        full_text = ""
        for chunk in self.generate_stream(messages):
            for item in chunk.get("content", []):
                if item.get("type") == "text":
                    full_text += item.get("text", "")
        return full_text

def get_model_path(models_dir: str = "models", model_repo: str = None, model_file: str = None):
    """
    Belirtilen veya varsayılan model yolunu döner.
    """
    if not model_repo:
        from download_model import DEFAULT_MODEL
        model_repo = DEFAULT_MODEL
        
    folder_name = model_repo.replace("/", "--")
    model_dir = Path(models_dir) / folder_name
    
    if model_file:
        full_path = model_dir / model_file
        if full_path.exists():
            return str(full_path)
    
    # Dosya belirtilmemişse veya yoksa dizinde ara
    if model_dir.exists():
        files = list(model_dir.glob("*.litertlm")) or list(model_dir.glob("*.tflite"))
        if files:
            return str(files[0])
            
    return None
import litert_lm
from pathlib import Path
import sys

MODELS_BASE_DIR = Path("models")

def list_models():
    if not MODELS_BASE_DIR.exists():
        print("No 'models' directory found. Please run download_model.py first.")
        return None

    models = []
    for subdir in MODELS_BASE_DIR.iterdir():
        if subdir.is_dir():
            litertlm_files = list(subdir.glob("*.litertlm"))
            tflite_files = list(subdir.glob("*.tflite"))
            model_files = litertlm_files or tflite_files
            if model_files:
                primary_file = model_files[0]
                models.append((subdir.name, primary_file, subdir))

    if not models:
        print("No models found. Please run download_model.py first.")
        return None

    print("\n=== Available models ===")
    for i, (name, path, _) in enumerate(models, 1):
        size_gb = path.stat().st_size / (1024 ** 3)
        print(f"[{i}] {name} ({path.name}) - {size_gb:.2f} GB")
    return models

def initialize_engine():
    available = list_models()
    if not available:
        sys.exit(1)

    while True:
        try:
            choice = input("\nEnter number of the model you want to use (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                sys.exit(0)
            idx = int(choice) - 1
            if 0 <= idx < len(available):
                model_name, model_path, model_dir = available[idx]
                break
            else:
                print("Invalid number!")
        except ValueError:
            print("Invalid input. Please enter a number or 'q'.")

    litert_lm.set_min_log_severity(litert_lm.LogSeverity.ERROR)

    engine_path = str(model_path) if model_path.suffix == ".litertlm" else str(model_dir)
    print(f"LiteRT-LM engine initialized with: {model_name} ({engine_path})")
    return litert_lm.Engine(engine_path)

def main_demo():
    """Basic terminal demo with correct streaming"""
    with initialize_engine() as engine:
        with engine.create_conversation() as conversation:
            print("Type 'exit' or 'q' to quit.\n")
            
            while True:
                user_input = input("👤 You: ")
                if user_input.lower() in ["exit", "q", "çık"]:
                    break
                
                print("🤖 AI: ", end="", flush=True)
                
                # DOĞRU STREAMING KODU (resmi LiteRT-LM API)
                for chunk in conversation.send_message_async(user_input):
                    for item in chunk.get("content", []):
                        if item.get("type") == "text":
                            print(item.get("text", ""), end="", flush=True)
                
                print("\n")  # Cevap bittiğinde yeni satır

if __name__ == "__main__":
    main_demo()
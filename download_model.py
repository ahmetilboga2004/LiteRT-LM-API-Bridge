import sys
from pathlib import Path
from huggingface_hub import snapshot_download, hf_hub_download
import huggingface_hub
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
if HF_TOKEN:
    huggingface_hub.login(token=HF_TOKEN)

DEFAULT_MODEL = "litert-community/SmolLM-135M-Instruct"
MODELS_BASE_DIR = Path("models")

def repo_to_folder_name(repo_id: str) -> str:
    return repo_id.replace("/", "--")

def check_model_exists(model_dir: Path) -> tuple[bool, list[Path]]:
    """Hem .litertlm hem de .tflite dosyalarını kontrol eder"""
    litertlm_files = list(model_dir.glob("*.litertlm"))
    tflite_files = list(model_dir.glob("*.tflite"))
    all_model_files = litertlm_files + tflite_files
    return bool(all_model_files), all_model_files

def print_existing_models():
    models = [d for d in MODELS_BASE_DIR.iterdir() if d.is_dir()] if MODELS_BASE_DIR.exists() else []
    if not models:
        print("No models installed yet.")
        return
    print("Installed models:")
    for i, model_dir in enumerate(models, 1):
        has_model, files = check_model_exists(model_dir)
        if has_model:
            size_gb = sum(f.stat().st_size for f in files) / (1024 ** 3)
            print(f"[{i}]  {model_dir.name} ({size_gb:.2f} GB)")
        else:
            print(f"[{i}]  {model_dir.name} (No model file found)")

def download_model(repo_id: str) -> bool:
    folder_name = repo_to_folder_name(repo_id)
    model_dir = MODELS_BASE_DIR / folder_name
    model_dir.mkdir(parents=True, exist_ok=True)

    has_model, _ = check_model_exists(model_dir)
    if has_model:
        print(f"Model '{repo_id}' already exists at '{model_dir}'.")
        return True

    print(f"\nDownloading model -> '{repo_id}'")
    print(f"Saving to: {model_dir}")
    try:
        snapshot_download(
            repo_id=repo_id, 
            local_dir=str(model_dir),
            allow_patterns=["*.litertlm", "*.tflite", "*.json"]
        )
    except Exception as e:
        print(f"Error downloading model: {e}")
        return False

    has_model, files = check_model_exists(model_dir)
    if not has_model:
        print(f"Download completed but no .litertlm or .tflite file found in '{model_dir}'.")
        return False

    size_gb = sum(f.stat().st_size for f in files) / (1024 ** 3)
    print(f"Model '{repo_id}' downloaded successfully!")
    print(f"Total size: {size_gb:.2f} GB")
    return True

def main():
    print("=" * 55)
    print("Welcome To The LiteRT-LM Model Downloader!")
    print("=" * 55)
    print_existing_models()
    print("\nEnter the Hugging Face repository ID")
    print(f"Default (press Enter): {DEFAULT_MODEL}\n")

    try:
        user_input = input("Enter model repo ID (or press Enter for default): ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nInput cancelled.")
        sys.exit(0)

    repo_id = user_input if user_input else DEFAULT_MODEL
    success = download_model(repo_id)

    if success:
        folder_name = repo_to_folder_name(repo_id)
        print(f"\nModel ready in: models/{folder_name}")
        print(f"Run: python inference.py")
    else:
        sys.exit(1)

if __name__ == "__main__":
    MODELS_BASE_DIR.mkdir(parents=True, exist_ok=True)
    main()
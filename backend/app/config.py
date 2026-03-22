import os
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Eigen AI
    eigen_api_key: str = ""
    eigen_api_base_url: str = "https://api-web.eigenai.com/api/v1"
    eigen_asr_model: str = "higgs_asr_3"
    eigen_chat_model: str = "higgs2p5"
    eigen_summarizer_model: str = "gpt-oss-120b"
    eigen_understanding_model: str = "higgs_audio_understanding_3p5"

    # Storage
    chroma_persist_dir: str = "./data/chroma_db"
    upload_dir: str = "./data/uploads"
    database_url: str = "sqlite:///./data/drdejavu.db"

    # App
    app_env: str = "development"
    secret_key: str = "change-me"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()

# Ensure directories exist
Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
Path(settings.chroma_persist_dir).mkdir(parents=True, exist_ok=True)

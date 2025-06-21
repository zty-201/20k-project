"""Configuration loader for Gemini.

Reads GEMINI_API_KEY or GOOGLE_API_KEY from environment (.env supported).
"""
from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True, slots=True)
class Settings:
    gemini_api_key: str | None = (
        os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    )

settings = Settings()

if settings.gemini_api_key:
    os.environ.setdefault("GOOGLE_API_KEY", settings.gemini_api_key)

if not settings.gemini_api_key:
    raise RuntimeError(
        "GEMINI_API_KEY (or GOOGLE_API_KEY) not found. "
        "Create a .env file (see .env.example) or export the variable."
    )

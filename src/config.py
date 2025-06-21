"""Configuration loader.

Reads environment variables (optionally from a .env file)
and provides typed access throughout the code‑base.
"""
from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True, slots=True)
class Settings:
    openai_api_key: str = os.environ.get("OPENAI_API_KEY", "")
    openai_api_base: str | None = os.environ.get("OPENAI_API_BASE")

settings = Settings()

if not settings.openai_api_key:
    raise RuntimeError(
        "OPENAI_API_KEY not found. "
        "Create a .env file (see .env.example) or export the variable."
    )

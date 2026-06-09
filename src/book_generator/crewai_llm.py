import os
from typing import List, Optional


def crew_model_name(provider: str, model: Optional[str] = None) -> str:
    if provider == "gemini":
        model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
        return model if model.startswith("gemini/") else f"gemini/{model}"
    if provider == "openai":
        model = model or os.getenv("OPENAI_MODEL", "gpt-4o")
        return model if model.startswith("openai/") else f"openai/{model}"
    raise RuntimeError(f"Unsupported LLM_PROVIDER for CrewAI: {provider}")


def provider_models(provider: str) -> List[Optional[str]]:
    if provider == "gemini":
        primary = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
        fallbacks = os.getenv("GEMINI_FALLBACK_MODELS", "gemini-2.0-flash,gemini-1.5-flash")
        values = [primary] + fallbacks.split(",")
        seen = set()
        return [m for m in (v.strip() for v in values) if m and not (m in seen or seen.add(m))]
    return [None]


def build_llm(provider: str, model: Optional[str] = None):
    try:
        from crewai import LLM
    except ImportError as exc:
        raise RuntimeError(
            "CrewAI is not installed. Activate .venv-crewai or run .\\scripts\\setup_env.ps1."
        ) from exc
    api_key = os.getenv("GEMINI_API_KEY") if provider == "gemini" else os.getenv("OPENAI_API_KEY")
    if not api_key:
        key = "GEMINI_API_KEY" if provider == "gemini" else "OPENAI_API_KEY"
        raise RuntimeError(f"Missing {key} for online CrewAI generation.")
    return LLM(
        model=crew_model_name(provider, model),
        api_key=api_key,
        temperature=float(os.getenv("CREWAI_TEMPERATURE", "0.35")),
        max_tokens=int(os.getenv("CREWAI_MAX_TOKENS", "8192")),
    )
import os
import json
import time
import urllib.error
import urllib.request
from collections.abc import Callable

from openai import OpenAI


def _response_text(response) -> str:
    if getattr(response, "output_text", None):
        return response.output_text
    chunks = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            text = getattr(content, "text", None)
            if text:
                chunks.append(text)
    return "\n".join(chunks)


def _retry(label: str, call: Callable[[], str], attempts: int = 3) -> str:
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            return call()
        except Exception as exc:  # API SDK exceptions differ by provider.
            last_error = exc
            print(f"{label} attempt {attempt}/{attempts} failed: {exc}")
            if attempt < attempts:
                time.sleep(2 * attempt)
    raise RuntimeError(f"{label} failed after {attempts} attempts: {last_error}")


def _unique_models(primary: str, fallbacks: str) -> list[str]:
    seen = set()
    models = []
    for model in [primary, *fallbacks.split(",")]:
        model = model.strip()
        if model and model not in seen:
            seen.add(model)
            models.append(model)
    return models


def generate_openai(prompt: str) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Missing OPENAI_API_KEY.")
    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", "gpt-5.2")

    def call() -> str:
        response = client.responses.create(model=model, input=prompt)
        return _response_text(response)

    return _retry(f"OpenAI model {model}", call)


def generate_gemini(prompt: str) -> str:
    if not os.getenv("GEMINI_API_KEY"):
        raise RuntimeError("Missing GEMINI_API_KEY.")
    models = _unique_models(
        os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        os.getenv("GEMINI_FALLBACK_MODELS", "gemini-2.0-flash"),
    )
    mode = os.getenv("GEMINI_API_MODE", "native").lower()
    last_error = None
    for model in models:
        try:
            if mode == "openai":
                return _retry(f"Gemini model {model}", lambda: _gemini_openai_call(model, prompt))
            return _retry(f"Gemini model {model}", lambda: _gemini_native_call(model, prompt))
        except Exception as exc:
            last_error = exc
            print(f"Trying next Gemini model after failure: {exc}")
    raise RuntimeError(f"All Gemini models failed: {last_error}")


def _gemini_openai_call(model: str, prompt: str) -> str:
    client = OpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You write valid LaTeX article content only."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""


def _gemini_native_call(model: str, prompt: str) -> str:
    key = os.environ["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.4},
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gemini HTTP {exc.code}: {body}") from exc
    parts = result.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    return "\n".join(part.get("text", "") for part in parts).strip()


def generate_article(provider: str, prompt: str) -> str:
    if provider == "openai":
        return generate_openai(prompt)
    if provider == "gemini":
        return generate_gemini(prompt)
    raise RuntimeError(f"Unsupported LLM_PROVIDER: {provider}")

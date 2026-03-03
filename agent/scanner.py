import json
import re
import time
import httpx
from dotenv import load_dotenv
from .config import load_settings
from .prompts import SYSTEM_PROMPT, USER_TEMPLATE
from .schemas import ScanResult

MAX_RETRIES = 5
INITIAL_BACKOFF = 5  # seconds

def _extract_json(text: str) -> str:
    """Strip markdown code fences if present, e.g. ```json ... ```"""
    m = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()

def scan(content: str, *, language: str="python", input_type: str="file", path_hint: str="unknown") -> dict:
    load_dotenv()
    s = load_settings()

    payload = {
        "model": s.model,
        "temperature": s.temperature,
        "max_tokens": s.max_tokens,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_TEMPLATE.format(
                language=language, input_type=input_type, path_hint=path_hint, content=content
            )},
        ],
    }

    print(f"[scanner] Using: {s.base_url} | Model: {s.model}")

    headers = {"Authorization": f"Bearer {s.api_key}"}
    with httpx.Client(base_url=s.base_url, headers=headers, timeout=60.0) as client:
        for attempt in range(MAX_RETRIES):
            r = client.post("/chat/completions", json=payload)
            if r.status_code == 429:
                wait = INITIAL_BACKOFF * (2 ** attempt)
                retry_after = r.headers.get("retry-after")
                if retry_after:
                    wait = max(wait, float(retry_after))
                print(f"[scanner] Rate limited (429). Retrying in {wait:.1f}s (attempt {attempt+1}/{MAX_RETRIES})...")
                time.sleep(wait)
                continue
            r.raise_for_status()
            data = r.json()
            break
        else:
            raise RuntimeError(f"API rate limit exceeded after {MAX_RETRIES} retries.")

    text = data["choices"][0]["message"]["content"]
    text = _extract_json(text)
    obj = json.loads(text)
    ScanResult.model_validate(obj)
    return obj
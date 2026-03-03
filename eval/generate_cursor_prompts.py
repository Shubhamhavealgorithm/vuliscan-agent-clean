import json
from pathlib import Path

CASES_PATH = Path("eval/datasets/cases.jsonl")
OUT_DIR = Path("eval/cursor_prompts")

PROMPT_TEMPLATE = """You are a security vulnerability scanner for Python code.

Return ONLY valid JSON that matches this schema:
{{
  "summary": "string",
  "overall_risk_score": 0-100,
  "findings": [
    {{
      "id": "string",
      "severity": "critical|high|medium|low|info",
      "category": "injection|auth|secrets|crypto|rce|ssrf|path_traversal|deserialization|deps|config|logging|dos|supply_chain|other",
      "file": "string",
      "line": "string",
      "title": "string",
      "evidence": "string",
      "impact": "string",
      "recommendation": "string"
    }}
  ]
}}

Context:
- language: {language}
- input_type: {input_type}
- path_hint: {path_hint}
- case_id: {case_id}

---INPUT START---
{content}
---INPUT END---

Return JSON only.
"""

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    count = 0
    for line in CASES_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)

        case_id = obj["case_id"]
        language = obj.get("language", "python")
        input_type = obj.get("input_type", "snippet")
        path_hint = obj.get("path_hint", "unknown")
        content = obj["content"]

        prompt = PROMPT_TEMPLATE.format(
            case_id=case_id,
            language=language,
            input_type=input_type,
            path_hint=path_hint,
            content=content,
        )

        (OUT_DIR / f"{case_id}.txt").write_text(prompt, encoding="utf-8")
        count += 1

    print(f"Wrote {count} prompt files to {OUT_DIR}")

if __name__ == "__main__":
    main()
# VULISCAN agent

**Agent name:** VULISCAN agent  
**Creator:** ShubhamD  
**Specialization:** Python code risk analyser + vulnerability finder  
**Cursor-ready:** Yes (`.cursorrules` included)

## What problem this agent solves
VULISCAN agent scans Python code/snippets/diffs and returns structured JSON findings for:
- SQL injection / unsafe query building
- Command injection / RCE patterns
- Path traversal
- Insecure deserialization (pickle)
- Hardcoded secrets

## Security requirements
- No secrets are committed.
- Copy `.env.example` → `.env` locally and fill API_KEY.
- Never commit `.env`.

## Install
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

## Usage
```bash
python scripts/scan_path.py --path path/to/file.py --language python
python scripts/scan_diff.py --diff path/to/change.diff --language python
```

## Performance metric (1–10,000)
Score formula:
- base = 2000
- quality = 6500 * F1 (match by finding.id)
- severity = 1000 * severity_accuracy
- penalty = 1500 * false_positive_ratio
Final: clamp(1..10000)

Run:
```bash
python eval/run_eval.py
```

## Benchmark vs default Cursor Claude
Use `eval/baseline_cursor_claude.md` to paste Claude outputs and compare side-by-side using the same scoring.

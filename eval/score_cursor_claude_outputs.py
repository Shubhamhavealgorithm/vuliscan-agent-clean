import json
from pathlib import Path

from agent.scoring import Case, ExpectedFinding, score_case

CASES_PATH = Path("eval/datasets/cases.jsonl")
OUT_DIR = Path("eval/cursor_claude_outputs")  # you save JSON files here

def load_cases():
    for line in CASES_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        expected = [ExpectedFinding(**e) for e in obj["expected"]]
        yield obj["case_id"], Case(case_id=obj["case_id"], expected=expected)

def main():
    scores = []
    missing = 0

    for case_id, case in load_cases():
        out_path = OUT_DIR / f"{case_id}.json"
        if not out_path.exists():
            missing += 1
            print(f"[MISSING] {case_id} -> {out_path}")
            continue

        output = json.loads(out_path.read_text(encoding="utf-8"))
        sc, details = score_case(output, case)
        scores.append(sc)
        print(case_id, sc, details)

    print("Cases scored:", len(scores))
    print("Missing outputs:", missing)

    if scores:
        print("Average score (1-10000):", sum(scores) / len(scores))
    else:
        raise SystemExit("No outputs found. Save Cursor Claude JSON to eval/cursor_claude_outputs/<case_id>.json")

if __name__ == "__main__":
    main()
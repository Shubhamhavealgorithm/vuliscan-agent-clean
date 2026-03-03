import json
from pathlib import Path
from agent.scanner import scan
from agent.scoring import Case, ExpectedFinding, score_case

def load_cases(path: str):
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        expected = [ExpectedFinding(**e) for e in obj["expected"]]
        yield obj, Case(case_id=obj["case_id"], expected=expected)

def main():
    cases_path = "eval/datasets/cases.jsonl"
    scores = []
    for raw, case in load_cases(cases_path):
        out = scan(raw["content"], language=raw.get("language","python"),
                   input_type=raw.get("input_type","snippet"), path_hint=raw.get("path_hint","unknown"))
        sc, details = score_case(out, case)
        scores.append(sc)
        print(case.case_id, sc, details)
    print("Cases:", len(scores))
    print("Average score (1-10000):", sum(scores)/len(scores))

if __name__ == "__main__":
    main()

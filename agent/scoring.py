from dataclasses import dataclass
from typing import Dict, List, Tuple, Set

@dataclass(frozen=True)
class ExpectedFinding:
    id: str
    severity: str
    category: str

@dataclass(frozen=True)
class Case:
    case_id: str
    expected: List[ExpectedFinding]

def _f1(tp: int, fp: int, fn: int) -> float:
    denom = (2 * tp + fp + fn)
    return (2 * tp / denom) if denom else 1.0

def score_case(output: Dict, case: Case) -> Tuple[int, Dict]:
    if not isinstance(output, dict) or "findings" not in output:
        return 1, {"reason": "missing_findings"}

    expected_ids: Set[str] = {e.id for e in case.expected}
    out_findings = output.get("findings", [])
    out_ids = [f.get("id", "") for f in out_findings if isinstance(f, dict)]
    out_id_set = set([x for x in out_ids if x])

    tp = len(out_id_set & expected_ids)
    fp = len(out_id_set - expected_ids)
    fn = len(expected_ids - out_id_set)

    f1 = _f1(tp, fp, fn)

    sev_acc = 0.0
    expected_map = {e.id: e for e in case.expected}
    matched = list(out_id_set & expected_ids)
    if matched:
        correct = 0
        for fid in matched:
            exp = expected_map[fid]
            out = next((f for f in out_findings if isinstance(f, dict) and f.get("id") == fid), None)
            if out and out.get("severity") == exp.severity:
                correct += 1
        sev_acc = correct / len(matched)

    fp_ratio = min(1.0, fp / (len(expected_ids) + 1))

    score = 2000 + int(6500 * f1) + int(1000 * sev_acc) - int(1500 * fp_ratio)
    score = max(1, min(10000, score))
    return score, {"tp": tp, "fp": fp, "fn": fn, "f1": f1, "sev_acc": sev_acc, "fp_ratio": fp_ratio, "score": score}

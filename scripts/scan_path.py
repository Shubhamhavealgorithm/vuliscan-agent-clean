import argparse
from pathlib import Path
from rich import print as rprint
from agent.scanner import scan

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    ap.add_argument("--language", default="python")
    args = ap.parse_args()

    p = Path(args.path)
    content = p.read_text(encoding="utf-8", errors="ignore")
    rprint(scan(content, language=args.language, input_type="file", path_hint=str(p)))

if __name__ == "__main__":
    main()

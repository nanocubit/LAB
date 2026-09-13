from __future__ import annotations
import argparse, json
from pathlib import Path
from .canonical import canonical_json_bytes, digest_json

def main() -> None:
    parser=argparse.ArgumentParser(prog="lab")
    sub=parser.add_subparsers(dest="cmd", required=True)
    for name in ("canonicalize", "digest"):
        p=sub.add_parser(name); p.add_argument("path")
    args=parser.parse_args()
    value=json.loads(Path(args.path).read_text(encoding="utf-8"))
    if args.cmd=="canonicalize": print(canonical_json_bytes(value).decode("utf-8"))
    else: print(digest_json(value))

if __name__ == "__main__": main()

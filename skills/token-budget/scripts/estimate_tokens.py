#!/usr/bin/env python3
"""Estimate token counts for files or stdin and warn against a budget.

Usage:
  python3 estimate_tokens.py FILE [FILE ...] [--budget N]
  cat prompt.txt | python3 estimate_tokens.py [--budget N]
"""
import argparse
import sys


def estimate(text):
    # shortcut: chars/4 heuristic is within ~20% for English and code; use the API token-counting endpoint for exact counts.
    return max(1, round(len(text) / 4)) if text else 0


def level(tokens, budget):
    if tokens > budget:
        return "OVER BUDGET"
    if tokens > budget * 0.8:
        return "near budget"
    return "ok"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("files", nargs="*", help="files to measure (default: stdin)")
    p.add_argument("--budget", type=int, default=10_000, help="token budget to compare against (default 10000)")
    args = p.parse_args(argv)

    sources = []
    if args.files:
        for path in args.files:
            try:
                with open(path, encoding="utf-8", errors="replace") as f:
                    sources.append((path, f.read()))
            except OSError as e:
                print(f"skip {path}: {e.strerror}", file=sys.stderr)
    else:
        sources.append(("stdin", sys.stdin.read()))

    total = 0
    for name, text in sources:
        t = estimate(text)
        total += t
        print(f"{t:>10,}  {name}")
    print(f"{total:>10,}  TOTAL (~est.) vs budget {args.budget:,}: {level(total, args.budget)}")
    return 1 if total > args.budget else 0


if __name__ == "__main__":
    sys.exit(main())

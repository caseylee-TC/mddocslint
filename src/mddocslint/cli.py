"""Command-line interface: mddocslint PATH [PATH ...]."""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from mddocslint import __version__
from mddocslint.core import Problem, lint
from mddocslint.rules import RULES

EXIT_CLEAN = 0
EXIT_PROBLEMS = 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mddocslint",
        description="Lint Markdown docs for front matter problems, heading-level jumps, "
        "and broken internal links.",
    )
    parser.add_argument("paths", nargs="+", type=Path, metavar="PATH",
                        help="Markdown files or folders to lint")
    parser.add_argument("--select", metavar="RULES",
                        help=f"comma-separated rules to run (default: all of {', '.join(RULES)})")
    parser.add_argument("--ignore", metavar="RULES", help="comma-separated rules to skip")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="output format (default: text)")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def parse_rule_list(parser: argparse.ArgumentParser, value: str) -> list[str]:
    names = [name.strip() for name in value.split(",") if name.strip()]
    unknown = [name for name in names if name not in RULES]
    if unknown:
        parser.error(f"unknown rule(s): {', '.join(unknown)} (available: {', '.join(RULES)})")
    return names


def select_rules(parser: argparse.ArgumentParser, args: argparse.Namespace) -> list[str]:
    selected = parse_rule_list(parser, args.select) if args.select is not None else list(RULES)
    ignored = parse_rule_list(parser, args.ignore) if args.ignore is not None else []
    rules = [name for name in selected if name not in ignored]
    if not rules:
        parser.error("no rules left to run")
    return rules


def report(problems: list[Problem], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps([{**asdict(p), "path": p.path.as_posix()} for p in problems], indent=2))
        return
    for p in problems:
        print(f"{p.path.as_posix()}:{p.line}:{p.column}: {p.rule}[{p.kind}] {p.message}")
    if problems:
        files = len({p.path for p in problems})
        print(f"{len(problems)} problem(s) in {files} file(s)", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    """Run the linter. Usage errors exit 2 via argparse; otherwise return 0 (clean) or 1."""
    parser = build_parser()
    args = parser.parse_args(argv)
    rules = select_rules(parser, args)
    missing = [str(path) for path in args.paths if not path.exists()]
    if missing:
        parser.error(f"path not found: {', '.join(missing)}")
    problems, file_count = lint(args.paths, {name: RULES[name] for name in rules})
    if file_count == 0:
        parser.error("no Markdown files found")
    report(problems, args.format)
    return EXIT_PROBLEMS if problems else EXIT_CLEAN

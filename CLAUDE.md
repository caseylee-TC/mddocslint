# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

mddocslint is a Python CLI that lints Markdown doc folders for three problems:
- missing front matter 
- skipped heading levels
- broken links 

This repo is MIT licensed.

## Stack

- Python 3.12
- Virtualenv at `.venv/` (not tracked)
- `argparse` for the CLI (no CLI framework)
- `pytest` for tests

## Commands

- Install (editable, with pytest): `pip install -e ".[dev]"`
- Run tests: `pytest`
- Run one test: `pytest tests/test_front_matter.py::test_missing`
- Run the linter: `mddocslint ./sample-docs`

## Rules

- `front-matter`
- `heading-jumps`
- `broken-links`

## Exit codes

- `0`: clean
- `1`: problems found
- `2`: usage error

## Layout

- `src/mddocslint/`: `cli.py` (argparse), `core.py` (Problem, Document, runner), `markdown.py` (shared parsing helpers)
- `src/mddocslint/rules/`: one module per rule, each exposing `RULE` and `check(doc, ctx)`, registered in `rules/__init__.py`
- `tests/`: test files
- `tests/fixtures/<rule>/<kind>/`: bad docs, one subfolder per problem kind (named after the kind), plus `valid/`
- `sample-docs/`: a clean demo set

## Conventions

- Use type hints
- Keep functions small
- No new dependencies without asking
- One rule per module
- `notes/` is gitignored and holds personal working notes; don't commit it
- `main` is the default branch; feature work happens on `feat/*` branches

## Environment (Windows)

- Activate the venv with `.venv\Scripts\Activate.ps1` (PowerShell) or `source .venv/Scripts/activate` (Git Bash)
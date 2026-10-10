import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from mddocslint.cli import main

ROOT = Path(__file__).parent.parent
SAMPLE_DOCS = str(ROOT / "sample-docs")
FRONT_MATTER = ROOT / "tests" / "fixtures" / "front-matter"
MISSING = FRONT_MATTER / "missing"
LINE_RE = re.compile(r"^.+:\d+:\d+: [a-z-]+\[[a-z-]+\] .+$")


def usage_error(argv: list[str]) -> int:
    with pytest.raises(SystemExit) as exc:
        main(argv)
    return exc.value.code


def test_clean_folder_exits_0_silently(capsys) -> None:
    assert main([SAMPLE_DOCS]) == 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_problems_exit_1_with_one_line_each(capsys) -> None:
    assert main([str(MISSING)]) == 1
    captured = capsys.readouterr()
    lines = captured.out.splitlines()
    assert len(lines) == 4
    assert all(LINE_RE.match(line) for line in lines)
    assert all("front-matter[missing]" in line for line in lines)
    assert "4 problem(s) in 4 file(s)" in captured.err


def test_single_file_argument() -> None:
    assert main([str(FRONT_MATTER / "valid" / "has-front-matter.md")]) == 0
    assert main([str(MISSING / "no-front-matter.md")]) == 1


def test_select_rule(capsys) -> None:
    assert main([str(MISSING), "--select", "front-matter"]) == 1


def test_json_format(capsys) -> None:
    assert main([str(MISSING), "--format", "json"]) == 1
    problems = json.loads(capsys.readouterr().out)
    assert len(problems) == 4
    assert set(problems[0]) == {"path", "line", "column", "rule", "kind", "message"}


def test_json_format_when_clean(capsys) -> None:
    assert main([SAMPLE_DOCS, "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out) == []


@pytest.mark.parametrize(
    "argv",
    [
        [],
        ["does-not-exist"],
        [SAMPLE_DOCS, "--select", "no-such-rule"],
        [SAMPLE_DOCS, "--ignore", "front-matter,heading-jumps"],
        [SAMPLE_DOCS, "--format", "xml"],
    ],
)
def test_usage_errors_exit_2(argv: list[str]) -> None:
    assert usage_error(argv) == 2


def test_folder_without_markdown_exits_2(tmp_path: Path) -> None:
    assert usage_error([str(tmp_path)]) == 2


def test_python_dash_m_entry_point() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "mddocslint", SAMPLE_DOCS], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr

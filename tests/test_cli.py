"""The command-line layer: exit codes (the CI gate), --rules, --quiet, and argument handling.

Rule behavior is covered by the per-rule tests; these tests check what a user or CI
sees when running `mddocslint PATH`.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from mddocslint.cli import main
from mddocslint.rules import RULES

ROOT = Path(__file__).parent.parent
SAMPLE_DOCS = ROOT / "sample-docs"
FIXTURES = ROOT / "tests" / "fixtures"
MISSING_FRONT_MATTER = FIXTURES / "front-matter" / "missing"
LINE_RE = re.compile(r"^.+:\d+:\d+: (?P<rule>[a-z-]+)\[[a-z-]+\] .+$")
SUMMARY_RE = re.compile(r"^\d+ problem\(s\) in \d+ file\(s\)$")


def run(capsys, *argv: str | Path) -> tuple[int, str, str]:
    """Call main() like the console script does; return (exit code, stdout, stderr)."""
    try:
        code = main([str(arg) for arg in argv])
    except SystemExit as exc:  # argparse usage errors and --version
        code = exc.code
    out, err = capsys.readouterr()
    return code, out, err


def reported_rules(out: str) -> set[str]:
    return {LINE_RE.match(line)["rule"] for line in out.splitlines()}


@pytest.fixture
def every_problem(tmp_path: Path) -> Path:
    """A doc with one problem per rule: no front matter, H1 -> H3, and a broken link."""
    path = tmp_path / "doc.md"
    path.write_text("# Title\n\n### Too deep\n\n[gone](nowhere.md)\n", encoding="utf-8")
    return path


# --- Exit codes: the CI gate -------------------------------------------------


def test_clean_docs_exit_0_with_no_output(capsys) -> None:
    assert run(capsys, SAMPLE_DOCS) == (0, "", "")


@pytest.mark.parametrize(
    "folder",
    [
        FIXTURES / "front-matter" / "missing",
        FIXTURES / "heading-jumps" / "skipped-level",
        FIXTURES / "broken-links" / "missing-file",
        FIXTURES / "broken-links" / "missing-anchor",
    ],
    ids=lambda path: path.relative_to(FIXTURES).as_posix(),
)
def test_problems_exit_1(capsys, folder: Path) -> None:
    code, out, err = run(capsys, folder)
    assert code == 1
    assert out
    assert SUMMARY_RE.match(err.strip())


def test_nonexistent_path_exits_2(capsys) -> None:
    code, _, err = run(capsys, ROOT / "does-not-exist")
    assert code == 2
    assert "path not found" in err


@pytest.mark.parametrize(
    ("target", "expected"),
    [
        (SAMPLE_DOCS, 0),
        (MISSING_FRONT_MATTER, 1),
        (ROOT / "does-not-exist", 2),
    ],
    ids=["clean", "problems", "usage-error"],
)
def test_real_process_exit_codes(target: Path, expected: int) -> None:
    """The exit code CI sees from a real process, not just main()'s return value."""
    result = subprocess.run(
        [sys.executable, "-m", "mddocslint", str(target)], capture_output=True, text=True
    )
    assert result.returncode == expected, result.stderr
    assert "Traceback" not in result.stderr


# --- --rules -----------------------------------------------------------------


def test_all_rules_run_by_default(capsys, every_problem: Path) -> None:
    code, out, _ = run(capsys, every_problem)
    assert code == 1
    assert reported_rules(out) == set(RULES)


@pytest.mark.parametrize(
    ("rules", "expected"),
    [
        ("front-matter", {"front-matter"}),
        ("heading-jumps", {"heading-jumps"}),
        ("broken-links", {"broken-links"}),
        ("front-matter,broken-links", {"front-matter", "broken-links"}),
        (" heading-jumps , broken-links ", {"heading-jumps", "broken-links"}),
    ],
)
def test_rules_runs_only_the_selected_rules(
    capsys, every_problem: Path, rules: str, expected: set[str]
) -> None:
    code, out, _ = run(capsys, every_problem, "--rules", rules)
    assert code == 1
    assert reported_rules(out) == expected


def test_rules_excluding_the_failing_rule_exits_0(capsys) -> None:
    assert run(capsys, MISSING_FRONT_MATTER, "--rules", "heading-jumps") == (0, "", "")


def test_rules_including_the_failing_rule_exits_1(capsys) -> None:
    code, out, _ = run(capsys, MISSING_FRONT_MATTER, "--rules", "front-matter")
    assert code == 1
    assert reported_rules(out) == {"front-matter"}


def test_rules_combines_with_ignore(capsys, every_problem: Path) -> None:
    code, out, _ = run(
        capsys, every_problem, "--rules", "front-matter,heading-jumps", "--ignore", "front-matter"
    )
    assert code == 1
    assert reported_rules(out) == {"heading-jumps"}


# --- --quiet -----------------------------------------------------------------


@pytest.mark.parametrize("flag", ["--quiet", "-q"])
def test_quiet_hides_problem_lines_but_keeps_summary_and_exit_code(
    capsys, flag: str
) -> None:
    loud_code, loud_out, loud_err = run(capsys, MISSING_FRONT_MATTER)
    quiet_code, quiet_out, quiet_err = run(capsys, MISSING_FRONT_MATTER, flag)
    assert loud_out  # the normal run does print problem lines
    assert quiet_out == ""
    assert quiet_err == loud_err
    assert SUMMARY_RE.match(quiet_err.strip())
    assert quiet_code == loud_code == 1


def test_quiet_on_clean_docs_exits_0_silently(capsys) -> None:
    assert run(capsys, SAMPLE_DOCS, "--quiet") == (0, "", "")


def test_quiet_combines_with_rules(capsys) -> None:
    assert run(capsys, MISSING_FRONT_MATTER, "--quiet", "--rules", "heading-jumps") == (0, "", "")


def test_quiet_suppresses_json_problems_too(capsys) -> None:
    loud_code, loud_out, loud_err = run(capsys, MISSING_FRONT_MATTER, "--format", "json")
    quiet_code, quiet_out, quiet_err = run(capsys, MISSING_FRONT_MATTER, "-q", "--format", "json")
    assert json.loads(loud_out)
    assert quiet_out == ""
    assert quiet_err == loud_err
    assert quiet_code == loud_code == 1


# --- Output format -----------------------------------------------------------


def test_text_output_is_one_line_per_problem(capsys) -> None:
    code, out, err = run(capsys, MISSING_FRONT_MATTER)
    lines = out.splitlines()
    assert code == 1
    assert len(lines) == 4
    assert all(LINE_RE.match(line) for line in lines)
    assert err.strip() == "4 problem(s) in 4 file(s)"


def test_json_output(capsys) -> None:
    code, out, _ = run(capsys, MISSING_FRONT_MATTER, "--format", "json")
    problems = json.loads(out)
    assert code == 1
    assert len(problems) == 4
    assert set(problems[0]) == {"path", "line", "column", "rule", "kind", "message"}


def test_json_output_when_clean(capsys) -> None:
    code, out, _ = run(capsys, SAMPLE_DOCS, "--format", "json")
    assert (code, json.loads(out)) == (0, [])


def test_single_file_argument(capsys) -> None:
    assert run(capsys, FIXTURES / "front-matter" / "valid" / "has-front-matter.md")[0] == 0
    assert run(capsys, MISSING_FRONT_MATTER / "no-front-matter.md")[0] == 1


# --- Argument handling: usage errors, never tracebacks -------------------------


@pytest.mark.parametrize(
    ("argv", "message"),
    [
        ([], "required: PATH"),
        (["does-not-exist"], "path not found"),
        ([SAMPLE_DOCS, "--rules", "no-such-rule"], "unknown rule(s): no-such-rule"),
        ([SAMPLE_DOCS, "--rules", "front-matter,typo"], "unknown rule(s): typo"),
        ([SAMPLE_DOCS, "--ignore", "no-such-rule"], "unknown rule(s): no-such-rule"),
        ([SAMPLE_DOCS, "--rules", ""], "no rules left to run"),
        ([SAMPLE_DOCS, "--ignore", ",".join(RULES)], "no rules left to run"),
        ([SAMPLE_DOCS, "--format", "xml"], "invalid choice: 'xml'"),
        ([SAMPLE_DOCS, "--no-such-flag"], "unrecognized arguments: --no-such-flag"),
        ([SAMPLE_DOCS, "--rules"], "expected one argument"),
    ],
)
def test_usage_errors_exit_2_with_a_message(capsys, argv: list, message: str) -> None:
    code, out, err = run(capsys, *argv)
    assert code == 2
    assert out == ""
    assert err.startswith("usage: mddocslint")
    assert message in err


def test_folder_without_markdown_is_a_usage_error(capsys, tmp_path: Path) -> None:
    code, _, err = run(capsys, tmp_path)
    assert code == 2
    assert "no Markdown files found" in err


def test_unknown_rule_lists_the_available_rules(capsys) -> None:
    _, _, err = run(capsys, SAMPLE_DOCS, "--rules", "nope")
    assert all(rule in err for rule in RULES)


def test_invalid_rule_in_a_real_process_has_no_traceback() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "mddocslint", str(SAMPLE_DOCS), "--rules", "nope"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "Traceback" not in result.stderr
    assert "unknown rule(s): nope" in result.stderr

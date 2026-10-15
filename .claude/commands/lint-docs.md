---
description: Run mddocslint on a docs folder, group the findings by rule, and suggest a fix for each
argument-hint: "[path] (default: sample-docs)"
allowed-tools: Bash(.venv/Scripts/mddocslint:*), Bash(mddocslint:*), Read, Glob, Grep
---

Lint Markdown docs with mddocslint and suggest fixes. Don't edit any files; only report.

## 1. Run the linter

Path to lint: `$ARGUMENTS`. If that's empty, use `sample-docs`.

Run:

```
.venv/Scripts/mddocslint --format json <path>
```

If `.venv/Scripts/mddocslint` doesn't exist, run `mddocslint --format json <path>` instead.

Check the exit code:

- `0`: no problems. Say the docs are clean and stop.
- `1`: problems found. Continue to step 2.
- `2`: usage error, such as a path that doesn't exist or has no `.md` files. Show the error message and stop.

The output is a JSON list. Each item has `path`, `line`, `column`, `rule`, `kind` and `message`.

## 2. Group the findings by rule

Make one section per rule that has findings, in this order: `front-matter`, `heading-jumps`, `broken-links`. Leave out rules with no findings. Start each section with the rule name and its number of findings.

Under each rule, list every finding as `path:line` with its kind and message, followed by a suggested fix.

## 3. Suggest a fix for each finding

Read the file at the reported line before suggesting a fix, so the suggestion is specific and not generic. Show the corrected Markdown when it's short.

| Rule | Kind | How to fix it |
| ---- | ---- | ------------- |
| `front-matter` | `missing` | Add a `---` block as the first line of the file, with at least a `title:` taken from the file's first heading or file name. |
| `front-matter` | `unclosed` | Add a closing `---` on its own line, with no indentation, at the end of the metadata. |
| `front-matter` | `empty` | Add at least one key, such as `title:`, or remove the empty block. |
| `front-matter` | `invalid-yaml` | Fix the YAML at the reported line using the message: quote values that contain `: `, close quotes and brackets, indent with spaces not tabs, add missing colons, and remove duplicate keys. |
| `heading-jumps` | `skipped-level` | Change the heading to one level below the previous heading, or add the missing heading level in between. Name the level you'd use. |
| `broken-links` | `missing-file` | Find the file the link was meant to point to (use Glob to search for similar names) and give the corrected relative path. If nothing matches, say so and suggest removing the link or creating the file. |
| `broken-links` | `missing-anchor` | Read the target file's headings and suggest the anchor that matches. Anchors are lowercase, with spaces turned into `-` and punctuation removed. A repeated heading gets `-1`, `-2` and so on added to its anchor. |

If a finding has a kind that isn't in this table, base the fix on its message.

## 4. Summarize

End with one line giving the total number of findings and files, and which rule has the most findings.

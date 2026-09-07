---
name: commit-message
description: Write a commit message for the staged (or current) changes in this repo's house style — short imperative subject, optional body explaining what and why. Use when the user asks to commit, or to draft or improve a commit message.
---

# Commit message

Draft commit messages that match this repository's existing history.

## Workflow

1. Inspect what is being committed:
   - `git status` to see staged vs. unstaged.
   - `git diff --staged` (or `git diff` if nothing is staged yet) to read the actual change.
   - `git log --pretty=format:'%s' -20` to re-check the current subject-line style before writing.
2. If nothing is staged, tell the user and ask whether to `git add -A` or stage specific files. Do not stage on your own.
3. Write the message following the rules below.
4. Show the user the proposed message. Only run `git commit` after they approve, or if they already asked you to commit in this turn.

## House style

Subject line:
- Imperative mood, as a command: "Add", "Fix", "Revert", "Change", "Update", "Remove".
- Capitalize the first word. No trailing period.
- No `type(scope):` prefix — this repo does not use Conventional Commits.
- Aim for ~50 characters, hard limit ~72. One line.
- Describe the change, not the file: "Add document tool", not "Update server.py".

Body (optional):
- Omit it for small, self-explanatory changes — most commits here have subject only.
- Add a body when the change is non-trivial, non-obvious, or needs justification.
- Separate from the subject with one blank line. Wrap at ~72 characters.
- Explain *what* changed and *why*, not how. Mention notable side effects
  (new tool registered, migration required, behavior change).
- Use present tense, same imperative voice as the subject.

Reference real examples from `git log` when in doubt:
- `Add document tool` — trivial, subject only.
- `Revert "Add document_path_to_markdown tool"` — revert format.
- `Add document_path_to_markdown tool` — has a 4-line body describing what the
  tool does, what it validates, and that it registers on the MCP server.

## Attribution

Follow the repo's configured commit trailers (Co-Authored-By, Claude-Session).
Do not add them unless the session's attribution guidance says to.

## Don't

- Don't invent scope or intent the diff doesn't show. If the "why" isn't clear
  from the change or the conversation, ask or leave the body out.
- Don't bundle unrelated changes into one message — flag it and suggest splitting.
- Don't commit without approval.

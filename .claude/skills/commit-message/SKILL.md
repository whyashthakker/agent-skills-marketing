---
name: commit-message
description: Generates conventional commit messages by analysing staged git
  changes. Use when the user asks to commit, write a commit message, or
  mentions git commits.
disable-model-invocation: true
allowed-tools: Read, Grep, Bash(git *)
argument-hint: optional scope or additional context
---

# Commit Message Generator

Analyse the current staged changes and generate a conventional commit message.

## Workflow
1. Run `git diff --cached --stat` to see which files changed
2. Run `git diff --cached` to see the actual diff content
3. Determine commit type: feat, fix, refactor, docs, test, chore, style, perf
4. Write subject line in imperative mood, max 72 characters
5. Add body paragraph explaining WHY the change was made

## Output Format
Output the commit message as plain text, ready to paste into git commit -m.
Never wrap in a code block.

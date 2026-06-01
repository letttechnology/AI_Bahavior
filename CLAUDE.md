# AI Memory

This repo stores AI session memory across projects. Read on every session start.

## Structure

- `memory/` — Project-specific memory files mirrored from each project's `memory/` directory
- `chat/` — Chat session .md exports (last session only, for continuity)

## On session start

For a project at `D:\workspace-vscode\{project}`:
1. Read `D:\workspace-vscode\{project}\CLAUDE.md` for project instructions
2. Read `D:\workspace-vscode\{project}\memory\preferences.md` for behavioral rules
3. Read `D:\workspace-vscode\{project}\memory\session-state.md` for what was done last
4. Read `memory/{project}/session-state.md` as fallback
5. Read `chat/last-chat.md` if exists for detailed prior context

## On session end

For the current project:
1. Copy `memory/` from project to `memory/{project}/`
2. Copy latest chat .md to `chat/last-chat.md`
3. Commit + push

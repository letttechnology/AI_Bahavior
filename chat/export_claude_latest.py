"""
export_claude_latest.py — Export the latest Claude Code session to markdown.

Claude Code stores conversations as JSONL files in:
  C:/Users/<user>/.claude/projects/<project-hash>/

Each session is a UUID-named .jsonl file. This script finds the most recently
modified one and exports user/assistant messages to a dated markdown file.
"""

import json
import os
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(os.environ['USERPROFILE']) / '.claude' / 'projects' / 'd--workspace-vscode'
AI_MEMORY_CHAT = Path('D:/workspace-vscode/AI_Memory/chat')


def find_latest_session():
    jsonl_files = [f for f in PROJECT_DIR.glob('*.jsonl') if f.stat().st_size > 1000]
    if not jsonl_files:
        raise FileNotFoundError(f'No session JSONL files found in {PROJECT_DIR}')
    return max(jsonl_files, key=lambda f: f.stat().st_mtime)


def extract_text(content):
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get('type') == 'text':
                parts.append(block.get('text', '').strip())
        return '\n'.join(p for p in parts if p)
    return ''


def export_session(jsonl_path):
    messages = []
    with open(jsonl_path, encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            if obj.get('type') not in ('user', 'assistant'):
                continue
            if obj.get('isSidechain'):
                continue

            msg = obj.get('message', {})
            role = msg.get('role', obj.get('type'))
            text = extract_text(msg.get('content', ''))
            if text:
                messages.append((role, text))

    return messages


def write_markdown(messages, session_id, out_path):
    lines = [
        f'# Claude Code Session Export',
        f'',
        f'**Session:** `{session_id}`  ',
        f'**Exported:** {datetime.now().strftime("%Y-%m-%d %H:%M")}  ',
        f'**Messages:** {len(messages)}',
        f'',
        '---',
        '',
    ]

    for role, text in messages:
        header = '## 🧑 User' if role == 'user' else '## 🤖 Assistant'
        lines.append(header)
        lines.append('')
        lines.append(text)
        lines.append('')
        lines.append('---')
        lines.append('')

    out_path.write_text('\n'.join(lines), encoding='utf-8')


def main():
    latest = find_latest_session()
    session_id = latest.stem
    print(f'Session: {session_id}')
    print(f'File: {latest}')

    messages = export_session(latest)
    print(f'Messages extracted: {len(messages)}')

    ts = datetime.now().strftime('%Y-%m-%d_%H%M')
    out_path = AI_MEMORY_CHAT / f'claude_ses_{session_id[:16]}_{ts}.md'
    AI_MEMORY_CHAT.mkdir(parents=True, exist_ok=True)
    write_markdown(messages, session_id, out_path)

    print(f'Exported: {out_path}')


if __name__ == '__main__':
    main()

"""
Export Claude Code sessions from .jsonl files to readable markdown.
Reads all sessions in C:\Users\<user>\.claude\projects\D--workspace-vscode\
and exports each one not already exported to AI_Memory\chat\.
"""
import json, os, glob
from datetime import datetime, timezone

SESSIONS_DIR = os.path.join(os.environ['USERPROFILE'], '.claude', 'projects', 'D--workspace-vscode')
OUT_DIR      = r'D:/workspace-vscode/AI_Memory/chat'

os.makedirs(OUT_DIR, exist_ok=True)

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

            msg_type = obj.get('type')
            if msg_type not in ('user', 'assistant'):
                continue

            ts_raw = obj.get('timestamp', '')
            try:
                ts = datetime.fromisoformat(ts_raw.replace('Z', '+00:00')).astimezone().strftime('%H:%M:%S')
            except Exception:
                ts = ''

            message = obj.get('message', {})
            role    = message.get('role', msg_type)
            content = message.get('content', '')

            # content can be a string or a list of blocks
            if isinstance(content, list):
                parts = []
                for block in content:
                    if isinstance(block, dict):
                        if block.get('type') == 'text':
                            parts.append(block.get('text', ''))
                        elif block.get('type') == 'tool_use':
                            parts.append(f"[tool: {block.get('name', '?')}]")
                        elif block.get('type') == 'tool_result':
                            pass  # skip tool results for readability
                    elif isinstance(block, str):
                        parts.append(block)
                content = '\n'.join(p for p in parts if p.strip())

            if not content or not content.strip():
                continue

            messages.append((role, ts, content.strip()))

    return messages

# Find all session .jsonl files
session_files = sorted(
    glob.glob(os.path.join(SESSIONS_DIR, '*.jsonl')),
    key=os.path.getmtime
)

exported = 0
for jsonl_path in session_files:
    mtime    = os.path.getmtime(jsonl_path)
    dt       = datetime.fromtimestamp(mtime)
    date_str = dt.strftime('%Y-%m-%d_%H%M')
    sid      = os.path.splitext(os.path.basename(jsonl_path))[0][:8]
    out_name = f'claude_{date_str}_{sid}.md'
    out_path = os.path.join(OUT_DIR, out_name)

    if os.path.exists(out_path):
        continue  # already exported

    messages = export_session(jsonl_path)
    if not messages:
        continue

    lines = [f'# Claude Code Session — {dt.strftime("%Y-%m-%d %H:%M")}', '']
    for role, ts, content in messages:
        lines.append(f'## [{role}] ({ts})')
        lines.append('')
        lines.append(content)
        lines.append('')

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f'Exported {len(messages)} messages → {out_name}')
    exported += 1

if exported == 0:
    print('All sessions already exported.')
else:
    print(f'\nDone. {exported} session(s) exported to {OUT_DIR}')

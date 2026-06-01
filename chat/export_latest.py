import sqlite3, os, json
from datetime import datetime

db_path = os.path.join(os.environ['USERPROFILE'], '.local/share/opencode/opencode.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute('SELECT id FROM session ORDER BY time_created DESC LIMIT 1')
row = cur.fetchone()
if not row:
    print('No sessions found')
    exit()
sid = row[0]

cur.execute('''
    SELECT p.data, m.data, p.time_created
    FROM part p
    JOIN message m ON m.id = p.message_id
    WHERE p.session_id = ?
    ORDER BY p.time_created
''', (sid,))
parts = cur.fetchall()
conn.close()

lines = []
for p in parts:
    pdata = json.loads(p[0]) if p[0] else {}
    mdata = json.loads(p[1]) if p[1] else {}
    role = mdata.get('role', 'system')
    text = pdata.get('text', '') or ''
    ts = datetime.fromtimestamp(p[2]/1000).strftime('%H:%M:%S') if p[2] else ''
    if text.strip():
        lines.append(f'## [{role}] ({ts})')
        lines.append('')
        lines.append(text)
        lines.append('')

out = os.path.join(os.environ['USERPROFILE'], '.local/share/opencode/chat', 'chat_latest.md')
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

from shutil import copy2
ai = 'D:\\workspace-vscode\\AI_Memory\\chat'
os.makedirs(ai, exist_ok=True)
ts_file = datetime.now().strftime('%Y-%m-%d_%H%M')
copy2(out, os.path.join(ai, f'chat-{ts_file}.md'))

print(f'Exported {len(lines)//3} messages from {sid[:20]}...')
print(f'Saved: {os.path.join(ai, f"chat-{ts_file}.md")}')

import sqlite3, os, json, sys
from datetime import datetime

db_path = os.path.join(os.environ['USERPROFILE'], '.local/share/opencode/opencode.db')
out_dir = os.path.join(os.environ['USERPROFILE'], '.local/share/opencode/chat')
os.makedirs(out_dir, exist_ok=True)
ai_dir = 'D:\\workspace-vscode\\AI_Memory\\chat'
os.makedirs(ai_dir, exist_ok=True)

def list_sessions():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT id, time_created, directory FROM session ORDER BY time_created DESC')
    for s in cur.fetchall():
        ts = datetime.fromtimestamp(s[1]/1000).strftime('%Y-%m-%d %H:%M') if s[1] else '?'
        d = s[2] or '(none)'
        print(f'{s[0][:24]}  {ts}  {d[:60]}')
    conn.close()

def find_session(sid_prefix):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT id FROM session WHERE id LIKE ?', (sid_prefix + '%',))
    rows = cur.fetchall()
    conn.close()
    if len(rows) == 0:
        print(f'No session matches prefix "{sid_prefix}"')
        return None
    if len(rows) > 1:
        print(f'Multiple sessions match prefix "{sid_prefix}":')
        for r in rows:
            print(f'  {r[0][:24]}')
        return None
    return rows[0][0]

def export_session(sid):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    full_id = find_session(sid)
    if not full_id:
        return
    cur.execute('''
        SELECT p.data, m.data, p.time_created
        FROM part p
        JOIN message m ON m.id = p.message_id
        WHERE p.session_id = ?
        ORDER BY p.time_created
    ''', (full_id,))
    parts = cur.fetchall()
    conn.close()
    if not parts:
        print(f'No messages found for session {full_id[:20]}...')
        return
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
    short_id = sid[:18].replace(' ', '_')
    ts = datetime.now().strftime('%Y-%m-%d_%H%M')
    fname = f'chat_{short_id}_{ts}.md'
    out = os.path.join(out_dir, fname)
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    from shutil import copy2
    copy2(out, os.path.join(ai_dir, fname))
    print(f'Exported {len(lines)//3} messages from {sid[:20]}...')
    print(f'Saved: {os.path.join(ai_dir, fname)}')

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args or args[0] == 'list':
        list_sessions()
    elif args[0] == 'recall':
        if len(args) < 2:
            print('Usage: recall.py recall <session_id_prefix>')
            print('Or:    recall.py list')
        else:
            export_session(args[1])
    else:
        export_session(args[0])

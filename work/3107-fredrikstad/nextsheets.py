"""Lag kontaktark av nedlastede, ikke gjennomgåtte detaljfliser. Registrerer arkinnhold i reviewed.json (markeres som sett etter visning)."""
import json, os, sys, subprocess
from pathlib import Path
P = Path(__file__).parent
s = json.loads((P / 'detail-esri.json').read_text())
rev = json.loads((P / 'reviewed.json').read_text()) if (P / 'reviewed.json').exists() else {}
todo = [x for x in s if x['id'] not in rev and (P / 'images' / f"{x['id']}.jpg").exists()]
lim = int(sys.argv[1]) if len(sys.argv) > 1 else 30
todo = sorted(todo, key=lambda x: (x['bbox'][0] // 3000, -x['bbox'][1]))[:lim]
tag = sys.argv[2]
(P / f'sheet-{tag}.json').write_text(json.dumps(todo))
subprocess.run([sys.executable, str(P / 'contact.py'), f'sheet-{tag}.json', tag, '6', '500'], check=True)
for x in todo: rev[x['id']] = f'qa/{tag}'
(P / 'reviewed.json').write_text(json.dumps(rev, indent=0))
print(len(todo), 'fliser;', len(rev), 'av', len(s), 'registrert')

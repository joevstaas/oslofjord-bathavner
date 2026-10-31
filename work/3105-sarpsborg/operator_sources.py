import requests,json,datetime,hashlib,re,concurrent.futures
from pathlib import Path
P=Path(__file__).parent
U={'skjeberg':'https://www.skjebergmarinesenter.no/','skjeberg-1250':'https://www.sarpsborg.com/aktuelt/stor-interesse-for-marinaen','olseng':'https://olsengmarina.no/','sarpsborg-bf':'https://www.havneweb.no/sarpsborg-bf/','seilforening':'https://www.sarpsborg-seilforening.no/brygger/','grimsoy':'https://seilbaatservice.no/batplass'}
def fetch(kv):
 key,url=kv;r=requests.get(url,timeout=25);r.raise_for_status();f=P/'raw'/f'{key}.html';f.write_bytes(r.content);f.with_suffix('.provenance.json').write_text(json.dumps(dict(url=url,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(r.content).hexdigest()),indent=1));text=re.sub(r'<(script|style)\b.*?</\1>','',r.text,flags=re.S|re.I);text=re.sub('<[^>]+>',' ',text);text=re.sub(r'\s+',' ',text);(P/'raw'/f'{key}.txt').write_text(text);return key,len(r.content)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for r in ex.map(fetch,U.items()):print(r,flush=True)

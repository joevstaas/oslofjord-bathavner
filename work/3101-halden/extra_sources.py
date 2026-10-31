import requests, json, hashlib,datetime,concurrent.futures
from pathlib import Path
P=Path(__file__).parent
urls={'sponvika-vel.html':'https://sponvikavel.no/om/','sponvika-velhuset.html':'https://sponvikavel.no/velhuset/','sponvika-2022.pdf':'https://sponvikavel.no/wp-content/uploads/2022/01/Medlemsinfobrev-2022-1.pdf','tangen.html':'https://www.visitoestfold.com/listing/tangen-brygge-gjestebrygge-i-tistedal/538830901/','gjestebrygger.html':'https://www.visitoestfold.com/halden/overnatting/gjestehavn/','anleggsbrygga.html':'https://www.visitoestfold.com/listing/gjestebrygge-nedstr%C3%B8ms-brekke-sluser/538833301/'}
def fetch(kv):
 k,u=kv;f=P/'raw'/k
 if f.exists():return k,'cached'
 try:
  r=requests.get(u,timeout=30);r.raise_for_status();f.write_bytes(r.content);f.with_suffix('.provenance.json').write_text(json.dumps(dict(url=u,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(r.content).hexdigest()),indent=1));return k,len(r.content)
 except Exception as e:return k,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for r in ex.map(fetch,urls.items()):print(r,flush=True)

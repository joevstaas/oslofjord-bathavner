import urllib.request,hashlib,datetime,json
from pathlib import Path
P=Path(__file__).parent
for k,u in {'son-nord2025':'https://www.sonhavn.no/wp-content/uploads/2025/07/son-havn-nord-oversikt.png','son-syd2019':'https://www.sonhavn.no/wp-content/uploads/2019/01/Oversiktsbilde-Son-Havn-SYD-080119.jpg'}.items():
 b=urllib.request.urlopen(u,timeout=40).read();ext='.png' if u.endswith('.png') else '.jpg';(P/'raw'/(k+ext)).write_bytes(b);(P/'raw'/(k+'-provenance.json')).write_text(json.dumps(dict(url=u,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(b).hexdigest()),indent=1));print(k,len(b),flush=True)

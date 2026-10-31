"""Lagre offentlige kommunale primærkilder med proveniens."""
import requests,json,hashlib,datetime,concurrent.futures
from pathlib import Path
P=Path(__file__).parent
URLS={'havner-2013.pdf':'https://www.sarpsborg.com/globalassets/dokumenter/politikk-og-planer/arealplanlegging/arealplan-dokumenter-2/smabathavnrapport-sarpsborg-kommunen-051213.pdf','kystsoneplan-2025.pdf':'https://sarpsborg.com/globalassets/dokumenter/politikk-og-planer/kunngjoringer/2025.11.27.--kystsoneplan-mindre-endring---vedtatt/vedlegg-2---revidert-planbeskrivelse.pdf'}
def fetch(kv):
 key,url=kv;p=P/'raw'/key
 if p.exists():return key,p.stat().st_size
 r=requests.get(url,timeout=45);r.raise_for_status();assert r.content.startswith(b'%PDF');p.write_bytes(r.content);p.with_suffix('.provenance.json').write_text(json.dumps(dict(url=url,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(r.content).hexdigest()),indent=1));return key,len(r.content)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
 for r in ex.map(fetch,URLS.items()):print(r)

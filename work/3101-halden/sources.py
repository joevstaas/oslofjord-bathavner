"""Lagre primærkilder og kommunens stedfestede havnekart; hentetid og hash følger hvert originaldokument."""
import requests,json,hashlib,datetime,re,html,concurrent.futures
from pathlib import Path
from urllib.parse import urljoin
P=Path(__file__).parent
urls={'kommune-batplasser.html':'https://www.halden.kommune.no/tjenester/miljo-og-teknisk/havn/batplasser/','kommune-gjestehavn.html':'https://www.halden.kommune.no/tjenester/miljo-og-teknisk/havn/gjestehavn/','haldenbf.html':'https://www.haldenbf.no/','seilforening.html':'https://www.haldenseilforening.net/','havneweb.html':'https://www.havneweb.no/haldenhavn/?mod=startsiden','engevika-kart.pdf':'https://www.halden.kommune.no/_f/p1/i256ab7c4-9cc5-40a2-94d4-fd81ab47702d/engevika-dagsturkart.pdf','ku-smabathavner.pdf':'https://www.halden.kommune.no/vil-du-vare-med-a-pavirke/politikk-og-planer/styringsgrupper-2019-2023/styringsgruppa-for-arealplanen/~/_f/p1/ie310fc7b-0440-47ab-acbf-55af0056bff4/240620-vedlegg-ku-for-enkeltomrader-revidert-251019-del-2rev-170620-m-bokmerker.pdf'}
def fetch(kv):
 k,u=kv;f=P/'raw'/k
 if f.exists():return k,'cached'
 try:
  r=requests.get(u,timeout=35);r.raise_for_status();f.write_bytes(r.content);f.with_suffix('.provenance.json').write_text(json.dumps(dict(url=u,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(r.content).hexdigest()),indent=1));return k,len(r.content)
 except Exception as e:return k,'ERROR '+str(e)[:120]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for r in ex.map(fetch,urls.items()):print(r,flush=True)
s=(P/'raw/kommune-batplasser.html').read_text();links=[]
for u,label in re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>',s,re.S|re.I):
 txt=html.unescape(re.sub('<[^>]+>','',label)).strip()
 if any(x in txt for x in ['Verven','Langbrygga','Sundsbrygga','Bro-overgangen','Felleskjøpet','Grønland','Tista senter','Tista Senter','Høvleriet','Reglement og prisliste']):
  ext='.png' if '.png' in u.lower() else '.pdf';key='kommunekart-'+str(len(links)+1)+ext;links.append(dict(key=key,label=txt,url=urljoin(urls['kommune-batplasser.html'],html.unescape(u))))
(P/'municipal-map-index.json').write_text(json.dumps(links,ensure_ascii=False,indent=1))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for r in ex.map(fetch,[(c['key'],c['url']) for c in links]):print(r,flush=True)

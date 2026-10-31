import json,urllib.request,urllib.parse,datetime,hashlib,concurrent.futures
from pathlib import Path
from html.parser import HTMLParser
P=Path(__file__).parent
U={'brreg-bat':'https://data.brreg.no/enhetsregisteret/api/enheter?'+urllib.parse.urlencode(dict(kommunenummer='3212',navn='båt',size=100)),'obu':'https://obat.no/obu-havner/','ursvik-vel':'https://ursvik.inngangen.com/2024/forslag.html','alvaern-turisme':'https://opplevnesodden.no/featured_item/alvaern/','fjellstrand-turisme':'https://opplevnesodden.no/featured_item/fjellstrand/','spro-utbygger':'https://www.hersleth.no/eiendom/utviklingsomrader/spro-havn-nesodden'}
class H(HTMLParser):
 def __init__(self):super().__init__();self.lines=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip and d.strip():self.lines.append(d.strip())
def f(z):
 k,u=z
 try:
  b=urllib.request.urlopen(u,timeout=40).read();ext='.json' if k.startswith('brreg') else '.html';(P/'raw'/(k+ext)).write_bytes(b)
  if ext=='.html':
   h=H();h.feed(b.decode('utf8',errors='replace'));(P/'raw'/(k+'.txt')).write_text('\n'.join(h.lines))
  (P/'raw'/(k+'-provenance.json')).write_text(json.dumps(dict(url=u,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(b).hexdigest()),indent=1));return k,len(b)
 except Exception as e:return k,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for r in ex.map(f,U.items()):print(r,flush=True)

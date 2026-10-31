"""Bevar primærkilder og tekstuttrekk med proveniens; kontakt ingen operatører."""
import json,urllib.request,hashlib,datetime,concurrent.futures
from pathlib import Path
from html.parser import HTMLParser
P=Path(__file__).parent
URLS={'vindfangerbukta': 'https://www.vindfangerbukta.no/havna/', 'drobak-bf': 'https://www.havneweb.no/drobak-bf/?mod=omhavnen', 'oscarsborg': 'https://oscarsborggjestehavn.no/', 'foreningsportal': 'https://frogn.foreningsportal.no/foreninger', 'gylteaasen': 'https://gylteaasenbaathavn.no/', 'solbukta': 'https://solbukta.net/baat/'}
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.lines=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip and d.strip():self.lines.append(d.strip())
def fetch(k,u):
 try:
  raw=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'oslofjord-bathavner/1.0'}),timeout=40).read();(P/'raw'/(k+'.html')).write_bytes(raw)
  p=Parser();p.feed(raw.decode('utf8',errors='replace'));(P/'raw'/(k+'.txt')).write_text('\n'.join(p.lines))
  (P/'raw'/(k+'-provenance.json')).write_text(json.dumps(dict(url=u,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(raw).hexdigest()),indent=1));return k,len(raw)
 except Exception as e:return k,repr(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for r in ex.map(lambda z:fetch(*z),URLS.items()):print(r,flush=True)

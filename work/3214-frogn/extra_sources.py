"""Tilleggskilder med råsvar, tekstuttrekk og proveniens."""
import json,urllib.request,hashlib,datetime,concurrent.futures
from pathlib import Path
from html.parser import HTMLParser
P=Path(__file__).parent
U={'gylteholmen':'https://www.gylteholmenbrygger.no/','dssf-brygger':'https://www.dssf.no/dssf/dssf-bryggeanlegg','dssf-gylte':'https://dssf.no/dssf/gylteholmen-brygger','haoya-friluftsrad':'https://www.oslofjorden.org/telting-pa-haoya/','gjestehavn-turist':'https://visitgreateroslo.com/no/drobak-gjestehavn','solbukta-birdlife2026':'https://oa.birdlife.no/Sider/Ekskursjoner_moeter/Eks_moe.php?category=1&id=1602&month=2026-08','solbukta-site':'https://www.solbukta.net/baat/index.html','gylteaasen-om':'https://gylteaasenbaathavn.no/om-oss.htm'}
for n in ['918941770','993149160','919329955','975628922','993956961','916260954']:U['brreg-'+n]='https://data.brreg.no/enhetsregisteret/api/enheter/'+n
class H(HTMLParser):
 def __init__(self):super().__init__();self.lines=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip and d.strip():self.lines.append(d.strip())
def fetch(z):
 k,u=z
 try:
  b=urllib.request.urlopen(u,timeout=35).read();ext='.json' if k.startswith('brreg') else '.html';(P/'raw'/(k+ext)).write_bytes(b)
  if ext=='.html':
   h=H();h.feed(b.decode('utf8',errors='replace'));(P/'raw'/(k+'.txt')).write_text('\n'.join(h.lines))
  (P/'raw'/(k+'-provenance.json')).write_text(json.dumps(dict(url=u,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(b).hexdigest()),indent=1));return k,len(b)
 except Exception as e:return k,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
 for r in e.map(fetch,U.items()):print(r,flush=True)

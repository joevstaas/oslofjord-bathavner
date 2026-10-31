import urllib.request,json,hashlib,datetime,concurrent.futures
from pathlib import Path
from html.parser import HTMLParser
P=Path(__file__).parent
urls={'oppegard-foreningen':'https://oppegaard-baatforening.no/foreningen.aspx','oppegard-hjem':'https://oppegaard-baatforening.no/','kyststi':'https://www.nordrefollo.kommune.no/tjenester/kultur-idrett-og-fritid/kyststi-langs-bunnefjorden/'}
for n in ['875473212','916034954','916260954','921055927','987337079']:urls['brreg-'+n]='https://data.brreg.no/enhetsregisteret/api/enheter/'+n
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
  b=urllib.request.urlopen(u,timeout=45).read();suffix='.json' if k.startswith('brreg') else '.html';f=P/'raw'/(k+suffix);f.write_bytes(b)
  if suffix=='.html':
   p=Parser();p.feed(b.decode('utf8',errors='replace'));(P/'raw'/(k+'.txt')).write_text('\n'.join(p.lines))
  (P/'raw'/(k+'-provenance.json')).write_text(json.dumps(dict(url=u,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(b).hexdigest()),indent=1))
  return k,len(b)
 except Exception as e:return k,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for r in ex.map(lambda a:fetch(*a),urls.items()):print(r,flush=True)

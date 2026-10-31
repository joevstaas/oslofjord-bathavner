"""Primærkilder med råarkiv, tekst og proveniens. Gjeldende bruk skilles fra planlagt/historisk."""
import json,urllib.request,hashlib,datetime,concurrent.futures
from pathlib import Path
from html.parser import HTMLParser
P=Path(__file__).parent
U={'kommune-havner':'https://www.hvaler.kommune.no/innhold/bygg-miljo-og-naring/havner/','borg-utleie':'https://www.borg-havn.no/utleie-batplasser/','borg-havneweb':'https://www.havneweb.no/borg-havn/?mod=sokplass','borg-fiskeri':'https://www.borg-havn.no/fiskeri-og-naeringskaier/','utgardskilen-bf':'https://www.xn--utgrdskilenbtforening-u2bj.no/om-oss-16647s.html','sand-marina':'https://sandmarina.no/','skjaerhalden-bf':'https://www.skjaerhalden-baatforening.no/','skjaerhalden-gjest':'https://www.hvalergjestehavn.no/','odegard-plan':'https://www.hvaler.kommune.no/nyhetsarkiv/varsel-av-oppstart-av-reguleringsplanarbeid-for-odegardskilen-bathavn/'}
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
  r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'oslofjord-bathavner/1.0'}),timeout=35);b=r.read();ext='.html';(P/'raw'/(k+ext)).write_bytes(b)
  h=H();h.feed(b.decode(r.headers.get_content_charset() or 'utf8',errors='replace'));(P/'raw'/(k+'.txt')).write_text('\n'.join(h.lines))
  (P/'raw'/(k+'-provenance.json')).write_text(json.dumps(dict(url=u,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(b).hexdigest()),indent=1));return k,len(b)
 except Exception as e:return k,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for r in ex.map(fetch,U.items()):print(r,flush=True)

"""Arkiver primærkilder og tekstuttrekk uten å anta aktuell drift eller lik kapasitet."""
import json,urllib.request,hashlib,datetime,concurrent.futures
from pathlib import Path
from html.parser import HTMLParser
P=Path(__file__).parent
U={'son-kommunen':'https://www.vestby.kommune.no/tjenester/friluftsliv-natur-og-miljo/son-havn','son-gjest':'https://www.sonhavn.no/son-gjestehavn/','son-fast':'https://www.sonhavn.no/smaabaathavn/','son-kart':'https://www.sonhavn.no/havnekart/','son-faq':'https://www.sonhavn.no/faq/ofte-stile-sporsmal-faq/','sonbf':'https://www.sonbaat.no/havnas-fasiliteter/','sonbf-regler':'https://www.sonbaat.no/havnereglement/','sonbf-avfall':'https://www.sonbaat.no/avfallshandtering/','sonskilen-om':'https://www.sonskilen.no/om-oss','sonskilen-tilbud':'https://www.sonskilen.no/vi-tilbyr','sonskilen-plass':'https://www.sonskilen.no/batplass','hvitsten-vel':'https://www.hvitstenvel.no/Hvitsten-Vel','strender':'https://www.vestby.kommune.no/om-vestby/strender-og-badeplasser','lag-foreninger':'https://www.vestby.kommune.no/tjenester/kultur-og-idrett/lag-og-foreninger','kjovangen-vel':'https://kjovangenvel.org/'}
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
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
 for r in e.map(fetch,U.items()):print(r,flush=True)

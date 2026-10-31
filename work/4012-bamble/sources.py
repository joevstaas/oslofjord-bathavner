"""Bevar primærkilder og tekstuttrekk med proveniens; kontakt ingen operatører."""
import json,urllib.request,hashlib,datetime,concurrent.futures
from pathlib import Path
from html.parser import HTMLParser
P=Path(__file__).parent
URLS={'gjestehavn-reglement':'https://www.bamble.kommune.no/contentassets/efe647c28339405982f6aa17ab356c00/reglement-for-langesund-gjestehavn_3.pdf','vestrestrand-innspill':'https://www.bamble.kommune.no/contentassets/1eaa40268ddc4fc4aaa1328e24b70a19/27-arkitektkontoret-henning-karlsen-as-for-vestrestrand-bathavn-200422.pdf','stathelle-marina-plan':'https://www.bamble.kommune.no/contentassets/8f19b4b15a3e45fa87a0665da0ef1173/ny-komplett-planbeskrivelse-05.10.20.pdf','stathelle-marina-ros':'https://www.bamble.kommune.no/contentassets/35c003a344e94929a9422c72847cd2c5/ros-analyse-plan-stathelle-marina-rettet-10.07.20.pdf','sjobua-valle':'https://www.visitnorway.no/listings/sjobua-marina-og-havn/18373/','stathelle-gjestebrygge':'https://www.visitnorway.no/listings//stathelle-gjestebrygge/23918','langoya-gjestehavn':'https://www.visitnorway.no/listings/langoya-gjestehavn/27593/','kongshavn-gjestehavn':'https://www.visitnorway.no/listings/kongshavn-gjestehavn/23916/','langesund-gjestehavn':'https://www.visitnorway.no/listings/langesund-gjestehavn/23915/','asenbakken':'https://lokalhistoriewiki.no/wiki/%C3%85senbakken','vallekjaer':'https://lokalhistoriewiki.no/wiki/Vallekj%C3%A6r_(vei_i_Bamble)','valle':'https://lokalhistoriewiki.no/wiki/Valle_(Bamble)','knbf-ost':'https://www.knbf.no/regioner/ost/medlemsforeninger-ost/'}
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
  raw=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'oslofjord-bathavner/1.0'}),timeout=40).read();ext='.pdf' if raw[:4]==b'%PDF' else '.html';(P/'raw'/(k+ext)).write_bytes(raw)
  if ext=='.html':p=Parser();p.feed(raw.decode('utf8',errors='replace'));(P/'raw'/(k+'.txt')).write_text('\n'.join(p.lines))
  (P/'raw'/(k+'-provenance.json')).write_text(json.dumps(dict(url=u,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(raw).hexdigest()),indent=1));return k,len(raw)
 except Exception as e:return k,repr(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for r in ex.map(lambda z:fetch(*z),URLS.items()):print(r,flush=True)

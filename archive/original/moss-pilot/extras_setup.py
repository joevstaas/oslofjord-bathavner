import sys,json,urllib.request,urllib.parse,concurrent.futures
from pathlib import Path
P=Path(__file__).parent;sys.path.insert(0,str(P/'deps'));from pyproj import Transformer
from lxml import html
T=Transformer.from_crs(4326,25833,always_xy=True);ss=[]
def add(k,lon,lat,size=1000):
 x,y=T.transform(lon,lat);ss.append(dict(id=k,bbox=[x-size/2,y-size/2,x+size/2,y+size/2],width=1500,height=1500))
places=json.loads((P/'places.json').read_text())
for key,n in [('kippenes','Kippenes'),('sildebaugen','Sildebaugen'),('nasle','Nasle'),('lersbauen','Lersbauen'),('kjellandsvik','Kjellandsvik'),('evjesund','Evjesund')]:
 q=places[n][0];add(key,q['lon'],q['lat'])
# Seeds selected from actual coastal overview pixels, not postal addresses.
for k,t,x,y in [('teibern','a-coast-2-0',170,333),('knutvika','a-coast-2-0',300,450),('roedsstrand','a-coast-2-1',180,430),('refsnes-gods','a-coast-1-4',244,120),('fleischer','a-coast-2-4',30,230)]:
 m=json.loads((P/'images'/f'{t}.json').read_text());a,b,c,d=m['bbox'];X=a+x/600*(c-a);Y=d-y/600*(d-b);ss.append(dict(id=k,bbox=[X-500,Y-500,X+500,Y+500],width=1500,height=1500))
(P/'extras.json').write_text(json.dumps(ss,indent=2))
urls={'abf-havn':'https://abf-teibern.no/baat/','soly-havn':'https://moss-seilforening.no/havn-og-klubbhus','havn':'https://www.moss-havn.no/','refsnes-vedtak':'https://www.statsforvalteren.no/siteassets/fm-oslo-og-viken/horinger-og-kunngjoringer/refsnes-bryggeforening/vedtak-om-tillatelse-etter-forurensningsloven-til-mudring-ved-felles-batanlegg---1_2864---moss-kommune.pdf'}
def f(q):
 k,u=q
 try:
  b=urllib.request.urlopen(u,timeout=20).read();(P/'raw'/f'{k}.data').write_bytes(b)
  if k=='refsnes-vedtak':return k,len(b)
  s=html.fromstring(b)
  for z in s.xpath('//script|//style'):z.drop_tree()
  txt=' '.join(s.text_content().split());(P/'raw'/f'{k}.txt').write_text(txt)
  return k,txt[:2500],[(a.text_content().strip(),a.get('href')) for a in s.xpath('//a[@href]|//iframe[@src]') if any(z in str(a.attrib).lower() for z in ['kart','maps','havn','bobil'])][:10]
 except Exception as e:return k,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for z in ex.map(f,urls.items()):print(z,flush=True)

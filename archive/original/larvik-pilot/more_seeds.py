import json,sys,urllib.request,urllib.parse
from pathlib import Path
P=Path(__file__).parent;sys.path.insert(0,str(P/'deps'))
from pyproj import Transformer
T=Transformer.from_crs(4326,25833,always_xy=True);ss=[]
for key,lon,lat in [('agnes-havn',10.0385,59.0118),('farris-gopledal',10.0150,59.078),('svenner',10.147,58.9695)]:
 x,y=T.transform(lon,lat);ss.append(dict(id=key,bbox=[x-500,y-500,x+500,y+500],width=1400,height=1400))
for key,src,px in [('gusland','a-coast-1-0',(391,450)),('ranvika','a-coast-6-2',(410,200)),('naver-vest','a-coast-2-0',(245,350)),('naver-ost','a-coast-2-0',(380,350))]:
 m=json.loads((P/'images'/f'{src}.json').read_text());a,b,c,d=m['bbox'];x=a+px[0]/600*(c-a);y=d-px[1]/600*(d-b);ss.append(dict(id=key,bbox=[x-500,y-500,x+500,y+500],width=1400,height=1400))
for key,addr in [('seilforening','Ødegårdsveien 20'),('knoln','Rekkevik Brygge 3')]:
 u='https://ws.geonorge.no/adresser/v1/sok?'+urllib.parse.urlencode({'sok':addr,'kommunenummer':'3909','treffPerSide':5});d=json.load(urllib.request.urlopen(u,timeout=20));(P/'raw'/f'address-{key}.json').write_text(json.dumps(d));a=next(a for a in d['adresser'] if a['adressetekst'].lower()==addr.lower());v=a['representasjonspunkt'];x,y=T.transform(v['lon'],v['lat']);ss.append(dict(id=key,bbox=[x-500,y-500,x+500,y+500],width=1400,height=1400));print(key,v,flush=True)
(P/'more-extras.json').write_text(json.dumps(ss,indent=2))

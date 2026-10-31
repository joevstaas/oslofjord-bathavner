"""Samle OSM-pirklynger, OSM-marinamerker og kandidater fra det systematiske kontaktarkssøket. Lager specs for detaljbilder."""
import json,warnings
from pathlib import Path
from shapely.geometry import shape,Point
from shapely.ops import transform
from pyproj import Transformer
warnings.filterwarnings('ignore');P=Path(__file__).parent
T=Transformer.from_crs(4326,25833,always_xy=True).transform
B=transform(T,shape(json.loads((P/'kommunegrense.geojson').read_text())['features'][0]['geometry']))
C=json.loads((P/'clusters.json').read_text())
# Funn fra kontaktark (coast-sheet-0..21), koordinater omregnet fra panelpiksler; flis-ID angir kilden.
M=[('M01','Sildeberget – stor bryggegruppe uten OSM-pir',192315,6559632,'coast-191700-6559200'),
 ('M02','Ivarsand øst – brygger med båter',194353,6549217,'coast-193500-6548400'),
 ('M03','Stathelle vest – bryggegruppe',193657,6558253,'coast-193500-6557400'),
 ('M04','Asvall/Fjeldstrand – brygger',197440,6555370,'coast-197100-6554700'),
 ('M05','Kuskjær – kai og brygger',196815,6556178,'coast-196200-6555600'),
 ('M06','Herre – elveløp med småbåter',188550,6564214,'coast-188100-6563700'),
 ('M07','Nordvest – brygger ved vik',186070,6567162,'coast-185400-6566400'),
 ('M08','Klokkersundet nord – marina (OSM node/5107367403)',190533,6547453,'coast-189900-6546600'),
 ('M09','Ivarsand vest – marina (OSM node/5107367404)',193068,6549493,'coast-192600-6549300'),
 ('M10','Langårsund? – OSM marina way/605714544',195529,6550040,'coast-195300-6549300'),
 ('M11','Valle øst/Havsundbukta – brygger',187880,6544800,'coast-187200-6543900'),
 ('M12','Langøya øst – mulig brygge',198700,6555526,'coast-198000-6554700'),
 # Brukerinnspill 2026-10-31 etter første leveranse: oversett i kontaktarkene.
 ('M13','Stranda ved Grosholmen – brygger (brukerinnspill)',189900,6547060,'brukerinnspill'),
 ('M14','Kjønnøya, Havparadiset – brygger (brukerinnspill)',190640,6545850,'brukerinnspill'),
 # Brukerinnspill runde 2 (2026-10-31), stedfestet i detaljbilder detail-U01..U11.
 ('M15','Grunnsundveien – båter langs kai (brukerinnspill)',189425,6545528,'brukerinnspill'),
 ('M16','Hafsundveien – brygge (brukerinnspill)',189990,6545370,'brukerinnspill'),
 ('M17','Trolldalen – molohavn (brukerinnspill)',189223,6544830,'brukerinnspill'),
 ('M18','Rognstranda – brygge (brukerinnspill)',195953,6552553,'brukerinnspill'),
 ('M19','Vinjekilen – brygge (brukerinnspill)',193913,6551723,'brukerinnspill')]
out=[]
for c in C:
 x0,y0,x1,y1=c['bounds'];side=max(450,x1-x0+200,y1-y0+200)
 out.append(dict(cid=c['cid'],kind='osm_pier_cluster',center=c['center'],side=side,inside=Point(c['center']).distance(B)<1,marks=[m['tags'].get('name') for m in c['marks']]))
for cid,name,x,y,src in M:
 d=Point(x,y).distance(B);out.append(dict(cid=cid,kind='bildefunn_kontaktark',name=name,center=[x,y],side=(300 if cid in('M13','M14') else 220 if cid>='M15' else 450),inside=d<1,dist_boundary=round(d),source_tile=src))
(P/'candidates.json').write_text(json.dumps(out,ensure_ascii=False,indent=1))
specs=[]
for c in out:
 x,y=c['center'];s=c['side'];px=int(min(1800,max(700,s/0.65)))
 specs.append(dict(id='detail-'+c['cid'],bbox=[x-s/2,y-s/2,x+s/2,y+s/2],width=px,height=px))
(P/'detail-specs.json').write_text(json.dumps(specs,indent=1))
for c in out:print(c['cid'],c['kind'][:4],[round(v) for v in c['center']],round(c['side']),c['inside'],c.get('dist_boundary',''),c.get('name',c.get('marks')))

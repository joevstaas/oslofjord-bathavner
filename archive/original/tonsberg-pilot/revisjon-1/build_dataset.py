import json,csv,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'deps'))
from shapely.geometry import Polygon,shape,mapping
from shapely.ops import transform,unary_union
from shapely.geometry.polygon import orient
from pyproj import Transformer
P=Path(__file__).parent
forward=Transformer.from_crs(4326,25833,always_xy=True).transform
back=Transformer.from_crs(25833,4326,always_xy=True).transform
boundary=unary_union([transform(forward,shape(f['geometry'])) for f in json.loads((P/'kommunegrense.geojson').read_text())['features']])
rows=[]
def add(name,key,size,pts,osm=(),sources=(),uncertain=False,note=''):
 rows.append(dict(name=name,map=key,display_size=size,pixels=pts,osm_ids=list(osm),sources=list(sources),uncertain=uncertain,note=note))
add('Ollebukta marina','sentrum',(1300,1138),[(534,632),(528,634),(519,657),(518,696),(849,905),(869,916),(885,900),(909,856),(894,848),(909,818),(880,793),(767,733),(752,746),(699,716),(544,639)],['way/38901313'],['https://www.ollebukta.no/'])
add('Kaldnes marina','sentrum',(1300,1138),[(442,680),(432,687),(439,710),(460,743),(475,734)],['way/38848945'])
add('Tønsberg gjestehavn – Brygga','sentrum',(1300,1138),[(353,278),(378,322),(407,369),(441,419),(475,471),(494,501),(488,514),(475,514),(461,484),(426,437),(393,387),(362,339),(337,292)],sources=['https://www.tonsberg.kommune.no/tjenester/kultur-idrett-og-fritid/turist-i-tonsberg/gjestehavna/'],note='Avgrenser bryggebeltet vest for sentrum; farleden er utelatt. Kommunen oppgir sesongstengt vinteren 2026/27.')
add('Kaldnes – indre bryggeanlegg','sentrum',(1300,1138),[(237,391),(255,394),(282,481),(298,570),(287,576),(274,562),(255,485)],uncertain=True,note='Beskrivende navn. Brygger i kanal mellom boligrekker; havnestatus og organisering må bekreftes.')
add('Kaldnes – ytre bryggeanlegg','sentrum',(1300,1138),[(258,374),(302,391),(324,445),(350,452),(374,531),(352,539),(325,465),(300,470),(279,400),(270,395)],uncertain=True,note='Beskrivende navn. Brygger ved boligrekker; havnestatus og organisering må bekreftes.')
add('Vallø Småbåthavn','vallo',(1300,1300),[(480,500),(540,351),(584,287),(609,282),(699,330),(753,375),(754,476),(717,542),(716,580),(627,589),(602,595),(484,519)],['relation/11898442','node/1891818749'])
add('Sjøsenteret Vallø','vallo',(1300,1300),[(588,785),(719,763),(731,834),(775,891),(721,919),(650,893),(586,847)],['way/546762948','node/5107343361'],['https://www.xn--btplassvall-x8a1x.no/'])
add('Bliksekilen Båthavn','bliksekilen',(1300,1300),[(592,495),(600,478),(608,457),(726,509),(694,656),(568,636)],['way/1217522237'])
add('Husvik/Nes – båthavn','husvik',(1219,1500),[(563,501),(650,479),(666,508),(616,579),(572,589),(535,518)],['way/546250542','node/5107520723'],note='Beskrivende navn; OSM-punkt og område er slått sammen som samme havn.')
add('Nordre Nes – bryggeanlegg','husvik',(1219,1500),[(423,937),(472,918),(477,934),(466,974),(449,986),(430,982)],['node/5107521786'],uncertain=True,note='Beskrivende navn. Få brygger; avgrensning og om dette er en felles småbåthavn må bekreftes.')
add('Søndre Nes – båthavn','husvik',(1219,1500),[(767,1023),(827,1030),(899,1075),(853,1112),(800,1100),(739,1080),(711,1109),(700,1102),(733,1061)],['node/5107521775'],note='Beskrivende navn; omfatter den sammenhengende bryggegruppen.')
add('Soria Moria Båtforening','husoy',(1300,1300),[(383,295),(427,297),(431,322),(383,338)],['node/3051926714'],uncertain=True,note='OSM navngir båtforeningen; lite bryggeanlegg med usikker yttergrense.')
add('Husøysund/Kirkegaten – mulig havneområde','husoy',(1300,1300),[(811,876),(847,844),(836,806),(770,736),(701,686),(668,707),(671,727)],['way/53878403'],uncertain=True,note='OSM har marinaområde, men topografisk kart viser ikke et tydelig sammenhengende marinaanlegg. Må kontrolleres mot ortofoto.')
add('Jarlsø Vest','jarlso',(1300,1300),[(846,775),(853,789),(827,903),(810,1010),(833,1140),(814,1158),(802,1125),(779,1119),(782,1097),(801,1099),(792,1060),(775,1009),(797,1004),(786,956),(809,953),(817,913),(780,902),(784,882),(816,888),(826,865),(787,853),(789,834),(833,846),(842,814),(798,803),(803,784)],sources=['https://www.havneweb.no/jarlso-brygge/'],note='Bryggesameiets boligtilknyttede båtplasser. Avgrenset til vestre bryggerekke; landanlegg er utelatt.')
add('Jarlsø – nordre gjestebrygger','jarlso',(1300,1300),[(951,733),(1019,738),(1028,766),(954,765)],sources=['https://jarlsoe.no/servicetilbud/'],note='To gjestebrygger ved broen; adskilt fra Jarlsø Vest.')
add('Rakkevik båthavn','vestfjord',(825,1500),[(620,510),(649,515),(663,546),(649,583),(616,575)],sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/899098242'])
add('Ringshaugodden – mulig småbåthavn','ringshaug',(900,1500),[(491,1034),(549,1043),(537,1068),(523,1080),(497,1098),(488,1090),(512,1069),(519,1056)],uncertain=True,note='Beskrivende navn. Moloområde; småbåtbruk og operativ status er ikke bekreftet.')
add('Furustrand – mulig småbåthavn','ringshaug',(900,1500),[(296,1289),(320,1300),(322,1322),(305,1341),(293,1338),(289,1314)],uncertain=True,note='Beskrivende navn. Lite moloområde ved campingplass; småbåtbruk må bekreftes.')
add('Karlsvika – mulig småbåthavn','karlsvika',(900,1500),[(687,1393),(706,1393),(716,1404),(733,1409),(732,1419),(706,1414),(700,1430),(680,1421)],uncertain=True,note='Beskrivende navn. Brygge-/moloområde kan ha annen bruk; krever bekreftelse.')
features=[]
for i,r in enumerate(rows,1):
 m=json.loads((P/'images'/f"{r['map']}.json").read_text()); x0,y0,x1,y1=m['bbox'];w,h=r['display_size']
 g=Polygon([(x0+x/w*(x1-x0),y1-y/h*(y1-y0)) for x,y in r['pixels']])
 assert g.is_valid,(r['name'],'invalid digitization')
 clipped=not boundary.covers(g);g=g.intersection(boundary)
 assert not g.is_empty and g.geom_type=='Polygon',(r['name'],g.geom_type)
 g=orient(g,sign=1)
 src=r['sources']+[f'https://www.openstreetmap.org/{o}' for o in r['osm_ids']]+[m['url']]
 geo=transform(back,g); center=geo.representative_point()
 prop=dict(id=f'3905-H{i:02d}-B01',harbour_id=f'3905-H{i:02d}',name=r['name'],municipality='Tønsberg',municipality_code='3905',status='usikker_kandidat' if r['uncertain'] else 'kart_og_kildeunderbygget',approval_status='til_godkjenning',geometry_role='forelopig_havneomrade',area_m2=round(g.area,1),longitude=round(center.x,7),latitude=round(center.y,7),sources=src,osm_ids=r['osm_ids'],method='manuell_avgrensning_fra_georeferert_topografisk_kart',retrieved_date='2026-10-28',source_observation_date=None,estimated_accuracy_m=None,needs_orthophoto_review=True,municipality_clipped=clipped,note=r['note'],map_attribution='© Kartverket; OSM-bidrag © OpenStreetMap contributors, ODbL')
 features.append(dict(type='Feature',properties=prop,geometry=mapping(geo)))
for i,a in enumerate(features):
 ga=transform(forward,shape(a['geometry']))
 assert ga.is_valid
 assert ga.difference(boundary).area<0.01
 for b in features[i+1:]:
  overlap=ga.intersection(transform(forward,shape(b['geometry']))).area
  assert overlap<1,(a['properties']['name'],b['properties']['name'],overlap)
fc=dict(type='FeatureCollection',name='Tønsberg – foreløpige småbåthavner',description='Screening av kommunens kyst og innsjøer i topografisk kart. Ikke dokumentert komplett. Alle avgrensninger trenger ortofotokontroll. Usikre kandidater er inkludert og tydelig merket.',features=features)
(P/'tonsberg-bathavner.geojson').write_text(json.dumps(fc,ensure_ascii=False,indent=2))
with (P/'tonsberg-metadata.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(features[0]['properties']),delimiter=';');writer.writeheader()
 for a in features:
  writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,list) else v for k,v in a['properties'].items()})
(P/'manual-digitization.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print(json.dumps(dict(features=len(features),supported=sum(not r['uncertain'] for r in rows),uncertain=sum(r['uncertain'] for r in rows),clipped=[f['properties']['name'] for f in features if f['properties']['municipality_clipped']],validation='valid polygons; within boundary; no overlaps >1 m2'),ensure_ascii=False))

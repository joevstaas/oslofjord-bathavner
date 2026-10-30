import sys,json,pathlib,csv,hashlib,datetime
R=pathlib.Path(__file__).parent;sys.path.insert(0,str(R/'deps'))
from shapely.geometry import shape,mapping,Polygon,Point,box
from shapely.geometry.polygon import orient
from shapely.ops import transform,unary_union
from pyproj import Transformer
from shapely.validation import explain_validity
T=Transformer.from_crs(4326,25833,always_xy=True);G=Transformer.from_crs(25833,4326,always_xy=True)
def save(n,o): (R/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def fc(fs):return dict(type='FeatureCollection',features=fs)
def f(p,g):return dict(type='Feature',properties=p,geometry=mapping(g) if g is not None else None)
boundary=shape(json.load(open(R/'kommunegrense.geojson'))['features'][0]['geometry']);features=[];geoms=[];checks=[]
for d in json.load(open(R/'digitization.json')):
 m=json.load(open(R/'images'/f"{d['image']}.json"));b=m['bbox'];w,h=d['frame']
 pts=[G.transform(b[0]+x/w*(b[2]-b[0]),b[3]-y/h*(b[3]-b[1])) for x,y in d['vertices']]
 g=orient(Polygon([[round(x,7),round(y,7)] for x,y in pts]),sign=1);inside=boundary.covers(g)
 assert g.is_valid,(d['id'],explain_validity(g));assert inside,('outside',d['id'])
 props={k:d[k] for k in ['id','harbour_id','name','status','osm_id']}
 props.update(kommunenummer='3901',municipality='Horten',geometry_role='vannomrade_ved_bryggeanlegg',method='manuell_digitalisering_georeferert_topografisk_kart',geometry_status='forelopig_ikke_offisiell',positional_accuracy_m=None,source_observation_date=None,retrieved='2026-10-28',reviewed='2026-10-28',reviewer='AI-assistent; ikke uavhengig fagkontroll',needs_orthophoto_review=True,inside_municipality=inside,area_m2=round(transform(T.transform,g).area),source_image=f"images/{d['image']}.png",image_metadata=f"images/{d['image']}.json",sources=list(dict.fromkeys([m['url']]+d['sources']+(['https://www.openstreetmap.org/'+d['osm_id']] if d['osm_id'] else []))),attribution='Kartgrunnlag © Kartverket; supplerende kandidater/navn © OpenStreetMap-bidragsytere (ODbL)',note=d.get('note') or ('Havnebruk støttet av kart og tilleggskilde. Geometrien er et manuelt forslag.' if d['status']=='kart_og_kilde' else 'Klassifisering og avgrensning må avklares.'))
 features.append(f(props,g));geoms.append(g);checks.append(dict(id=d['id'],valid=g.is_valid,closed=g.exterior.coords[0]==g.exterior.coords[-1],counterclockwise=g.exterior.is_ccw,inside_municipality=inside,area_m2=props['area_m2']))
for name,status in [('bathavner-alle-forslag.geojson',None),('bathavner-kart-og-kilde.geojson','kart_og_kilde'),('bathavner-ma-avklares.geojson','ma_avklares')]:save(name,fc([x for x in features if status is None or x['properties']['status']==status]))
follow=[
 f(dict(id='U01',name='Løvøya båthavn – kobling til kart',status='kildebekreftet_eksakt_bryggegruppe_uavklart',reason='Båthavn dokumentert av operatør/oversikt. Kandidat K01 ved Drasund er ikke sikkert knyttet til operatøren. Ikke talt som en ekstra havn.',source_image='images/lovoya.png',sources=['https://lovoyaoslofjord.no/','https://velihavn.no/gjestehavner/vestfold/lovoya-bathavn']),Point(10.439467,59.4457)),
 f(dict(id='U02',name='Falkensten vel båthavn',status='oppfort_i_havneoversikt_lokasjon_uavklart',reason='Nevnt i Horten havns oversikt. Nøyaktig bryggeanlegg og eventuell overlapp med andre funn må avklares. Forretningsadresse er ikke brukt som havnelokasjon.',source_image='images/lovoya.png',sources=['https://www.hortenhavn.no/fritidsbaat/']),None),
 f(dict(id='U03',name='Seilforeningen Julaften af Indre Havn',status='oppfort_i_havneoversikt_avgrensning_uavklart',reason='Forening i Horten havns oversikt. Ikke sikkert grunnlag for eget polygon eller for å telle en separat havn.',source_image='images/indre-havn.png',sources=['https://www.hortenhavn.no/fritidsbaat/','https://julaften.wordpress.com/']),None),
 f(dict(id='U04',name='Keisemarken båt og badehus',status='oppfort_i_havneoversikt_avgrensning_uavklart',reason='Nevnt i Horten havns oversikt. Må avklare brygger og grense mot Pluggen/andre nærliggende anlegg.',source_image='images/indre-vest.png',sources=['https://www.hortenhavn.no/fritidsbaat/']),None)]
save('oppfolgingspunkter.geojson',fc(follow));grid=[]
for s in json.load(open(R/'scan-maps.json')):
 gg=transform(G.transform,box(*s['bbox'])).intersection(boundary)
 grid.append(f(dict(id=s['id'],status='visuelt_gjennomgatt_topografisk_kart',image='images/'+s['id']+'.png',nominal_map_pixel_size_m=2,orthophoto_review=False,screening_resolution='oversiktsgjennomgang; kandidater i detalj',water_selection='Minst 20 vannpiksler i 6.25 m/piksel kommuneoversikt innen kommunen per 4 x 4 km rute',water_area_estimate_m2=s['water_area_estimate_m2'],reused=bool(s.get('cache_source'))),gg))
save('dekningsruter.geojson',fc(grid));coverage=unary_union([shape(x['geometry']) for x in grid]);overlaps=[]
for i,g in enumerate(geoms):
 for j in range(i):
  area=transform(T.transform,g.intersection(geoms[j])).area
  if area>1:overlaps.append(dict(a=features[i]['properties']['id'],b=features[j]['properties']['id'],area_m2=round(area,1)))
supported=[x for x in features if x['properties']['status']=='kart_og_kilde'];uncertain=[x for x in features if x['properties']['status']=='ma_avklares']
qa=dict(date='2026-10-28',polygons=len(features),harbour_groups=len({x['properties']['harbour_id'] for x in features}),source_supported_polygons=len(supported),source_supported_groups=len({x['properties']['harbour_id'] for x in supported}),uncertain_polygons=len(uncertain),uncertain_groups=len({x['properties']['harbour_id'] for x in uncertain}),scan_tiles=len(grid),cached_scan_tiles=sum(x['properties']['reused'] for x in grid),checks=checks,overlaps=overlaps,all_polygons_inside_scan_coverage=all(coverage.covers(g) for g in geoms),complete_inventory=False,completeness_and_recall_measured=False,orthophoto_access='Ikke tilgjengelig i forrige pilot. Ingen nye autentiseringsforsøk; ingen flyfotoverifikasjon.',imagery_acquisition_dates_known=False,osm_local_extracts=len(list((R/'raw').glob('*.osm'))),independent_human_review=False)
save('kvalitetskontroll.json',qa)
with (R/'havneoversikt.csv').open('w',newline='') as z:
 fields=['id','harbour_id','name','status','area_m2','source_image'];w=csv.DictWriter(z,fieldnames=fields);w.writeheader()
 for x in features:w.writerow({k:x['properties'][k] for k in fields})
manifest=[]
for q in sorted((R/'images').glob('*.json')):
 m=json.load(open(q));png=q.with_suffix('.png');manifest.append(dict(id=m['id'],file=str(png.relative_to(R)),metadata=str(q.relative_to(R)),bytes=png.stat().st_size,sha256=hashlib.sha256(png.read_bytes()).hexdigest(),crs=m['crs'],bbox=m['bbox'],url=m['url'],retrieved=m['retrieved'],source_observation_date=None))
save('bildemanifest.json',manifest)
print(json.dumps({k:v for k,v in qa.items() if k!='checks'},ensure_ascii=False))

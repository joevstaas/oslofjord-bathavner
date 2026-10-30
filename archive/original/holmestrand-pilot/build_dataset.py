"""Transform reviewed image vertices into reproducible WGS84 polygon proposals."""
import sys,json,pathlib,shutil,csv
ROOT=pathlib.Path(__file__).parent
sys.path.insert(0,str(ROOT/'deps'))
from shapely.geometry import Polygon,shape,mapping,box,Point
from shapely.geometry.polygon import orient
from shapely.ops import transform,unary_union
from pyproj import Transformer
from shapely.validation import explain_validity

def save(name,obj): (ROOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def fc(features): return dict(type='FeatureCollection',features=features)
def feat(props,geom): return dict(type='Feature',properties=props,geometry=mapping(geom) if geom is not None else None)
to_geo=Transformer.from_crs(25833,4326,always_xy=True)
to_utm=Transformer.from_crs(4326,25833,always_xy=True)
boundary=shape(json.loads((ROOT/'kommunegrense.geojson').read_text())['features'][0]['geometry'])
original=ROOT/'images/original-sentrum.png'
if not original.exists():
    shutil.copyfile(ROOT.parent/'holmestrand-sentrum.png',original)
merc_to_geo=Transformer.from_crs(3857,4326,always_xy=True)
save('images/original-sentrum.json',dict(id='original-sentrum',bbox=[1146583.1865142034,8284737.665785735,1150383.1865142034,8288937.665785735],width=3800,height=4200,crs='EPSG:3857',retrieved='2026-10-28',source_observation_date=None,source='© Kartverket, Topografisk norgeskart'))
m=json.loads((ROOT/'images/original-sentrum.json').read_text())
from urllib.parse import urlencode
m['url']='https://wms.geonorge.no/skwms1/wms.topo?'+urlencode(dict(service='WMS',version='1.3.0',request='GetMap',layers='topo',styles='',crs=m['crs'],bbox=','.join(map(str,m['bbox'])),width=m['width'],height=m['height'],format='image/png'))
save('images/original-sentrum.json',m)
features=[];geoms=[];checks=[]
for d in json.loads((ROOT/'digitization.json').read_text()):
    m=json.loads((ROOT/'images'/f"{d['image']}.json").read_text());b=m['bbox'];fw,fh=d['frame']
    xy=[(b[0]+px/fw*(b[2]-b[0]), b[3]-py/fh*(b[3]-b[1])) for px,py in d['vertices']]
    converter=merc_to_geo if m['crs']=='EPSG:3857' else to_geo
    coords=[tuple(round(v,7) for v in converter.transform(x,y)) for x,y in xy]
    g=orient(Polygon(coords),sign=1)
    if not g.is_valid: raise ValueError((d['id'],explain_validity(g)))
    gu=transform(to_utm.transform,g)
    inside=boundary.covers(g)
    props={k:d[k] for k in ['id','harbour_id','name','status','osm_id']}
    props.update(kommunenummer='3903',municipality='Holmestrand',geometry_role='vannomrade_ved_bryggeanlegg',method='manuell_digitalisering_georeferert_topografisk_kart',geometry_status='forelopig_ikke_offisiell',positional_accuracy_m=None,source_observation_date=None,retrieved='2026-10-28',reviewed='2026-10-28',reviewer='AI-assistent; ikke uavhengig fagkontroll',needs_orthophoto_review=True,inside_municipality=inside,area_m2=round(gu.area),source_image=f"images/{d['image']}.png",image_metadata=f"images/{d['image']}.json",sources=[m['url']]+d['sources']+(['https://www.openstreetmap.org/'+d['osm_id']] if d['osm_id'] else []),attribution='Kartgrunnlag © Kartverket; supplerende kandidater/navn © OpenStreetMap-bidragsytere (ODbL)',note=('Havnebruk støttet av kart og tilleggskilde; geometrien er et manuelt forslag.' if d['status']=='kart_og_kilde' else 'Bryggegruppe synlig i kart; klassifisering, navn/operatør og avgrensning må avklares.'))
    if d['harbour_id']=='K05': props['note']='Båtplasser ved Thorrud er dokumentert av tilbyder. Kobling av den enkelte bryggegruppe til operatør og faktisk havneavgrensning er ikke bekreftet.'
    features.append(feat(props,g));geoms.append(g)
    checks.append(dict(id=d['id'],valid=g.is_valid,closed=g.exterior.coords[0]==g.exterior.coords[-1],counterclockwise=g.exterior.is_ccw,inside_municipality=inside,area_m2=round(gu.area)))
    if not inside: raise ValueError(('Outside municipality',d['id']))
overlaps=[]
for i,a in enumerate(geoms):
 for j in range(i):
    area=transform(to_utm.transform,a.intersection(geoms[j])).area
    if area>1: overlaps.append(dict(a=features[i]['properties']['id'],b=features[j]['properties']['id'],area_m2=round(area,2)))
save('bathavner-alle-forslag.geojson',fc(features))
save('bathavner-kart-og-kilde.geojson',fc([f for f in features if f['properties']['status']=='kart_og_kilde']))
save('bathavner-ma-avklares.geojson',fc([f for f in features if f['properties']['status']=='ma_avklares']))
unresolved=[
 feat(dict(id='U01',name='Eidsfoss / Kølabånn',status='batplasser_kildebekreftet_geometri_uavklart',point_role='omtrentlig_lokaliseringspunkt_ikke_havnegrense',reason='Lokal kilde bekrefter småbåtplasser. Kartet viser kai og få brygger, men gir ikke sikker bassenggrense.',sources=['https://visiteidsfoss.no/om-eidsfoss/aktorer/foreningen-eikern-dampskipselskap/'],source_image='images/kolabann-detail.png'),Point(10.0372,59.5956)),
 feat(dict(id='U02',name='Rydningen Småbåtforening',status='forening_bekreftet_havn_ikke_lokalisert',point_role=None,reason='Enhetsregisteret oppgir drift og vedlikehold av båtbrygge. Forretningsadressen er ikke brukt som havnelokasjon. Kan overlappe annet anlegg; telles ikke som egen etablert havn.',sources=['https://data.brreg.no/enhetsregisteret/api/enheter/920720714']),None),
 feat(dict(id='U03',name='Eikernveien Camping',status='undersokelsespunkt_ikke_bekreftet_bathavn',point_role='omtrentlig_campinglokasjon_ikke_havnelokasjon',reason='Camping ved innsjøen er dokumentert. Ikke tilstrekkelig grunnlag til å klassifisere egen småbåthavn.',sources=['https://visiteidsfoss.no/spisesteder/thorrud-camping/','https://www.norcamp.de/nb/norge/eikernveien-camping.969.1.html']),Point(10.0045537,59.6227444)),
 feat(dict(id='P01',name='Langøya – planlagt gjestebåthavn',status='planforslag_ikke_telt_som_eksisterende',point_role=None,reason='Planinitiativ datert 12.01.2026 beskriver planlagt anlegg. Ikke behandlet som eksisterende småbåthavn.',sources=['https://holmestrand.kommune.no/_f/p1/i999d3687-7c6b-4435-84ca-126fb527b16a/planinitiativ_langoya_v2-12012026.pdf'],source_image='images/langoya.png'),None)
]
save('oppfolgingspunkter.geojson',fc(unresolved))
grid=[]
for s in json.loads((ROOT/'scan-maps.json').read_text()):
    g=transform(to_geo.transform,box(*s['bbox'])).intersection(boundary)
    props=dict(id=s['id'],status='visuelt_gjennomgatt_topografisk_kart',image='images/'+s['id']+'.png',nominal_map_pixel_size_m=2,orthophoto_review=False,screening_resolution='oversiktsgjennomgang; detaljer undersøkt for kandidater',water_selection='Vannfargemaske i 8 m/piksel oversiktskart; minst 20 vannpiksler innen kommunen per 4 x 4 km rute',water_area_estimate_m2=s['water_area_estimate_m2'])
    grid.append(feat(props,g))
save('dekningsruter.geojson',fc(grid))
coverage=unary_union([shape(f['geometry']) for f in grid])
qa=dict(date='2026-10-28',polygons=len(features),harbour_groups=len({f['properties']['harbour_id'] for f in features}),source_supported_polygons=sum(f['properties']['status']=='kart_og_kilde' for f in features),source_supported_groups=len({f['properties']['harbour_id'] for f in features if f['properties']['status']=='kart_og_kilde'}),uncertain_polygons=sum(f['properties']['status']=='ma_avklares' for f in features),uncertain_groups=len({f['properties']['harbour_id'] for f in features if f['properties']['status']=='ma_avklares'}),scan_tiles=len(grid),checks=checks,overlaps=overlaps,all_polygons_inside_scan_coverage=all(coverage.covers(g) for g in geoms),complete_inventory=False,completeness_and_recall_measured=False,orthophoto_access='ikke tilgjengelig: Norge i bilder krever GeoID/token og avtalt tilgang',imagery_acquisition_dates_known=False,osm_query='8 lokale OSM API-kartuttrekk; nasjonal/kommunevid Overpass-spørring feilet. Seks unike leisure=marina-objekter i de hentede uttrekkene.')
save('kvalitetskontroll.json',qa)
with (ROOT/'havneoversikt.csv').open('w',newline='') as f:
    fields=['id','harbour_id','name','status','area_m2','inside_municipality','source_image'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for a in features:w.writerow({k:a['properties'][k] for k in fields})
print(json.dumps({k:v for k,v in qa.items() if k not in ['checks']},ensure_ascii=False,indent=2))

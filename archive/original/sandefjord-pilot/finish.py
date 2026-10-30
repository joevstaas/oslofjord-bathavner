import json,csv,datetime,sys,collections,hashlib
from pathlib import Path
P=Path(__file__).parent;O=P.parent/'oslofjord-kartlegging';sys.path.insert(0,str(P/'deps'));sys.path.insert(0,str(P))
from shapely.geometry import shape,Point,box
from shapely.ops import transform,unary_union
from pyproj import Transformer
from digitize import rows,municipal,SERVICE,REPORT
F=Transformer.from_crs(4326,25833,always_xy=True).transform;B=Transformer.from_crs(25833,4326,always_xy=True).transform
now=datetime.datetime.now(datetime.timezone.utc);stamp=now.isoformat(timespec='seconds').replace('+00:00','Z');start=datetime.datetime.fromisoformat('2026-10-29T14:54:46+00:00');elapsed=int((now-start).total_seconds());date='2026-10-29'
fc=json.loads((P/'sandefjord-bathavner.geojson').read_text());fs=fc['features'];boundary=unary_union([transform(F,shape(f['geometry'])) for f in json.loads((P/'kommunegrense.geojson').read_text())['features']]);geoms=[transform(F,shape(f['geometry'])) for f in fs]
assert len(fs)==67 and len({f['properties']['harbour_id'] for f in fs})==65
assert len({f['properties']['id'] for f in fs})==len(fs)
assert all(g.is_valid and boundary.buffer(.01).covers(g) and g.area>0 for g in geoms)
assert all(geoms[i].intersection(geoms[j]).area<1 for i in range(len(fs)) for j in range(i+1,len(fs)))
# Every municipal OBJECTID is explicitly routed to the final feature(s), including
# the three additional operator names in the one physical harbour of Roabukta.
def ids(n):return [f['properties']['id'] for f in fs if n in f['properties']['source_register_members']]
ledger=[]
for n,m in municipal.items():
 out=ids(n);assert out,n;p=m['properties'];matches=[f for f in fs if f['properties']['id'] in out];status='inkludert_usikker_kandidat' if any(f['properties']['classification']=='mulig_smabathavn' for f in matches) else ('inkludert_i_felles_fysisk_havneomrade' if n in [8,24,35,39] else 'inkludert')
 ledger.append(dict(candidate_id=f'MUN-{n:02d}',name=p['Navn'],source=SERVICE,source_objectid=n,source_label=p['Nr'],coordinate_source='GeoJSON geometry; x/y attributes not trusted',longitude=m['geometry']['coordinates'][0],latitude=m['geometry']['coordinates'][1],decision=status,feature_ids=out,reason='Kommunalt kartfestet og dokumentert anlegg; bilde kontrollert. '+('Fire kildenavn i samme fysiske område; operatørgrenser ikke kartlagt.' if n in [8,24,35,39] else matches[0]['properties']['note']),reviewed_date=date))
# Manually reconciled OSM identities after reviewing the imagery. Distances alone
# were only search hints; generic points remain approximate and are not counted twice.
osm_match={'node/13432037501':20,'way/563127798':38,'way/1218298959':13,'way/1218065128':29,'node/2088640421':'EXT-FRAMNES-NORD','way/1218322415':30,'node/5107482938':14,'way/1218301840':'EXT-HUVIK','node/13431173101':22,'way/1079317965':5,'way/1218866789':17,'node/5107367932':8,'node/5107367934':4,'node/5107367935':49,'node/5107482197':28,'node/5107482943':36,'node/5107482944':34,'node/5107482945':51,'node/5107482946':1,'way/1079317893':3,'node/13431173001':21,'way/1219097028':18}
for q in json.loads((P/'osm-candidates.json').read_text()):
 osmid=q['osm_id'];target=osm_match[osmid];out=ids(target) if isinstance(target,int) else [f['properties']['id'] for f in fs if f['properties']['candidate_id']==target];assert out
 ledger.append(dict(candidate_id='OSM-'+osmid,name=q['name'],source='https://www.openstreetmap.org/'+osmid,source_objectid=None,source_label=None,coordinate_source='OSM node or mean way vertex position; approximate',longitude=q['lon'],latitude=q['lat'],decision='knyttet_til_allerede_registrert_anlegg',feature_ids=out,reason='Kandidat kontrollert mot kommunal kilde og/eller bilde; ikke talt som ekstra anlegg. Generiske OSM-punkter kan være upresise og er ikke brukt som havnegrenser.',reviewed_date=date))
 for f in fs:
  if f['properties']['id'] in out:
   pp=f['properties'];pp['osm_ids']=list(dict.fromkeys(pp['osm_ids']+[osmid]));pp['sources']=list(dict.fromkeys(pp['sources']+['https://www.openstreetmap.org/'+osmid]))
for key in ['EXT-HUVIK','EXT-FRAMNES-NORD']:
 matches=[f for f in fs if f['properties']['candidate_id']==key];q=matches[0]['properties'];ledger.append(dict(candidate_id=key,name=q['name'],source=q['sources'][0],source_objectid=None,source_label=None,coordinate_source='Georeferenced imagery / verified operator site',longitude=q['longitude'],latitude=q['latitude'],decision='inkludert_usikker_kandidat' if q['classification']=='mulig_smabathavn' else 'inkludert',feature_ids=[x['properties']['id'] for x in matches],reason=q['note'],reviewed_date=date))
# Explicit extra non-harbour decisions. Isolated private piers are also covered
# by sector logs; the list is not a census of every private landing stage.
for cid,name,image,px,why in [
 ('EX-NATHOLMEN-8','Natholmen – lite nordre åtteplassers anlegg','p56',(304,252),'Rapport side 75 omtaler et separat anlegg med åtte plasser. Ikke dokumentert som egen felles småbåthavn etter unntaket; under terskelen og ikke lagt inn som ekstra havn.'),
 ('EX-FOLEHAVNA','Folehavna – spredte private pirer','folehavna',(390,290),'Detaljbildet viser enkeltpirer og naturvik; ikke sammenhengende fellesanlegg med minst ti tydelige båtplasser.'),
 ('EX-VORA','Vøra-området – strand og private brygger','vora',(65,230),'Utsnittets strand og spredte private landfester gir ikke grunnlag for en ny felles småbåthavn. Båter på opplagsplass på land er ikke havn.'),
 ('EX-FRAMNES-SERVICE','Framnæs – nordre rene service-/industrikaier','framnes-nord',(628,194),'Rene kai- og serviceområder er utelatt; fingerbryggene lenger sør er en egen usikker kandidat.'),
 ]:
 m=json.loads((P/'images'/f'{image}.json').read_text());a,b,c,d=m['bbox'];scale=600 if image.startswith('p') else 1000;x=a+px[0]/scale*(c-a);y=d-px[1]/scale*(d-b);lon,lat=B(x,y);ledger.append(dict(candidate_id=cid,name=name,source=REPORT if image=='p56' else m['url'],source_objectid=None,source_label=None,coordinate_source='Georeferenced imagery; indicative candidate position',longitude=lon,latitude=lat,decision='utelatt',feature_ids=[],reason=why,reviewed_date=date))
(P/'candidate-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
with (P/'candidate-ledger.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(ledger[0]),delimiter=';');w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()} for r in ledger)
# Record the final checks and the exact file hashes, without claiming imagery dates.
for f in fs:f['properties']['attribution']='Sandefjord kommune (havneoversikt og utredning); © Kartverket; imagery: Esri, Vantor, Earthstar Geographics and the GIS User Community; OSM © OpenStreetMap contributors (ODbL)'
fc['description']='Foreløpig kommuneleveranse med kandidatlogg: kommunal utredning og kartlag, topografisk screening og Esri-bildekontroll. Lokale bildedatoer, nøyaktighet, fullstendighet og dagens drift er ikke verifisert. Fysiske havneområder, ikke juridiske drifts-/eiendomsgrenser. Avventer godkjenning.'
(P/'sandefjord-bathavner.geojson').write_text(json.dumps(fc,ensure_ascii=False,indent=2)+'\n')
with (P/'sandefjord-metadata.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(fs[0]['properties']),delimiter=';');w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in q['properties'].items()} for q in fs)
meta=[]
for f in (P/'images').glob('*.json'):
 try:
  q=json.loads(f.read_text())
  if 'source' in q and 'bbox' in q:meta.append(q)
 except ValueError:pass
coverage=dict(municipality='Sandefjord',municipality_code='3907',method_version='1.1',schema_version='1.1',municipal_register_candidates=66,osm_candidates_reviewed=22,additional_candidates_included=2,explicit_extra_exclusions=4,candidate_ledger_rows=len(ledger),topographic_scan_tiles_reviewed=24,coastal_imagery_tiles_reviewed=22,detailed_municipal_images_reviewed=66,extra_detail_images_downloaded=4,source_images_by_provider=dict(collections.Counter(m['source'] for m in meta)),downloaded_image_payload_bytes=sum(m.get('bytes',0) for m in meta),all_municipal_objectids_reconciled=True,all_exported_polygons_visually_reviewed=True,qa_sheets=[f'images/qa-{i}.jpg' for i in range(8)],validation='67 valid positive-area polygons, 65 unique harbour IDs; within municipality; unique feature IDs; no overlap >=1 m2',limitations=['Lokale opptaksdatoer og oppgitt posisjonsnøyaktighet er ukjente; dagens drift er ikke generelt verifisert.','Kapasitet kommer normalt fra det kommunale kartlaget; referanseår er ukjent og tallene kan avvike fra rapport 2022 og nettsider 2026. Ingen automatisk summering av overlappende driftsnavn.','Roabukta er ett fysisk havneområde med fire kildenavn; interne operatørgrenser er ikke kartlagt. Hesteskoen/MiljøMarina og Sandefjord gjestehavn/La Scala er heller ikke dobbelttelt.','19 polygoner har usikker avgrensning. Historiske bøye-/wireplasser kan strekke seg utenfor synlige brygger.','24 topografiske sektorer og 22 brede bildeutsnitt gir systematisk screening av den bebodde kystsonen og øyer i disse utsnittene. Grovkontroll av Goksjø er inkludert; øvrig innland og hele det sørlige sjøterritoriet har ikke heldekkende detaljbildekontroll.','Ikke en uttømmende individuell registrering av hver privat brygge: 66 kommunale kandidater, 22 OSM-kandidater og eksplisitte tillegg har egne vurderinger; spredte private enkeltbrygger er også vurdert på sektornivå. Ingen fullstendighetsgaranti.','Det ekstra bildet varnes var feilsentrert og teller ikke som detaljkontroll av Vårnes. Kommunens badeplasskilde omtaler badebrygge; en slik brygge alene kvalifiserer ikke.'])
(P/'coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')
sectors=[]
for spec in json.loads((P/'scan-order.json').read_text()):
 bbox=spec['bbox'];near=[]
 for n,q in municipal.items():
  x,y=F(*q['geometry']['coordinates'])
  if box(*bbox).covers(Point(x,y)):near.append(f'MUN-{n:02d}')
 sectors.append(dict(tile=spec['id'],bbox_25833=bbox,topographic_review='gjennomgått',imagery_tile='a-'+spec['id'] if (P/'images'/('a-'+spec['id']+'.jpg')).exists() else None,registered_candidates=near,private_piers='Spredte enkeltbrygger langs bolig-/hyttekyst er ikke slått sammen til havn bare på grunn av nærhet. Mindre udokumenterte anlegg kan være oversett.',review_date=date))
(P/'sector-review.json').write_text(json.dumps(sectors,ensure_ascii=False,indent=2)+'\n')
(P/'source-notes.json').write_text(json.dumps({'retrieved_date':date,'sources':[{'url':REPORT,'type':'kommunal PDF','reference':'22.12.2022, vedtatt 28.02.2023','finding':'66 navngitte anlegg; rapporten tar selv forbehold om utelatte private anlegg. Planarealer er ikke fysiske havnegrenser.'},{'url':SERVICE,'type':'kommunalt ArcGIS-punktlag','finding':'66 objekter. Bruk geometry, ikke x/y-feltene: noen koordinatattributter og Nr-etiketter er feil/duplisert.'},{'url':'https://www.huvik.no/b%C3%A5tplasser','type':'operatør','finding':'32 utleieplasser oppgitt ved Framnæsveien 3 B. Separat fra kommunens Huvik-kandidat.'},{'url':'https://www.framnes-maritime.no/','type':'operatør','finding':'Service-/løfteanlegg, samt samarbeid om båtplasser med Framnæs Båthavn AS i sør. Fast bruk av nordre fingerbrygger er ikke avklart.'}]},ensure_ascii=False,indent=2)+'\n')
timing=dict(started_utc=start.isoformat().replace('+00:00','Z'),finished_utc=stamp,elapsed_wall_seconds=elapsed,elapsed_wall_minutes=round(elapsed/60,1),measurement='Veggklokketid inkludert søk, nedlasting, feilsøking, kildekontroll, bildeanalyse, geometriarbeid og dokumentasjon. Aktiv beregningstid ikke isolert.',actual_input_tokens=None,actual_output_tokens=None,actual_billed_cost=None,cost_note='Sesjonen eksponerer ikke tokenregnskap eller fakturering. Faktisk kostnad per kommune kan ikke beregnes forsvarlig fra antall bilder eller minutter alene. Ingen betalte datasett kjøpt.',workload=dict(source_images=len(meta),source_image_bytes=coverage['downloaded_image_payload_bytes'],municipal_candidates=66,exported_polygons=67))
(P/'timing.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2)+'\n')
s=json.loads((O/'status.json').read_text());r=next(x for x in s['municipalities'] if x['code']=='3907');r.update(status='til_godkjenning',revision=1,method_version='1.1',schema_version='1.1',finished_utc=stamp,elapsed_wall_seconds=elapsed,result=str(P/'sandefjord-bathavner.geojson'),metadata=str(P/'sandefjord-metadata.csv'),polygons=67,harbours=65,possible_harbours=2,uncertain_geometries=19,candidate_ledger=str(P/'candidate-ledger.json'));s.update(updated_utc=stamp,next_municipality_started=False);(O/'status.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
assert len(json.loads((O/'oslofjorden-bathavner-samlet.geojson').read_text())['features'])==85
with (P/'sandefjord-metadata.csv').open(encoding='utf-8-sig') as f:rs=list(csv.DictReader(f,delimiter=';'));assert len(rs)==67 and {r['id'] for r in rs}=={r['properties']['id'] for r in fs}
print(json.dumps(dict(polygons=67,harbours=65,possible=2,uncertain_geometries=19,ledger_rows=len(ledger),source_images=len(meta),elapsed_wall_minutes=timing['elapsed_wall_minutes'],approved_combined_unchanged=85),ensure_ascii=False))

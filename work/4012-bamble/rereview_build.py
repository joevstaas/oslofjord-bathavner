"""Bygg Bamble rev-02 fra uendret rev-01 og eksplisitt detaljkontroll. Samledata og nettsted røres ikke."""
import json,csv,copy,runpy,hashlib,datetime,time,shutil,warnings
from pathlib import Path
from PIL import Image,ImageDraw
from pyproj import Transformer
from shapely.geometry import Polygon,shape,mapping,box
from shapely.geometry.polygon import orient
from shapely.ops import transform
warnings.filterwarnings('ignore')
P=Path(__file__).parent;R=P.parents[1];OLD=R/'data/kommuner/4012-bamble/rev-01';O=OLD.parent/'rev-02';O.mkdir(exist_ok=True)
assert not (O/'approval.json').exists(),'Godkjent revisjon må ikke overskrives.'
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=1)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def csvwrite(p,rows):
 with p.open('w',encoding='utf-8-sig',newline='') as h:
  keys=list(dict.fromkeys(k for row in rows for k in row));w=csv.DictWriter(h,fieldnames=keys,delimiter=';',lineterminator='\n');w.writeheader()
  w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in row.items()} for row in rows)
session=P/'rereview-session.json'
if not session.exists():
 files=list(OLD.glob('*'))+list((R/'data/samlet').glob('*'))+[f for f in (R/'site').rglob('*') if f.is_file()]
 write(session,dict(started_utc=datetime.datetime.fromtimestamp((P/'detail_sweep.py').stat().st_birthtime,datetime.timezone.utc).isoformat(),started_unix=(P/'detail_sweep.py').stat().st_birthtime,timing_scope='Fra opprettelse av detaljpanelverktøy. Innledende fil- og bildegjennomgang før dette er ikke målt.',protected_sha256={str(f.relative_to(R)):sha(f) for f in files if f.is_file()}))
S=read(session)
for fn,digest in S['protected_sha256'].items():assert sha(R/fn)==digest,fn
T=Transformer.from_crs(4326,25833,always_xy=True).transform;B=Transformer.from_crs(25833,4326,always_xy=True).transform
boundary=transform(T,shape(read(OLD/'kommunegrense.geojson')['features'][0]['geometry']))
D=runpy.run_path(str(P/'rereview_decisions.py'))['D'];frames={v['cid']:v for v in read(P/'detail-sweep-index.json')};names=read(P/'raw/rereview-stedsnavn.json')
features=copy.deepcopy(read(OLD/'bathavner.geojson')['features']);old_features=copy.deepcopy(features)
for f in features:f['properties'].update(revision=2,detail_review_id=None,digitisation_frame=None)
ledger=copy.deepcopy(read(OLD/'candidate-ledger.json'));new_changes=[];next_id=39;panels=[]
images=[(f,read(f.with_suffix('.json'))) for f in sorted((P/'images').glob('coast-*.jpg'))]
for cid,d in D.items():
 fr=frames[cid];a,b,c,e=fr['review_bbox'];row=dict(candidate_id=cid,kind='bildefunn_detaljgjennomgang',center_25833=[(a+c)/2,(b+e)/2],osm_ids=[],osm_marks=[],image_id=fr['image_id'],review_bbox=fr['review_bbox'],decision='utelatt',reason=d.get('reason'),note='',feature_ids=[],reviewed_date='2026-10-31',detail_review_id=cid)
 if d['action']=='include':
  hid=f'4012-H{next_id:02}';next_id+=1;alias=d.get('previous_candidate_id');ident=alias or cid
  for part_no,part in enumerate(d['parts'],1):
   raw=Polygon([(a+x/800*(c-a),e-y/800*(e-b)) for x,y in part['pixels']]);assert raw.is_valid,cid
   g=raw.intersection(boundary);assert g.geom_type=='Polygon' and g.area>25,cid
   g=orient(g,sign=1);geo=transform(B,g);q=geo.representative_point()
   matches=[(f,m) for f,m in images if box(*m['bbox']).covers(raw)]
   assert matches,(cid,'Ingen enkelt kildeflis dekker hele omrisset')
   img,m=matches[0];p=copy.deepcopy(old_features[0]['properties'])
   for k in p:
    if k.startswith('berth_count_'):p[k]=None
   p.update(id=hid+f'-B{part_no:02}',harbour_id=hid,candidate_id=ident,name=d['name'],name_is_descriptive=True,classification=d['classification'],classification_basis=d['basis'],revision=2,area_m2=round(g.area,1),longitude=round(q.x,7),latitude=round(q.y,7),sources=[names[cid]['url'],m.get('image_url') or m['url']],osm_ids=[],imagery_source=m['source'],imagery_retrieved_date=m['retrieved_date'],source_observation_date=None,image_resolution_m_per_pixel=round((m['bbox'][2]-m['bbox'][0])/m['width'],3),needs_orthophoto_review=True,note=d['note'],geometry_status='usikker_avgrensning',water_body='brakkvann_elveos' if cid=='N16' else 'saltvann_eller_brakkvann',municipality_clipped=raw.difference(boundary).area>.01,image_id=img.stem,image_sha256=m['sha256'],detail_review_id=cid,digitisation_frame=cid)
   f=dict(type='Feature',properties=p,geometry=mapping(geo));features.append(f)
   row.update(candidate_id=ident,decision='inkludert_'+d['classification'],reason=d['basis'],note=d['note'],feature_ids=row['feature_ids']+[p['id']],image_id=img.stem)
   new_changes.append(dict(id=p['id'],harbour_id=hid,candidate_id=ident,detail_review_id=cid,change='lagt_til',previous_decision='utelatt' if alias else 'ikke_registrert',classification=p['classification'],name=p['name'],reason=d['basis']))
   # Overlegg i samme georefererte panel som ble digitalisert.
   im=Image.open(P/'qa'/f'{cid}-clean.jpg').copy();dr=ImageDraw.Draw(im)
   dr.line([((x-a)/(c-a)*800,(e-y)/(e-b)*800) for x,y in g.exterior.coords],fill='red',width=3)
   pn=Image.new('RGB',(800,825),'white');pn.paste(im,(0,25));ImageDraw.Draw(pn).text((4,4),p['id']+' '+p['name'],fill='black');panels.append(pn)
 if d.get('previous_candidate_id'):
  index=next(i for i,x in enumerate(ledger) if x['candidate_id']==d['previous_candidate_id']);row['previous_decision']=ledger[index]['decision'];ledger[index]=row
 else:ledger.append(row)
for n in range(0,len(panels),4):
 im=Image.new('RGB',(1600,1650),'white')
 for i,pn in enumerate(panels[n:n+4]):im.paste(pn,(i%2*800,i//2*825))
 im.save(P/'qa'/f'rev02-additions-{n//4:02}.jpg',quality=95)
# S015 beholdes som åpen identitetsavklaring, med stedfestet kandidat.
for row in ledger:
 if row['candidate_id']=='S015':
  row.update(reason='Kyststien – trekantet molobasseng: N01 ved Kruksdalen/Krukodden er funnet og inkludert som 4012-H39-B01. Formen passer beskrivelsen, men identitet med brukerens opprinnelige skjermbilde er ikke bekreftet.',note='Se detail-review.json / N01.',feature_ids=['4012-H39-B01'])
summary=dict(polygons=len(features),harbours=len({f['properties']['harbour_id'] for f in features}),possible_harbours=len({f['properties']['harbour_id'] for f in features if f['properties']['classification']=='mulig_smabathavn'}),uncertain_geometries=sum(f['properties']['needs_orthophoto_review'] for f in features),new_harbours=len({v['harbour_id'] for v in new_changes}),new_polygons=len(new_changes),previous_polygons=len(old_features),new_detail_candidates=len(D),previously_excluded_now_included=sum(bool(d.get('previous_candidate_id')) for d in D.values()),published_capacity_harbours=sum(f['properties']['berth_count_published'] is not None for f in features))
write(O/'bathavner.geojson',dict(type='FeatureCollection',name='Bamble – småbåthavner rev-02 til godkjenning',description='Detaljgjennomgang etter brukerinnspill. Kartleggingsforslag, ikke juridiske grenser. Bildedato, nøyaktighet og dagens drift er ikke verifisert. Innlandet er ikke systematisk kartlagt.',method_version='1.2',schema_version='1.1',features=features))
csvwrite(O/'metadata.csv',[f['properties'] for f in features]);write(O/'candidate-ledger.json',ledger);csvwrite(O/'candidate-ledger.csv',ledger);write(O/'summary.json',summary);csvwrite(O/'changes.csv',new_changes)
write(O/'detail-review.json',[dict(**frames[cid],decision=D[cid],feature_ids=[f['properties']['id'] for f in features if f['properties'].get('detail_review_id')==cid]) for cid in D])
write(O/'digitisation.json',dict(previous_revision='rev-01',previous_digitisation='rev-01/digitisation.json',new_decisions=D))
for name in ['kommunegrense.geojson','clusters.json','neighbour-pending.json']:
 shutil.copy2(OLD/name,O/name)
write(O/'cluster-review-index.json',read(OLD/'cluster-review-index.json')+list(frames.values()))
write(O/'source-provenance.json',read(OLD/'source-provenance.json')+[read(P/'raw/rereview-stedsnavn.provenance.json')])
write(O/'name-source-results.json',names)
shutil.copy2(P/'rereview_decisions.py',O/'decisions.py')
coverage=read(OLD/'coverage.json');coverage.update(revision=2,detail_sweep_cells=255,detail_sweep_sheets=64,detail_sweep_native_resolution_m_per_pixel=0.73,detail_sweep_completed=True,detail_sweep_review_record='sweep-review.json',detail_candidates_reviewed=len(D),additional_detail_harbours=summary['new_harbours'],independent_gap_sweep='Fullført 255 kystceller à 500 m, vist i ca. 0,73 m/px; ark 25–63 fra bevart tidligere gjennomgang, ark 0–24 fullført i denne kjøringen. Alle 12 tidligere nye funn og seks tilleggsfunn er avgjort i egne detaljpaneler.',limitations=['Ukjent opptaksdato, posisjonsnøyaktighet og dagens drift. Eksportoppløsning er ikke kildens nøyaktighet.','Skyer ved industrikysten i G024/G028/G030/G031: disse delene er ikke tilstrekkelig visuelt kontrollert; ingen negativ havnekonklusjon.','Mørkt vann, skygge og mosaikkskjøter kan skjule mindre anlegg. Fullført gjennomgang er ikke garanti for fullstendighet.','N01 passer beskrivelsen av Kyststien-bassenget, men identiteten med brukerens originalskjermbilde er ikke bekreftet.','Innlandet er ikke systematisk gjennomgått.','Driftsgrenser ved Valle, Stoa og nye anlegg er ikke dokumentert.','Kommunegrensen er generalisert; kjente nabofunn beholdt.','Originalbilder beholdes lokalt; ny henting kan gi en annen mosaikk.'])
coverage['final_outline_qa']=[f'work/4012-bamble/qa/rev02-additions-{n:02}.jpg' for n in range(4)]
coverage['preserved_outline_qa']='Uendrede 43 omriss fra rev-01; tidligere visuelt kontrollert mot kildebildene.'
write(O/'coverage.json',coverage)
prior=read(P/'sweep-notes.json');write(O/'sweep-review.json',dict(cells=read(P/'sweep-index.json'),sheets_previously_reviewed=prior['sheets_reviewed'],previous_review_evidence='Bevart work/4012-bamble/sweep-notes.json; 12 funn tatt til eksplisitt beslutning i detail-review.json.',sheets_completed_this_run=list(range(25)),all_sheets_reviewed=list(range(64)),outcomes_this_run=[dict(sheets=[0,1,2],outcome='Spredte privatbrygger og naturkyst; ingen nye kandidater.'),dict(sheets=[3],outcome='Herreelva revurdert som N16; industrikai i resten.'),dict(sheets=[4,5,6,7,8],outcome='Industrikyst; skyer i G024/G028/G030/G031 er kontrollhull.'),dict(sheets=[9],outcome='Eksisterende Isdammen; nabokaier uten nye sikre båtplassanlegg.'),dict(sheets=[10,11],outcome='C013 revurdert som N13; ikke under ti plasser.'),dict(sheets=[12,13],outcome='Eksisterende flytebrygge og spredte privatbrygger.'),dict(sheets=[14,15],outcome='C029 og M05 revurdert som N14/N15.'),dict(sheets=[16,17,18,19,20,21,22,23,24],outcome='Eksisterende havner, separate privatbrygger og naturkyst; C039/Vaterlands gate fortsatt separate landfester.' )],detail_decisions='detail-review.json',limitations=coverage['limitations']))
questions=read(OLD/'open-questions.json')
questions[2].update(place=', '.join(f['properties']['name'] for f in features if f['properties']['classification']=='mulig_smabathavn'),need='Bekreft faste båtplasser og felles drift. De mulige anleggene beholdes som usikre; Vinjestranda H11 er småbåthavn etter tidligere brukerinnspill.')
questions.extend([dict(id='Q06',place='Kruksdalen / Krukodden (N01)',need='Avklar om H39 er brukerens tidligere viste trekantede Kyststien-basseng. Stedfestet kandidat inkludert; identitet ikke bekreftet.',polygon_exported=True),dict(id='Q07',place='Industrikysten G024/G028/G030/G031',need='Alternativt skyfritt bilde kreves for de skjulte delene av kysten. Ikke tilstrekkelig kontrollert i Esri-mosaikken.',polygon_exported=False)])
write(O/'open-questions.json',questions)
print(json.dumps(summary,ensure_ascii=False))

"""Bygg avventende leveranse fra eksplisitte, manuelle omriss. Godkjente data endres ikke."""
import json,csv,runpy,warnings,collections
from pathlib import Path
from shapely.geometry import shape,Polygon,mapping
from shapely.geometry.polygon import orient
from shapely.ops import transform
from pyproj import Transformer
warnings.filterwarnings('ignore');P=Path(__file__).parent;R=P.parents[1];O=R/'data/kommuner/4001-porsgrunn/rev-01';assert not (O/'approval.json').exists();O.mkdir(parents=True,exist_ok=True)
T=Transformer.from_crs(4326,25833,always_xy=True).transform;BACK=Transformer.from_crs(25833,4326,always_xy=True).transform
boundary=transform(T,shape(json.loads((P/'kommunegrense.geojson').read_text())['features'][0]['geometry']))
ns=runpy.run_path(str(P/'decisions.py'));D=ns['D'];frames={x['cid']:x for x in json.loads((P/'cluster-review-index.json').read_text())};C={c['cid']:c for c in json.loads((P/'clusters.json').read_text())};IC={c['cid']:c for c in json.loads((P/'image-candidates.json').read_text())};assert set(C)|set(IC)<=set(D)
feats=[];groups={};parts=collections.Counter()
for cid,d in D.items():
 if d['action']!='include':continue
 hid=groups.setdefault(d['group'],f'4001-H{len(groups)+1:02}');osm=[p['id'] for p in C.get(cid,{}).get('piers',[])]
 for k,part in enumerate(d['parts']):
  r=frames[part['frame']];a,b,c,e=r['review_bbox'];m=json.loads((P/'images'/(r['image_id']+'.json')).read_text());W=r['review_width'];H=r['review_height'];raw=Polygon([(a+x/W*(c-a),e-y/H*(e-b)) for x,y in part['pixels']]);assert raw.is_valid,(cid,k);g=raw.intersection(boundary);assert g.geom_type=='Polygon' and g.area>10,(cid,k,g.geom_type,g.area);g=orient(g,sign=1);geo=transform(BACK,g);q=geo.representative_point();cap=None;cl=d['classification'];parts[hid]+=1
  components=[]
  if k==0 and cid=='C006':
   components=[dict(source=d['sources'][1],reference_period='juni 2019, ferdigstilt april 2019',capacity=170,approximate=True,scope='Hele Herøya Motorbåtforenings nye anlegg, ikke polygonet',additive=False,current_capacity_verified=False)]
  if k==0 and cid=='M01D':
   components=[dict(source=d['sources'][0],reference_period='udatert reiselivsside lest 2026-10-31',capacity=25,scope='Hele gjesteanlegget; maks ett døgn. Ikke kapasitet per pir',additive=False,current_capacity_verified=False)]
  if k==0 and cid=='C036':
   components=[dict(source=d['sources'][0],reference_period='udatert foreningspresentasjon lest 2026-10-31',capacity=460,scope='Hele Brevik Båtforening, ikke bare Dalsbukta eller dette polygonet',additive=False,current_capacity_verified=False)]
  if k==0 and cid=='C061':
   components=[dict(source=d['sources'][2],reference_period='årsmøtedokument med utleieopplysninger 2025',capacity_text='Nytt bryggeanlegg: 45 x 3 m, 31 x 3,5 m, 23 x 4 m, 2 x 4,5 m og 8 x 5 m. Gammel betongbrygge: 14, jollebrygge: 15, gangbru: 3. Foreningseide 16 flytebryggeplasser er en eierskapsdel; jolle-/bøyeplasser nevnes igjen i utleieavsnitt.',scope='Ulike deler og eierskap, ikke sikkert knyttet til hvert polygon',additive=False,current_capacity_verified=False)]

  p=dict(id=hid+f'-B{parts[hid]:02}',harbour_id=hid,candidate_id=cid,name=d['name'],name_is_descriptive=not bool(d['sources']) or cid in ['M01BV','M01BO','C011','M11'],municipality='Porsgrunn',municipality_code='4001',classification=cl,classification_basis=d['basis'],approval_status='til_godkjenning',approved_utc=None,revision=1,method_version='1.2',schema_version='1.1',geometry_role='brygger_batplasser_og_mellomliggende_sjo',method='manuell_digitalisering_georeferert_flybilde_med_osm_og_kildekontroll',area_m2=round(g.area,1),area_crs='EPSG:25833',longitude=round(q.x,7),latitude=round(q.y,7),sources=list(dict.fromkeys(d['sources']+['https://www.openstreetmap.org/'+v for v in osm]+[m['url']])),osm_ids=osm,imagery_source=m['source'],imagery_retrieved_date=m['retrieved_date'],source_observation_date=None,image_resolution_m_per_pixel=None,processed_pixel_size_m=round((m['bbox'][2]-m['bbox'][0])/m['width'],3),imagery_processing=m.get('processing'),source_ground_sampling_distance_m=None,estimated_accuracy_m=None,needs_orthophoto_review=d['unc'],needs_dated_imagery_review=True,current_operation_verified=False,reviewed_date='2026-10-31',berth_count_published=cap,berth_count_source=d['sources'][0] if cap else None,berth_count_approximate=None,berth_count_scope='Hele anleggsgruppen, ikke dette delpolygonet. Ikke summer mellom polygoner.' if cap else None,berth_count_reference_period=None,source_register_objectid=None,source_register_number=None,source_register_members=[],capacity_components=components,municipality_clipped=raw.difference(boundary).area>.01,cross_municipality_group_id=None,attribution='© Kartverket; © OpenStreetMap contributors (ODbL); imagery: Esri, Vantor, Earthstar Geographics and the GIS User Community; Porsgrunn kommune, Telemarkskanalen og kildeangitte operatører',note=d['note'],geometry_status='usikker_avgrensning' if d['unc'] else 'forelopig_avgrensning',water_body=d['water'],image_id=r['image_id'],image_sha256=m['sha256'],digitisation_frame=part['frame'])
  feats.append(dict(type='Feature',properties=p,geometry=mapping(geo)))
def write(fn,x):(O/fn).write_text(json.dumps(x,ensure_ascii=False,indent=1)+'\n')
def csvwrite(fn,rows):
 with (O/fn).open('w',encoding='utf-8-sig',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in row.items()} for row in rows)
write('bathavner.geojson',dict(type='FeatureCollection',name='Porsgrunn – småbåthavner rev-01 til godkjenning',description='Kartleggingsforslag, ikke juridiske grenser. Kysten systematisk bildesøkt; Porsgrunnselva, Sundjordkanalen og utvalgte innlandskandidater kontrollert. Innlandet ikke fullkartlagt; historisk Clarity brukt ved skyer. Ukjent bildedato, åpne avklaringer og historiske kildeopplysninger beholdt.',method_version='1.2',schema_version='1.1',features=feats));csvwrite('metadata.csv',[f['properties'] for f in feats]);write('digitisation.json',D)
L=[]
for cid,c in {**C,**IC}.items():
 d=D[cid];related=[cid]+d.get('related',[]);ids=[f['properties']['id'] for f in feats if f['properties']['candidate_id'] in related];r=frames[cid]
 L.append(dict(candidate_id=cid,kind='osm_klynge' if cid in C else 'bildefunn_eller_kontrollramme',osm_ids=[p['id'] for p in c.get('piers',[])],image_id=r['image_id'],review_bbox=r['review_bbox'],decision='inkludert_'+d['classification'] if d['action']=='include' else 'dekket_av_annen_kandidat' if d.get('related') else 'utelatt',reason=d.get('basis') or d['reason'],note=d.get('note',''),feature_ids=ids,reviewed_date='2026-10-31'))
for cid in set(D)-set(C)-set(IC):
 d=D[cid];ids=[f['properties']['id'] for f in feats if f['properties']['candidate_id']==cid]
 L.append(dict(candidate_id=cid,kind='delkandidat_fra_bildekontroll',osm_ids=[],image_id=None,review_bbox=None,decision='inkludert_'+d['classification'] if d['action']=='include' else 'utelatt',reason=d.get('basis') or d.get('reason'),note=d.get('note',''),feature_ids=ids,reviewed_date='2026-10-31'))
write('candidate-ledger.json',L);csvwrite('candidate-ledger.csv',L)
summary=dict(polygons=len(feats),harbours=len(groups),possible_harbours=len({f['properties']['harbour_id'] for f in feats if f['properties']['classification']=='mulig_smabathavn'}),uncertain_geometries=sum(f['properties']['needs_orthophoto_review'] for f in feats),osm_piers=sum(len(c['piers']) for c in C.values()),osm_clusters=len(C),image_review_frames=len(IC),published_capacity_harbours=sum(f['properties']['berth_count_published'] is not None for f in feats));write('summary.json',summary);print(summary)

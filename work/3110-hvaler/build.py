"""Bygg avventende rev-01 fra eksplisitte manuelle beslutninger. Endrer ikke samlefil/nettsted."""
import json,csv,runpy,warnings,collections
from pathlib import Path
from shapely.geometry import shape,Polygon,mapping
from shapely.geometry.polygon import orient
from shapely.ops import transform
from pyproj import Transformer
warnings.filterwarnings('ignore');P=Path(__file__).parent;R=P.parents[1];O=R/'data/kommuner/3110-hvaler/rev-01'
assert not (O/'approval.json').exists(),'Opprett ny revisjon; godkjent revisjon må ikke overskrives.'
O.mkdir(parents=True,exist_ok=True)
T=Transformer.from_crs(4326,25833,always_xy=True).transform;B=Transformer.from_crs(25833,4326,always_xy=True).transform
boundary=transform(T,shape(json.loads((P/'kommunegrense.geojson').read_text())['features'][0]['geometry']))
D=runpy.run_path(str(P/'decisions.py'))['D'];C={c['cid']:c for c in json.loads((P/'clusters.json').read_text())};frames={x['cid']:x for x in json.loads((P/'cluster-review-index.json').read_text())}
assert set(C)<=set(D),'Alle klynger skal ha eksplisitt beslutning'
feats=[];groups={};parts=collections.Counter()
for cid,d in sorted(D.items()):
 if d['action']!='include':continue
 frameid=d['frame'];r=frames[frameid];a,b,c,e=r['review_bbox'];m=json.loads((P/'images'/(r['image_id']+'.json')).read_text());W=r['review_width'];H=r['review_height']
 raw=Polygon([(a+x/W*(c-a),e-y/H*(e-b)) for x,y in d['pixels']]);assert raw.is_valid,cid
 g=raw.intersection(boundary);assert g.geom_type=='Polygon' and g.area>25,cid;g=orient(g,sign=1);geo=transform(B,g);q=geo.representative_point();hid=groups.setdefault(d['group'],f'3110-H{len(groups)+1:02}');cap=d.get('capacity');cl=d['classification'];osm=[p['id'] for p in C.get(frameid,C.get(cid[:4],{'piers':[]}))['piers']] if cid.startswith('C') else [];parts[hid]+=1
 p=dict(id=hid+f'-B{parts[hid]:02}',harbour_id=hid,candidate_id=cid,name=d['name'],name_is_descriptive=True,municipality='Hvaler',municipality_code='3110',classification=cl,classification_basis=d['basis'],approval_status='til_godkjenning',approved_utc=None,revision=1,method_version='1.2',schema_version='1.1',geometry_role='brygger_batplasser_og_mellomliggende_sjo',method='manuell_digitalisering_georeferert_flybilde_med_osm_og_kildekontroll',area_m2=round(g.area,1),area_crs='EPSG:25833',longitude=round(q.x,7),latitude=round(q.y,7),sources=list(dict.fromkeys(d['sources']+['https://www.openstreetmap.org/'+v for v in osm]+[m['url']])),osm_ids=osm,imagery_source=m['source'],imagery_retrieved_date=m['retrieved_date'],source_observation_date=None,image_resolution_m_per_pixel=round((m['bbox'][2]-m['bbox'][0])/m['width'],3),estimated_accuracy_m=None,needs_orthophoto_review=cl=='mulig_smabathavn',needs_dated_imagery_review=True,current_operation_verified=False,reviewed_date='2026-10-31',berth_count_published=cap,berth_count_source=d['sources'][0] if cap else None,berth_count_approximate=d['capacity_approximate'] if cap else None,berth_count_scope=d['capacity_scope'] if cap else None,berth_count_reference_period='ukjent_referanseperiode_nettside_lest_2026-10-31' if cap else None,source_register_objectid=None,source_register_number=None,source_register_members=[],capacity_components=d['capacity_components'],municipality_clipped=raw.difference(boundary).area>0.01,cross_municipality_group_id=None,attribution='© Kartverket; © OpenStreetMap contributors (ODbL); imagery: Esri, Vantor, Earthstar Geographics and the GIS User Community; kildeangitte operatører og organisasjoner',note=d['note'],geometry_status='usikker_avgrensning' if cl=='mulig_smabathavn' else 'forelopig_avgrensning',water_body='saltvann_eller_brakkvann',image_id=r['image_id'],image_sha256=m['sha256'])
 if d['unc']:p['needs_orthophoto_review']=True;p['geometry_status']='usikker_avgrensning'
 feats.append(dict(type='Feature',properties=p,geometry=mapping(geo)))
def write(fn,x):(O/fn).write_text(json.dumps(x,ensure_ascii=False,indent=1)+'\n')
def csvwrite(fn,rows):
 with (O/fn).open('w',encoding='utf-8-sig',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in x.items()} for x in rows)
write('bathavner.geojson',dict(type='FeatureCollection',name='Hvaler – småbåthavner rev-01 til godkjenning',description='Kartleggingsforslag, ikke juridiske grenser. Kjente usikkerheter og åpne kandidater beholdt. Bare kysten er systematisk bildesøkt; innlandet ikke fullkartlagt.',method_version='1.2',schema_version='1.1',features=feats));csvwrite('metadata.csv',[f['properties'] for f in feats])
L=[]
for cid,c in C.items():
 d=D[cid];related=[f['properties']['id'] for f in feats if D[f['properties']['candidate_id']]['frame']==cid or f['properties']['candidate_id'][:4]==cid]
 L.append(dict(candidate_id=cid,osm_ids=[p['id'] for p in c['piers']],osm_marks=c['marks'],image_id=frames[cid]['image_id'],review_bbox=frames[cid]['review_bbox'],decision='inkludert_'+d['classification'] if d['action']=='include' else 'delt_i_sjopolygoner' if d['action']=='split' else 'utelatt',reason=d.get('basis') or d['reason'],note=d.get('note',''),feature_ids=related,reviewed_date='2026-10-31'))
for cid,d in D.items():
 if not cid.startswith('G'):continue
 r=frames[d['frame']]
 L.append(dict(candidate_id=cid,osm_ids=[],osm_marks=[],image_id=r['image_id'],review_bbox=r['review_bbox'],decision='inkludert_'+d['classification'],reason=d['basis'],note=d['note'],feature_ids=[f['properties']['id'] for f in feats if f['properties']['candidate_id']==cid],reviewed_date='2026-10-31'))
for q in json.loads((P/'open-questions.json').read_text()):
 L.append(dict(candidate_id=q['id'],osm_ids=[],osm_marks=[],image_id=None,review_bbox=None,decision='aapen_kildekandidat',reason=q['place']+': '+q['need'],note='Kilder: '+' '.join(q.get('sources',[])),feature_ids=[],reviewed_date='2026-10-31'))
write('candidate-ledger.json',L);csvwrite('candidate-ledger.csv',L)
summary=dict(polygons=len(feats),harbours=len(groups),possible_harbours=len({f['properties']['harbour_id'] for f in feats if f['properties']['classification']=='mulig_smabathavn'}),uncertain_geometries=sum(f['properties']['needs_orthophoto_review'] for f in feats),osm_piers=948,osm_clusters=len(C),open_source_candidates=len(json.loads((P/'open-questions.json').read_text())),published_scalar_capacity_harbours=sum(f['properties']['berth_count_published'] is not None for f in feats))
summary['capacity_observations_harbours']=len({f['properties']['harbour_id'] for f in feats if f['properties']['capacity_components']});write('summary.json',summary);write('digitisation.json',D);print(summary)

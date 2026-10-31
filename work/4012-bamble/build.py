"""Bygg avventende rev-01 fra eksplisitte manuelle beslutninger. Endrer ikke samlefil/nettsted."""
import json,csv,runpy,warnings
from pathlib import Path
from shapely.geometry import shape,Polygon,mapping
from shapely.geometry.polygon import orient
from shapely.ops import transform
from pyproj import Transformer
warnings.filterwarnings('ignore');P=Path(__file__).parent;R=P.parents[1];O=R/'data/kommuner/4012-bamble/rev-01'
assert not (O/'approval.json').exists(),'Opprett ny revisjon; godkjent revisjon må ikke overskrives.'
O.mkdir(parents=True,exist_ok=True)
T=Transformer.from_crs(4326,25833,always_xy=True).transform;B=Transformer.from_crs(25833,4326,always_xy=True).transform
boundary=transform(T,shape(json.loads((P/'kommunegrense.geojson').read_text())['features'][0]['geometry']))
D=runpy.run_path(str(P/'decisions.py'))['D'];cands={c['cid']:c for c in json.loads((P/'candidates.json').read_text())}
CL={c['cid']:c for c in json.loads((P/'clusters.json').read_text())};frames={x['cid']:x for x in json.loads((P/'cluster-review-index.json').read_text())}
assert set(cands)<=set(D),set(cands)-set(D)
ATTR='© Kartverket; © OpenStreetMap contributors (ODbL); imagery: Esri, Vantor, Earthstar Geographics and the GIS User Community; kildeangitte operatører, organisasjoner og Bamble kommune'
NAMED={'C004','C006','C012','C021','C025','C028','C030','C035','C035S','C037','C038','C038K','M14'}
feats=[];n=0
# Stabile havne-ID-er: rekkefølgen fra første leveranse (H01–H32) beholdes; senere tillegg får nye numre bakerst.
LATER=['C026','M15','M16','M17','M18','M19']
order=[c for c in sorted(D) if D[c]['action']=='include' and c not in LATER]+[c for c in LATER if D[c]['action']=='include']
for cid in order:
 d=D[cid];n+=1;hid=f'4012-H{n:02}';osm=[p['id'] for p in CL.get(cid,{}).get('piers',[])]
 for k,part in enumerate(d['parts']):
  r=frames[part['frame']];a,b,c,e=r['review_bbox'];m=json.loads((P/'images'/(r['image_id']+'.json')).read_text());W=r['review_width'];H=r['review_height']
  raw=Polygon([(a+x/W*(c-a),e-y/H*(e-b)) for x,y in part['pixels']]);assert raw.is_valid,(cid,k)
  g=raw.intersection(boundary);assert g.geom_type=='Polygon' and g.area>25,(cid,k,g.geom_type);g=orient(g,sign=1);geo=transform(B,g);q=geo.representative_point();cap=d.get('capacity') if k==0 else None;cl=d['classification']
  p=dict(id=f'{hid}-B{k+1:02}',harbour_id=hid,candidate_id=cid,name=d['name'],name_is_descriptive=cid not in NAMED,municipality='Bamble',municipality_code='4012',classification=cl,classification_basis=d['basis'],approval_status='til_godkjenning',approved_utc=None,revision=1,method_version='1.2',schema_version='1.1',geometry_role='brygger_batplasser_og_mellomliggende_sjo',method='manuell_digitalisering_georeferert_flybilde_med_osm_og_kildekontroll',area_m2=round(g.area,1),area_crs='EPSG:25833',longitude=round(q.x,7),latitude=round(q.y,7),sources=list(dict.fromkeys(d['sources']+['https://www.openstreetmap.org/'+v for v in osm]+[m.get('image_url') or m['url']])),osm_ids=osm,imagery_source=m['source'],imagery_retrieved_date=m['retrieved_date'],source_observation_date=None,image_resolution_m_per_pixel=round((m['bbox'][2]-m['bbox'][0])/m['width'],3),estimated_accuracy_m=None,needs_orthophoto_review=bool(d['uncertain_geometry']),needs_dated_imagery_review=True,current_operation_verified=False,reviewed_date='2026-10-31',berth_count_published=cap,berth_count_source=d['sources'][0] if cap else None,berth_count_approximate=d['capacity_approximate'] if cap else None,berth_count_scope=d['capacity_scope'] if cap else None,berth_count_reference_period='ukjent_referanseperiode_nettside_lest_2026-10-31' if cap else None,source_register_objectid=None,source_register_number=None,source_register_members=[],capacity_components=[],municipality_clipped=raw.difference(boundary).area>0.01,cross_municipality_group_id=None,attribution=ATTR,note=d['note'],geometry_status='usikker_avgrensning' if d['uncertain_geometry'] else 'forelopig_avgrensning',water_body='brakkvann_elveos' if cid=='M06' else 'saltvann_eller_brakkvann',image_id=r['image_id'],image_sha256=m['sha256'])
  feats.append(dict(type='Feature',properties=p,geometry=mapping(geo)))
def write(fn,x):(O/fn).write_text(json.dumps(x,ensure_ascii=False,indent=1)+'\n')
def csvwrite(fn,rows):
 with (O/fn).open('w',encoding='utf-8-sig',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in x.items()} for x in rows)
write('bathavner.geojson',dict(type='FeatureCollection',name='Bamble – småbåthavner rev-01 til godkjenning',description='Kartleggingsforslag, ikke juridiske grenser. Kjente usikkerheter og åpne kandidater beholdt. Bare kysten er systematisk bildesøkt; innlandet ikke fullkartlagt.',method_version='1.2',schema_version='1.1',features=feats));csvwrite('metadata.csv',[f['properties'] for f in feats])
L=[]
for cid,c in cands.items():
 d=D[cid];related=[f['properties']['id'] for f in feats if f['properties']['candidate_id'] in (cid,cid+'S',cid+'K',cid+'W',cid+'E')]
 L.append(dict(candidate_id=cid,kind=c['kind'],center_25833=[round(v,1) for v in c['center']],osm_ids=[p['id'] for p in CL.get(cid,{}).get('piers',[])],osm_marks=c.get('marks',[]),image_id=frames[cid]['image_id'],review_bbox=frames[cid]['review_bbox'],decision='inkludert_'+d['classification'] if d['action']=='include' else 'utelatt',reason=d.get('basis') or d['reason'],note=d.get('note',''),feature_ids=related,reviewed_date='2026-10-31'))
SRC=[('S001','Stathelle og Omegn Båtforening','KNBF-medlem (126 medlemmer, ikke kapasitet); forretningsadresse Strandgata 42 Stathelle. Havneplassering ikke dokumentert; kan ha tilknytning til C025.','https://www.knbf.no/regioner/ost/medlemsforeninger-ost/'),
 ('S002','Langesund og Omegn Seilforening','Registrert forening (c/o-adresse); ingen stedfestet havn funnet.','https://data.brreg.no/enhetsregisteret/api/enheter/924750952'),
 ('S003','Valle Båtforening','Registrert ved Valleskolen; havneplassering ikke dokumentert.','https://data.brreg.no/enhetsregisteret/api/enheter/917212929'),
 ('S004','Fagerheim Båtforening','Kontaktadresse Ørvikstubben; mulig kobling til C033 er ikke dokumentert.','https://data.brreg.no/enhetsregisteret/api/enheter/998543401'),
 ('S005','Cocheplassen Båtforening','Kontaktadresse Martha Cochs vei; mulig kobling til C016 er ikke dokumentert.','https://data.brreg.no/enhetsregisteret/api/enheter/990905339'),
 ('S006','Sandvika Småbåtforening','To steder heter Sandvika i Bamble (vik ved Langesund og ved Trosby); havn ikke stedfestet.','https://data.brreg.no/enhetsregisteret/api/enheter/917926492'),
 ('S007','Mjælvika Båthavn SA','Adresse Sildetangveien; stedsnavn ikke funnet i Kartverkets søk. Ikke stedfestet.','https://data.brreg.no/enhetsregisteret/api/enheter/924572329'),
 ('S008','Sameiet Leirvad Båthavn','Adresse Ivarsandveien; mulig kobling til M02 er ikke dokumentert.','https://data.brreg.no/enhetsregisteret/api/enheter/996594408'),
 ('S009','Hegnas Marina','Adresse Valleveien 1011 (nær Valle); kan inngå i Valle-anleggene, ikke koblet.','https://data.brreg.no/enhetsregisteret/api/enheter/954128334'),
 ('S010','Vestrestrand båthavn','Planinnspill 2022 omtaler båtplassutleie siden 1930-tallet og 15 plasser langs land; kommunens PDF svarte 404 ved henting. Mulig del av C004 B02.','https://www.bamble.kommune.no/contentassets/1eaa40268ddc4fc4aaa1328e24b70a19/27-arkitektkontoret-henning-karlsen-as-for-vestrestrand-bathavn-200422.pdf'),
 ('S011','Langesund Båthavn AS / Båtforeningenes havneutvalg (Stoa)','Adresser på Stoa; støtter Stoa-navnet for C035S, men ikke driftsgrenser.','https://data.brreg.no/enhetsregisteret/api/enheter/930153605'),
 ('S013','Stråholmen småbåthavn (brukerinnspill runde 2)','Molohavn ved Stråholmen ligger i Kragerø (ca. 3,3 km utenfor Bamble-grensen). Ikke del av leveransen; ført i neighbour-pending.json.','https://api.kartverket.no/stedsnavn/v1/navn?sok=Str%C3%A5holmen'),
 ('S014','Vaterlands gate, Langesund (brukerinnspill runde 2)','Rekke av korte private brygger med separate landfester (C039). Sameiet Vaterland Brygge og Sameiet Andersens Brygge har adresse her, men sameienavn dokumenterer ikke faste båtplasser eller felles anlegg. Fortsatt utelatt; bør avklares mot sameiene.','https://data.brreg.no/enhetsregisteret/api/enheter/988458597'),
 ('S015','Kyststien – trekantet molobasseng (brukerinnspill runde 2)','Brukerens skjermbilde viser molobasseng med rundt tjue båter, men stedet kunne ikke stedfestes (Kyststien er en sti, ikke et adressenavn). Ikke vurdert; trenger koordinat eller stedsnavn.',''),
 ('S016','Rognstranda nord – brygge ved stranda (brukerinnspill runde 2)','Brygge med få båter ved badestranda; under ti plasser i bildet. Utelatt.',''),
 ('S012','Kverndalen og Kommunebrygga (Stathelle), Kuskjær og Sykehusbrygga (Langesund)','Kommunale havneeiendommer; ingen egen småbåthavn avgrenset utover C025. Kuskjær vurdert som M05.','https://www.bamble.kommune.no/vei-vann-havn-og-renovasjon/havn/havner-og-havneeiendommer-i-bamble-kommune/')]
for cid,name,reason,url in SRC:L.append(dict(candidate_id=cid,kind='kildekandidat',center_25833=None,osm_ids=[],osm_marks=[],image_id=None,review_bbox=None,decision='aapen_kildekandidat',reason=name+': '+reason,note='Kilde: '+url,feature_ids=[],reviewed_date='2026-10-31'))
write('candidate-ledger.json',L);csvwrite('candidate-ledger.csv',L)
summary=dict(polygons=len(feats),harbours=len({f['properties']['harbour_id'] for f in feats}),possible_harbours=len({f['properties']['harbour_id'] for f in feats if f['properties']['classification']=='mulig_smabathavn'}),uncertain_geometries=sum(f['properties']['needs_orthophoto_review'] for f in feats),osm_piers=sum(len(c['piers']) for c in CL.values()),osm_clusters=len(CL),image_candidates=sum(c['kind']=='bildefunn_kontaktark' for c in cands.values()),open_source_candidates=len(SRC),published_capacity_harbours=sum(f['properties']['berth_count_published'] is not None for f in feats))
write('summary.json',summary);write('digitisation.json',D);print(summary)

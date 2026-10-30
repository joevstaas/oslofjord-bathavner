import sys,json,csv,collections
from pathlib import Path
P=Path(__file__).parent;sys.path.insert(0,str(P/'deps'))
from shapely.geometry import Polygon,shape,mapping
from shapely.ops import transform,unary_union
from shapely.geometry.polygon import orient
from pyproj import Transformer
from digitize import rows
F=Transformer.from_crs(4326,25833,always_xy=True).transform;B=Transformer.from_crs(25833,4326,always_xy=True).transform
boundary=unary_union([transform(F,shape(f['geometry'])) for f in json.loads((P/'kommunegrense.geojson').read_text())['features']]);groups={};parts=collections.Counter();features=[];projected=[]
for i,r in enumerate(rows):
 group=r['group']
 if group not in groups:groups[group]=f'3103-H{len(groups)+1:02d}'
 hid=groups[group];parts[hid]+=1;fid=f'{hid}-B{parts[hid]:02d}';m=json.loads((P/'images'/f"{r['image']}.json").read_text());a,b,c,d=m['bbox'];g=Polygon([(a+x/r['display_width']*(c-a),d-y/r['display_height']*(d-b)) for x,y in r['pixels']]);assert g.is_valid,(r['name'],'invalid polygon');clipped=not boundary.covers(g);original=g;g=g.intersection(boundary);assert g.geom_type=='Polygon' and g.area>original.area*.5,(r['name'],'outside/split',g.geom_type,g.area/original.area)

 g=orient(g,sign=1);geo=transform(B,g);q=geo.representative_point();uncertain=r.get('geometry_uncertain',False);sources=list(dict.fromkeys(r['sources']+[f'https://www.openstreetmap.org/{o}' for o in r['osm_ids']]+[m['url']]))
 p=dict(candidate_id=r['candidate_id'],source_register_objectid=None,source_register_number=None,berth_count_reference_period=r.get('berth_count_reference_period'),source_register_members=r.get('source_register_members',[]),capacity_components=r.get('capacity_components',[]),id=fid,harbour_id=hid,name=r['name'],name_is_descriptive=r['name_is_descriptive'],municipality='Moss',municipality_code='3103',classification='mulig_smabathavn' if r['possible'] else 'smabathavn',classification_basis=r['basis'],approval_status='til_godkjenning',approved_utc=None,revision=1,method_version='1.1',schema_version='1.1',geometry_role='brygger_batplasser_og_mellomliggende_sjo',method=r['tracing_method'],area_m2=round(g.area,1),area_crs='EPSG:25833',longitude=round(q.x,7),latitude=round(q.y,7),sources=sources,osm_ids=r['osm_ids'],imagery_source=m['source'],imagery_retrieved_date=m.get('retrieved_date','2026-10-29'),source_observation_date=None,image_resolution_m_per_pixel=round((c-a)/m['width'],4),estimated_accuracy_m=None,needs_orthophoto_review=uncertain,needs_dated_imagery_review=True,current_operation_verified=False,reviewed_date='2026-10-29',berth_count_published=r['capacity'],berth_count_source=r['sources'][0] if r['capacity'] is not None and r['sources'] else None,berth_count_approximate=r.get('capacity_approximate',False) if r['capacity'] is not None else None,berth_count_scope='hele_havnegruppen' if r['capacity'] is not None else None,municipality_clipped=clipped,cross_municipality_group_id=None,attribution='Moss Havn, kildeangitte operatører og felles avfallsplan; © Kartverket; imagery: Esri, Vantor, Earthstar Geographics and the GIS User Community; OSM © OpenStreetMap contributors (ODbL)',note=r['note']+(' Vannmiljø: '+r['water_body']+'.' if r.get('water_body','saltvann')!='saltvann' else ''),geometry_status='usikker_avgrensning' if uncertain else 'forelopig_avgrensning',image_id=r['image'],image_sha256=m.get('sha256'))
 features.append(dict(type='Feature',properties=p,geometry=mapping(geo)));projected.append(g)
issues=[]
for i,g in enumerate(projected):
 for j in range(i+1,len(projected)):
  area=g.intersection(projected[j]).area
  if area>=1:issues.append(dict(a=features[i]['properties']['id'],b=features[j]['properties']['id'],a_name=features[i]['properties']['name'],b_name=features[j]['properties']['name'],area_m2=round(area,2)))
fc=dict(type='FeatureCollection',name='Moss – småbåthavner, revisjon 1',description='Foreløpig kommuneleveranse med bilde-/kildekontroll og kandidatlogg. Opptaksdato, posisjonsnøyaktighet, fullstendighet og dagens drift er ikke generelt verifisert. Fysiske båthavnområder, ikke juridiske grenser. Avventer godkjenning.',method_version='1.1',schema_version='1.1',features=features)
(P/'moss-bathavner.geojson').write_text(json.dumps(fc,ensure_ascii=False,indent=2)+'\n')
with (P/'moss-metadata.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(features[0]['properties']),delimiter=';');w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in x['properties'].items()} for x in features)
(P/'manual-digitization.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');(P/'overlap-issues.json').write_text(json.dumps(issues,ensure_ascii=False,indent=2)+'\n');summary=dict(polygons=len(features),harbours=len(groups),possible_harbours=len({x['properties']['harbour_id'] for x in features if x['properties']['classification']=='mulig_smabathavn'}),uncertain_geometries=sum(x['properties']['needs_orthophoto_review'] for x in features),clipped=[x['properties']['id'] for x in features if x['properties']['municipality_clipped']],overlap_issues=issues);(P/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False))

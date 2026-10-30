import sys,json,csv,collections
from pathlib import Path
P=Path(__file__).parent;sys.path.insert(0,str(P/'deps'))
from shapely.geometry import Polygon,shape,mapping
from shapely.ops import transform,unary_union
from shapely.geometry.polygon import orient
from pyproj import Transformer
from digitize import rows
F=Transformer.from_crs(4326,25833,always_xy=True).transform;B=Transformer.from_crs(25833,4326,always_xy=True).transform
boundary=unary_union([transform(F,shape(f['geometry'])) for f in json.loads((P/'kommunegrense.geojson').read_text())['features']]);groups={};parts=collections.Counter();features=[];rejected=[]
for i,r in enumerate(rows):
 group=r.get('group') or 'row-'+str(i)
 if group not in groups:groups[group]=f'3907-H{len(groups)+1:02d}'
 hid=groups[group];parts[hid]+=1;fid=f'{hid}-B{parts[hid]:02d}'
 m=json.loads((P/'images'/f"{r['image']}.json").read_text());x0,y0,x1,y1=m['bbox'];w=r['display_width'];h=r['display_height'];g=Polygon([(x0+x/w*(x1-x0),y1-y/h*(y1-y0)) for x,y in r['pixels']]);assert g.is_valid,(r['name'],'invalid outline')
 original=g;clipped=not boundary.covers(g);g=g.intersection(boundary)
 if g.is_empty:rejected.append(dict(name=r['name'],reason='utenfor_kommunegrensen'));continue
 assert g.geom_type=='Polygon', (r['name'],g.geom_type)
 fraction=g.area/original.area
 assert fraction>.5,(r['name'],'mostly outside municipality',fraction)
 
 # Align shared quay/molo edges, retaining independently identified harbour interiors.
 trim_against={19:[3],17:[6],27:[12],16:[5]}
 for other in features:
  if other['properties'].get('source_register_objectid') in ([30] if r.get('candidate_id')=='EXT-HUVIK' else trim_against.get(r.get('municipal_objectid'),[])):
   prior=transform(F,shape(other['geometry']));cut=g.intersection(prior).area
   if cut>0:
    g=g.difference(prior.buffer(0.02))
    if g.geom_type=='MultiPolygon' and r.get('municipal_objectid')==17:
     pieces=sorted(g.geoms,key=lambda a:a.area,reverse=True);assert sum(z.area for z in pieces[1:])<5;g=pieces[0];r['note']+=' En kontrollert rest på 4,6 m² ved nordkaien er utelatt som avgrensningsartefakt.'
    assert g.geom_type=='Polygon',(r['name'],'edge trim split',g.geom_type);r['note']+=f' Felles kaigrense tilpasset nabopolygon; {cut:.1f} m² teknisk overlapp fjernet.'
 g=orient(g,sign=1);geo=transform(B,g);q=geo.representative_point();sources=list(dict.fromkeys(r['sources']+[f'https://www.openstreetmap.org/{o}' for o in r.get('osm_ids',[])]+[m['url']]))
 uncertainty=r.get('geometry_uncertain',False)
 p=dict(candidate_id=r['candidate_id'],source_register_objectid=r.get('municipal_objectid'),source_register_number=r.get('municipal_source_number'),berth_count_reference_period='ukjent; kommunalt kartlag hentet 2026-10-29' if r.get('municipal_objectid') else None,source_register_members=r.get('source_register_members',[r['municipal_objectid']] if r.get('municipal_objectid') else []),capacity_components=r.get('capacity_components',[]),id=fid,harbour_id=hid,name=r['name'],name_is_descriptive=r['name_is_descriptive'],municipality='Sandefjord',municipality_code='3907',classification='mulig_smabathavn' if r['possible'] else 'smabathavn',classification_basis=r['basis'],approval_status='til_godkjenning',approved_utc=None,revision=1,method_version='1.1',schema_version='1.1',geometry_role='brygger_batplasser_og_mellomliggende_sjo',method=r.get('tracing_method','manuell_digitalisering_georeferert_flybilde_med_topografisk_og_kildebasert_kontroll'),area_m2=round(g.area,1),area_crs='EPSG:25833',longitude=round(q.x,7),latitude=round(q.y,7),sources=sources,osm_ids=r.get('osm_ids',[]),imagery_source='Esri World Imagery',imagery_retrieved_date=m.get('retrieved_date','2026-10-29'),source_observation_date=None,image_resolution_m_per_pixel=round((x1-x0)/m['width'],4),estimated_accuracy_m=None,needs_orthophoto_review=uncertainty,needs_dated_imagery_review=True,current_operation_verified=False,reviewed_date='2026-10-29',berth_count_published=r['capacity'],berth_count_source=('https://services3.arcgis.com/dLSgnt8bVopEJNp3/arcgis/rest/services/B%C3%A5thavner/FeatureServer/0' if r.get('municipal_objectid') else r['sources'][0]) if r['capacity'] is not None and r['sources'] else None,berth_count_approximate=True if r['capacity'] is not None else None,berth_count_scope='hele_havnegruppen' if r['capacity'] is not None else None,municipality_clipped=clipped,cross_municipality_group_id=None,attribution='© Kartverket; imagery: Esri, Vantor, Earthstar Geographics, and the GIS User Community; OSM © OpenStreetMap contributors (ODbL)',note=r['note'],geometry_status='usikker_avgrensning' if uncertainty else 'forelopig_avgrensning',image_id=r['image'],image_sha256=m.get('sha256'))
 features.append(dict(type='Feature',properties=p,geometry=mapping(geo)))
# Geometry validity/overlap is checked before export; no automatic repairs of semantic boundaries.
issues=[]
for i,a in enumerate(features):
 ga=transform(F,shape(a['geometry']));assert ga.is_valid
 for b in features[i+1:]:
  gb=transform(F,shape(b['geometry']));area=ga.intersection(gb).area
  
  if area>=1:issues.append(dict(a=a['properties']['id'],b=b['properties']['id'],area_m2=round(area,2)))
(P/'overlap-issues.json').write_text(json.dumps(issues,indent=2))
fc=dict(type='FeatureCollection',name='Sandefjord – småbåthavner, revisjon 1',description='Foreløpig kommuneleveranse etter visuell kart-/flybildegjennomgang og dokumentkilder. Opptaksdato og nøyaktighet ukjent. Fullstendighet og dagens drift er ikke garantert. Avventer godkjenning.',method_version='1.1',schema_version='1.1',features=features)
(P/'sandefjord-bathavner.geojson').write_text(json.dumps(fc,ensure_ascii=False,indent=2))
with (P/'sandefjord-metadata.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(features[0]['properties']),delimiter=';');writer.writeheader()
 for a in features:writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in a['properties'].items()})
(P/'manual-digitization.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
(P/'excluded-geometries.json').write_text(json.dumps(rejected,ensure_ascii=False,indent=2))
summary=dict(polygons=len(features),harbours=len({f['properties']['harbour_id'] for f in features}),possible_harbours=len({f['properties']['harbour_id'] for f in features if f['properties']['classification']=='mulig_smabathavn'}),uncertain_geometries=sum(f['properties']['geometry_status']=='usikker_avgrensning' for f in features),clipped=[f['properties']['id'] for f in features if f['properties']['municipality_clipped']],validation='valid polygons; within official boundary',overlap_issues=issues)
(P/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False))

import json,csv,hashlib,datetime,shutil
from pathlib import Path
from pyproj import Transformer
from shapely.geometry import shape,Polygon,mapping
from shapely.ops import transform,unary_union
from PIL import Image,ImageDraw
P=Path(__file__).parent; R=P.parents[2]; O=R/'data/kommuner/3903-holmestrand/rev-02-holmsaasen';O.mkdir(exist_ok=True)
assert not (O/'approval.json').exists(), 'Godkjent supplement skal ikke overskrives'
def write(n,d): (O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
m=json.loads((P/'images/holmsaasen-bay.json').read_text());bb=m['actual_bbox']; W,H=m['width'],m['height']; toLL=Transformer.from_crs(25833,4326,always_xy=True).transform; toUTM=Transformer.from_crs(4326,25833,always_xy=True).transform
# Vertices read manually in the displayed 1600-pixel review frame, scaled to the original image.
specs=[('H08','Holmsåsen – nordre brygge i campingbukta','mulig_smabathavn',[(677,665),(689,668),(678,708),(677,737),(648,733),(651,707),(663,674)],'Felles pir med flere utriggere og fortøyde småbåter. Minst ti faste plasser kan ikke telles sikkert; felles drift/operatør er ikke dokumentert.'),('H09','Holmsåsen – søndre fellespir i campingbukta','smabathavn',[(496,825),(620,884),(606,916),(487,851)],'Én sammenhengende fellespir med tydelig rekke av utriggere og minst ti synlige båtplasser. Ingen publisert kapasitet eller operatør er fastslått.')]
features=[]; pix=[]
for hid,name,cls,vertices,reason in specs:
 v=[(x*W/1600,y*H/1600) for x,y in vertices];pix.append(v)
 utm=Polygon([(bb[0]+x/W*(bb[2]-bb[0]),bb[3]-y/H*(bb[3]-bb[1])) for x,y in v]);g=transform(toLL,utm)
 props=dict(id=f'3903-{hid}-B01',harbour_id=f'3903-{hid}',name=name,name_is_descriptive=True,municipality='Holmestrand',municipality_code='3903',classification=cls,classification_basis=reason,approval_status='til_godkjenning',revision=2,scope='Avgrenset supplement: bukta i brukerens skjermbilde, ikke ny full kommuneanalyse',method_version='1.2',schema_version='1.1',geometry_role='brygger_batplasser_og_mellomliggende_sjo',method='manuell_digitalisering_georeferert_flybilde',geometry_status='usikker_avgrensning',area_m2=round(utm.area,1),longitude=g.centroid.x,latitude=g.centroid.y,needs_orthophoto_review=True,source_observation_date=None,current_operation_verified=False,berth_count_published=None,imagery_source='Esri World Imagery',imagery_retrieved_date=m['retrieved_date'],image_id=m['id'],image_sha256=m['sha256'],image_resolution_m_per_pixel=round((bb[2]-bb[0])/W,3),sources=[m['url']],attribution=m['attribution'],note='Beskrivende navn; campingtilknytning er geografisk, ikke bekreftet operatørforhold. Omriss er manuelt forslag med ukjent bildedato og posisjonsnøyaktighet.')
 features.append(dict(type='Feature',properties=props,geometry=mapping(g)))
write('bathavner.geojson',dict(type='FeatureCollection',features=features))
with (O/'metadata.csv').open('w') as f:
 wr=csv.DictWriter(f,fieldnames=list(features[0]['properties']),delimiter=';',lineterminator='\n');wr.writeheader();wr.writerows([x['properties'] for x in features])
write('digitisation.json',dict(image_id=m['id'],frame=[W,H],bbox=bb,crs='EPSG:25833',vertices=[dict(id=f['properties']['id'],pixels=v) for f,v in zip(features,pix)]))
base=json.loads((R/'data/kommuner/3903-holmestrand/rev-01/bathavner.geojson').read_text()); combined=json.loads((R/'data/samlet/oslofjorden-bathavner-samlet.geojson').read_text())
municipal=shape(json.loads((R/'archive/original/holmestrand-pilot/kommunegrense.geojson').read_text())['features'][0]['geometry']); boundary=transform(toUTM,municipal)
ugs=[transform(toUTM,shape(f['geometry'])) for f in features]; old=unary_union([transform(toUTM,shape(f['geometry'])) for f in combined['features']]);outside=[g.difference(boundary).area for g in ugs]; overlaps=[g.intersection(old).area for g in ugs]
validation=dict(features=2,groups=2,all_geometries_valid=all(g.is_valid for g in ugs),unique_ids=len({f['properties']['id'] for f in features})==2,id_collisions_with_combined=sorted({f['properties']['id'] for f in features}&{f['properties']['id'] for f in combined['features']}),outside_municipality_m2=outside,overlap_with_combined_m2=overlaps,internal_overlap_m2=ugs[0].intersection(ugs[1]).area,csv_rows=2,baseline_sha256=hashlib.sha256((R/'data/kommuner/3903-holmestrand/rev-01/bathavner.geojson').read_bytes()).hexdigest())
write('validation.json',validation)
assert validation['all_geometries_valid'] and not validation['id_collisions_with_combined'] and max(outside+overlaps)<.01
for name in ['holmsaasen-bay','holmsaasen-overview']:
 for ext in ['jpg','json']: shutil.copy2(P/f'images/{name}.{ext}',O/f'{name}.{ext}')
im=Image.open(P/'images/holmsaasen-bay.jpg').convert('RGB');d=ImageDraw.Draw(im)
for f,v in zip(features,pix):d.line(v+[v[0]],fill='#ff4444',width=4); d.text((v[0][0]+12,v[0][1]),f['properties']['id'],fill='white',stroke_width=2,stroke_fill='black')
im.save(O/'review-overlay.jpg',quality=94)
# Detailed crops for visual review, preserving the same underlying georeferenced frame.
for i,v in enumerate(pix):
 xs,ys=zip(*v);crop=(int(min(xs)-45),int(min(ys)-45),int(max(xs)+70),int(max(ys)+45)); im.crop(crop).resize((int((crop[2]-crop[0])*3),int((crop[3]-crop[1])*3))).save(O/f'detail-{i+1}.jpg')
write('source-provenance.json',dict(imagery=m,context_sources=[dict(url='https://www.drammen.no/overnatting-og-konferanse/holmsasen-camping-p6283123',finding='Bekrefter camping ved vannet, ikke båtplasser/operatør for pirene'),dict(url='https://virksomhet.brreg.no/nb/oppslag/underenheter/973322516',finding='Campingregistrering er ikke dokumentasjon for bryggedrift')],user_image='Brukerens skjermbilde 2026-10-31; brukt til stedsidentifikasjon, ikke georeferering'))
write('open-questions.json',['H08: antall faste plasser og felles drift er ikke dokumentert.','Operatør og offisielle navn for begge pirene ukjent.','Bildedato, posisjonsnøyaktighet og nåværende drift er ikke verifisert.','Gamle K04 ligger nord for campingbukta; navn/avgrensning bør etterprøves ved full Holmestrand-revisjon.'])
write('summary.json',dict(status='til_godkjenning',scope='Holmsåsen campingbukt og umiddelbart omkringliggende kyst i to bilderammer',new_features=2,new_groups=2,possible_groups=1,baseline_unchanged=True,combined_unchanged=True,website_unchanged=True))
print(json.dumps(validation,indent=2))

"""Lag georefererte detaljpaneler for funn fra full kystgjennomgang, fra bevarte kildefliser."""
import json,datetime,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
from shapely.geometry import box,Point
P=Path(__file__).parent
notes=json.loads((P/'sweep-notes.json').read_text())
extra=[dict(id='N13',cell='G044',xy=[192660,6558300],obs='Revurder brygge i vik ved industrikysten'),dict(id='N14',cell='G060',xy=[196350,6556700],obs='Revurder brygger ved bebyggelsen sør for Stathelle'),dict(id='N15',cell='G062',xy=[196800,6556190],obs='Revurder båter langs kai ved næringsbygg'),dict(id='N16',cell='G014',xy=[188800,6564320],obs='Kontroll av Herreelva og eksisterende avgrensning')]
old_candidates={c['cid']:c for c in json.loads((P/'candidates.json').read_text())}
extra += [dict(id='N17',cell='C019',xy=old_candidates['C019']['center'],obs='Revurder C019, langbrygge med utriggere'),dict(id='N18',cell='C020',xy=old_candidates['C020']['center'],obs='Revurder C020, brygge med utriggere')]
findings=notes['findings']+extra
findings[3]['xy']=[192025,6548050]
findings[9]['xy']=[189645,6545750]
imgs=[(f,json.loads(f.with_suffix('.json').read_text())) for f in sorted((P/'images').glob('coast-*.jpg'))]
cands=json.loads((P/'candidates.json').read_text());frames=[];panels=[]
for c in findings:
 cid=c['id'];x,y=c['xy'];side=440 if cid=='N10' else 240;fr=[x-side/2,y-side/2,x+side/2,y+side/2];S=800
 can=Image.new('RGB',(S,S),'black');used=[]
 for f,m in imgs:
  inter=box(*m['bbox']).intersection(box(*fr))
  if inter.is_empty or inter.area<1:continue
  a,b,e,d=m['bbox'];u,v,w,z=inter.bounds;W,H=m['width'],m['height']
  im=Image.open(f);crop=im.crop(((u-a)/(e-a)*W,(d-z)/(d-b)*H,(w-a)/(e-a)*W,(d-v)/(d-b)*H))
  ww,hh=round((w-u)/side*S),round((z-v)/side*S)
  if ww and hh:can.paste(crop.resize((ww,hh)),(round((u-fr[0])/side*S),round((fr[3]-z)/side*S)))
  used.append(f.stem)
 can.save(P/'qa'/f'{cid}-clean.jpg',quality=96)
 dr=ImageDraw.Draw(can)
 for v in range(0,S,100):
  dr.line([(v,0),(v,S)],fill='white');dr.text((v+2,2),str(v),fill='cyan')
  dr.line([(0,v),(S,v)],fill='white');dr.text((2,v+2),str(v),fill='cyan')
 pn=Image.new('RGB',(S,S+25),'white');pn.paste(can,(0,25));ImageDraw.Draw(pn).text((4,4),cid+' '+c['obs'],fill='black');panels.append(pn)
 near=sorted(cands,key=lambda v:Point(v['center']).distance(Point(x,y)))[:2]
 frames.append(dict(cid=cid,review_bbox=fr,review_width=S,review_height=S,image_id=used[0],source_tiles=used,cell=c['cell'],observation=c['obs'],nearest_candidates=[dict(cid=v['cid'],distance_m=round(Point(v['center']).distance(Point(x,y))),name=v.get('name')) for v in near]))
for n in range(0,len(panels),4):
 sh=Image.new('RGB',(1600,1650),'white')
 for i,p in enumerate(panels[n:n+4]):sh.paste(p,(i%2*800,i//2*825))
 sh.save(P/'qa'/f'detail-sweep-{n//4:02}.jpg',quality=95)
(P/'detail-sweep-index.json').write_text(json.dumps(frames,ensure_ascii=False,indent=1)+'\n')
print(json.dumps(frames,ensure_ascii=False,indent=1))

"""Forstørret vurderingsutsnitt: zoom.py <panel-cid> x0 y0 x1 y1 -> qa/zoom-<cid>.jpg med panelpikselrutenett hver 20. px."""
import sys
from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).parent;cid=sys.argv[1];x0,y0,x1,y1=map(int,sys.argv[2:6]);k=900/max(x1-x0,y1-y0)
im=Image.open(P/'qa'/f'{cid}-clean.jpg').crop((x0,y0,x1,y1));im=im.resize((int((x1-x0)*k),int((y1-y0)*k)));d=ImageDraw.Draw(im)
for v in range((x0//20+1)*20,x1,20):d.line([((v-x0)*k,0),((v-x0)*k,im.height)],fill=(255,255,0) if v%100==0 else (255,255,255),width=1);d.text(((v-x0)*k+2,2),str(v),fill='cyan')
for v in range((y0//20+1)*20,y1,20):d.line([(0,(v-y0)*k),(im.width,(v-y0)*k)],fill=(255,255,0) if v%100==0 else (255,255,255),width=1);d.text((2,(v-y0)*k+2),str(v),fill='cyan')
im.save(P/'qa'/f'zoom-{cid}.jpg',quality=92)
# Valgfritt: tegn gjeldende beslutningsomriss for paneler (rødt) for kontroll.
if len(sys.argv)>6:
 import runpy;D=runpy.run_path(str(P/'decisions.py'))['D']
 for d in D.values():
  for part in d.get('parts',[]):
   if part['frame']==cid:d.update();ImageDraw.Draw(im).line([((x-x0)*k,(y-y0)*k) for x,y in part['pixels']+part['pixels'][:1]],fill='red',width=2)
 im.save(P/'qa'/f'zoom-{cid}.jpg',quality=92)

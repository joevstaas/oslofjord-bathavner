import json,sys
from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).parent;name=sys.argv[1];ss=json.loads((P/name).read_text());tag=Path(name).stem
for a in range(0,len(ss),4):
 can=Image.new('RGB',(1200,1260),'white')
 for j,s in enumerate(ss[a:a+4]):
  im=Image.open(P/'images'/(s['id']+'.jpg')).resize((600,600));d=ImageDraw.Draw(im)
  for v in range(50,600,50):
   d.line([(v,0),(v,600)],fill=(85,85,120));d.text((v+1,0),str(v),fill='yellow',stroke_width=1,stroke_fill='black');d.line([(0,v),(600,v)],fill=(85,85,120));d.text((0,v+1),str(v),fill='yellow',stroke_width=1,stroke_fill='black')
  can.paste(im,((j%2)*600,(j//2)*630+30));ImageDraw.Draw(can).text(((j%2)*600+3,(j//2)*630+4),s['id'],fill='black')
 can.save(P/'images'/f'{tag}-contact-{a//4}.jpg')

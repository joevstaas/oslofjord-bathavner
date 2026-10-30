import json,sys
from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).parent;ss=json.loads((P/'osm-candidates.json').read_text());start=int(sys.argv[1]) if len(sys.argv)>1 else 0;end=int(sys.argv[2]) if len(sys.argv)>2 else len(ss)
for a in range(start,end,6):
 can=Image.new('RGB',(1800,1260),'white')
 for j,i in enumerate(range(a,min(a+6,end))):
  im=Image.open(P/'images'/f'p{i:02d}.jpg').resize((600,600));d=ImageDraw.Draw(im)
  for v in range(50,600,50):
   d.line([(v,0),(v,600)],fill=(85,85,120));d.text((v+1,0),str(v),fill='yellow',stroke_width=1,stroke_fill='black');d.line([(0,v),(600,v)],fill=(85,85,120));d.text((0,v+1),str(v),fill='yellow',stroke_width=1,stroke_fill='black')
  can.paste(im,((j%3)*600,(j//3)*630+30));ImageDraw.Draw(can).text(((j%3)*600+3,(j//3)*630+4),f'p{i:02d} '+ss[i]['name'],fill='black')
 can.save(P/'images'/f'contact-{a:02d}.jpg')

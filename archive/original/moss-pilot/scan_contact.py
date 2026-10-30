import json,sys
from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).parent;kind=sys.argv[1] if len(sys.argv)>1 else 'topo';ss=json.loads((P/('scan.json' if kind=='topo' else 'coast-esri.json')).read_text());ss.sort(key=lambda s:(-s['bbox'][3],s['bbox'][0]));(P/('scan-order-'+kind+'.json')).write_text(json.dumps(ss,indent=2))
for a in range(0,len(ss),6):
 can=Image.new('RGB',(1800,1260),'white')
 for j,s in enumerate(ss[a:a+6]):
  path=P/'images'/(s['id']+('.png' if kind=='topo' else '.jpg'))
  if not path.exists():continue
  im=Image.open(path).resize((600,600));can.paste(im,((j%3)*600,(j//3)*630+30));ImageDraw.Draw(can).text(((j%3)*600+3,(j//3)*630+5),s['id'],fill='black')
 can.save(P/'images'/f'scan-{kind}-{a//6}.jpg')

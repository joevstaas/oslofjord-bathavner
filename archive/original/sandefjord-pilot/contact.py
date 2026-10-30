from pathlib import Path
import json,sys
from PIL import Image,ImageDraw
P=Path(__file__).parent;fs=json.loads((P/'raw/municipal-harbour-points.geojson').read_text())['features'];start=int(sys.argv[1]) if len(sys.argv)>1 else 1;end=int(sys.argv[2]) if len(sys.argv)>2 else 67
for a in range(start,end,6):
 can=Image.new('RGB',(1800,1260),'white')
 for j,n in enumerate(range(a,min(a+6,end))):
  path=P/'images'/f'p{n:02d}.jpg'
  if not path.exists():continue
  f=next(x for x in fs if x['properties']['OBJECTID']==n);im=Image.open(path).resize((600,600));can.paste(im,((j%3)*600,(j//3)*630+30));ImageDraw.Draw(can).text(((j%3)*600+5,(j//3)*630+5),f'p{n:02d} '+f['properties']['Navn']+' '+str(f['properties']['antall_bå']),fill='black')
 can.save(P/'images'/f'contact-{a:02d}.jpg')

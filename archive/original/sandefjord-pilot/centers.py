import sys,json
from pathlib import Path
from PIL import Image,ImageDraw
from digitize import rows
P=Path(__file__).parent
nums=[10,17,19,22,25,39]
for a in range(0,len(nums),4):
 sheet=Image.new('RGB',(1200,1240),'white')
 for j,n in enumerate(nums[a:a+4]):
  rr=[r for r in rows if r['municipal_objectid']==n];r=rr[-1] if n==22 else rr[0];xs,ys=zip(*r['pixels']);cx=300;cy=300;x0=int(cx-70);y0=int(cy-70);box=(x0,y0,x0+140,y0+140)
  im=Image.open(P/'images'/f'p{n:02d}.jpg').resize((1200,1200)).crop(tuple(v*2 for v in box)).resize((600,600));d=ImageDraw.Draw(im)
  def xy(x,y):return ((x-x0)*600/140,(y-y0)*600/140)
  for v in range((x0//10+1)*10,x0+140,10):
   x,_=xy(v,y0);d.line([(x,0),(x,600)],fill=(100,100,150),width=1);d.text((x+1,2),str(v),fill='yellow',stroke_width=1,stroke_fill='black')
  for v in range((y0//10+1)*10,y0+140,10):
   _,y=xy(x0,v);d.line([(0,y),(600,y)],fill=(100,100,150),width=1);d.text((1,y+1),str(v),fill='yellow',stroke_width=1,stroke_fill='black')
  d.line([xy(*q) for q in r['pixels']]+[xy(*r['pixels'][0])],fill='red',width=2)
  sheet.paste(im,((j%2)*600,(j//2)*620+20));ImageDraw.Draw(sheet).text(((j%2)*600+3,(j//2)*620+3),f'p{n:02d} '+r['name'],fill='black')
 sheet.save(P/'images'/f'center-{a//4}.jpg')

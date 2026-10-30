from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).parent
specs=[('p09',280,280,140),('p03',320,270,140),('p08',260,300,180),('p15',240,270,140),('p16',260,290,160),('p14',365,265,180),('p13',490,80,160),('fritzoe',230,275,160)]
for a in range(0,len(specs),4):
 can=Image.new('RGB',(1200,1240),'white')
 for j,(k,cx,cy,span) in enumerate(specs[a:a+4]):
  x0=cx-span//2;y0=cy-span//2;im=Image.open(P/'images'/(k+'.jpg')).resize((1200,1200)).crop((x0*2,y0*2,(x0+span)*2,(y0+span)*2)).resize((600,600));d=ImageDraw.Draw(im)
  for v in range((x0//10+1)*10,x0+span,10):
   z=(v-x0)*600/span;d.line([(z,0),(z,600)],fill=(90,90,140));d.text((z,0),str(v),fill='yellow',stroke_width=1,stroke_fill='black')
  for v in range((y0//10+1)*10,y0+span,10):
   z=(v-y0)*600/span;d.line([(0,z),(600,z)],fill=(90,90,140));d.text((0,z),str(v),fill='yellow',stroke_width=1,stroke_fill='black')
  can.paste(im,((j%2)*600,(j//2)*620+20));ImageDraw.Draw(can).text(((j%2)*600+3,(j//2)*620+3),k,fill='black')
 can.save(P/'images'/f'zoom-{a//4}.jpg')

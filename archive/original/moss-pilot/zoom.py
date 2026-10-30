from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).parent
specs=[('p05',300,300,360),('fleischer',210,375,160),('fleischer',465,430,160),('p03',290,295,200),('p07',300,300,240),('p00',280,250,180)]
for a in range(0,len(specs),4):
 can=Image.new('RGB',(1200,1240),'white')
 for j,(k,cx,cy,span) in enumerate(specs[a:a+4]):
  x0=cx-span//2;y0=cy-span//2;im=Image.open(P/'images'/(k+'.jpg')).resize((1200,1200)).crop((x0*2,y0*2,(x0+span)*2,(y0+span)*2)).resize((600,600));d=ImageDraw.Draw(im)
  for v in range((x0//20+1)*20,x0+span,20):
   z=(v-x0)*600/span;d.line([(z,0),(z,600)],fill=(90,90,140));d.text((z,0),str(v),fill='yellow',stroke_width=1,stroke_fill='black')
  for v in range((y0//20+1)*20,y0+span,20):
   z=(v-y0)*600/span;d.line([(0,z),(600,z)],fill=(90,90,140));d.text((0,z),str(v),fill='yellow',stroke_width=1,stroke_fill='black')
  can.paste(im,((j%2)*600,(j//2)*620+20));ImageDraw.Draw(can).text(((j%2)*600+3,(j//2)*620+3),k,fill='black')
 can.save(P/'images'/f'zoom-{a//4}.jpg')

import urllib.request,urllib.parse,json,concurrent.futures,sys
from pathlib import Path
P=Path(__file__).parent;sys.path.insert(0,str(P/'deps'));from shapely.geometry import Point,shape
G=shape(json.loads((P/'kommunegrense.geojson').read_text())['features'][0]['geometry'])
names=['Kippenes','Refsnes','Rødsstranda','Røedsstranda','Støtvig','Rørvik','Lersbauen','Teibern','Nasle','Knutvika','Fuglevik','Evjesund','Djupeklo','Kjellandsvik','Sildebaugen','Neset']
def f(name):
 u='https://ws.geonorge.no/stedsnavn/v1/navn?'+urllib.parse.urlencode(dict(sok=name,treffPerSide=100))
 try:
  a=json.load(urllib.request.urlopen(u,timeout=20));(P/'raw'/f'name-{name}.json').write_text(json.dumps(a,ensure_ascii=False));out=[]
  for z in a.get('navn',[]):
   q=z['representasjonspunkt'];pt=(q['øst'],q['nord'])
   if G.buffer(.005).intersects(Point(*pt)):out.append(dict(name=z.get('skrivemåte'),type=z.get('navneobjekttype'),lon=pt[0],lat=pt[1]))
  return name,out
 except Exception as e:return name,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:out=dict(ex.map(f,names))
(P/'places.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False))

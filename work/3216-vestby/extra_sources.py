import runpy,urllib.request,hashlib,datetime,json
from pathlib import Path
P=Path(__file__).parent
ns={'__file__':str(P/'sources.py')};exec((P/'sources.py').read_text().split('with concurrent.futures')[0],ns)
for z in {'sonbf-havneweb':'https://www.havneweb.no/sonbaat/?mod=omhavnen','son-kart-side':'https://www.sonhavn.no/smaabaathavn/gjestehavnkartflyfoto/','sonskilen-sok':'https://www.sonskilen.no/sok-batplass','sonskilen-havneweb':'https://www.havneweb.no/sonskilen-bh/?mod=sokplass'}.items():print(ns['fetch'](z),flush=True)
for k,u in {'son-kart2018':'https://www.sonhavn.no/wp-content/uploads/2018/02/Havnekart.png','son-kart2019':'https://www.sonhavn.no/wp-content/uploads/2019/01/Havnekart.png'}.items():
 try:
  b=urllib.request.urlopen(u,timeout=35).read();(P/'raw'/(k+'.png')).write_bytes(b);(P/'raw'/(k+'-provenance.json')).write_text(json.dumps(dict(url=u,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(b).hexdigest()),indent=1));print(k,len(b),flush=True)
 except Exception as e:print(k,str(e),flush=True)

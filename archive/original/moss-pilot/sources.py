import sys,json,urllib.request,concurrent.futures
from pathlib import Path
P=Path(__file__).parent;sys.path.insert(0,str(P/'deps'));from lxml import html
urls={'sjekta':'https://sjekta.no','refsnes':'https://refsnessmaabaatforening.com','nasle':'https://nasle.no','kambo':'https://www.kambomarina.no/kambo_marina/batplass','betongen':'https://www.betongen.no/','abf':'https://abf-teibern.no/','rygge':'https://www.havneweb.no/ryggebf/','fiske':'https://fiske-baatforening.no/','verket':'https://verketgjestehavn.no/','soly':'https://moss-seilforening.no/'}
def get(q):
 k,u=q
 try:
  b=urllib.request.urlopen(u,timeout=18).read();(P/'raw'/f'{k}.html').write_bytes(b);s=html.fromstring(b);txt=' '.join(s.text_content().split());(P/'raw'/f'{k}.txt').write_text(txt);return k,txt[:1500],[(a.text_content().strip(),a.get('href')) for a in s.xpath('//a[@href]') if any(z in (a.text_content()+a.get('href')).lower() for z in ['havn','båt','kontakt','kart','om oss'])][:15]
 except Exception as e:return k,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 for x in ex.map(get,urls.items()):print(x,flush=True)

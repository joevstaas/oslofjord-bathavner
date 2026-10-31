"""Collect public primary sources for Moss enrichment; never edit approved geometry."""
import concurrent.futures, datetime, hashlib, json, pathlib, urllib.request
from html.parser import HTMLParser
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/berikelse/3103-moss/pilot-01'
SOURCES = [
 ('S01','Fiske – om havnen','https://www.fiske-baatforening.no/index.php/om-fiske.html','operator'),
 ('S02','Rygge Båtforening','https://www.havneweb.no/ryggebf/','operator'),
 ('S03','Kambo Båtforening','https://www.havneweb.no/kambobf/','operator'),
 ('S04','Kambo Marina','https://www.kambomarina.no/','operator'),
 ('S05','Moss Motorbåtforening','https://www.betongen.no/','operator'),
 ('S06','Nasle historisk blogg','https://naslebrygge.wordpress.com/','operator_historical'),
 ('S07','Søly – Havneweb','https://www.havneweb.no/moss-sf/','operator'),
 ('S08','Søly – havn og klubbhus','https://www.moss-seilforening.no/havn-og-klubbhus','operator'),
 ('S09','Vansjø – båtplasser','https://www.havneweb.no/vansjo/?mod=sokplass','operator'),
 ('S10','Verket Havn','https://www.verkethavn.no/','operator'),
 ('S11','Knutvika – Vindsteg','https://knutvika.no/','operator'),
 ('S12','Arbeidernes Båtforening Moss','https://abf-teibern.no/baat/','operator'),
 ('S13','Moss Havn – kanal og Tollbodbrygga','https://www.moss-havn.no/','operator'),
 ('S14','Felles avfallsplan, historisk referanse ca. 2020 ikke bekreftet','https://www.kambomarina.no/kambo_marina/avfallsplan','municipal_plan_mirror_historical'),
 ('S15','Refsnes småbåtforening – registrert nettsted','https://refsnessmaabaatforening.com/','operator_candidate'),
 ('S16','Støtvig Hotel – spørsmål og svar','https://www.stotvighotel.com/nb/sporsmal-og-svar','operator'),
 ('S17','Røedsstranda – salgsopplysninger','https://www.finn.no/realestate/plots/ad.html?finnkode=464346697','sales_listing'),
 ('S18','Fuglevik Båtservice – kontakt','https://www.fuglevik-bs.no/kontakt-oss/','service_operator'),
]
ORGS = ['958467362','883336402','996958663','882921662','983392229','918686878','991373721','979250029','982743354','912159515','995878321','922347034','993100544','985441464','920520111','930391204','916250258','990798664','913241045','917198616','990894116']
SOURCES += [('BR'+n,'Enhetsregisteret '+n,'https://data.brreg.no/enhetsregisteret/api/enheter/'+n,'organisation_register') for n in ORGS]
class Text(HTMLParser):
 def __init__(self): super().__init__(); self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'): self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'): self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip and d.strip():self.parts.append(d.strip())
def collect(spec):
 sid,title,url,kind=spec
 r=dict(source_id=sid,title=title,url=url,source_type=kind,accessed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reference_date=None)
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'MossHarbourEnrichment/1.0 (public-source research)'})
  with urllib.request.urlopen(req,timeout=25) as res:
   raw=res.read();r.update(http_status=res.status,resolved_url=res.url,content_type=res.headers.get('Content-Type'),last_modified_http=res.headers.get('Last-Modified'))
  r['raw_sha256']=hashlib.sha256(raw).hexdigest()
  if kind=='organisation_register':
   j=json.loads(raw);keys=['organisasjonsnummer','navn','organisasjonsform','registreringsdatoEnhetsregisteret','stiftelsesdato','hjemmeside','konkurs','underAvvikling','underTvangsavviklingEllerTvangsopplosning','slettedato']
   text=json.dumps({k:j.get(k) for k in keys},ensure_ascii=False,indent=2)
   r['archive_scope']='Selected non-personal entity fields; raw response hash retained, full response not stored.'
  else:
   parser=Text();parser.feed(raw.decode('utf-8','replace'));text='\n'.join(parser.parts)
   r['archive_scope']='HTML text extraction; scripts and styles omitted; not a rendered or full HTML archive.'
  dest=OUT/'sources'/(sid+'.txt');dest.write_text(text);r['snapshot_path']=str(dest.relative_to(ROOT));r['snapshot_sha256']=hashlib.sha256(dest.read_bytes()).hexdigest();r['retrieval_status']='retrieved'
 except Exception as e:r.update(retrieval_status='failed',error=str(e))
 return r
if __name__=='__main__':
 (OUT/'sources').mkdir(parents=True,exist_ok=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: results=list(pool.map(collect,SOURCES))
 (OUT/'sources.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
 for r in results: print(r['source_id'],r['retrieval_status'],r.get('error',''))

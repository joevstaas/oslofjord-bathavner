"""Collect public primary sources for Holmestrand enrichment; never edit approved geometry."""
import concurrent.futures, datetime, hashlib, json, pathlib, urllib.request, subprocess
from html.parser import HTMLParser
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/berikelse/3903-holmestrand/pilot-01'
SOURCES = [
 ('HS01','Holmestrand Småbåthavn – operatør','https://holmestrandsmabathavn.no/','operator'),
 ('HS02','Holmestrand kommune – småbåthavn','https://holmestrand.kommune.no/innbyggerhjelpen/naring-transport-og-samfunn/parkering-vei-og-havn/havn-og-bobil/smabathavn/','municipal'),
 ('HS03','Holmestrand kommune – gjestehavn','https://holmestrand.kommune.no/innbyggerhjelpen/naring-transport-og-samfunn/parkering-vei-og-havn/havn-og-bobil/gjestehavn/','municipal'),
 ('HS04','Nordre Jarlsberg Brygge – båthavna','https://njb.no/bathavna/','operator'),
 ('HS05','NJB Marina – Havneweb','https://www.havneweb.no/njb-marina/','operator'),
 ('HS06','NJB Marina – spørsmål og svar','https://njb.no/wp-content/uploads/2024/04/FAQ_NJB_Marina.pdf','operator_document'),
 ('HS07','Bjerkøya – om anlegget','https://bjerkbat.no/OmOss/InformasjonomBjerk%C3%B8yab%C3%A5tforening.aspx','operator'),
 ('HS08','Bjerkøya – nyheter','https://bjerkbat.no/','operator'),
 ('HS09','Sande & Havna Båtforening','https://www.havneweb.no/sandehavnabf/','operator'),
 ('HS10','Holm Brygge','https://www.holmbrygge.no/','operator'),
 ('HS11','Thorrud – fasiliteter','https://thorrudcamping.no/fasiliteter/','operator'),
 ('HS12','Thorrud – om oss','https://thorrudcamping.no/om-oss/','operator'),
 ('HS13','Thorrud – informasjon og priser','https://thorrudcamping.no/informasjon/','operator'),
 ('HS14','Kommunalt kunnskapsgrunnlag 2020 – mulig eldre kilde','https://holmestrand.kommune.no/_f/p1/i3f2e8be2-8a44-44e1-87fa-b7d1eb615b67/kunnskapsgrunnlag-pr-250620docx.pdf','municipal_document'),
 ('HS15','Anleggsplan 2020–2028','https://holmestrand.kommune.no/_f/p1/iab4e779d-804c-4437-8bff-00434dfab166/annleggsplan-for-idrett-friluftsliv-og-kultur-2020-2028-392438.pdf','municipal_document'),
 ('HS16','Bjerkøya – Velihavn','https://velihavn.no/hjemmehavner/bjerkoya-batforening','harbour_directory'),
 ('HS17','Holmestrand Båtforening – tildeling','https://holmestrand-baatforening.no/?page_id=172','association'),
]
SOURCES.append(('HS18','NJB – opplagspriser','https://njb.no/wp-content/uploads/2026/06/Prisliste_opplag_NJB_Marina_20260605.pdf','operator_document'))
SOURCES.append(('HS19','Langøya – planinitiativ 12.01.2026','https://holmestrand.kommune.no/_f/p1/i999d3687-7c6b-4435-84ca-126fb527b16a/planinitiativ_langoya_v2-12012026.pdf','planning_document'))
ORGS = ['936760600','985747970','912886786','997317599','896548972','912086275','987352965','915094821']
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
  req=urllib.request.Request(url,headers={'User-Agent':'HolmestrandHarbourEnrichment/1.0 (public-source research)'})
  with urllib.request.urlopen(req,timeout=25) as res:
   raw=res.read();r.update(http_status=res.status,resolved_url=res.url,content_type=res.headers.get('Content-Type'),last_modified_http=res.headers.get('Last-Modified'))
  r['raw_sha256']=hashlib.sha256(raw).hexdigest()
  if kind=='organisation_register':
   j=json.loads(raw);keys=['organisasjonsnummer','navn','organisasjonsform','registreringsdatoEnhetsregisteret','stiftelsesdato','hjemmeside','konkurs','underAvvikling','underTvangsavviklingEllerTvangsopplosning','slettedato']
   text=json.dumps({k:j.get(k) for k in keys},ensure_ascii=False,indent=2)
   r['archive_scope']='Selected non-personal entity fields; raw response hash retained, full response not stored.'
  elif raw.startswith(b'%PDF'):
   pdf=OUT/'sources'/(sid+'.pdf');pdf.write_bytes(raw)
   text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-']).decode('utf-8');r['archive_scope']='PDF text extraction; original PDF stored locally.'
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

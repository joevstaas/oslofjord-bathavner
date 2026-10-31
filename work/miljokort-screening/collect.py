"""Bounded public-source screening, with snapshots, errors and candidate snippets."""
import json,urllib.request,urllib.parse,hashlib,datetime,re,concurrent.futures,io
from html.parser import HTMLParser
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'data/miljokort/screening-01';W=R/'work/miljokort-screening/raw';W.mkdir(exist_ok=True)
class Page(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.text=[];self.links=[];self.current=None
 def handle_starttag(self,t,a):
  a=dict(a)
  if t in ('script','style','noscript'):self.skip+=1
  if t=='a':self.current=[a.get('href',''),'']
 def handle_endtag(self,t):
  if t in ('script','style','noscript'):self.skip=max(0,self.skip-1)
  if t=='a' and self.current:self.links.append(self.current);self.current=None
 def handle_data(self,d):
  if not self.skip:
   d=' '.join(d.split())
   if d:self.text.append(d)
   if self.current:self.current[1]+=' '+d
pat=re.compile(r'(spylevann|renseanlegg|spyleplass|farlig avfall|miljøstasjon|miljøcontainer|miljøkontainer|septik|slipestøv|avfallsplan|ålegras|ålegress)',re.I)
urls={urllib.parse.urldefrag(u)[0] for g in json.loads((O/'inventory.json').read_text()) for u in g['urls']}
urls.update(s['url'] for s in json.loads((R/'data/miljokort/pilot-01/sources.json').read_text()) if not s['id'].startswith('L'))
urls.update(json.loads((R/'work/miljokort-screening/extra-urls.json').read_text()))
results=[]
def fetch(u):
 sid=hashlib.sha256(u.encode()).hexdigest()[:16];p=W/(sid+'.bin');rec=dict(id=sid,url=u,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  if p.exists():b=p.read_bytes();rec['cache']=True
  else:
   req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (public harbour environmental evidence review)'})
   with urllib.request.urlopen(req,timeout=12) as h:b=h.read(6_000_000);rec['final_url']=h.url;rec['http_status']=h.status
   p.write_bytes(b)
  rec['sha256']=hashlib.sha256(b).hexdigest();rec['snapshot']=str(p.relative_to(R))
  if b.startswith(b'%PDF'):
   try:
    import pypdf
    text='\n'.join(page.extract_text() or '' for page in pypdf.PdfReader(io.BytesIO(b)).pages);links=[]
   except Exception as e:text='';links=[];rec['parse_error']=str(e)
  else:
   page=Page();page.feed(b.decode('utf-8',errors='replace'));text='\n'.join(page.text);links=page.links
  (W/(sid+'.txt')).write_text(text);rec['text_path']=str((W/(sid+'.txt')).relative_to(R));rec['text_chars']=len(text)
  rec['snippets']=[text[max(0,m.start()-100):m.end()+230].replace('\n',' ') for m in list(pat.finditer(text))[:24]]
  rec['links']=[urllib.parse.urljoin(u,l) for l,label in links if re.search(r'milj[oø]|avfall|hms|reglement|spyl|septik|ordensreg',l+' '+label,re.I) and urllib.parse.urlparse(urllib.parse.urljoin(u,l)).scheme in ('https','http')][:8]
 except Exception as e:rec['error']=str(e)
 return rec
for phase in range(2):
 batch=sorted(urls-{r['url'] for r in results})
 with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:results.extend(pool.map(fetch,batch))
 print('phase',phase+1,'sources',len(results),'with hits',sum(bool(r.get('snippets')) for r in results),'errors',sum('error' in r for r in results),flush=True)
 if phase==0:
  urls.update(u for r in results for u in r.get('links',[]) if not any(host in urllib.parse.urlparse(u).netloc for host in ['facebook','instagram','youtube','linkedin','twitter']))
(R/'work/miljokort-screening/source-screening-full.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
(O/'source-screening.json').write_text(json.dumps([{k:v for k,v in r.items() if k not in ['snippets','links']} for r in results],ensure_ascii=False,indent=2)+'\n')
print('done',flush=True)

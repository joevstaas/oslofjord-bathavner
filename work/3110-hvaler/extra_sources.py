from pathlib import Path
P=Path(__file__).parent;n={'__file__':str(P/'sources.py')};exec((P/'sources.py').read_text().split('with concurrent.futures')[0],n)
U={'hvaler-bf':'https://hvalerbaatforening.no/','listranda':'https://www.listrandabatforening.no/','herfol-marina':'https://www.herfoelmarina.no/','dypedal':'https://www.hvalermarinesenter.no/omoss.html','edholmen':'https://www.edholmen.no/','brattesto':'https://www.brattestomarina.no/','hvaler-camping':'https://www.hvalercamping.no/tjenester/'}
for z in U.items():print(n['fetch'](z),flush=True)
import urllib.request,hashlib,datetime,json
u='https://www.hvaler.kommune.no/contentassets/df50af304dee4936bd3685c41fbe7412/strategisk-havneplan-2018-2028.pdf'
b=urllib.request.urlopen(u,timeout=45).read();f=P/'raw/havneplan2018.pdf';f.write_bytes(b);f.with_suffix('.provenance.json').write_text(json.dumps(dict(url=u,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(b).hexdigest()),indent=1));print('pdf',len(b),flush=True)

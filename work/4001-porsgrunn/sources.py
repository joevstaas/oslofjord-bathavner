"""Lagre primærkilder med innhentingstid og SHA-256; ingen operatøradresser brukt som sjøposisjon."""
import requests,json,datetime,hashlib,concurrent.futures
from pathlib import Path
P=Path(__file__).parent
urls={'pmf.html':'https://www.batforening.com/','pmf-havner.html':'https://www.havneweb.no/batforening/?mod=omhavnen','brevik.html':'https://www.havneweb.no/brevik-bf/?mod=omhavnen','skjelsvik.html':'https://www.havneweb.no/skjelsvik-bf/?mod=omhavnen','heistad.html':'https://www.havneweb.no/heistad-mbf/?mod=omhavnen','brevik-seil.html':'https://brevikseilforening.no/','brevik-seivall.html':'https://brevikseilforening.no/seivall/','langangen.html':'https://langangen.com/index.php?Itemid=602&catid=17&id=107%3Abatforeningen&option=com_content&view=article','pmv-plan.pdf':'https://www.porsgrunn.kommune.no/media/kjcjdo2e/10-notat-smaabaathavn-pmv-20082020.pdf','gjestehavner-2013.pdf':'https://www.telemarkskanalen.no/dbimgs/13-11-01%20Rapport%20gjestehavner%20-%20endelig%20og%20offentlig.pdf'}
urls.update({'nystrand.html':'https://nystrandbf.org/','dovik.html':'https://www.dbf-porsgrunn.com/','dovik-2024.pdf':'https://www.dbf-porsgrunn.com/wordpress/wp-content/uploads/2025/03/ARSMOTEDOMUMENT-2025_09.03.25.pdf','downtown.html':'https://www.visittelemark.no/produkter/down-town-gjestebrygge','kanal-kyst.html':'https://www.telemarkskanalen.no/fritidsbat/strekning-for-strekning/fra-kysten-til-skien','sjoloftet.html':'https://www.sjoloftet.no/','pmf-80aar.pdf':'https://www.batforening.com/wp-content/uploads/2016/04/80-%C3%A5rs-beretning.pdf'})
urls.update({'heroya.html':'https://www.havneweb.no/heroya/','heroya-local.html':'https://heroya.wordpress.com/omhff/hff-medlemsorganisasjoner/heroya-motorbatforening/','heroya-2019.pdf':'https://www.hydro.com/globalassets/07-media/nabo-info-porsgrunn-juni2019.pdf'})
urls.update({'sandoya.html':'https://www.havneweb.no/sandoyabatforening/','sjoloftet-marina.html':'https://www.sjoloftet.no/sjloftet-marina','sundjord-plan.pdf':'https://www.porsgrunn.kommune.no/media/idefyybu/4-planbeskrivelse.pdf','pmf-2023.pdf':'https://www.batforening.com/wp-content/uploads/2023/04/PMF-lov-rev.10.03.23.pdf'})
def fetch(kv):
 k,u=kv;f=P/'raw'/k
 if f.exists():return k,'cached'
 try:
  r=requests.get(u,timeout=30);r.raise_for_status();f.write_bytes(r.content);f.with_suffix('.provenance.json').write_text(json.dumps(dict(url=u,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(r.content).hexdigest()),indent=1));return k,len(r.content)
 except Exception as e:return k,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for r in ex.map(fetch,urls.items()):print(r,flush=True)

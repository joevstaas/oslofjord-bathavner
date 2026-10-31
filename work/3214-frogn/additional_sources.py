import runpy
from pathlib import Path
P=Path(__file__).parent
# Reuse parser/fetcher without rerunning previous collection.
s=(P/'extra_sources.py').read_text().split('with concurrent.futures')[0]
n={'__file__':str(P/'extra_sources.py')};exec(s,n)
U={'bergholmen':'https://www.oslofjorden.org/bygningene-pa-bergholmen/','solbergstrand':'https://solbergstrand.no/strandkomiteer/','gylteaasen-vel':'https://www.xn--gv-kka.no/omoss/informasjon/','adresse-gylteveien4':'https://ws.geonorge.no/adresser/v1/sok?sok=Gylteveien%204&kommunenummer=3214&treffPerSide=10'}
for z in U.items():print(n['fetch'](z),flush=True)

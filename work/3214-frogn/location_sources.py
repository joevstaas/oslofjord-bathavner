from pathlib import Path
P=Path(__file__).parent;n={'__file__':str(P/'extra_sources.py')};exec((P/'extra_sources.py').read_text().split('with concurrent.futures')[0],n)
U={'bergholmen-hytte':'https://friluftsliv.oslofjorden.org/hytteoversikt/bergholmen-befalsboligen','bergholmen-bv':'https://b-v.no/havner/bergholmen','tajebukta-leverandor':'https://sfmarina.com/sf-projects/haoya/','tajebukta-posisjon':'https://pequod.nesodd1.no/?page_id=5509','dragsund-posisjon':'https://pequod.nesodd1.no/?page_id=9244'}
for z in U.items():print(n['fetch'](z),flush=True)

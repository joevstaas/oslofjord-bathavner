from pathlib import Path
P=Path(__file__).parent;n={'__file__':str(P/'sources.py')};exec((P/'sources.py').read_text().split('with concurrent.futures')[0],n)
U={'edholmen-marina':'https://www.edholmenmarina.no/','skjaerhalden-havneweb':'https://www.havneweb.no/skjarhalden-bf/','halden-bf-brattholmen':'https://www.haldenbf.no/','siljeholmen':'https://www.siljeholmenvel.com/','listranda-brygger':'https://www.listrandabatforening.no/bryggeplasser/'}
for z in U.items():print(n['fetch'](z),flush=True)

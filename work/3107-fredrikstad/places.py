"""Stedsnavnoppslag (Kartverket stedsnavn-API) for navn i foreningsregisteret, avgrenset til Fredrikstad."""
import json, time, requests
from pathlib import Path
P = Path(__file__).parent
names = ['Alshus', 'Bekkhus', 'Bilet', 'Bjølstad', 'Bruket', 'Bukkenes', 'Dypedal', 'Eiemyr', 'Engelsviken', 'Fagerstrand', 'Gamlebyen', 'Gaustad',
         'Gressvik', 'Hankø', 'Hankøsund', 'Hasselvika', 'Helleskilen', 'Herretangen', 'Holm', 'Humlekjær', 'Karibukta', 'Kiærs bruk', 'Kjøkøya', 'Kjøkøy',
         'Klintebukta', 'Krosnes', 'Nøkledypet', 'Langøen', 'Langøya', 'Lervik', 'Lisleby', 'Ranøyen', 'Marnet', 'Nabbetorp', 'Ødegårdskilen', 'Nøkleby',
         'Olastranda', 'Vesterelva', 'Huthholmen', 'Ramseklo', 'Rolvsøy', 'Rød', 'Sandbukta', 'Selbak', 'Seut', 'Skjærviken', 'Slevik', 'Stenebråten',
         'Øyenkilen', 'Sundløkka', 'Torp', 'Underlien', 'Vaterland', 'Vikerkilen', 'Åsebu', 'Øra', 'Østre Oksrødkilen', 'Oksrødkilen', 'Elingård',
         'Vikane', 'Glombo', 'Kråkerøy', 'Rauøy', 'Bjørnevåg', 'Ødegårdkilen', 'Isegran', 'Kongens brygge', 'Lahellemoen', 'Lahelle', 'Saltnes',
         'Ålestranda', 'Gunneland', 'Krosnesbukta', 'Bellevue', 'Flisvika', 'Sandvika', 'Værste', 'Tordenskiold', 'Nygaard', 'Engalsvik']
out = {}
for n in names:
    r = requests.get('https://ws.geonorge.no/stedsnavn/v1/navn', params=dict(sok=n, knr='3107', utkoordsys=25833, treffPerSide=10), timeout=30).json()
    out[n] = [dict(name=x['skrivemåte'], type=x['navneobjekttype'], x=round(x['representasjonspunkt']['øst']), y=round(x['representasjonspunkt']['nord'])) for x in r.get('navn', [])]
    time.sleep(0.2)
(P / 'raw/stedsnavn.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
for n, v in out.items():
    print(n, '|', '; '.join(f"{x['type']} {x['x']},{x['y']}" for x in v[:4]))

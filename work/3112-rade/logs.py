"""Kandidatlogg, dekning, kildenotater og nabofunn for Råde rev. 1."""
import json, csv
from pathlib import Path
P = Path(__file__).parent
fs = json.loads((P / 'rade-bathavner.geojson').read_text())['features']
by_c = {}
for f in fs:
    by_c.setdefault(f['properties']['candidate_id'], []).append(f['properties'])
BR = 'https://virksomhet.brreg.no/nb/oppslag/enheter/'
OSM = 'https://www.openstreetmap.org/'
L = []
def add(cid, name, x, y, decision, reason, sources=(), link=None):
    ps = by_c.get(link or cid, [])
    L.append(dict(candidate_id=cid, name=name, x_25833=x, y_25833=y, decision=decision, reason=reason, sources=list(sources),
                  feature_ids=[p['id'] for p in ps], harbour_ids=sorted({p['harbour_id'] for p in ps}), reviewed_date='2026-10-29'))
for f in fs:
    p = f['properties']
    if p['candidate_id'] not in [l['candidate_id'] for l in L]:
        add(p['candidate_id'], p['name'], None, None, 'inkludert_' + p['classification'], p['classification_basis'], p['sources'][:-1])
add('OSM-node/5106918395', 'OSM Småbåtshavn, Båthavnveien Makrellrød', 259643, 6582301, 'samordnet_med_kildeanlegg', 'Samme fysiske havn som Råde båtforening.', [OSM + 'node/5106918395'], 'SRC-RBF')
for oid, x, y, note in [('node/1298738114', 259802, 6582104, 'Makrellrød'), ('node/6560408479', 259817, 6582142, 'Makrellrød'),
                        ('node/5822268071', 258323, 6582890, 'Fuglevik kanal'), ('node/5843563715', 258392, 6582620, 'Fuglevik sør'),
                        ('node/9083591817', 257803, 6579732, 'Saltholmen'), ('node/7636246450', 264465, 6587665, 'Vansjø'),
                        ('node/1326819932', 265771, 6588594, 'Vansjø')]:
    add('OSM-' + oid, f'OSM slipp ({note})', x, y, 'utelatt_ikke_havn_alene', 'Utsettingsrampe kvalifiserer ikke alene. Nærliggende anlegg er vurdert separat; ved Vansjø ble ingen bryggeanlegg funnet i detaljbildet.', [OSM + oid])
add('OSM-node/6255853844', 'OSM Båtslipp (øst)', 270136, 6583771, 'utenfor_kommunen', 'Ligger utenfor Råde i 300 m-beltet; ikke behandlet.', [OSM + 'node/6255853844'])
add('VIS-aven-midt', 'Åven – T-brygge mellom vestre og indre anlegg', 256893, 6582700, 'utelatt_under_terskel', 'Én T-brygge med om lag fem–seks båter; ingen dokumentasjon av felles drift.')
add('VIS-aven-nord', 'Åven nord – enkeltbrygge', 256764, 6583247, 'utelatt_under_terskel', 'Enkelt brygge med få båter.')
add('VIS-makrellrod-nord', 'Makrellrød – nordre separat brygge', 259790, 6582280, 'utelatt_separat_brygge', 'Kort separat brygge nord for bassenget, få båter; mulig servicebrygge. Ikke tegnet som del av havnepolygonet.')
add('VIS-saltholmen-vest', 'Saltholmen – vestre L-brygge', 257630, 6579730, 'utelatt_under_terskel', 'Liten brygge vest for bassenget med få båter.')
add('VIS-kure-n1', 'Kurefjorden øst – brygge nord', 258060, 6585230, 'utelatt_under_terskel', 'Én brygge med fire synlige båter.')
add('VIS-kure-n2', 'Kurefjorden øst – brygge sør', 258120, 6585020, 'utelatt_under_terskel', 'Én brygge med utriggere, om lag 5–8 plasser; ikke dokumentert felles anlegg.')
add('VIS-fuglevik-sma', 'Fuglevik – små brygger vest i bukta', 258120, 6582730, 'utelatt_under_terskel', 'To korte brygger uten synlige båter.')
add('SEK-krokstad-nord', 'Krokstadfjorden nordside – spredte brygger', 260600, 6583400, 'utelatt_sektorvurdering', 'Seks–sju korte brygger med 2–5 båter hver langs separate eiendommer. Ikke summert.')
add('VIS-krokstad-nordbrygge', 'Krokstadfjorden indre – liten nordbrygge', 261230, 6583680, 'utelatt_under_terskel', 'Kort brygge med tre båter.')
add('SEK-saltnes-kyst', 'Saltnes vestkyst – spredte private brygger', 258750, 6581250, 'utelatt_sektorvurdering', 'Enkeltbrygger, de fleste uten synlige båter. Kommunedelplanen beskriver Saltnes som preget av mange enkeltbrygger.', ['https://www.rade.kommune.no/_f/p1/i1db1d7e1-c08e-4118-a0e8-f70e09a26638/kommunedelplan_for_saltnesomraadet-vedtatt_210607.pdf'])
add('SRC-OKETANGEN', 'Øketangen bryggeforening', None, None, 'utenfor_kommunen', 'Fellesbryggen ligger ved Bauen i Singlefjorden, Sarpsborg. Råde er bare omtalt som mulig dumpested.', ['https://www.statsforvalteren.no/ostfold-buskerud-oslo-og-akershus/miljo-og-klima/forurensning/tillatelse-til-mudring-i-sjo-ved-oketangen-bryggeforenings-fellesbrygge-i-sarpsborg-kommune/'])
add('SRC-FUGLEVIK-MARINA', 'Fuglevik Marina (enkeltpersonforetak)', None, None, 'utenfor_kommunen', 'Forretningsadresse i Moss; gjelder Fuglevik i tidligere Rygge, ikke Fuglevik i Råde.', [BR + '996859886'])
add('SRC-SALTHOLMEN-SAMEIE', 'Saltholmen sameie', None, None, 'apen_ikke_stedfestet', 'Sameie registrert 1928 med adresse Hvalfangerveien. Ingen dokumentasjon av eget sjøanlegg funnet; ikke påstått kobling til båthavna.', [BR + '899048822'])
add('SRC-KDP-NAERING', 'Agnes Brygge / Skjærgårdsbrygger AS (kommunedelplan 2007)', None, None, 'utelatt_ikke_havn', 'Omtalt som næringsvirksomhet i kommunedelplanen, ikke som småbåthavn.', ['https://www.rade.kommune.no/_f/p1/i1db1d7e1-c08e-4118-a0e8-f70e09a26638/kommunedelplan_for_saltnesomraadet-vedtatt_210607.pdf'])
add('OSMPIR-saltnes-sor', 'Saltnes sør (nord for Saltholmen) – OSM-pirer og molo', 257900, 6580300, 'utelatt_under_terskel', 'Kontrollert i zoom etter brukerinnspill: korte enkeltbrygger uten båtplassanlegg.')
add('OSMPIR-aven-nord', 'Åven nordkyst – OSM-pirer og molo', 256600, 6583250, 'utelatt_under_terskel', 'Kontrollert i zoom etter brukerinnspill: enkeltbrygger med få eller ingen båter.')
add('OSMPIR-aven-sor', 'Åven sør – fire OSM-moloer', 256750, 6581870, 'utelatt_ikke_havn_alene', 'Kontrollert i zoom etter brukerinnspill: små steinmoloer uten synlige båtplasser.')
add('OSMPIR-vansjo-gard', 'Vansjø, gård/leir ved 266270/6588950 – små brygger', 266270, 6588950, 'utelatt_under_terskel', 'To–tre korte brygger; vårbilde uten båter. Bruk og antall plasser ukjent.')
add('OSMPIR-kure-tasken-s', 'Kurefjorden øst – enkeltbrygge sør for Tasken', 258451, 6584262, 'utelatt_under_terskel', 'Kort brygge uten synlige båter.')
add('USER-ENGHOLM', 'Brukereksempel Engholmveien/Larkollveien', 254500, 6584150, 'utenfor_kommunen_allerede_godkjent_i_moss', 'Ligger i Moss og er dekket av godkjent polygon 3103-H07-B01 (Nasle bryggesameie – Rørvika øst). Ingen endring.')
(P / 'candidate-ledger.json').write_text(json.dumps(L, ensure_ascii=False, indent=1) + '\n')
with (P / 'candidate-ledger.csv').open('w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(L[0]), delimiter=';'); w.writeheader()
    w.writerows({k: json.dumps(v, ensure_ascii=False) if isinstance(v, list) else v for k, v in r.items()} for r in L)
pending = [
    dict(kommune='Fredrikstad (3107)', sted='Saltholmen båthavn, søndre del', x_25833=257700, y_25833=6579550, note='Søndre del av Saltnes båtforenings bryggeanlegg ligger utenfor Råde. Cross-group X-SALTHOLMEN-3112-3107.'),
    dict(kommune='Fredrikstad (3107)', sted='Sør for Saltholmen – brygge med mange båter', x_25833=257807, y_25833=6579302, note='Sett i Råde-utsnitt, ikke vurdert.'),
    dict(kommune='Moss (3103, godkjent)', sted='Larkollen/Kurefjorden vest – brygge med båter', x_25833=255300, y_25833=6583600, note='Nærmeste godkjente Moss-polygon er 886 m unna. Ikke behandlet; godkjent Moss-leveranse er ikke endret.')]
(P / 'neighbour-pending.json').write_text(json.dumps(pending, ensure_ascii=False, indent=1) + '\n')
cells = json.loads((P / 'cells.json').read_text()); det = json.loads((P / 'detail-esri.json').read_text())
cov = dict(boundary_source='https://api.kartverket.no/kommuneinfo/v1/kommuner/3112/omrade?utkoordsys=4326', boundary_crs='EPSG:4326',
           working_crs='EPSG:25833', overview_tiles=dict(topo=26, esri=26, size_m=4000, step_m=3600, px=1600),
           shore_cells_1km=len(cells), detail_tiles=len(det), detail_tile_px=1320, detail_tile_m=1100,
           detail_selection='1 km-ruter med 2–99 % vann i topografisk kart, pluss ruter med OSM-objekter. Vannmasken er bare prioritering; resultatet er kontrollert mot oversiktsmosaikk.',
           review_levels=dict(sjo_kyst='detaljkontroll av 39 kystfliser (ca. 2,2 m/px i kontaktark) og 10 zoomutsnitt på 0,67 m/px ved alle anlegg',
                              vansjo_og_elv='oversiktskontroll av 66 fliser (ca. 2,75 m/px i kontaktark); zoom ved to OSM-slipper og Grimstadstøa. Vårbilder uten båter; små fellesbrygger kan være oversett',
                              sosteroyene='kontrollert i kystfliser; ingen bryggeanlegg sett',
                              smaa_vann_under_2_prosent='bare oversiktsmosaikk'),
           gaps=['Vansjø-strendene er ikke detaljkontrollert fortløpende i høy oppløsning.',
                 'Esri-eksport med 0,5 m/px ga HTTP 500/tom href; 0,67 m/px ble brukt.', 'Overpass-hovedtjenesten svarte 406/502; speilet overpass.private.coffee ble brukt.'],
           osm_pier_crosscheck='Etter brukerinnspill: 99 OSM-pirer/-moloer innen 50 m av Råde hentet med geometri (maps.mail.ru-speil) og sjekket mot polygonene. 58 lå over 30 m fra et polygon; alle klynger er vurdert i zoom eller tidligere detaljbilde. Ingen nye kvalifiserende anlegg i Råde. Se osm-uncovered-piers.json.',
           images_downloaded=len(list((P / 'images').glob('*.json'))))
(P / 'coverage.json').write_text(json.dumps(cov, ensure_ascii=False, indent=1) + '\n')
src = dict(osm_overpass=dict(endpoint='https://overpass.private.coffee/api/interpreter', file='raw/overpass-rade.json', note='11 kandidater/slipper og 91 pirer innen 300 m av kommunen'),
           nominatim='raw/nominatim-*.json', brreg='raw/brreg-*.json',
           operators={'Råde båtforening': 'https://www.rbf.no/index.php/batplasser (402 plasser, 4 gjesteplasser)',
                      'Saltnes båtforening': 'https://saltnesbf.no/?page_id=19 (220 bryggeplasser; 325 medlemmer pr 1.1.2021)'},
           kommune='Kommunedelplan for Saltnesområdet 2007–2019 (vedtaksdato angitt i filnavn som 210607): to småbåthavner, Saltholmen (190) og Makrellrød (280); historiske tall. Lokal kopi raw/kommunedelplan-saltnes-2007.pdf',
           property_listing='https://www.finn.no/385649027 (Nordre Tasken: felles bryggeanlegg ved Kurefjorden)',
           not_found='Ingen kommunal temakartdatabase eller fullstendig havneliste for Råde ble funnet.')
(P / 'source-notes.json').write_text(json.dumps(src, ensure_ascii=False, indent=1) + '\n')
print(len(L), 'loggrader')

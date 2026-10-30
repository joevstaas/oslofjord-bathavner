"""Felles hjelpere for decisions.py (metode 1.2). inc() / exc() / man() skriver til D."""
import json
from pathlib import Path
P = Path('.')
D = {}
NEAR = json.loads((P / 'raw/nearnames.json').read_text()) if (P / 'raw/nearnames.json').exists() else {}
AUTO = {c['cid']: c for c in json.loads((P / 'auto-candidates.json').read_text())}
EXC_SMALL = 'Enkeltbrygge(r) med få synlige båter; ikke dokumentert felles anlegg med minst 10 plasser.'
EXC_PRIV = 'Spredte private brygger ved separate eiendommer/hytter; ikke summert.'
BR = 'https://virksomhet.brreg.no/nb/oppslag/enheter/'
PREF = ('Brygge', 'Vik i sjø', 'Våg i sjø', 'Nes i sjø', 'Sund i sjø', 'Strand i sjø', 'Halvøy i sjø', 'Øy i sjø', 'Holme i sjø')

def autoname(cid):
    marks = [m['name'] for m in AUTO.get(cid, {}).get('marks', []) if m.get('name')]
    if marks: return ' / '.join(dict.fromkeys(marks)), False
    for t in PREF:
        for n in NEAR.get(cid, []):
            if n.endswith(f'({t})'): return n.split(' (')[0] + ' – båthavn', True
    return f'Båthavn {cid}', True

def inc(cid, cls='s', unc=False, name=None, note='', group=None, sources=(), osm=(), action='inc', descr=None, **kw):
    nm, d0 = (name, True if descr is None else descr) if name else autoname(cid)
    D[cid] = dict(action=action, group=group or cid, name=nm, descr=d0 if descr is None else descr,
                  cls='smabathavn' if cls == 's' else 'mulig_smabathavn',
                  basis=kw.pop('basis', 'minst_10_synlige_plasser_i_sammenhengende_anlegg' if cls == 's' else 'flere_brygger_men_felles_drift_eller_kapasitet_uklar'),
                  unc=unc or cls == 'm', note=note, sources=list(sources), osm=list(osm), **kw)

def exc(cids, why=EXC_SMALL):
    for c in cids.split(): D[c] = dict(action='exc', why=why)

def man(cid, coords, **kw):
    inc(cid, action='man', coords=coords, **kw)

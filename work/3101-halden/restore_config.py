"""Gjenopprett lette, bevarte analyseinnganger uten å overskrive lokale filer."""
from pathlib import Path
import shutil
P=Path(__file__).parent;O=P.parents[1]/'data/kommuner/3101-halden/rev-01'
for d in ['raw','images','qa']:(P/d).mkdir(parents=True,exist_ok=True)
for src in (O/'analysis-config').glob('*.json'):
 dst=P/src.name
 if not dst.exists():shutil.copyfile(src,dst)
for src,dst in [(O/'kommunegrense.geojson',P/'kommunegrense.geojson'),(O/'source-candidates.json',P/'source-candidates.json')]:
 if not dst.exists():shutil.copyfile(src,dst)
print('Lette konfigurasjoner gjenopprettet. Bilde-/råkildepakken må finnes separat.')

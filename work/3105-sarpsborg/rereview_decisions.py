"""Brukerens seks skjermbilder stedfestet mot bevarte flybilder. Bygger på rev-01 uten å slette gamle omriss."""
import runpy
from pathlib import Path
ns=runpy.run_path(str(Path(__file__).parent/'decisions.py'));D=ns['D'];inc=ns['inc'];omit=ns['omit']
# Funksjonenes globale D er samme objekt som D over.
for cid in ['U02A','U02B','U02C','U02D','U03','U04','U05','U06','U06B']:
 omit(cid,'Søke-/lokaliseringsramme for brukerinnspill. Ikke et selvstendig havnefunn.')
inc('U02N','Øketangen – nordre båtplassbrygge',[('U02E',[(440,10),(555,25),(555,55),(440,40)])],['user-provided:2026-10-31/image-2'],possible=True,note='Brukerens bilde 2, stedfestet via grått hus, bukter og brygger. Samlet pir med plasser; nøyaktig kapasitet/felles drift ikke avklart. Ikke summert med søndre pir.')
inc('U02S','Øketangen – søndre båtplassbrygge',[('U02E',[(395,100),(425,100),(435,195),(400,205)])],['user-provided:2026-10-31/image-2'],possible=True,note='Brukerens bilde 2. Egen fysisk pir med plassrekke; kapasitet og organisering uklare. Holdt som egen mulig gruppe, uten aggregering med nordre pir.')
inc('U03M','Materialgården – søndre båtplassanlegg',[('U03B',[(435,500),(495,500),(495,580),(425,575),(425,560),(470,565),(475,505)])],['user-provided:2026-10-31/image-3'],possible=True,note='L-formet brygge med faste plasser, tydelig i brukerbildet. Tidligere oversett som en del av strand-/moloområde. Nordre molo og små enkeltbrygger er ikke automatisk havn.')
inc('U04K','Karlsøy bru – båtplassbrygger ved sørenden',[('U04B',[(350,305),(385,305),(360,380),(340,370)]),('U04B',[(415,320),(450,320),(400,405),(380,400)])],['user-provided:2026-10-31/image-4'],note='To plasserte båtplasspirer ved samme lille havnefront sørøst for brua. Brukerbildet viser samlet plassmønster over ti plasser. Bru, bygning og land er holdt utenfor.')
inc('U05J','Bjerkenes – nordvestre fellesbrygge',[('U05B',[(435,350),(465,330),(505,400),(485,420)])],['user-provided:2026-10-31/image-5'],note='Tydelig tosidig fellespir med mer enn ti avgrensede plasser i brukerbildet. Ikke samme brygge som C047 på østsiden av neset. Østre små private pir er utelatt.')
inc('U06N','Kapellanveien – nordre av to sørlige båtplasspirer',[('U06C',[(215,555),(255,545),(265,575),(225,590)])],['user-provided:2026-10-31/image-6'],possible=True,note='Brukerbildet viser utriggere på begge sider; kapasitet rundt prosjektgrensen og felles drift ikke dokumentert. Egen foreløpig gruppe. Små enkeltpirer lenger nord utelates.')
inc('U06S','Kapellanveien – søndre båtplasspir',[('U06C',[(225,615),(270,625),(270,650),(225,645)])],['user-provided:2026-10-31/image-6'],possible=True,note='Egen fysisk pir med tosidig plassmønster i brukerbildet; antall/felles drift må bekreftes. Ikke summert med nabopiren for å nå terskelen.')
for cid,rel in [('U02E',['U02N','U02S']),('U03B',['U03M']),('U04B',['U04K']),('U05B',['U05J']),('U06C',['U06N','U06S'])]:omit(cid,'Stedfestet kontrollramme for brukerinnspill; se relaterte sjøpolygoner.',rel)
REPORT=ns['REPORT']
rep=ns['rep']
rep('U03M',[('U03B',[(465,505),(490,505),(490,580),(425,580),(425,560),(465,560)])])
rep('U04K',[('U04B',[(335,300),(385,300),(365,385),(335,375)]),('U04B',[(415,310),(455,310),(410,405),(375,400)])])
rep('U05J',[('U05B',[(420,345),(455,325),(510,405),(480,435)])])
omit('U02F','Detaljramme for nordre Øketangen-pir; U02N.', ['U02N'])
rep('U02N',[('U02F',[(265,370),(350,370),(405,390),(455,400),(455,420),(270,405)])])

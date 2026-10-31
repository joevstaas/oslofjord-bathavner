"""Registrer ferdig analyse som avventende; endrer aldri godkjente samledata."""
import json,datetime,time,shutil
from pathlib import Path
P=Path(__file__).parent;R=P.parents[1];O=R/'data/kommuner/3207-nordre-follo/rev-01'
assert not (O/'approval.json').exists(), 'Godkjent revisjon må ikke overskrives; opprett ny revisjon.'
now=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds');run=json.loads((P/'run.json').read_text());run.update(finished_utc=now,elapsed_wall_seconds=round(time.time()-run['started_unix']),tokens_measured=None,cost_measured=None,note='Veggklokketid fra oppstart, inkludert nettventing og kontekstoverføring; ikke ren prosessortid.')
(O/'timing.json').write_text(json.dumps(run,ensure_ascii=False,indent=1)+'\n')
for fn in ['kommunegrense.geojson','pier-review-index.json']:shutil.copy2(P/fn,O/fn)
provenance=[]
for f in sorted((P/'raw').glob('*provenance.json')):provenance.append(dict(local_source=str(f.relative_to(R)),**json.loads(f.read_text())))
(O/'source-provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=1)+'\n')
coverage=dict(scope='Hele kommunens OSM-kystlinje med 20 m grensemargin dekket av 14 sammenhengende, overlappende bildefliser. Kontaktark gjennomgått uavhengig av kandidater; 58 kartlagte brygger detaljkontrollert. 17 bildefliser rundt innlandsbrygger er en kandidatsjekk, ikke fullstendig innsjøkartlegging.',coastal_review_sheets=[f'work/3207-nordre-follo/qa/coast-sheet-{n}.jpg' for n in range(3)],inland_review_sheets=[f'work/3207-nordre-follo/qa/inland-sheet-{n}.jpg' for n in range(3)],pier_review_sheets=[f'work/3207-nordre-follo/qa/piers-{n:02}.jpg' for n in range(10)],final_outline_review='work/3207-nordre-follo/qa/qa-0.jpg',reviewed_utc=now,limitations=['OSM-kystlinjen er et søkegrunnlag, ikke bevis på fullstendighet.','Flybildenes opptaksdato er ukjent; innhentingsdato er ikke opptaksdato.','Ingen feltbefaring, operatørkontakt eller uavhengig kapasitetsmåling.','Foreningsregister gir organisasjonsidentitet, ikke havneposisjon.','Bildene er beholdt lokalt sammen med georeferering og sjekksum. De er ikke publisert i Git; tilsvarende ny nedlasting garanterer ikke samme mosaikk.'])
(O/'coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=1)+'\n')
s=json.loads((R/'status.json').read_text());record=dict(name='Nordre Follo',code='3207',status='til_godkjenning',revision=1,method_version='1.2',schema_version='1.1',started_utc=run['started_utc'],finished_utc=now,elapsed_wall_seconds=run['elapsed_wall_seconds'],result=str((O/'bathavner.geojson').relative_to(R)),metadata=str((O/'metadata.csv').relative_to(R)),polygons=2,harbours=2,possible_harbours=1,saltwater_harbours=1,possible_freshwater_harbours=1,uncertain_geometries=1,work_dir=str(P.relative_to(R)),approved_utc=None)
s['municipalities']=[m for m in s['municipalities'] if m['code']!='3207']+[record];s['updated_utc']=now;s['in_progress']='Nordre Follo rev-01 ferdig til godkjenning: én dokumentert saltvannshavn og én mulig ferskvannshavn. Samlefil/nettsted uendret. Ingen neste kommune startet.';s['next_municipality_started']=False
(R/'status.json').write_text(json.dumps(s,ensure_ascii=False,indent=1)+'\n')
print('registered pending',run['elapsed_wall_seconds'],'seconds')

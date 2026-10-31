"""Ferdigstill kommuneleveranse til godkjenning; ingen innlemming eller godkjenning."""
import json,hashlib,datetime,time,shutil
from pathlib import Path
P=Path(__file__).parent;R=P.parents[1];O=R/'data/kommuner/3212-nesodden/rev-01'
assert not (O/'approval.json').exists(),'Godkjent revisjon må ikke overskrives.'
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=1)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds');run=json.loads((P/'run.json').read_text());summary=json.loads((O/'summary.json').read_text());val=json.loads((O/'validation.json').read_text())
run.update(finished_utc=now,elapsed_wall_seconds=round(time.time()-run['started_unix']),tokens_measured=None,cost_measured=None,note='Målt veggklokketid fra oppstart, inkludert nettventing og gjentatte tjenestefeil. Ikke ren prosessortid.')
write(O/'timing.json',run)
for fn in ['kommunegrense.geojson','cluster-review-index.json','clusters.json']:
 shutil.copy2(P/fn,O/fn)
shutil.copy2(P/'decisions.py',O/'decisions.py')
provenance=[]
for p in sorted((P/'raw').glob('*provenance.json')):provenance.append(dict(local_source=str(p.relative_to(R)),**json.loads(p.read_text())))
write(O/'source-provenance.json',provenance)
write(O/'coverage.json',dict(scope='Systematisk kystsøk, også Steilene, Ildjernet, Langøyene og småøyer i kommunegrensen. Ett supplerende innlandsutsnitt er ikke komplett ferskvannskartlegging.',coastline_source='Fire fullstendige OSM-delruter, lagret separat med spørring, svar og proveniens.',osm_coast_length_m=val['osm_coast_length_m'],coast_tiles=val['coast_tiles'],additional_images=val['additional_images'],coast_outside_image_coverage_m=val['osm_coast_outside_image_coverage_m'],coast_contact_sheets=[f'work/3212-nesodden/qa/coast-sheet-{n}.jpg' for n in range(11)],cluster_review_index='cluster-review-index.json',clusters_reviewed=84,piers_in_clusters=310,independent_gap_sweep='Alle 65 kystfliser er gjennomgått på kontaktark uavhengig av kandidatlisten; ingen ekstra sikker havnepolygon utenfor kandidatene påvist. Dette er ikke bevis på fullstendighet.',final_outline_qa=[f'work/3212-nesodden/qa/qa-{n}.jpg' for n in range(2)],limitations=['Ukjent opptaksdato og posisjonsnøyaktighet; eksportoppløsning er ikke målenøyaktighet.','Gjesteplasser, medlemmer og total kapasitet holdes atskilt.','Industri-, service-, rutebåt- og badebrygger kvalifiserer ikke alene.','Ett mislykket ekstra detaljutsnitt C007 ble erstattet med kontroll i eksisterende georeferert kystflis.','Originalbilder og råkilder er beholdt lokalt; ikke publisert i Git. Ny nedlasting kan gi en annen mosaikk.'],reviewed_utc=now))
write(O/'open-questions.json',[
 dict(id='S001',place='Bomansvik',need='Operatørkilde eller datert bilde som stedfester faste båtplasser og gjør sjøomrisset etterprøvbart.',polygon_exported=False),
 dict(id='S002',place='Kavringstrand',need='Avklar om de mulige bryggene øst for Kavringen er eget felles anlegg, hvem som driver dem og om de hører til samme fysiske havnegruppe som Kavringen.',polygon_exported=True,candidate_id='C053E'),
 dict(id='S003',place='Steilene østlige kaier',need='Avklar faste plasser/gjestebruk kontra jolle-/service-/anløpsbruk og fysisk omfang etter ombygging.',polygon_exported=False),
 dict(id='S004',place='Ildjernet',need='Bekreft felles organisering og antall faste plasser i C024/C028; kandidatenes klassifisering forblir mulig.',polygon_exported=True),
 dict(id='S005',place='Spro og Steilene',need='Datert ortofoto etter omtalt ferdigstillelse/fornyelse for å kontrollere at bildet viser dagens utstrekning.',polygon_exported=True)])
st=json.loads((R/'status.json').read_text());record=dict(name='Nesodden',code='3212',status='til_godkjenning',revision=1,method_version='1.2',schema_version='1.1',started_utc=run['started_utc'],finished_utc=now,elapsed_wall_seconds=run['elapsed_wall_seconds'],result=str((O/'bathavner.geojson').relative_to(R)),metadata=str((O/'metadata.csv').relative_to(R)),candidate_ledger=str((O/'candidate-ledger.json').relative_to(R)),polygons=summary['polygons'],harbours=summary['harbours'],possible_harbours=summary['possible_harbours'],uncertain_geometries=summary['uncertain_geometries'],approved_utc=None,work_dir=str(P.relative_to(R)))
st['municipalities']=[m for m in st['municipalities'] if m['code']!='3212']+[record];st.update(updated_utc=now,in_progress='Nesodden rev-01 ferdig til godkjenning: 11 polygoner / 11 anleggsgrupper, inkludert 3 mulige. Godkjente samledata og nettsted uendret. Ingen neste kommune startet.',next_municipality_started=False)
write(R/'status.json',st);print('finished',run['elapsed_wall_seconds'],'seconds')

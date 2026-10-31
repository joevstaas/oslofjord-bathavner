"""Ferdigstill bare Frogn til godkjenning; bevar godkjente samledata og nettsted."""
import json,hashlib,datetime,time,shutil,math
from pathlib import Path
P=Path(__file__).parent;R=P.parents[1];O=R/'data/kommuner/3214-frogn/rev-01'
assert not (O/'approval.json').exists()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=1)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds');run=json.loads((P/'run.json').read_text());s=json.loads((O/'summary.json').read_text());v=json.loads((O/'validation.json').read_text())
run.update(finished_utc=now,elapsed_wall_seconds=round(time.time()-run['started_unix']),tokens_measured=None,cost_measured=None,note='Målt veggklokketid fra oppstart, inkludert tjenestefeil og nettventing; ikke ren prosessortid.')
write(O/'timing.json',run)
for fn in ['kommunegrense.geojson','cluster-review-index.json','clusters.json','open-questions.json','decisions.py']:shutil.copy2(P/fn,O/fn)
provenance=[]
for p in sorted((P/'raw').glob('*provenance.json')):
 m=json.loads(p.read_text());matches=[f for f in (P/'raw').iterdir() if f.is_file() and not f.name.endswith('provenance.json') and hashlib.sha256(f.read_bytes()).hexdigest()==m.get('sha256')]
 m['archived_response_files']=[str(f.relative_to(R)) for f in matches];assert matches,p
 provenance.append(dict(local_provenance=str(p.relative_to(R)),**m))
write(O/'source-provenance.json',provenance)
write(O/'image-requests.json',json.loads((P/'specs.json').read_text())+json.loads((P/'detail-specs-wide.json').read_text()))
write(O/'coverage.json',dict(scope='Systematisk bildegjennomgang av kyst inkl. Håøya, Kaholmene/Oscarsborg, Bergholmen, øyer i Hallangspollen og Bunnefjorden innenfor offisiell kommunegrense. Innlandet er ikke systematisk bildesøkt.',coastline_source='Fire komplette OSM-delruter med spørring, råsvar og proveniens.',osm_coast_length_m=v['osm_coast_length_m'],coast_tiles=79,additional_images=8,coast_outside_image_coverage_m=v['osm_coast_outside_image_coverage_m'],coast_contact_sheets=[f'work/3214-frogn/qa/coast-sheet-{n}.jpg' for n in range(14)],cluster_review_index='cluster-review-index.json',clusters_reviewed=81,piers_in_clusters=256,independent_gap_sweep='Alle 79 kystfliser visuelt kontrollert på kontaktark uavhengig av OSM-klyngene. Solbergstrand G001 og Bergholmen G003/G004 har fått egne polygoner uten OSM-pirer. G002 var duplikat av C068 og er slettet etter overlappskontroll. Ingen fullstendighetspåstand.',final_outline_qa=[f'work/3214-frogn/qa/qa-{n}.jpg' for n in range(4)],final_outline_qa_reviewed=True,limitations=['Opptaksdato og posisjonsnøyaktighet ukjent. Eksportoppløsning er ikke målenøyaktighet.','Flere operatører i samme fysiske anleggsgruppe; ingen eiendoms-/operatørgrenser hevdes.','Private nabobrygger summeres ikke til ti-plassregelen; service-/ferge-/badebruk er ikke havnebevis.','Smale detaljforespørsler feilet; åtte ekstra 1100m-ruter ble brukt i stedet. Alle 87 bilder er fullstendig dekodet og hashkontrollert.','Originalbilder og råkilder ligger lokalt, er ikke i Git. Ny nedlasting kan gi en annen mosaikk.','Solbukta er en åpen kandidat uten nåtidspolygon fordi udatert bilde og skadereferat ikke bekrefter dagens anlegg.'],reviewed_utc=now))
record=dict(name='Frogn',code='3214',status='til_godkjenning',revision=1,method_version='1.2',schema_version='1.1',started_utc=run['started_utc'],finished_utc=now,elapsed_wall_seconds=run['elapsed_wall_seconds'],result=str((O/'bathavner.geojson').relative_to(R)),metadata=str((O/'metadata.csv').relative_to(R)),candidate_ledger=str((O/'candidate-ledger.json').relative_to(R)),polygons=s['polygons'],harbours=s['harbours'],possible_harbours=s['possible_harbours'],uncertain_geometries=s['uncertain_geometries'],approved_utc=None,work_dir=str(P.relative_to(R)))
st=json.loads((R/'status.json').read_text());st['municipalities']=[m for m in st['municipalities'] if m['code']!='3214']+[record]
st.update(updated_utc=now,in_progress=f"Frogn rev-01 til godkjenning: {s['polygons']} polygoner / {s['harbours']} anleggsgrupper, inkludert {s['possible_harbours']} mulig. Samlet 469 godkjente polygoner / 16 kommuner og nettsted uendret. Vestby ikke startet.",next_municipality_started=False)
write(R/'status.json',st);print('finished',run['elapsed_wall_seconds'],'seconds')

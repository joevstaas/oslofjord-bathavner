# Halden – rev-01 godkjent

**66 polygoner / 31 foreløpige anleggsgrupper**, inkludert **11 mulige havner**. Alle avgrensninger har kontrollbehov; lokal bildedato og absolutt nøyaktighet er ukjent. Brukeren godkjente revisjonen 2026-10-31T16:48:04Z. Alle 66 polygonene er innlemmet i samledata og nettstedets lokale kartdata. Kjente usikkerheter er beholdt.

`bathavner.geojson` er WGS84. `metadata.csv` har semikolon og én identisk egenskapsrad per polygon. Gruppene beskriver foreløpige fysiske anlegg, ikke en opptelling av juridiske operatører. `candidate-ledger.json/.csv` dekker 29 OSM-klynger, 25 ekstra kontrollrammer og tre delkandidater. `source-candidates.json` dokumenterer kommunekart, foreninger, planer og Haldenkanalen.

Kysten er systematisk bildesøkt i 125 celler à 500 m / 32 ark. 77 OSM-pirer i 29 klynger er gjennomgått. Nye anlegg uten egne OSM-pirer er blant annet funnet i Røsneskilen, Mørvik, Ystehedekilen og sørover Idefjorden. 38 kystfliser dekker hele den uttrekte OSM-kystlinjen (78,3 km med 20 m kontrollbelte); dette er ikke et fullstendighetsbevis. Innlandet er bare kandidat- og kildestyrt kontrollert, blant annet ved Tangen og Brekke.

Kommunens båtplassider og elleve vedlegg er sammenholdt med bilder. Sundsbrygga har nå langsidesplasser; gamle utriggere er ikke kopiert. Gjestehavn og faste plasser i sentrum er skilt uten dobbel geometri. Tista er samlet i én foreløpig kommunal/fysisk gruppe med separate sjøbelter. Høvleriet er ombygd siden eldre kartfoto. Vestre Tistasenter syd 2 og en liten Grønland-rekke er ikke sikkert avgrenset. Dokumentert gjestebrygge oppstrøms Brekke står også åpen uten polygon; Anleggsbrygga er levert.

Røsnes har fem Halden-polygoner med grensegruppe `ROSNES-3101-3105`. De overlapper ikke godkjente `3105-H20-B01/B02` i Sarpsborg. Gruppering, driftsforhold og presis grense må fortsatt kontrolleres. Godkjente geometrier er uendret.

Det oppgis ingen total nåtidskapasitet. Felleskjøpets tre store langsidesplasser og kommunens små gjestedelopplysninger ligger som ikke-additive `capacity_components`, med avgrenset kildeomfang. Velbryggas 28 plasser i 2022 er dokumentert, men ikke plassert på en tilfeldig Sponvika-polygon. Planforslag fra KU 2020 er ikke brukt som eksisterende havneareal. Landopplag, ramper, sluser, rene industrikaier og spredte private brygger er utelatt.

Alle 66 endelige omriss er kontrollert visuelt med eksportert GeoJSON som overlegg. Teknisk kontroll: gyldige geometrier, unike ID-er, 0 m² utenfor kommunen, ingen intern overlapp eller overlapp med de 692 godkjente polygonene, fullstendig CSV-samsvar. SHA-256 bekrefter uendret godkjent grunnlag. Se `validation.json`, `visual-review.json`, `coverage.json` og de elleve punktene i `open-questions.json`. Solglitter begrenser særlig Knivsø og Unnebergstranda.

Originalbilder, native EPSG:3857-bilder, omprojiserte UTM-bilder, mosaikker, rå XML/PDF/HTML og QA ligger lokalt i `work/3101-halden/`, utenfor Git. `imagery-manifest.json` og `source-manifest.json` bevarer kildehenvisninger, forespørsler, dimensjoner, transformasjoner og hasher. Bevar denne råpakken separat for identisk visuell etterprøving. Pikselstørrelsen i et avledet bilde er ikke opptaksoppløsning. `source-access-limitations.json` oppgir kilder der rå HTML ikke lot seg laste ned.

Skript: `work/3101-halden/build.py`, `qa.py`, `validate.py`, `finalize.py` og `restore_config.py`. Lette innganger er bevart i `analysis-config/`. En ny nedlasting kan gi andre bilder og er ikke identisk rekonstruksjon. Bygg/finalisering stopper ved godkjent revisjon; opprett ny revisjon da. Målt veggklokke: 1927 sekunder; tokens og pris er ikke målt.

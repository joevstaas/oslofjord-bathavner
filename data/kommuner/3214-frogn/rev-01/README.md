# Frogn (3214), rev-01 – godkjent

24 sjøpolygoner / 18 fysiske anleggsgrupper, inkludert én mulig havn (Bergholmen, to polygoner). Ti polygoner har usikker avgrensning. Brukergodkjent og innlemmet i samledata og nettstedets lokale kartdata. Samlet 493 polygoner / 17 kommuner. Vestby er ikke startet. Godkjenningen beholder alle usikkerheter; den bekrefter ikke dagens kapasitet, drift eller fullstendighet.

## Filer

- `bathavner.geojson`: WGS84/EPSG:4326, én feature per sjøpolygon. `harbour_id` grupperer deler av samme fysiske anlegg; dette er ikke et register over eksklusive operatører.
- `metadata.csv`: samme egenskaper, UTF-8 BOM og semikolon.
- `candidate-ledger.json` / `.csv`: alle 81 OSM-klynger, tre ekstra bildesøk-kandidater og fem åpne kildeavklaringer.
- `digitisation.json`, `decisions.py`, `clusters.json`, `cluster-review-index.json`: endelige beslutninger, piksler og georefererte kontrollutsnitt.
- `kommunegrense.geojson`, `coverage.json`, `imagery-manifest.json`, `image-requests.json`, `source-provenance.json`: grense, dekning, forespørsler, kilder, innhentingstid og SHA-256.
- `validation.json`, `summary.json`, `open-questions.json`, `timing.json`: kontroller, tall, avklaringer og målt veggklokketid.

## Resultat

| Anleggs-ID | Navn / fysisk gruppe | Polygoner | Klasse |
| --- | --- | ---: | --- |
| 3214-H01 | Dragsund, Håøya | 2 | smabathavn |
| 3214-H02 | Nordvestre Frogn | 1 | smabathavn |
| 3214-H03 | Tåjebukta, Håøya | 1 | smabathavn |
| 3214-H04 | Hallangspollen | 1 | smabathavn |
| 3214-H05 | Hallangspollen | 1 | smabathavn |
| 3214-H06 | Hallangspollen | 2 | smabathavn |
| 3214-H07 | Gylteholmen Brygger | 1 | smabathavn |
| 3214-H08 | Oscarsborg Gjestehavn | 1 | smabathavn |
| 3214-H09 | Vindfangerbukta / Husvikholmen | 3 | smabathavn |
| 3214-H10 | Drøbak Båtforening | 1 | smabathavn |
| 3214-H11 | Drøbak Gjestehavn | 1 | smabathavn |
| 3214-H12 | Hallangspollen | 1 | smabathavn |
| 3214-H13 | Hallangspollen | 1 | smabathavn |
| 3214-H14 | Hallangspollen | 1 | smabathavn |
| 3214-H15 | Stakabukta | 2 | smabathavn |
| 3214-H16 | Bunnefjorden | 1 | smabathavn |
| 3214-H17 | Solbergstrand | 1 | smabathavn |
| 3214-H18 | Bergholmen | 2 | mulig_smabathavn |

## Kildebelagt kapasitet

| Anlegg | Publisert opplysning | Omfang og forbehold |
| --- | --- | --- |
| Tåjebukta | 90 gjesteplasser | Leverandørens beskrivelse av bygget prosjekt, ukjent referanseperiode. Ikke ny kapasitetsmåling. |
| Gylteholmen Brygger | 68 faste plasser + 12 faste gjesteplasser | 68 er ikke total inkl. gjester. 12 er egen `capacity_components`-observasjon. |
| Oscarsborg Gjestehavn | ca. 110 båter | Hele gjestehavnen; ikke hver brygge eller fergekai. |
| Drøbak Gjestehavn | 48 gjesteplasser | Visit Greater Oslo; hele gjestehavnen, ukjent referanseperiode. |

Kilder: [SF Marina](https://sfmarina.com/sf-projects/haoya/), [Gylteholmen](https://www.gylteholmenbrygger.no/), [Oscarsborg](https://oscarsborggjestehavn.no/), [Visit Greater Oslo](https://visitgreateroslo.com/no/drobak-gjestehavn). Feltet `current_operation_verified` er false; kapasitet er publiserte kildeverdier, ikke bekreftet drift i dag. Medlemstall, sengeplasser og landopplag er ikke telt som båtplasser.

## Åpne avklaringer og begrensninger

- Gylteåsen Båthavn oppgis med 70 plasser i Frogn foreningsportal. Gylteveien 4 peker mot nordre Vindfangerbukta, men eksakte delbrygger er ikke bekreftet. Tallet er ikke lagt på hele havnegruppen eller på et anlegg lenger nord med lignende navn.
- Solbukta: en udatert bildemosaikk viser fingerbrygge, mens BirdLife-referatet som vises i august 2026-kalenderen omtaler hele anlegget som ødelagt og på land. Hendelsesår og eventuell gjenetablering er ikke uavhengig verifisert. Åpen kandidat uten nåtidspolygon; ikke bevis på at havnen aldri har eksistert.
- Bergholmen har dokumentert besøks-/kystledbruk og brygger, men ti faste plasser er ikke bekreftet. Begge delpolygoner klassifiseres mulig; ferge-/servicebruk og små kaikantavgrensninger trenger kontroll.
- Torkildstranda Båtforening og Fløyspjeld Båtforening er registrerte navn. Foreningsadresse beviser ikke hvilke sjøbrygger de disponerer. C081 beholdes med geografisk navn, uten operatørtilordning.
- Dragsunds to brygger er koordinatkontrollert mot kildens beskrivelse av ytre ny og indre eldre brygge og ført som én fysisk gruppe. Tåjebukta ligger lenger sør. Håøya og Bergholmen tilhører geografisk Frogn; eierskap hos Oslo kommune endrer ikke dette.
- Vindfangerbukta/Husvikholmen er én fysisk gruppe i tre sjøpolygoner. Operatøransvar fordeles ikke uten kartbelegg. Hallangspollens separate anlegg får beskrivende navn.
- 79 kystfliser og åtte ekstra detaljfliser, ca. 76,29 km OSM-kyst innenfor kommunegrensen med 20 m toleranse. Full dekning av denne kystlinjen er teknisk kontrollert; det er ikke bevis på fullstendighet. Innlandet er ikke systematisk bildesøkt.
- Opptaksdato, absolutt posisjonsnøyaktighet og aktuell drift er ukjent. Ca. 0,733 m eksportpiksel er ikke målenøyaktighet. Omrissene er foreløpige kartleggingsforslag, ikke juridiske grenser.

## Kontroll

Alle 24 eksporterte omriss er projisert tilbake på originalbildene og visuelt kontrollert. Overlappskontrollen avdekket at bildesøk-kandidat G002 var samme brygge som C068; duplikatet ble fjernet. Unike ID-er, gyldig geometri, kommunegrense, null overlapp internt/mot 469 godkjente polygoner, CSV-samsvar og bildehash/dekoding er validert. Ved godkjenning ble Frogn lagt til samlefilen. De 469 tidligere features er bevart uendret med kanonisk SHA-256 i `approval.json`. Nettstedets kartdata og tellinger er oppdatert. Publisering skjer etter merge/utrulling.

## Lokalt underlag og reproduksjon

Originalbilder med JSON-georeferering og råkilder ligger i `work/3214-frogn/images/` og `raw/`, kontrollark i `qa/`. Disse er ignorert av Git og må tas vare på separat for identisk visuell etterprøving. Kildenes publiseringsvilkår gjelder; en ny nedlasting kan gi en annen mosaikk.

Bruk prosjektets `.venv` og tilpassede skript i `work/3214-frogn/`. For ny rekonstruksjon må råsvar/bilder gjenskapes fra lagrede forespørsler/proveniens eller tilbakeføres fra lokalt arkiv. Kopier `open-questions.json` til arbeidsmappen. Kjør `clusters.py`, `review_clusters.py`, deretter `gap_frames.py` (de to ekstra Bergholmen-rammene). Gjenbruk leveransens endelige `decisions.py`. Kjør `build.py`, `qa.py`, kontroller hvert omriss på nytt, og `validate.py`. `finalize.py` skriver status/timing og skal ikke brukes ukritisk etter godkjenning. Godkjent rev-01 må ikke overskrives; lag ny revisjon ved senere endringer.

Målt veggklokketid ligger i `timing.json`; tokens og kostnad er ikke målt.

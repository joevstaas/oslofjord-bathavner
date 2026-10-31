# Bamble (4012) – revisjon 1 til godkjenning

Analysert 31. oktober 2026 etter brukerens bestilling. **38 anleggsgrupper / 43 polygoner, inkludert sju mulige havner.** 17 polygoner har usikker avgrensning. Åtte anlegg (H31–H38) ble lagt til etter brukerinnspill i to runder, og Vinjestranda (H11) ble oppgradert fra mulig til småbåthavn. Leveransen venter på brukerens godkjenning; samlefil og nettsted er ikke endret (fortsatt 469 polygoner / 16 kommuner). Ingen neste kommune er startet.

| ID | Anlegg/kandidat | Klasse | Polygoner | Publisert kapasitet |
|---|---|---|---:|---:|
| 4012-H01 | Prestvika – båthavn | Småbåthavn | 1 | |
| 4012-H02 | Vallekjær – bryggeanlegg | Småbåthavn | 1 | |
| 4012-H03 | Valle gjestehavn / Sjøbua Marina | Småbåthavn | 2 | ca. 120 båter (gjestehavn) |
| 4012-H04 | Finmarkstranda – langbrygge | Småbåthavn | 1 | |
| 4012-H05 | Havsund marina | Småbåthavn | 1 | |
| 4012-H06 | Sekkekilen vest – langbrygge | Småbåthavn | 1 | |
| 4012-H07 | Sekkekilen øst – langbrygge | Småbåthavn | 1 | |
| 4012-H08 | Isdammen Marina | Småbåthavn | 1 | |
| 4012-H09 | Skjerkebukta – brygger ved båtsenter | Mulig | 1 | |
| 4012-H10 | Stathelle vest ved Martha Cochs vei – flytebryggeanlegg | Småbåthavn | 1 | |
| 4012-H11 | Vinjestranda – langbrygge (oppgradert etter brukerinnspill) | Småbåthavn | 1 | |
| 4012-H12 | Strandsletta båthavn og camping | Småbåthavn | 2 | |
| 4012-H13 | Stathelle gjestehavn og småbåthavn ved Parken | Småbåthavn | 1 | |
| 4012-H14 | Stathelle Marina | Småbåthavn | 1 | 445 |
| 4012-H15 | Salen båthavn | Småbåthavn | 2 | |
| 4012-H16 | Ørvik nord – firkantet flytebrygge | Småbåthavn | 1 | |
| 4012-H17 | Langesund småbåthavn (OSM-navn) | Småbåthavn | 1 | |
| 4012-H18 | Stoa båthavn | Småbåthavn | 1 | |
| 4012-H19 | Langøya gjestehavn | Småbåthavn | 1 | |
| 4012-H20 | Langesund gjestehavn – Dampskipsbrygga | Småbåthavn | 1 | |
| 4012-H21 | Langesund gjestehavn – Kongshavn | Småbåthavn | 1 | |
| 4012-H22 | Sildeberget – marina | Småbåthavn | 1 | |
| 4012-H23 | Prisgrunnbukta – mulig felles brygge i vik | Mulig | 1 | |
| 4012-H24 | Søndre Eikstrand – mulig båthavn ved Asvallveien | Mulig | 1 | |
| 4012-H25 | Herre (Herrejordet) – bryggerekke i elveløpet | Mulig | 1 | |
| 4012-H26 | Kjøya øst – marina | Småbåthavn | 1 | |
| 4012-H27 | Kjøya vest – brygger | Småbåthavn | 1 | |
| 4012-H28 | Brevikstrand båthavn – vest | Småbåthavn | 1 | |
| 4012-H29 | Brevikstrand båthavn – øst | Småbåthavn | 2 | |
| 4012-H30 | Stangbukta – lite båtbasseng | Mulig | 1 | |
| 4012-H31 | Stranda ved Grosholmen – kaianlegg (brukerinnspill) | Småbåthavn | 1 | |
| 4012-H32 | Havparadiset, Kjønnøya – brygge og kai (brukerinnspill) | Småbåthavn | 1 | |
| 4012-H33 | Sauøya – brygge i Vinjekilen (revurdert etter brukerinnspill) | Småbåthavn | 1 | |
| 4012-H34 | Grunnsundveien – båter langs kai (brukerinnspill) | Mulig | 1 | |
| 4012-H35 | Hafsundveien – bryggeanlegg i vik (brukerinnspill) | Småbåthavn | 1 | |
| 4012-H36 | Trolldalen – molohavn (brukerinnspill) | Småbåthavn | 1 | |
| 4012-H37 | Rognstranda – brygge (brukerinnspill) | Småbåthavn | 1 | |
| 4012-H38 | Vinjekilen – brygger (brukerinnspill) | Mulig | 2 | |

Navn med tankestrek er stedsbeskrivende (`name_is_descriptive=true`) og bygger på Kartverkets stedsnavn ved anlegget. Nabobasseng med ukjent operatør er levert som egne anleggsgrupper; 38 grupper er derfor ikke en påstand om 30 uavhengige operatører. Foreningers registrerte adresse er bare brukt som støtte for navn, aldri som havneposisjon.

## Leveransen

- `bathavner.geojson`: polygoner i WGS84, lengdegrad før breddegrad; status `til_godkjenning`.
- `metadata.csv`: samme egenskaper og rader som GeoJSON, semikolon, UTF-8 med BOM.
- `candidate-ledger.json`/CSV: 40 OSM-pirklynger, 12 kandidater bare fra bildesøket, 7 fra brukerinnspill og 16 åpne kildekandidater eller vurderte brukerinnspill. Hver rad har beslutning og begrunnelse.
- `open-questions.json`: fem avklaringsbehov (Stoa/Langesund, Valle-grensene, mulige anlegg, foreninger uten stedfestet havn, datert ortofoto).
- `neighbour-pending.json`: to bryggeanlegg like utenfor kommunegrensen (M07, M12) og Stråholmen i Kragerø (brukerinnspill).
- `digitisation.json`, `decisions.py`, `cluster-review-index.json`: beslutninger, pikselomriss og georefererte rammer.
- `validation.json`, `coverage.json`, `imagery-manifest.json`, `source-provenance.json`, `timing.json`: kontroll, dekning, kilder og målt tid.

## Metode og dekning

Metode 1.2 / skjema 1.1. Alle omriss er tegnet manuelt i georefererte Esri-bilder (EPSG:25833). 130 kystfliser dekker hele OSM-kystlinjen i kommunen (ca. 224 km, 0 m utenfor bildedekning), og de er gjennomgått på kontaktark uavhengig av OSM. OSM har bare 144 pirer i Bamble. Bildesøket ga 12 ekstra kandidater, blant dem store anlegg uten OSM-pir som Sildeberget, Kjøya og Brevikstrand. 32 detaljbilder er hentet for kandidater som ikke var dekket av én flis. Alle 43 eksporterte omriss er sett som overlegg på kildebildet; omkring 20 ble rettet etter første kontroll (forskyvning, land eller parkering i omrisset). Teknisk validering er bestått: gyldige polygoner, 0 m² utenfor kommunen, ingen overlapp internt eller mot samlefilen, unike ID-er og CSV i samsvar.

Innlandet er ikke systematisk kartlagt. Ett innlandsutsnitt ved en OSM-pir er sett.

## Kilder og kapasiteter

- Bamble kommune: sidene «Havner og havneeiendommer» og «Gjestehavner og uthavner». Kommunale gjestehavner er Kongshavn, Dampskipsbrygga, Langøya og Stathelle; i tillegg har kommunen Stoa båthavn.
- Stathelle Marina: 445 båtplasser ifølge lokalhistoriewiki (Åsenbakken), referanseperiode ukjent.
- Valle: «plass til rundt 120 båter» i gjestehavna ifølge lokalhistoriewiki. Dette er ikke faste plasser og gjelder bare B01.
- Enhetsregisteret: navnestøtte for Isdammen, Strandsletta, Sildeberget, Brevikstrand og Skjerkebukta.
- KNBF: Stathelle og Omegn Båtforening er medlem (126 medlemmer). Medlemstall er ikke kapasitet.
- Ikke hentet: kommunens plan-PDF-er for Stathelle Marina og Vestrestrand svarte 404, og visitnorway.no avviste automatisk henting (403). Dette er loggført og ikke omgått.

## Begrensninger

Ukjent bildeopptaksdato og ukjent posisjonsnøyaktighet. Dagens drift er ikke verifisert. Kontaktarkene er vist med ca. 1,8 m/px. Brukeren påviste ni mangler eller feilvurderinger etter leveransen, hovedsakelig små anlegg langs kai eller brygger uten OSM-pir. Kontaktarkene var klart utilstrekkelige alene, og flere slike anlegg kan finnes. Kommunegrensen fra Kommuneinfo er generalisert. Grensene mellom Valle-aktørene og mellom Stoa og Langesund småbåthavn er ikke dokumentert. Godkjenning vil ikke være en verifikasjon av fullstendighet.

## Brukerinnspill runde 2 som ikke ga nytt polygon

- **Stråholmen:** havna ligger i Kragerø og er ført i `neighbour-pending.json`.
- **Vaterlands gate, Langesund:** rekka av korte private brygger med hver sin landfeste er fortsatt utelatt. Bryggesameiene i gata er registrert, men det dokumenterer ikke ett felles anlegg med faste plasser. Bør avklares mot sameiene.
- **Kyststien, trekantet molobasseng:** kunne ikke stedfestes. Trenger stedsnavn eller koordinat.
- **Rognstranda nord, ved stranda:** brygge med få båter, under ti plasser. Utelatt.

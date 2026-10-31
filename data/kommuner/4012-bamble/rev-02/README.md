# Bamble (4012) – revisjon 2 til godkjenning

**53 anleggsgrupper / 59 polygoner**, inkludert 13 mulige havner og 33 usikre avgrensninger.

Ny detaljgjennomgang etter brukerinnspill er fullført i det tilgjengelige bildegrunnlaget. Endring fra rev-01: **15 nye anleggsgrupper / 16 nye polygoner**. De tidligere 43 polygonene og ID-ene er bevart. Revisjon 1 er uendret. Leveransen er ikke godkjent eller innlemmet i samledata/nettsted.

## Gjennomgang og funn

255 kystceller à 500 m (64 ark) er gjennomgått med kildeflisene vist i ca. 0,73 m/px. Ark 25–63 var allerede kontrollert i en bevart, påbegynt gjennomgang; ark 0–24 er fullført nå. Alle 12 tidligere tilleggsfunn og seks nye kontrollfunn har fått eksplisitte beslutninger i egne detaljpaneler. I tillegg er 17 tidligere utelatte kandidater revurdert med kontroll av eksisterende omriss, slik at nabohavner ikke telles dobbelt.

Fem tidligere utelatelser er omgjort: C013 (Skjerkebukta nord), C029 (Bunes), M05 (Ekstrand båtbyggeri/Kuskjær), C019 (Vinjestranda øst) og C020 (Høvika). C013, C029, C019 og C020 var feilvurdert som for små; ved båtbyggeriet er faste plasser fortsatt usikkert.

## Nye anlegg

| ID | Anlegg | Klasse | Polygoner |
|---|---|---|---:|
| 4012-H39 | Kruksdalen / Krukodden – trekantet molobasseng | Småbåthavn | 1 |
| 4012-H40 | Rakkestadstranda – molobasseng | Småbåthavn | 1 |
| 4012-H41 | Brennevinstranda ved Kjøya – bryggeanlegg | Småbåthavn | 1 |
| 4012-H42 | Kjøya sør – brygge | Mulig | 1 |
| 4012-H43 | Kjerra ved Stranda – langbrygge | Småbåthavn | 1 |
| 4012-H44 | Tonerhavna, Kjønnøya – brygge | Mulig | 1 |
| 4012-H45 | Håvøyveien – brygger i indre vik | Småbåthavn | 2 |
| 4012-H46 | Hafsundveien – båter langs kai ved camping | Mulig | 1 |
| 4012-H47 | Isnesbukta – båter langs kai | Mulig | 1 |
| 4012-H48 | Skjerkebukta nord ved Skjerkøyveien – bryggeanlegg | Småbåthavn | 1 |
| 4012-H49 | Bunes ved Kveldroveien – bryggeanlegg | Småbåthavn | 1 |
| 4012-H50 | Ekstrand båtbyggeri / Kuskjær – mulig båtplassanlegg | Mulig | 1 |
| 4012-H51 | Herreelva ved Rafnesveien – båter langs søndre kai | Mulig | 1 |
| 4012-H52 | Vinjestranda øst ved Åbyfjorden – langbrygge | Småbåthavn | 1 |
| 4012-H53 | Høvika ved Høvikåsen – brygge | Småbåthavn | 1 |

## Leveranser og kontroll

- `bathavner.geojson` og `metadata.csv`: samme 59 polygonrader, WGS84, status `til_godkjenning`.
- `changes.csv`: alle 16 nye polygoner med begrunnelser.
- `candidate-ledger.json`/CSV, `detail-review.json` og `excluded-review.json`: sporbare kandidatbeslutninger.
- `sweep-review.json` og `coverage.json`: hvilke ark som er gjennomgått, med kontrollhull.
- `digitisation.json`, `decisions.py` og `cluster-review-index.json`: manuelle pikselomriss og georeferering. Rev-01s beslutninger beholdes i rev-01.
- `outline-review.json`: de 16 nye eksportomrissene er visuelt kontrollert som overlegg på kildebildene.
- `validation.json`: gyldige polygoner, unike ID-er, 0 m² utenfor kommunen, ingen intern overlapp eller overlapp mot samledata, CSV-samsvar og bildehashkontroll.
- `preservation-manifest.json`: rev-01, godkjente samledata og nettsted er kontrollert uendret med SHA-256.
- Originalbilder med georeferering er bevart lokalt i `work/4012-bamble/images/`. Nye stedsnavn er kontrollert mot Kartverkets punkt-API; navnene er beskrivende, ikke verifiserte operatørnavn.

## Kjente begrensninger

**Skydekte deler av industrikysten i G024/G028/G030/G031 er ikke tilstrekkelig visuelt kontrollert.** Fullført gjennomgang betyr at alle feltene er behandlet; det er ikke en garanti for fullstendighet. Ukjent opptaksdato, nøyaktighet og dagens drift gjelder fortsatt. Innlandet er ikke systematisk kartlagt.

Det trekantede bassenget ved Kruksdalen/Krukodden er stedfestet og inkludert som H39. Det passer beskrivelsen av brukerens «Kyststien»-basseng, men identiteten med originalskjermbildet er ikke bekreftet.

Driftsgrenser ved Valle/Stoa og for nye anlegg er ikke dokumentert. Separate private brygger er ikke summert. Mulige service-/salgsplasser ved båtbyggeri og camping holdes som usikre. Ingen nye publiserte kapasitetstall er lagt til.

Ny målt veggklokketid: 585 sekunder. Målingen starter ved opprettelsen av detaljpanelverktøyet; innledende lesing og bildekontroll før dette er ikke målt. Tokens og pris er ikke målt.

# Nordre Follo (3207), revisjon 1 – godkjent

Analysert 31. oktober 2026 på brukerens bestilling. Brukeren godkjente leveransen 31. oktober 2026. Polygonene er innlemmet i samledata og nettstedets lokale kartdata; kjente usikkerheter er beholdt. Se `approval.json`.

| Anlegg/kandidat | Klasse | Polygoner | Viktig avgrensning |
|---|---|---:|---|
| Oppegård Båtforening / Ljansbruket | Småbåthavn | 1 | Bare Nordre Follo-delen; grensegruppe `X-HVERVEN-0301-3207` knytter til godkjent Oslo-del `0301-H28`. |
| Gjevika ved Langen | Mulig småbåthavn | 1 | Ferskvann. Felles båtplasser omtalt, men eksakt operatørkobling og antall faste plasser er uavklart. |

## Resultater og kildegrunnlag

`bathavner.geojson` og `metadata.csv` inneholder samme to polygonrader og to lokale anleggs-ID-er. Ljansbruket er en kommunedel av et eksisterende grenseanlegg, ikke nødvendigvis et nytt fysisk anlegg i en senere deduplisert total. `candidate-ledger.json`/CSV sporer 58 OSM-brygger, to samlede havnebeslutninger og fire åpne kildekandidater. Rader for enkeltbrygger og havnebeslutninger er forskjellige evidensnivåer, ikke 64 forskjellige havner.

- [Oppegård Båtforenings egen side](https://oppegaard-baatforening.no/foreningen.aspx) oppgir 350 plasser og besøksadresse Ingierstrandveien 2–4. Tallet gjelder hele havnen, inkludert Oslo-delen. Ikke summer det med Oslo eller tolk det som kapasitet bare i Nordre Follo. Kapasitetens referanseperiode er ukjent; omtale av sommersesong 2025 på siden daterer ikke tallet.
- [Enhetsregisteret, 875473212](https://data.brreg.no/enhetsregisteret/api/enheter/875473212) bekrefter organisasjonen; registeradresse brukes ikke alene som stedfesting.
- [Gjevik Vel](https://gjevikvel.no/2018/11/27/bilder/) omtaler felles båtplasser i Gjevika og skiller dem fra badebryggen. OSM-pir 416709856 og bilde `inland-02` viser et samlet båtanlegg i bukta. Ingen eksakt kapasitet er anslått.
- [Gjevik Båtforenings registerpost](https://data.brreg.no/enhetsregisteret/api/enheter/916034954) omtaler båthavn med båtplasser og opplagskrybber, men stedfester ikke det eksakte anlegget. Kandidaten gis derfor et beskrivende navn og mulig-klasse.
- [Kommunens kyststiside](https://www.nordrefollo.kommune.no/tjenester/kultur-idrett-og-fritid/kyststi-langs-bunnefjorden/) avgrenser kyststrekningen fra Sjødalsstrand/Ås-grensen til Ljansbruket/Oslo-grensen. Dette er geografisk støtte, ikke dokumentasjon på at alle brygger er havner.

## Gjennomføring og kontroll

Offisiell kommunegrense fra Kartverkets kommuneinfo, OSM-uttrekk med pirer/marinaer og Esri World Imagery. Manuell digitalisering i georefererte bilder; ingen automatisk buffergeometri brukes i eksporten. `digitisation.json` bevarer bildepunktene og beslutningene. Avgrensningen omfatter brygger, plasser og mellomliggende vann, ikke opplag eller eiendom på land.

14 overlappende kystfliser dekker hele den innhentede OSM-kystlinjen innenfor kommunen med 20 m grensemargin, ca. 10,96 km. Kontaktark gjennomgått som et separat kystsøk; registrerte brygger også kontrollert i detaljutsnitt. 17 innlandsfliser dekker registrerte bryggekandidater. Innsjøer er **ikke systematisk fullkartlagt**. Ett detaljbilde ved Ljansbruket gir totalt 32 vellykkede originalbilder. To detaljforsøk uten bildelevaranse er ikke brukt som evidens.

Alle eksportomriss er kontrollert visuelt etter kommuneavklipping. Teknisk kontroll viser gyldige geometrier, unike ID-er, 0 m² utenfor kommunen, ingen overlapp med godkjente polygoner og fullt CSV-samsvar. Før innlemming ble samlefil og manifest kontrollert uendret (456 polygoner / 14 kommuner). Etter godkjenning inneholder samlefilen 458 polygoner / 15 kommuner. Alle 456 tidligere godkjente features er bevart uendret, kontrollert med kanonisk SHA-256. Se `validation.json`.

Originalbilder, råkilder, tekstuttrekk og kontrollark ligger lokalt i `work/3207-nordre-follo/`. `imagery-manifest.json`, `source-provenance.json` og `coverage.json` gir URL-er, innhentingstid, faktisk bildeutstrekning og sjekksummer. Bildene følger ikke Git etter eksisterende prosjektpraksis. Bevar arbeidsmappen ved flytting til annen maskin; hentet mosaikk kan endre seg.

## Åpne forhold

- Elvestadsletta, Fløyspjeld, Kjøkkenodden og Båtsvikdalen er loggført uten polygon. Adresse i kommunen er utilstrekkelig bevis på en havn der; disse navnene skal ikke brukes til å øke kommunens havnetall.
- Kystens spredte boligbrygger, bade-/rekreasjonsbrygger og små enkeltanlegg er utelatt når felles havn eller terskelen ikke er dokumentert. Ingen summering av enkeltbrygger langs stranden.
- Oslo-delens tidligere navn Hvervenbukta/Fiskevollen er ikke endret. Nettstedets samlede havnetall bruker grensegruppe som felles nøkkel. Kommunevise havnekort beholder sine lokale ID-er. 350 plasser overføres ikke som kapasitet for kommunedelen.
- Bildedato og posisjonsnøyaktighet er ukjent. Publiserte nettkilder er ikke feltverifikasjon av dagens drift, kapasitet eller renseanlegg.

## Reproduksjon

Kjør med prosjektets `.venv` fra repoets rot: `setup.py`, `overpass_fetch.py`, `coverage.py`, deretter `fetch_images.py specs.json esri`, `sources.py`, `pier_review.py`, `build.py`, `qa.py`, `validate.py` i `work/3207-nordre-follo/`. Hent i tillegg `detail-oppegard` med spesifikasjonen i `imagery-manifest.json`; `detail_specs.py` lager denne. Kontroller nye bilder visuelt før en ny revisjon. `finalize.py` registrerer avventende status og tid, aldri godkjenning. `build.py` og `finalize.py` avbryter nå for denne godkjente revisjonen. Bevar den leverte revisjonen; regenerering er ikke en ny godkjenning.

# Nesodden (3212) – revisjon 1 godkjent

Analysert 31. oktober 2026 etter brukerens bestilling. **11 anleggsgrupper / 11 polygoner, inkludert tre mulige havner.** Brukeren godkjente revisjonen 31. oktober 2026. Samlefil og nettstedets lokale kartdata er oppdatert: 469 godkjente polygoner fra 16 kommuner. Se `approval.json`; de tre mulige havnene og åpne spørsmål er beholdt. Ingen neste kommune er startet.

| ID | Anlegg/kandidat | Klasse |
|---|---|---|
| 3212-H01 | Steilene – Nesodden Seilforenings havn | Småbåthavn |
| 3212-H02 | Spro Båthavn | Småbåthavn |
| 3212-H03 | Fagerstrand Båtforening | Småbåthavn |
| 3212-H04 | Ildjernet nordvest – mulig felles brygge | Mulig småbåthavn |
| 3212-H05 | Ildjernet øst – mulig felles båtplassanlegg | Mulig småbåthavn |
| 3212-H06 | Alværn brygge – båtplassanlegg | Småbåthavn |
| 3212-H07 | Oksval Båthavn | Småbåthavn |
| 3212-H08 | Kavringen / Sjøsenteret Nesodden – marina | Småbåthavn |
| 3212-H09 | Kavringstrand – mulig felles brygge øst for Kavringen | Mulig småbåthavn |
| 3212-H10 | Ursvikbukta – felles båtplassanlegg | Småbåthavn |
| 3212-H11 | Blylaget – felles båtplassanlegg | Småbåthavn |

De to mulige Ildjernet-anleggene er avgrenset hver for seg. Brygger med separate landfester rundt øya er ikke summert til én sikker havn. Kavringstrand er en fysisk kandidat med beskrivende navn; identitet, operatør og eventuell felles havnegruppe med Kavringen er uavklart. De 11 lokale anleggsgruppene er derfor ikke en påstand om 11 uavhengige operatører.

## Leveransen

- `bathavner.geojson`: polygoner i WGS84 / EPSG:4326, lengdegrad før breddegrad; status `godkjent_av_bruker`.
- `metadata.csv`: nøyaktig samme egenskaper/rader som GeoJSON, semikolon, UTF-8 med BOM.
- `candidate-ledger.json`/CSV: 84 OSM-bryggeklynger og tre supplerende kildeavklaringer. C053 har to eksporterte fysiske kandidater; rader er ikke et separat havnetall.
- `open-questions.json`: fem konkrete avklaringsbehov, blant annet Bomansvik, Kavringstrand og Steilene.
- `digitisation.json`, `decisions.py` og `cluster-review-index.json`: eksplisitte beslutninger, bildepunkter og georefererte rammer brukt ved manuell digitalisering.
- `validation.json`, `coverage.json`, `imagery-manifest.json`, `source-provenance.json` og `timing.json`: kontroll, dekning, kildehenvisninger og målt tidsbruk.

## Kilder og kapasiteter

Offisiell kommunegrense fra [Kartverkets kommuneinfo](https://api.kartverket.no/kommuneinfo/v1/kommuner/3212/omrade?utkoordsys=4326), fire fullstendige OSM-delruter, georeferert Esri World Imagery og kildebelagte operatør-/foreningsopplysninger. Registeradresser er ikke brukt alene som stedfesting.

| Opplysning | Kilde og behandling |
|---|---|
| Oksval: ca. 290 ordinære båtplasser, gjesteplasser i tillegg | [Operatørens historieside](https://www.obh.no/omoss/historie/). Referanseperioden er ukjent. Ca. 450 medlemmer er ikke kapasitet. |
| Spro: ca. 180 plasser og gjestehavn | [Operatørens side](https://sprobathavn.no/). Havnen tilbyr plasser i 2026, og bildet viser fysisk molo og monterte brygger. Kapasiteten er publisert, ikke målt. [Utbygger](https://www.hersleth.no/eiendom/utviklingsomrader/spro-havn-nesodden) omtaler ferdigstillelse i 2025. |
| Steilene: faste plasser og gjestebruk | [Seilforeningen](https://nesoddenseilforening.no/next/p/97799/havna) og [Havneweb](https://www.havneweb.no/nesoddenseilforening/?mod=omhavnen). Minst 20 normalt tilgjengelige gjesteplasser er ikke tolket som total kapasitet. |
| Fagerstrand: dokumentert havn med medlemsplasser og gjesteleie | [Operatørens side](https://www.havneweb.no/fabat/?mod=startsiden). Ingen dedikerte gjesteplasser ifølge operatøren; ledige medlemsplasser kan leies. KNBF-medlemstall er ikke båtplasser. |
| Kavringen: båtplasser og vinteropplag | [Operatørens Havneweb](https://www.havneweb.no/sjosenteretnesodden/). Landopplag er ikke tegnet inn i sjøpolygonet. Ingen usikret kapasitet overført. |
| Ursvikbukta: forening og flere lokale bryggeinteresser | [Ursvikbuktens Båtforening](https://www.ursvikbukten.no/) og [Ursvik Vel](https://ursvik.inngangen.com/2024/forslag.html). Fysisk anlegg er kartlagt uten å tilordne hele området til én eksklusiv operatør eller overføre gamle plasstall. |
| Blylaget: navn og lokalisering | [OBU-havnelistens koordinat](https://obat.no/obu-havner/), [Enhetsregisteret](https://data.brreg.no/enhetsregisteret/api/enheter/818992912) og synlig båtplassanlegg. Bryggene ligger nord for grensen mot Frogn. |

Plasstallene for Oksval og Spro skal ikke uten videre summeres til dagens totale kommunekapasitet; kildeomfang og referanseperioder varierer. Tjenester som Spro-kunder kan kjøpe hos Skjæløy Slipp beviser ikke at tilsvarende opplags- eller renseanlegg finnes lokalt på Spro.

## Dekning og kontroll

65 overlappende kystfliser dekker hele den innhentede OSM-kystlinjen innenfor kommunegrensen med 20 m grensemargin, ca. 55,15 km inkludert øyer. Alle flisene er gjennomgått på kontaktark uavhengig av kandidatlisten. 310 OSM-bryggeobjekter er vurdert gjennom 84 klynger i georefererte detaljutsnitt. Seks ekstra detaljbilder og ett supplerende innlandsutsnitt gir totalt 72 vellykkede originalbilder. Ett mislykket ekstra detaljforsøk ved Steilene ble erstattet av et utsnitt fra eksisterende kystflis. Innlandet er **ikke systematisk fullkartlagt**.

Alle 11 eksporterte omriss er visuelt kontrollert på originalbildene etter eksport. Fem har eksplisitt usikker avgrensning: de tre mulige havnene samt Spro og Steilene, hvor publiserte opplysninger om nyere utbygging/fornyelse gjør datert kontroll særlig relevant. Alle har ukjent bildeopptaksdato og ukjent posisjonsnøyaktighet. Eksportens pikseloppløsning er ikke en målt posisjonsnøyaktighet.

Teknisk validering består: gyldige polygoner, unike ID-er, 0 m² utenfor kommunegrensen, ingen intern overlapp eller overlapp med godkjente polygoner, fullt CSV-samsvar. Før innlemming ble samlefil og manifest kontrollert uendret med SHA-256. Etter innlemming er alle 458 tidligere godkjente features kontrollert uendret med kanonisk SHA-256. Ingen nye grensegrupper er opprettet.

## Avklaringer og begrensninger

**Bomansvik er ikke erklært uten havn.** Båtforeningen er oppført i [KNBFs medlemsoversikt](https://www.knbf.no/regioner/ost/medlemsforeninger-ost/), men bildet viser en steinkai uten tilstrekkelig dokumentasjon på sjøutstrekningen av faste plasser. Kandidaten beholdes åpen uten et oppdiktet polygon. Dette hindrer en påstand om komplett havneregister.

Østlige kaier ved Steilene kan være tilhørende jolle-/service-/gjesteanlegg; dette må avklares før et ekstra polygon. Industri-/trenings-/servicekaier ved Svestad, rutebåtkaier på Nesoddtangen, friluftsbrygger på Langøyene og spredte private brygger er utelatt når det ikke foreligger et selvstendig båtplassanlegg etter prosjektregelen. OSM-marina-merker er brukt som kandidathjelp, ikke som bevis for alle nærliggende brygger.

Ingen befaring, operatørkontakt eller uavhengig kontroll av dagens drift/rensing er utført. Ingen fullstendighetspåstand mot Mepex/SALT fremsettes.

## Reproduksjon og bevaring

Arbeidsskriptene ligger i `work/3212-nesodden/`. Bruk prosjektets `.venv`. Rekkefølge for en **ny revisjon**: `setup.py`, `overpass_post.py`, `coverage.py`, `fetch_images.py specs.json esri`, supplerende detaljutsnitt, `sources.py`/`extra_sources.py`, `clusters.py`, `review_clusters.py`, eksplisitt `decisions.py`, `build.py`, `qa.py`, `validate.py`, `finalize.py`. `build.py` og `finalize.py` avbryter for denne godkjente revisjonen. Les skriptenes revisjonsstier før kjøring. Kildene og dagens beslutninger kan ikke erstatte en ny visuell kontroll ved endrede bilder.

Originalbilder, georeferering, råsvar, tekstuttrekk og QA-ark er beholdt lokalt under `work/3212-nesodden/`; de følger eksisterende prosjektpraksis og er ikke publisert i Git. Bevar arbeidsmappen ved maskinflytting. Manifestene angir faktisk bildeutstrekning, innhentingstid, URL og sjekksum; ny nedlasting garanterer ikke samme mosaikk. Følg kildenes bruksvilkår ved eventuell publisering av bilder.

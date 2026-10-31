# Hvaler rev-01 – godkjent

Kartleggingsforslag datert 2026-10-31 på branch `data/hvaler-analysis`, fra main `6a9fa50` etter merge av Vestby PR #8. Godkjent av brukeren og innlemmet i samlefil og nettsted.

## Resultat

- 69 sjøpolygoner / 66 foreløpige fysiske anleggsgrupper.
- 46 grupper klassifisert småbåthavn; 20 grupper klassifisert mulig småbåthavn.
- 68 polygoner har usikker avgrensning / behov for ortofotokontroll. Alle har ukjent bildeopptaksdato og trenger datert bildekontroll.
- 7 åpne kildeavklaringer; de beholdes også ved eventuell godkjenning.

Anleggsgrupper er foreløpig gruppering av fysiske brygger, ikke et verifisert antall operatører. Private brygger ved separate landfester er ikke summert til havner. Fiskeri-, ferge-, bade- og servicekaier kvalifiserer ikke alene. Innlandet er ikke systematisk bildesøkt, og det gis ingen fullstendighetspåstand.

## Filer

- `bathavner.geojson`: WGS84-polygoner godkjent av brukeren.
- `metadata.csv`: semikolonseparert UTF-8 med samme felter og rekkefølge som GeoJSON.
- `candidate-ledger.json` / `.csv`: eksplisitte vurderinger av alle 335 OSM-bryggeklynger, én supplerende bildekandidat og sju åpne kildekandidater.
- `digitisation.json`, `decisions.py`, `cluster-review-index.json`: manuelle koordinatbeslutninger og kobling til georefererte bildeutsnitt.
- `imagery-manifest.json`, `image-requests.json`, `source-provenance.json`: kildehenvisninger, forespørsler, georeferering, hentetider og SHA-256.
- `coverage.json`, `validation.json`, `summary.json`, `timing.json`: dekning, tekniske kontroller, antall og målt veggklokketid.
- `open-questions.json`: oppfølgingsbehov for navn, operatørgrenser, kapasitet og eksisterende anlegg.

Originalbilder, råkilder og kontrollark ligger lokalt i `work/3110-hvaler/`, utenfor Git. Metadataene kan ikke erstatte originalbilder ved visuell etterprøving. Gjentatt henting kan gi en annen bildemosaikk.

## Dekning og kontroll

Fire komplette Overpass-delruter er deduplisert til 5960 objekter. 948 pirer innenfor kommunegrensen med 20 m buffer er gruppert i 335 klynger; hver klynge har en eksplisitt beslutning. Svenske objekter i uttrekket er filtrert med den offisielle kommunegrensen.

274 overlappende kystfliser er gjennomgått uavhengig av klyngene, med 19 supplerende bilder og sju ekstra kontrollutsnitt. Den brukte OSM-kystlinjen med grensebuffer er ca.661,25 km og har ingen udekket lengde i dette flisesettet. Dette er en kontroll av søkegrunnlaget, ikke et uavhengig mål på kommunens offisielle kystlengde.

Alle 69 eksporterte omriss er kontrollert som overlegg på bildene. Omriss som skar gjennom båtplasser er justert og kontrollert etter ny eksport. Teknisk validering består: gyldig geometri, unike ID-er, innenfor kommunegrensen, ingen arealoverlapp innbyrdes eller med de 502 godkjente polygonene, CSV-samsvar og bildehash/dekoding. De 502 tidligere godkjente polygonene fra 18 kommuner er bevart uendret, kontrollert med kanonisk SHA-256 i `approval.json`. Samledata og nettsted inneholder nå 571 polygoner fra 19 kommuner.

## Navn, operatører og kapasitet

Hovedanleggene omfatter blant annet Utgårdskilen, Dypedal, Stokken, Sand, Brattestø, Vikerhavn, Skipstadsand, Lauer, Skjærhalden, Herføl og Edholmen. Generiske stedsnavn er beskrivende når operatør eller havnenavn ikke er sikkert knyttet til den konkrete bryggen.

| Kildeobservasjon | Behandling |
| --- | --- |
| Sand Marina ca.250 plasser | Ett omtrentlig operatørtall på hovedanlegget; ikke overført til søndre naboanlegg eller østsiden av sundet. |
| Utgårdskilen båtforening ca.140 plasser | Operatørobservasjon; Borgs 52 næringsplasser er ikke en tilleggssum for fritidsbåter. Eksakte grenser må avklares. |
| Skjærhalden gjestehavn ca.100 gjestebåter, 37 reserverbare | Separate komponenter: 37 er en delmengde. 100 gjelder hele operatørens gjestehavn, ikke bare hovedbryggepolygonet. |
| Skjærhalden båtforening ca.300 plasser | Komponent med uttrykkelig uavklart fordeling mellom sjøområdene. Ikke en samlet kapasitet for alle havner i Skjærhalden. |
| Borg Havns liste, oppdatert 2024-01-01 | Daterte delanlegg/utleieplasser; ikke dagens totale fysiske havnekapasitet. |
| Havneplan 2018–2028 | Historisk situasjonsbeskrivelse skilles fra foreslåtte utvidelser. Kroksands 32 og Vikerhavns ca.125 er daterte observasjoner. Planlagte plasser brukes ikke som bygget kapasitet. |

Papperhavn, vestre deler av Vikerhavn, operatørgrensene ved Stokken/Listranda og fordelingen i Skjærhalden er åpne avklaringer. Det legges ikke ekstra polygoner til rene fiskeri-/trafikkkaier bare fordi kommunen tilbyr enkelte fritidsplasser i samme havneområde. Manglende skalar kapasitet betyr ukjent, ikke null.

## Gjenskaping og godkjenning

Bruk `.venv` med prosjektets `requirements.txt`. Når lokalt bilde-/råunderlag finnes:

```bash
.venv/bin/python work/3110-hvaler/build.py
.venv/bin/python work/3110-hvaler/qa.py
.venv/bin/python work/3110-hvaler/validate.py
.venv/bin/python scripts/validate_project.py
```

`build.py` nekter å overskrive en godkjent revisjon. Teknisk validering erstatter ikke visuell vurdering. Brukergodkjenningen er registrert; den fjerner ikke usikkerhetene. Godkjenning og kontroll av tidligere features er registrert i `approval.json`.

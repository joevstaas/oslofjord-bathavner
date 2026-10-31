# Vestby (3216), rev-01 – godkjent

**8 fysiske anleggsgrupper / 9 sjøpolygoner, inkludert 3 mulige havner.** Alle ni avgrensninger har kontrollbehov, blant annet på grunn av ukjent bildeopptaksdato og nyere bryggeendringer. Leveransen er brukergodkjent og innlemmet i samlefilen og nettstedets lokale kartdata. Samlet 502 polygoner / 18 kommuner. Hvaler er ikke startet.

## Leveranse

- `bathavner.geojson`: WGS84/EPSG:4326, én feature per sjøpolygon, felles `harbour_id` for deler av samme fysiske anlegg. Ikke juridiske eiendoms-/operatørgrenser.
- `metadata.csv`: identiske egenskaper, UTF-8 BOM, semikolon.
- `candidate-ledger.json` / `.csv`: eksplisitte beslutninger for 16 OSM-klynger, to ekstra bildekandidater og fire åpne kildeavklaringer.
- `decisions.py`, `digitisation.json`, `clusters.json`, `cluster-review-index.json`: beslutninger, manuelle piksler og georefererte utsnitt.
- `kommunegrense.geojson`, `coverage.json`, `image-requests.json`, `imagery-manifest.json`, `source-provenance.json`: kildebelegg og faktisk bildereferering med innhentingstid, SHA-256 og lokale råfilreferanser.
- `summary.json`, `validation.json`, `timing.json`, `open-questions.json`: tall, kontroller, målt veggklokketid og avklaringer.

## Kartlagte anlegg

| Anlegg | Navn / fysisk gruppe | Polygoner | Klasse |
| --- | --- | ---: | --- |
| 3216-H01 | Hvitsten | 1 | mulig_smabathavn |
| 3216-H02 | Son havn nord / Sonskilen | 2 | smabathavn |
| 3216-H03 | Sonsbukta | 1 | mulig_smabathavn |
| 3216-H04 | Son havn syd / Son Spa | 1 | smabathavn |
| 3216-H05 | Søndre Brevik båthavn | 1 | smabathavn |
| 3216-H06 | Son Gjestehavn | 1 | smabathavn |
| 3216-H07 | Hvitsten | 1 | smabathavn |
| 3216-H08 | Kjøvangen | 1 | mulig_smabathavn |

Son havn nord/Sonskilen har to polygoner rundt land: vestre brygger og hovedbasseng med molobrygge. Gjestehavnen i sentrum er egen gruppe med fysisk og kildebelagt plassering. Son havn syd ved Son Spa er eget fysisk anlegg; kommunens tekst unntar SC-brygga fra kommunalt ansvar. Ingen eksklusiv operatørgrense hevdes for hele gruppen.

De tre mulige er Andersbrygga i Hvitsten, en liten båtplassrekke på vestsiden av Sonsbukta og rekken ved Kjøvangen. Felles organisering og/eller ti faste plasser er ikke tilstrekkelig verifisert. Bade-/anløpskaiene ved Emmerstad og Kjøvangen er utelatt, likeså separate private brygger. NIVA/servicekaier ved Solbergstrand gir ikke alene grunnlag for havn. Den allerede godkjente småbåthavnen nord for grensen i Frogn er ikke duplisert.

## Kapasitet og kildekonflikter

| Anlegg / kilde | Publisert opplysning | Behandling |
| --- | --- | --- |
| Sonskilen, «Om oss» | 679 båtplasser | Udatert referanseperiode; motstrid med annen operatørside. |
| Sonskilen, «Vi tilbyr» | 775 båtplasser | Beholdt separat fra 679. Omfang mot elva og kommunalt leieareal må avklares. |
| Søndre Brevik, foreningens hovedside | 141 andelsplasser | Beholdt separat fra Havneweb, med ukjent referanseperiode. |
| Søndre Brevik, Havneweb | 150–200 båter ekskl. jolleplasser | Intervall, ikke valgt som erstatning for 141; definisjon og dato må avklares. |
| Son Gjestehavn, 2026-side | 65 forhåndsreserverbare gjesteplasser | Delmengde, ikke total kapasitet. Ikke sikkert at alle ligger i sentrumspolygonet. |

Kildene finnes som egne `capacity_components` på relevant fysisk gruppe; bare ett delpolygon bærer hver komponentliste for å unngå dobbelttelling. `berth_count_published` er null for alle polygoner fordi det ikke finnes ett entydig tall med sikkert avgrenset omfang. Dette betyr **ukjent/ikke entydig**, ikke null båtplasser. Medlemstall, breddemeter brygge, vinterplasser i sjø og opplag på land er ikke summert til båtplasskapasitet. Aktuell drift er ikke uavhengig verifisert.

Primærkilder: [Sonskilen om oss](https://www.sonskilen.no/om-oss), [Sonskilen vi tilbyr](https://www.sonskilen.no/vi-tilbyr), [Son Båtforening](https://www.sonbaat.no/havnas-fasiliteter/), [Havneweb Son Båtforening](https://www.havneweb.no/sonbaat/?mod=omhavnen), [Son Gjestehavn](https://www.sonhavn.no/son-gjestehavn/), [Son havnekart](https://www.sonhavn.no/smaabaathavn/gjestehavnkartflyfoto/), [Hvitsten Vel](https://www.hvitstenvel.no/Hvitsten-Vel).

## Dekning og kontroll

Fire komplette Overpass-delruter ga 255 unike elementer i kommunens rektangulære søkeområde. Etter grensekontroll inngår 68 OSM-pirer i 16 klynger med 20 m toleranse. 31 kystfliser og én ekstra detaljflis er fullstendig dekodet og hashkontrollert. Alle ca. 28,15 km OSM-kyst innenfor kommunegrensen med 20 m toleranse er dekket av bildene. Hele kystflisesettet er visuelt gjennomgått uavhengig av OSM-kandidatene; to ekstra bildekandidater er ført i loggen. To supplerende utsnitt av Son brukes fordi OSM-klyngeomrisset alene ikke dekker hele det synlige hovedbassenget.

Alle ni eksporterte omriss er projisert tilbake på originalbildene og visuelt kontrollert. Hovedbasseng og molobrygge ble samlet i ett polygon etter at kontrollen viste overlapp innen samme fysiske havnegruppe. Endelig validering viser gyldig geometri, unike ID-er, null areal utenfor kommunegrensen, ingen overlapp internt eller mot 493 godkjente polygoner og fullt CSV-samsvar. De 493 tidligere godkjente features er bevart uendret, kontrollert med kanonisk SHA-256 i `approval.json`. Nettstedets lokale kartdata og tellinger er oppdatert.

## Begrensninger og åpne spørsmål

- Nye bryggearbeider omtales i operatørkilder fra 2025. Operatørkartet fra juli 2025 brukes til navne-/inndelingskontroll; en byggetegning eller et planlagt anlegg erstatter ikke georeferert dokumentasjon på faktisk bygget omriss. Alle avgrensninger beholdes med kontrollbehov.
- Hølenselva/Såna oppstrøms brua har dokumenterte båtplasser, men full avgrensning og operatørtilhørighet er ikke verifisert i bildene. Ingen ekstra elvepolygon er eksportert. Havnegruppens polygoner må ikke tolkes som full kartlegging av alle operatørens plasser.
- Opptaksdato og absolutt posisjonsnøyaktighet er ukjent. Ca. 0,733 m per eksportpiksel er ikke målenøyaktighet. Polygonene er foreløpige kartleggingsforslag.
- Kapasitet, operatøransvar og foreningsrettigheter må avklares som beskrevet i `open-questions.json`. Ingen direkte operatørhenvendelser er utført.
- Innlandet er ikke systematisk bildesøkt. Fire fullførte Overpass-ruter og full bildedekning av registrert kyst beviser ikke fullstendighet.

## Reproduksjon og lokalt arkiv

Arbeidsunderlag ligger i `work/3216-vestby/`: originalbilder med tilhørende JSON i `images/`, råkilder/operatørkart i `raw/`, kontrollark i `qa/`. Disse er ignorert av Git og må bevares separat for identisk visuell etterprøving. Kildenes vilkår gjelder; ny nedlasting kan gi en annen mosaikk. To eldre «Havnekart»-bildeadresser ga bare kartikoner og brukes ikke som kartbelegg.

Bruk prosjektets `.venv` og de kommunevise skriptene. Med originalarkivet gjenopprettet: kjør `clusters.py`, `review_clusters.py`, deretter `gap_frames.py`. Kopier leveransens `open-questions.json` til arbeidsmappen og bruk endelige `decisions.py`. Kjør `build.py`, `qa.py`, kontroller alle omriss og kjør `validate.py`. `setup.py`, `overpass_post.py`, `coverage.py`, `fetch_images.py`, `sources.py`, `extra_sources.py` og `map_sources.py` dokumenterer innhentingen. `retry_inland.py` dokumenterer et mislykket oppdelingsforsøk; det komplette svaret kom senere i den ordinære delruten. `finalize.py` skriver status og timing og skal ikke brukes etter godkjenning uten ny revisjon.

Målt veggklokketid inkluderer nettventing. Tokens og kostnad er ikke målt. Brukeren har godkjent leveransen. Godkjenningen beholder kjente usikkerheter og bekrefter ikke fullstendighet, aktuell kapasitet eller drift.

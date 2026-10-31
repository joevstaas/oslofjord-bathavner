# Sarpsborg – rev-01 til godkjenning

**39 foreløpige anleggsgrupper / 54 polygoner**, inkludert **11 mulige havner**. 53 avgrensninger har ekstra kontrollbehov; alle har ukjent lokal bildedato. Ikke innlemmet i samlefil eller nettsted. Godkjenning gjelder denne revisjonen og fjerner ikke usikkerhet.

GeoJSON er WGS84. Metadata-CSV har semikolon og samme polygonrader. `candidate-ledger.json/.csv` dokumenterer alle 59 OSM-klynger, 21 supplerende kontrollrammer og 28 kommunale kildekandidater. Kontrollrammer og kildekandidater er ikke nye anleggstall. Anleggsgruppene er foreløpige, ikke en opptelling av juridiske operatører.

137 kystceller à 500 m er visuelt gransket i 35 ark, uavhengig av havnelisten. OSM-map-API ga 121 pirer i 59 klynger. Alle 28 havneområder i kommunerapporten fra 2013 er stedfestet og vurdert; rapporten brukte minst 20 plasser og er derfor ikke fullstendig etter prosjektets ti-plassregel. Bildegjennomgangen fant flere manglende brygger. Innsjø-/elvekandidater er kontrollert, men hele innlandet er ikke fullkartlagt.

Kapasitet: bare tre nyere publiserte gruppetall er scalarfelt (Skjebergkilens marina 1250, kommunen 13.05.2026; Sarpsborg Baatforening 400, ukjent nettsidereferanseperiode; seilforeningen ca. 100 per 01.05.2025). Hvert tall står én gang per gruppe. Historiske tall og avvik er separate, ikke-additive `capacity_components`. Seilforeningen opplyser at satellittbildet er foreldet etter nye pirer i 2025; utvidelsen er ikke konstruert uten bildegrunnlag.

`open-questions.json` har ti avklaringspunkter, inkludert nyere brygger, service kontra faste plasser, Bukkholmen/Bukkenes, foreløpige driftsgrenser, kapasitetsavvik og Røsnes ved Halden-grensen. Ved Holm ligger hovedbryggene i allerede kartlagt Fredrikstad. Røsnes har to små Sarpsborg-utklipp, resten av anlegget hører til Halden.

Alle 54 endelige eksportomriss er kontrollert visuelt med GeoJSON som overlegg. Teknisk kontroll: gyldig geometri, unike ID-er, 0 m² utenfor kommunen, ingen intern overlapp eller overlapp med godkjent grunnlag, fullstendig CSV-samsvar. Godkjente 630 polygoner / 20 kommuner er SHA-256-kontrollert uendret. Se `validation.json`, `visual-review.json`, `coverage.json` og `timing.json` (målt veggklokke 2330 sekunder; tokens/pris ikke målt).

Lokale originalbilder, native EPSG:3857-bilder, omprojiserte utsnitt, rå XML/PDF/HTML og QA ligger i `work/3105-sarpsborg/` og er utelatt fra Git. `imagery-manifest.json` og `source-manifest.json` bevarer forespørsler, koordinatsystemer, dimensjoner, nedlastingsdatoer og hasher. Bilder kan være mosaikker/omprojiseringer; dette øker ikke opptaksnøyaktigheten. Bilde-/kildepakken må bevares separat for identisk visuell etterprøving.

Skript: `work/3105-sarpsborg/build.py`, `qa.py` og `validate.py`. `restore_config.py` gjenoppretter lette konfigurasjoner fra `analysis-config/` dersom arbeidsmappen mangler dem. Råbilder og OSM må fortsatt finnes/hentes på nytt, og nye uttrekk kan gi annet bildeinnhold. Kjør aldri bygget mot en godkjent revisjon; opprett ny revisjon.

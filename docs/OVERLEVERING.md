# Overlevering til lokal AI-agent

## Autoritativ status ved eksport 2026-10-29

Samlefilen har 210 godkjente polygoner: Holmestrand 14, Horten 16, Tønsberg 20, Færder 35, Sandefjord 67, Larvik 32, Moss 26. Brukeren har godkjent alle disse kommuneleveransene. Det ikke-godkjente suppleringsfunnet Våle båthavn i Holmestrand er fortsatt utenfor samlefilen.

Kommunevise primærfiler i data/kommuner er avledet direkte fra den godkjente samlefilen. De har samme geometrier og egenskaper som samlefilen; CSV er generert fra disse egenskapene. Originale kommuneleveranser er bevart i archive/original, også eldre/ikke-godkjente revisjoner og forslag. Ikke bland alle GeoJSON-filer fra arkivet inn i samlefilen.

## Stier og reproduksjon

- Gammel `/workspace/oslofjord-kartlegging/METODIKK.md` tilsvarer nå docs/METODIKK.md.
- Godkjent samlet GeoJSON og manifest ligger i data/samlet.
- Gamle `/workspace/<kommune>-pilot/...` finnes relativt som archive/original/<kommune>-pilot/....
- status.jsons primærleveransestier er tilpasset lokal prosjektstruktur.
- Absolutte /workspace-stier i gamle kilde-/dekningsnotater, HTML-visere og historiske tekster er bevart som proveniens. De er ikke lokale Mac-stier.
- Det finnes ikke én ferdig generisk analysepipeline. Historiske skript er kommunevise og kan inneholde hardkodede datoer, antall og stier. Tilpass kopier i work/ før de brukes.
- Historiske finalize-/finish-/byggeskript kan endre godkjenningsstatus og overskrive data. Ikke kjør dem ukritisk.
- Maskinspesifikke deps-mapper, nettleserinstallasjon, Python-cache, credentials og kontokonfigurasjoner er utelatt. Opprett et nytt .venv på Mac; requirements er et kompatibilitetsutgangspunkt, ikke en låst Mac-verifisert installasjon.

## Bildeunderlaget

Prosjekt-ZIP inneholder ikke images-mappene. Den separate bilde-ZIP legger alle opprinnelige images-mapper under archive/original/<kommune>-pilot/images/. Dette inkluderer originalutsnitt, JSON med georeferering, kontaktark og kontrolloverlegg. Begge ZIP-filer har samme toppmappe. Dersom du pakker ut bildearkivet et annet sted, flytt de enkelte images-mappene inn i tilsvarende arkivmapper; ikke erstatt prosjektmappen med en tom mappe.

Originalbildene og tilhørende JSON må beholdes sammen. Uten bildepakken kan leveransene leses og geometri kontrolleres teknisk, men eksportomriss kan ikke etterprøves mot de lokale originalbildene. Henting av tilsvarende bilder senere garanterer ikke samme bildemosaikk.

Kilder har egne vilkår. Kartverket, Esri og OSM er kildeangitt i data og metodikk; pakken innebærer ikke at bildene kan publiseres videre uten å følge leverandørvilkårene. Ingen påstand om ensartet bildedato eller posisjonsnøyaktighet.

## Kontroller og åpne forhold

Lokalt valideringsskript kontrollerer antall, kommunevis samsvar, metadata, geometriers gyldighet og ID-er. Det er ikke en ny visuell godkjenning eller test av fullstendighet. Historiske leveranser har ulikt skjema; ikke harmoniser ukjente verdier til sikre verdier.

Moss har én mulig havn og 15 usikre avgrensninger. Sjekta og Refsnes småbåtforening er loggført uten sikker sjøpolygon. Larvik har også åpne navngitte kildekandidater. Se kommunenes kandidatlogger og metodikken. Brukergodkjenning beholdt disse begrensningene.

Aktive tids-/tokenregnskap fra denne samtalen kan ikke overføres til Claude. Registrer ny tidsbruk separat; faktiske tokens/priser må komme fra verktøy som faktisk måler dem.


## Hvaler rev-01 godkjent og innlemmet

Hvaler ligger på branch `data/hvaler-analysis`, med 69 polygoner / 66 foreløpige anleggsgrupper, inkludert 20 mulige. Se `data/kommuner/3110-hvaler/rev-01/README.md` og `open-questions.json`. 68 avgrensninger har kontrollbehov. Brukeren har godkjent innlemming; usikkerhetene er beholdt. Godkjent grunnlag er nå 571 polygoner / 19 kommuner. De 502 tidligere polygonene er kontrollert uendret i `approval.json`. Sarpsborg er ikke startet.

Lokal bilde-/råkildesamling ligger i `work/3110-hvaler/`, utenfor Git. Tekniske kontroller kan kjøres med `work/3110-hvaler/validate.py` når originalbildene finnes. `build.py`/`qa.py` gjenskaper avventende eksport og overlegg, men en godkjent revisjon må aldri overskrives. Hvaler er klargjort for commit/push/PR etter brukerens beskjed.

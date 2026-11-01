# Overlevering til lokal AI-agent

**Gjeldende status 2026-11-01:** 816 polygoner fra 23 kommuner, fordelt på 664 foreløpige fysiske havnegrupper i nettstedets gruppering. Flere polygoner kan tilhøre samme gruppe. Porsgrunn er innlemmet; Ås er uavklart. Eldre statusoversikter nedenfor er historiske. Se `status.json` og `data/samlet/samlet-manifest.json` for gjeldende leveranser. Brukergodkjenning er ikke uavhengig fagkontroll.

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


### Bamble – revisjon 2 godkjent og innlemmet 2026-10-31

Brukeren godkjente rev-02 og ba om commit, push og PR. Alle 59 polygoner / 53 anleggsgrupper er innlemmet, inkludert 13 mulige havner og 33 usikre avgrensninger. Samlet 630 polygoner fra 20 kommuner. De 571 tidligere godkjente features, inkludert Frogn, Vestby og Hvaler fra siste main, er bevart med kanonisk SHA-256 i `data/kommuner/4012-bamble/rev-02/approval.json`. Rev-01 er bevart som historisk, ikke-godkjent leveranse. Skydekte deler av industrikysten, ukjent bildedato/drift og øvrige åpne avklaringer beholdes. Godkjenning verifiserer ikke fullstendighet eller antall operatører. Nettstedets kartdata og kommunestatus er oppdatert. Ingen neste kommune er startet.

### Sarpsborg rev-01 – ferdig til godkjenning 2026-10-31

Gjeldende avventende leveranse: `data/kommuner/3105-sarpsborg/rev-01/`, 54 polygoner / 39 foreløpige anleggsgrupper, inkludert 11 mulige. 53 avgrensninger har ekstra kontrollbehov, alle har ukjent bildedato. Ti åpne punkter er bevart. Samledata/nettsted er fortsatt 630 polygoner / 20 godkjente kommuner; Sarpsborg er ikke innlemmet og Halden er ikke startet.

Se kommune-README, `coverage.json`, `validation.json`, `visual-review.json`, `source-candidates.json` og `open-questions.json`. Særlig viktig: seilforeningens nye pirer fra 2025 er ikke avbildet sikkert; historiske kapasiteter fra 2013 er ikke nåtidsmålinger. Bryggen og Walberg er skilt, og Røsnes er klippet ved Halden-grensen. Kysten er systematisk bildesøkt i 137 celler / 35 ark, innlandet bare kandidatvis.

Arbeidsmappe `work/3105-sarpsborg/` har originalbilder, omprojiserte utsnitt/mosaikker, rå XML/PDF/HTML og QA utenfor Git. Disse må bevares separat for identisk visuell kontroll. `analysis-config/` bevarer lette innganger; `restore_config.py` kopierer dem tilbake uten overskriving. `build.py` og `finalize.py` stopper ved godkjent revisjon. Nye råuttak kan endre bildet og må ikke fremstilles som identisk rekonstruksjon. Gjeldende gren: `codex/sarpsborg-analysis`; ingen commit/push/PR bestilt for denne analysen.

### Sarpsborg rev-02 – rettet etter brukerinnspill

Gjeldende avventende revisjon er nå `data/kommuner/3105-sarpsborg/rev-02/`: 62 polygoner / 46 foreløpige grupper, 16 mulige, 61 usikre avgrensninger. Åtte polygoner / sju grupper er lagt til etter seks stedfestede brukerbilder. Holm er allerede kartlagt i Fredrikstad; Øketangen, Materialgården, Karlsøy bru, Bjerkenes og Kapellanveien ga tillegg. Alle 54 tidligere geometrier og ID-er er uendret; rev-01 er bevart. Se `user-feedback.json`, `revision-changes.json` og kommune-README. Elleve åpne avklaringer beholdes. Godkjente samledata/nettsted er uendret, og Halden er ikke startet.

Bruk `rereview_build.py`, `rereview_qa.py`, `rereview_validate.py` og `rereview_finish.py` for rev-02. Nye omriss og bildehenvisninger ligger i `rereview_decisions.py`. Brukeroriginaler, søkeutsnitt og QA ligger lokalt utenfor Git. De tidligere generiske skriptene bygger rev-01 og skal ikke brukes som erstatning for rev-02. Ingen commit, push eller PR er bestilt for denne rettingen.

### Sarpsborg rev-02 godkjent og innlemmet

Brukeren har godkjent Sarpsborg rev-02 og bestilt commit, push og PR. Samlefil og nettsted inneholder nå 692 polygoner / 21 godkjente kommuner. Sarpsborg bidrar med 62 polygoner / 46 foreløpige grupper, inkludert 16 mulige og 61 usikre avgrensninger. Elleve åpne avklaringer er beholdt. De 630 tidligere features er kontrollert uendret; se `data/kommuner/3105-sarpsborg/rev-02/approval.json`. Halden er ikke startet. Kjør `rereview_validate.py` for godkjent rev-02; byggeskriptene stopper ved godkjent revisjon.


### Halden rev-01 – ferdig til godkjenning 2026-10-31

Brukeren ba om Halden alene etter merge av Sarpsborg PR #12. Leveransen i `data/kommuner/3101-halden/rev-01/` har 66 polygoner / 31 foreløpige fysiske grupper, inkludert 11 mulige. Alle 66 avgrensninger trenger datert ortofotokontroll. Elleve åpne punkter er beholdt. Godkjente samledata og nettsted er uendret: 692 polygoner / 21 kommuner.

Kysten er gransket i 125 celler / 32 ark, supplert med 77 OSM-pirer i 29 klynger og 25 kontrollrammer. Nye bildefunn er blant annet Røsneskilen, Mørvik, Ystehedekilen, Sanderødstranda og Bakke. Kommunens båtplasskart, gjestehavn og Haldenkanalen er kildekontrollert. Eldre utriggere ved Sundsbrygga er ikke kopiert; usikre historiske Tista-rekker og gjestebrygga oppstrøms Brekke står åpne uten polygon. Innlandet er ikke fullkartlagt.

Røsnes har fem Halden-deler med `ROSNES-3101-3105`, klippet mot offisiell grense uten arealoverlapp med godkjente `3105-H20-B01/B02`. Sarpsborg-geometriene er uendret. Tre publiserte store plasser ved Felleskjøpet og gjestedelopplysninger er kapasitetskomponenter med begrenset omfang, ikke hele havnetall. Velbryggas 28 plasser i 2022 er ikke koblet sikkert til en bestemt Sponvika-brygge. Planforslag fra KU 2020 er ikke bygget-geometri.

Se kommune-README, `coverage.json`, `validation.json`, `visual-review.json`, `source-candidates.json`, `source-access-limitations.json` og `open-questions.json`. Originalbilder, rå XML/PDF/HTML og QA ligger lokalt i `work/3101-halden/` utenfor Git og må bevares separat. `analysis-config/` og `restore_config.py` bevarer lette innganger; ny nedlasting kan gi endret bildeinnhold. `build.py`/`finalize.py` stopper ved godkjent revisjon. Aktiv branch er `codex/halden-analysis`. Ingen commit, push, PR, innlemming eller neste kommune er bestilt for Halden.


### Halden rev-01 godkjent og innlemmet 2026-10-31

Brukeren godkjente og bestilte commit, push og PR. Alle 66 polygoner / 31 foreløpige anleggsgrupper er innlemmet, inkludert 11 mulige. Samlet 758 polygoner fra 22 kommuner. De 692 tidligere features er bevart uendret med kanonisk SHA-256 i `data/kommuner/3101-halden/rev-01/approval.json`. Alle 66 avgrensningers kontrollbehov, elleve åpne avklaringer, ukjent bildedato/drift og ufullstendig innlandskartlegging beholdes. Nettstedets lokale kartdata og kommunestatus er oppdatert; publisering følger merge/utrulling. Ingen neste kommune er startet. Bygg/finalisering av Halden stopper nå ved godkjent revisjon; teknisk kontroll bruker `work/3101-halden/validate.py`.


### Holmsåsen – avgrenset etterkontroll 2026-10-31

Brukerbildet av campingbukta er stedfestet i georefererte Esri-flybilder. Begge viste pirer manglet: H08 nordre pir beholdes som mulig småbåthavn (ti faste plasser/felles drift uklart), H09 søndre fellespir har minst ti tydelige plasser og klassifiseres som småbåthavn. To nye polygoner / to grupper ligger til godkjenning i `data/kommuner/3903-holmestrand/rev-02-holmsaasen/`. Eksisterende K04 med Holmsåsen-navn ligger nord for brukerbildets bukt; navnesøk alene var misvisende. To bilderammer og tilstøtende enkeltbrygger er kontrollert; dette er ikke full ny kommuneanalyse. Omriss er visuelt kontrollert og geometrier/ID-er/kommunegrense/overlapp/CSV kontrollert uten feil. Ukjent bildedato, nøyaktighet og operatører beholdes. Godkjent leveranse, samlet fil og nettsted er uendret. Læring: treff på stedsnavn må kontrolleres geometrisk før det hevdes at et brukerfunn allerede finnes.


### Holmsåsen godkjent og innlemmet 2026-10-31

Brukeren ba eksplisitt om innlemming av begge nye polygoner. H08 (mulig småbåthavn) og H09 (småbåthavn) er innlemmet med kjente usikkerheter. Samlet 760 polygoner / 22 kommuner; Holmestrand har nå 16 polygoner. De 758 tidligere features er bevart uendret, dokumentert med kanonisk SHA-256 i supplementets approval.json. Pilotleveransen rev-01 er uendret; godkjent supplement er koblet via status.json og kontrolleres sammen med hovedleveransen. Lokale kartdata er oppdatert. Ukjent bildedato, operatører og usikre avgrensninger beholdes.


### Porsgrunn rev-01 – ferdig til godkjenning 2026-10-31

Brukeren ba om Porsgrunn alene. Leveranse i `data/kommuner/4001-porsgrunn/rev-01/`: **56 polygoner / 28 foreløpige anleggsgrupper**, inkludert **3 mulige**, alle 56 med kontrollbehov. Tolv åpne avklaringer beholdes. Samlefil og nettsted er uendret, **760 polygoner / 22 godkjente kommuner**. Holmsåsen-supplementet kom inn parallelt før første Porsgrunn-bygg; start-/avstemte hasher er bevart i run.json.

62 OSM-klynger / 152 pirer og 25 ekstra kontrollrammer er vurdert. Hele hovedserien på 259 kyst-/elvenære 500 m-celler / 65 ark er visuelt lest. 51 hovedfliser dekker uttrekt marin OSM-kyst; tre historiske Clarity-mosaikker supplerer skyer over østlige øyer og åtte nordlige kontrollceller er ettersett. Dette er ikke fullstendighetsbevis. Innlandet og alle oppstrøms bekker/innsjøstrender er ikke fullkartlagt.

PMF, gjestehavner, Sundjordkanalen, Bråten, Herøya, Heistad, Døvik, Skjelsvik, Nystrand, Seivall, Brevik, Sandøya og Langangen/Kilen er kildekontrollert. Eiklund/Kreppa, Ørjevik, Bjønnes, Dåpan og Bjørkøybukta er også kontrollert som bildefunn. Kotøya, Dikkon-campingbrygga og Dåpan er mulige. Porselænsfabrikkens lille gjestebrygge og Dikkons molo er åpne uten polygon. PMV-planens110 plasser er ikke tegnet som eksisterende. Bro/rekkverk/landopplag ved Langangen ble først feiltolket og deretter forkastet ved eksportkontroll; foreningen i Kilen/Halvarp har egen, foreløpig stedskobling.

Alle eksporterte omriss er visuelt kontrollert; ID-er, geometri, grense, intern/nabo-overlapp, bildehasher og CSV-samsvar er validert. Kapasitetsdeler er ikke summert til nåtidstotaler: ventelistegrenser, medlemmer, utleiehendelser og 16 foreningseide Langangen-plasser er ikke ekstra havnekapasitet.

Råpakken på omtrent540 MB er lokalt i `work/4001-porsgrunn/`, utenfor Git. Bevar den separat; ny nedlasting er ikke identisk rekonstruksjon. Lette innganger i `analysis-config/`, kilde-/bildemanifester i leveransen. Bygg/finalisering stopper ved godkjent revisjon. Aktiv gren `codex/porsgrunn-analysis` i isolert arbeidsområde. Ingen commit, push, PR, innlemming eller neste kommune er bestilt. Ås er fortsatt uavklart kystkommune, ingen ny analyse startet.

## Porsgrunn rev-01 godkjent og innlemmet 2026-10-31

Brukeren godkjente 56 polygoner / 28 foreløpige anleggsgrupper, inkludert 3 mulige havner. Samlefilen og nettstedets lokale kartdata inneholder nå 816 polygoner fra 23 godkjente kommuner. Alle 760 tidligere godkjente feature-objekter er bevart uendret; SHA-256 og godkjenningstidspunkt er registrert i data/kommuner/4001-porsgrunn/rev-01/approval.json. Førkontrollen er bevart i validation-before-approval.json.

Alle 56 usikre avgrensninger, tolv åpne avklaringer, ukjente bildedatoer og ufullstendig innlandsgjennomgang beholdes. Godkjenningen gjør ikke disse sikre. Brukeren har senere bestilt commit, push og PR. Ingen publisering er bestilt. Ingen neste kommune startet; Ås står fortsatt som uavklart kystkommune.

## Miljøkort – pilot 31. oktober 2026

På brukerens bestilling er tre kildebaserte miljøkort laget for Lille Herbern, Karenslyst og Revierhavnen i data/miljokort/pilot-01/. Tretten observasjoner, fire kildearkiver med SHA-256, CSV/JSON og felles mal er bevart. Ingen kontakt eller befaring er utført. Tiltaksstatus skilles fra bevisstyrke og målt effekt. Karenslysts åpningstidspunkter spriker; Revierhavnens idriftsettelse er uavklart. Hullene er dokumentasjonshull, ikke bekreftet fravær av tiltak. Kartkoblinger trenger kontroll; delte tjenester og landarealer skal ikke tilordnes automatisk til sjøpolygon. Samlefilens 816 polygoner og nettstedet er uendret. Validering av kildereferanser, snapshot-hasher og CSV/JSON-samsvar er bestått. Ingen commit, push eller PR er bestilt for miljøkortpiloten.

### Miljøkort integrert i lokal kartvisning 2026-10-31

Tre egne stedspunkter og miljøkort er koblet inn via environment-cards.js og data/environment-cards.json. Ni kilder totalt: fire om tiltak, fem om stedfesting. Kartverket gir Lille Herbern navnepunkt og Karenslysts besøksadresse; Revierhavnen oppgir grov egen posisjon. Tilknyttede havnegrupper H13/H02/H23 gir geografisk kontekst, ikke verifiserte driftsgrenser. Karenslysts spyleplass og Revierhavnens Østslippen er fortsatt ikke presist stedfestet. Kilder, datoer, dokumentasjonshull og delte tjenester vises i kortene. Ingen rå-HTML publiseres. Godkjente 816 sjøpolygoner er uendret; ingen publisering, commit eller PR er utført for dette arbeidet.

Miljøkortene er etter brukerinnspill forenklet til 3–4 korte statuslinjer og én neste avklaring. Detaljer og kildeliste er samlet under «Kilder og grunnlag». Alle opprinnelige observasjoner er bevart; ingen ny miljøvurdering er lagt til. Nettleserkontroll av kortvisning og åpning av kildegrunnlag er bestått.

### Tre nye miljøkort 2026-10-31

Sonskilen (MK-04), Skjebergkilens Marina (MK-05) og Bispebrygga (MK-06) er lagt til i samme enkle kortvisning. Totalt seks kort, 25 observasjoner og 19 kildeoppslag i data/miljokort/pilot-01/. Alle nye kort er kontrollert i nettleseren. Besøks-/registeradresser fra Kartverket er tydelig skilt fra nøyaktig spyleplass; Bispebrygga har ingen bekreftet kobling til godkjent sjøpolygon. Ingen nye geometrier eller miljøeffekter godkjent. Lokalt nettsted oppdatert; ikke publisert. Validering av kilder, CSV/JSON og uendret samlefil samt 13 automatiske tester er bestått.

### Kildescreening av miljøkortgrunnlag 2026-10-31

Alle 664 offentlige anleggsgrupper er inventert. Minst 69 har begrunnet kortgrunnlag: 50 med konkrete tiltak/tjenester/rutiner og 19 med kun eldre fellesplaner. 595 er uavklart. 306 kildeoppslag, 77 vurderte evidensposter; 24 tilgangsfeil og seks gjenværende PDF-lesefeil. Fullstendig individuelt nettsøk for alle navn er ikke utført; dette er en nedre grense, ikke endelig totalt antall mulige kort. Delte tjenester og grensekryssende grupper telles uten duplikater. Bispebrygga holdes utenfor de 664 inntil sikker kobling foreligger. Se data/miljokort/screening-01/README.md, assessment.csv, kilde- og punktkontroller. Godkjente data og nettsted er uendret av screeningen.

### Miljøkort med vekt på båtvedlikehold

Etter brukerens tilslutning er de seks korte miljøkortene innrettet mot spylevann, båtpuss og arbeidsavfall. Én neste avklaring beholdes. Øvrige tiltak og alle opprinnelige observasjoner er bevart under kildegrunnlaget. Regelverkskontekst henviser til høringsutkastet og statsrådens status 16.10.2026 om revisjon og ny høring. Ingen anlegg er klassifisert som omfattet eller i samsvar med forskriften. Screeningtallet 69 gjelder fortsatt bredt miljøkortgrunnlag, ikke forskriftsomfang eller etterlevelse.

### Kapasitetsfilter i kartet

Under Layers → Filter finnes «200+ båtplasser». Filteret gjelder kartflater,
punkter, navn, havnesøk og turens havneutvalg. Dagens kilder gir 20 fysiske
havnegrupper med publisert kapasitet ≥200; dette er ingen fullstendig opptelling
av store havner. Ukjente og motstridende tall utelates, omtrentlige og eldre tall
merkes i havnekortet med kilde og referanseperiode. Moss bruker siste separate
kildegjennomgang; kommunegrensedelte grupper får felles kapasitet uten summering.
Filteret sier ingenting om forskriftsvirkeområde eller etterlevelse.
Bygges med `scripts/harbour_capacity.py` via `scripts/build_flyover_data.py`.

### Arealanslag for kapasitet

Etter brukerbestilling er arealmodell v1 testet og lagt til lokalt. 97 publiserte
kapasiteter, 15 berørte kommuner; 62 treningsgrupper i Sandefjord. Kommunebalansert
logmodell har medianavvik 26,4 % ved kommuneblokkert validering. 567 ukjente får
grove anslag: 16 trolig ≥200, 203 trolig under 200, 348 usikre. Utenfor
kalibreringsarealet og mulige havner beholdes som usikre; ingen sannsynlighet
eller intervallgaranti hevdes. Standardfilteret er fortsatt publisert kapasitet.
Valgfritt inkluderes trolige, eller også mulige treff fra øvre spenn. Kart, søk
og tur bruker samme filterfunksjon. Publiserte tall og godkjente geometrier er
bevart. Modellgrunnlag, kilde-ID-er og holdte prediksjoner publiseres i separat
capacity-model.json. Se docs/KAPASITETSANSLAG.md for reproduksjon og begrensninger.

Mobilvisningen (≤720 px) er begrenset til én bryter for 200+ med publisert
kapasitet, kort treffantall og beskjed om at ukjent kapasitet utelates.
Modellvalg og lange modellforklaringer vises bare på større skjermer.
Havnekort kan fortsatt vise én kort linje med arealanslag og usikkerhetsspenn.
Ved overgang fra stor til liten skjerm nullstilles modellvalget til publisert,
slik at et skjult modellvalg ikke endrer mobilfilterets betydning.

### Rettet oppstartsfeil på produksjonsadresse uten skråstrek

Vercel bruker `/labs/oslofjord-bathavner` uten avsluttende skråstrek. Relative
skriptstier løste derfor til `/labs/`, og manglende CapacityFilter ga en TypeError
under init, feilaktig vist som «Could not load data». Skript, miljøkortdata og
modell-lenker bruker nå eksplisitt nettstedsti. Filteret faller tilbake til
publisert kapasitet hvis tilleggsmodulen mangler. Regresjonstest dekker rutene
uten skråstrek, med skråstrek og med index.html. Testserver må ha `site/` som rot;
server fra selve labs-mappen gjenskaper ikke produksjonsrutingen.

### Flyover-rute med alle kartlagte kommuner

Rutens eldre liste manglet Porsgrunn, Bamble, Halden, Sarpsborg og Nordre Follo.
Alle 23 er nå med; retur til Oslo vises separat og øker ikke kommunetelleren.
Ruteutvalget hentes fra kommunedata med geografisk rekkefølge og automatisk
inkludering av nye kommuner som ikke er ført opp i rekkefølgen. Aktivt
kapasitetsfilter begrenser fortsatt turen til kommuner med treff, og telleren
følger dette utvalget. Regresjonstest kjører faktisk rutebygging mot kartdata,
kontrollerer 23 unike kommuner, retur, fremtidige kommuner og filtrert tur.

### Norsk og engelsk nettside

Nettsiden har norsk bokmål som standard og språkvelger «Norsk / English» på både
mobil og stor skjerm. Valget lagres lokalt i nettleseren; blokkert lagring
hindrer ikke språkbytte. `html lang`, sidetittel, beskrivelse, tilgjengelighets-
etiketter, kartkontroller, tur, filter, metode-/informasjonspaneler, Moss-
berikelse og miljøkort bruker språkvalget. Kartposisjon, tur og filter beholdes
ved språkbytte; åpne kort oppdateres uten ny kameraflyging. Mobilfilteret er
fortsatt begrenset til publisert kapasitet. Stedsnavn og kildetitler beholdes;
opprinnelige kartleggingsnotater vises merket på originalspråket.

Oversettelser ligger i `site/labs/oslofjord-bathavner/i18n.js`. Statiske tekster
merkes med `data-i18n` og tilsvarende attributtmarkører; dynamiske tekster bruker
`t`/`tx` og navngitte parametere. Godkjente kartdata og kildefakta endres ikke av
oversettelsene. Tester dekker norsk standard, lagring/lagringsfeil, like
parametere i begge språk, alle brukte statiske nøkler og engelske oversettelser
av samtlige miljøkortoppsummeringer og strukturerte evidenstekster.

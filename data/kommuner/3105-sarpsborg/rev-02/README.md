# Sarpsborg – rev-02 godkjent

**62 polygoner / 46 foreløpige anleggsgrupper**, inkludert **16 mulige havner** og **61 usikre avgrensninger**. Alle har ukjent lokal opptaksdato. Rev-01 er bevart. Brukeren har godkjent rev-02 og bedt om commit, push og PR. Samledata og nettsted er oppdatert: 692 godkjente polygoner / 21 kommuner. Kjente usikkerheter og elleve åpne avklaringer er beholdt.

Revisjonen følger brukerens seks skjermbilder. Holm ligger i Fredrikstad og finnes allerede som 3107-H60-B01/B02. Ved de fem øvrige stedene er **åtte nye polygoner / sju grupper** lagt til: to separate mulige pirer ved Øketangen, et mulig L-anlegg ved Materialgården, to pirer i én gruppe ved Karlsøy bru, en fellespir nordvest på Bjerkenes og to separate mulige pirer langs Kapellanveien. Små private nabobrygger er ikke summert for å nå ti-plassregelen.

Jeg overså disse fem stedene i første gjennomgang. En registrert kystscreening og full OSM-/bildedekning er ikke bevis på at alle havner ble gjenkjent. Egne utsnitt og brukerbildene gjør plassmønstrene lettere å tolke. Ved Øketangen, Materialgården og Kapellanveien er kapasitet/felles drift fortsatt uavklart; derfor mulig klasse. Ingen nye kapasitetstall er konstruert fra antall synlige båter.

Alle 54 tidligere geometrier og ID-er er kontrollert uendret. Alle åtte nye omriss er visuelt kontrollert etter eksport; teknisk kontroll viser gyldig geometri, unike ID-er, 0 m² utenfor kommunen, ingen intern overlapp eller overlapp med godkjente data og fullt CSV-samsvar. Se `revision-changes.json`, `visual-review.json`, `validation.json` og `user-feedback.json`.

GeoJSON og metadata-CSV har 62 samsvarende rader. Kandidatloggen dekker 59 OSM-klynger, 36 ekstra søke-/kontrollrammer og 28 historiske kommunekandidater. Rammer og kildekandidater er ikke nye havner. Opprinnelig systematisk kystscreening omfattet 137 celler / 35 ark; revisjon 2 er en målrettet kontroll av brukerinnspill, ikke en ny fullstendig kystgjennomgang. Innlandet er fortsatt ikke fullkartlagt.

De ti tidligere avklaringspunktene er beholdt, med ett nytt punkt om brukerfunnenes drift, plassantall og bildedato. Særlig beholdes seilforeningens usikre 2025-utvidelse, historiske kapasitetsavvik og Røsnes ved Halden-grensen. Gruppene er foreløpige, ikke en opptelling av juridiske operatører. Se rev-01/README.md for opprinnelig metode- og kildegrunnlag.

Brukerbildene er bevart lokalt med SHA-256. De inneholder ikke CRS/koordinater; stedfesting bruker samsvarende kystform, hus, veier og pirer mot de bevarte georefererte bildene. Skjermbildenes opptaksdato er ukjent; de er ikke automatisk nyere enn Esri-bildene. Originaler, råkilder og QA ligger utenfor Git i `work/3105-sarpsborg/` og må bevares separat for identisk visuell etterprøving. Kilde- og bildemanifestene viser provenienskjeden.

Skript: `rereview_decisions.py`, `rereview_build.py`, `rereview_qa.py`, `rereview_validate.py` og `rereview_finish.py`. Veggklokketid og måleomfang står i `timing.json`; tokens/pris er ikke målt. Rev-02 er godkjent og innlemmet. Ingen neste kommune er startet.

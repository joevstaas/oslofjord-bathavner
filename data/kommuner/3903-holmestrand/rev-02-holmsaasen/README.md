# Holmsåsen – avgrenset ny analyse, til godkjenning

To nye polygoner / to separate anleggsgrupper i campingbukta fra brukerbildet:

- **3903-H08-B01, nordre pir:** mulig småbåthavn. Sammenhengende pir med utriggere, men ti faste plasser kan ikke telles sikkert. Operatør og faste plasser er ikke dokumentert.
- **3903-H09-B01, søndre pir:** småbåthavn. Én fellespir med tydelig sammenhengende plassmønster og minst ti plasser. Dette er en terskelvurdering, ikke oppgitt kapasitet.

Begge var fraværende i godkjent leveranse. Gamle `3903-K04-B01`, «Holmsåsen – søndre bryggegruppe», ligger nord for bukta i brukerbildet. Navnelikhet ga først et misvisende svar; koordinat- og bildekontrollen avklarer at ingen av de to nye pirene dekkes av dette polygonet. Det gamle omrisset beholdes uendret. Denne leveransen er et supplement, ikke en full revisjon av kommunen.

## Grunnlag og avgrensning

To georefererte Esri-rammer er gjennomgått: nordlig oversikt 800 × 800 m og campingbukt/sørlig nærområde 800 × 800 m, med overlapp. Brukerbildet er gjenkjent på strandlinje, campingrekker, vei og begge pirer; omriss er tegnet i det hentede georefererte bildet. Andre små enkeltbrygger langs boliger nord og sør og rundt neset er sett, men ikke summert til et havneanlegg. Etablert Holm Brygge og gamle K04 i nord gir ikke grunnlag for å slå sammen de to pirene i bukta. Ingen felles juridisk operatør hevdes.

Flybildenes opptaksdato og absolutte nøyaktighet er ukjent. Hentetid er ikke opptaksdato. Esri svarte tomt for enkelte eksportforespørsler; det vellykkede bildet ble hentet i EPSG:3857 og eksplisitt omprojisert til EPSG:25833 med bevart original. Prosessering og SHA-256 står i bildemetadataene. Offentlige campingopplysninger bekrefter beliggenhet, men dokumenterer ikke pirenes operatør eller kapasitet.

## Kontroll

`review-overlay.jpg` og to detaljpaneler er visuelt kontrollert etter eksport. Geometriene er gyldige, har unike ID-er og 0 m² utenfor kommunegrensen, innbyrdes overlapp eller overlapp med samlet fil. GeoJSON og metadata-CSV er sammenholdt. Navn er beskrivende. Godkjent rev-01, samlefil og nettsted er uendret; supplementet venter på brukergodkjenning.

Reproduksjon: `work/3903-holmestrand/holmsaasen-review/build.py`. Pikselpunkter og eksakt bilderamme står også i `digitisation.json`. Se `open-questions.json` for gjenstående usikkerheter.

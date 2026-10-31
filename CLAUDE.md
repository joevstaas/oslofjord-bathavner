# Instrukser for videreføring

Les docs/METODIKK.md, docs/OVERLEVERING.md og status.json før arbeid.
Metodikken er autoritativ. Historiske kommunelogger beskriver status på det tidspunktet; status.json viser dagens status.

## Godkjent status
Holmestrand, Horten, Tønsberg, Færder, Sandefjord, Larvik, Moss, Råde, Fredrikstad, Bærum, Asker, Lier, Drammen, Oslo, Nordre Follo, Nesodden, Frogn, Vestby, Hvaler og Bamble er godkjent.
Samlet GeoJSON inneholder 630 polygoner fra 20 kommuner. Nordre Follo rev-01 er godkjent og innlemmet (én saltvannshavn og én mulig ferskvannshavn); usikkerhetene er beholdt. Nesodden rev-01 er godkjent og innlemmet: 11 polygoner / 11 anleggsgrupper, inkludert 3 mulige. Åpne avklaringer og usikkerheter er beholdt. Frogn rev-01 er godkjent og innlemmet: 24 polygoner / 18 anleggsgrupper, inkludert én mulig (Bergholmen). Ti usikre avgrensninger og fem åpne kildeavklaringer beholdes. Vestby rev-01 er godkjent og innlemmet: 9 polygoner / 8 anleggsgrupper, inkludert 3 mulige. Alle 9 avgrensninger har kontrollbehov. Kapasitetsavvik og åpne avklaringer er beholdt. Hvaler rev-01 er godkjent og innlemmet: 69 polygoner / 66 foreløpige anleggsgrupper, inkludert 20 mulige. 68 avgrensninger har kontrollbehov; sju åpne kildeavklaringer og ukjent bildeopptaksdato beholdes. Bamble rev-02 er godkjent og innlemmet: 59 polygoner / 53 anleggsgrupper, inkludert 13 mulige og 33 usikre avgrensninger. Skydekte kontrollhull og åpne avklaringer beholdes. Samledata og nettsted er oppdatert. Ingen neste kommune er startet.
Prosjektomfang: alle kommuner med kystlinje mot indre eller ytre Oslofjord. Brukeren godkjenner hver kommune ved å se på GeoJSON-filen.

## Arbeidsregler
- Arbeid med én kommune om gangen, bare etter brukerens beskjed.
- Vent på eksplisitt godkjenning før neste kommune og før innlemming i samlefilen.
- Bevar kjente usikkerheter og åpne kandidater etter godkjenning.
- Lever GeoJSON og metadata-CSV. Registrer både anlegg og polygoner.
- Bruk ti-plassregelen og unntakene nøyaktig slik metodikken beskriver.
- Foreningsadresse er ikke bevis for havneposisjon. Planområde er ikke eksisterende havn.
- Bevar originalbilder, georeferering, kildehenvisninger og kandidatbeslutninger.
- Kontroller alle eksporterte omriss visuelt mot bildene, og valider geometri, ID-er, kommunegrense, overlapp og CSV-samsvar.
- Registrer veggklokketid. Ikke fremstill anslått tokenforbruk eller pris som målt.
- Oppdater metodikk og status. Hold kommunikasjonen kort og på norsk.
- Bruk relative stier. Opprett nye revisjoner; ikke overskriv godkjente geometrier.

## Lokal oppstart
Opprett .venv med Python 3.11 eller nyere og installer requirements.txt.
Kjør python scripts/validate_project.py. Det skal gi 630 polygoner / 20 kommuner.
Skriptet bruker prosjektets plassering, ikke /workspace.

## Historiske skript
archive/original er kilde-/kontrollarkiv, ikke en automatisk produksjonspipeline.
Ikke kjør finish.py, finalize.py, build_dataset.py eller andre historiske skript direkte mot godkjente leveranser.
De kan overskrive status, datoer, kildefiler eller godkjenninger. Kopier og tilpass dem i work/ ved behov.
Gamle sys.path-innsettinger til deps er ikke lokale installasjoner; bruk .venv.

## Første oppgave
Kontroller overleveringen og relative filstier. Rapporter manglende underlag.
Ikke start neste kommune før brukeren ber om det.

# Instrukser for videreføring

Les docs/METODIKK.md, docs/OVERLEVERING.md og status.json før arbeid.
Metodikken er autoritativ. Historiske kommunelogger beskriver status på det tidspunktet; status.json viser dagens status.

## Godkjent status
Holmestrand, Horten, Tønsberg, Færder, Sandefjord, Larvik, Moss, Råde, Fredrikstad, Bærum, Asker, Lier, Drammen, Oslo, Nordre Follo, Nesodden, Frogn, Vestby, Hvaler, Bamble, Sarpsborg, Halden og Porsgrunn er godkjent.
Samlet GeoJSON inneholder 817 polygoner fra 23 kommuner. Nordre Follo rev-01 er godkjent og innlemmet (én saltvannshavn og én mulig ferskvannshavn); usikkerhetene er beholdt. Nesodden rev-01 er godkjent og innlemmet: 11 polygoner / 11 anleggsgrupper, inkludert 3 mulige. Åpne avklaringer og usikkerheter er beholdt. Frogn rev-01 er godkjent og innlemmet: 24 polygoner / 18 anleggsgrupper, inkludert én mulig (Bergholmen). Ti usikre avgrensninger og fem åpne kildeavklaringer beholdes. Vestby rev-01 er godkjent og innlemmet: 9 polygoner / 8 anleggsgrupper, inkludert 3 mulige. Alle 9 avgrensninger har kontrollbehov. Kapasitetsavvik og åpne avklaringer er beholdt. Hvaler rev-01 er godkjent og innlemmet: 69 polygoner / 66 foreløpige anleggsgrupper, inkludert 20 mulige. 68 avgrensninger har kontrollbehov; sju åpne kildeavklaringer og ukjent bildeopptaksdato beholdes. Bamble rev-02 er godkjent og innlemmet: 59 polygoner / 53 anleggsgrupper, inkludert 13 mulige og 33 usikre avgrensninger. Skydekte kontrollhull og åpne avklaringer beholdes. Samledata og nettsted er oppdatert. Sarpsborg rev-02 etter seks brukerinnspill er godkjent og innlemmet: 62 polygoner / 46 foreløpige anleggsgrupper, inkludert 16 mulige og 61 usikre avgrensninger. Åtte polygoner / sju grupper er lagt til; de 54 tidligere geometrier er uendret. Holm er allerede i Fredrikstad. Se data/kommuner/3105-sarpsborg/rev-02/README.md og user-feedback.json. Samledata og nettsted er oppdatert. Elleve åpne avklaringer og øvrige usikkerheter beholdes. Halden rev-01 er godkjent og innlemmet: 66 polygoner / 31 foreløpige anleggsgrupper, inkludert 11 mulige. Alle 66 avgrensninger trenger datert ortofotokontroll; elleve åpne punkter og ufullstendig innlandskartlegging beholdes. Se data/kommuner/3101-halden/rev-01/README.md. Halden er innlemmet i samledata og nettsted.
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
Kjør python scripts/validate_project.py. Det skal gi 817 polygoner / 23 kommuner.
Skriptet bruker prosjektets plassering, ikke /workspace.

## Historiske skript
archive/original er kilde-/kontrollarkiv, ikke en automatisk produksjonspipeline.
Ikke kjør finish.py, finalize.py, build_dataset.py eller andre historiske skript direkte mot godkjente leveranser.
De kan overskrive status, datoer, kildefiler eller godkjenninger. Kopier og tilpass dem i work/ ved behov.
Gamle sys.path-innsettinger til deps er ikke lokale installasjoner; bruk .venv.

## Første oppgave
Kontroller overleveringen og relative filstier. Rapporter manglende underlag.
Ikke start neste kommune før brukeren ber om det.

## Porsgrunn godkjent
Porsgrunn rev-01 er godkjent og innlemmet: 56 polygoner / 28 foreløpige anleggsgrupper, inkludert 3 mulige. Alle 56 avgrensninger har kontrollbehov; tolv åpne punkter og ufullstendig innlandsgjennomgang beholdes. Se data/kommuner/4001-porsgrunn/rev-01/README.md. Samledata og nettstedets lokale kartdata er oppdatert: 817 polygoner / 23 godkjente kommuner. Brukeren har bestilt commit, push og PR for Porsgrunn. Ingen neste kommune startet. Ås står fortsatt som uavklart kystkommune i restlisten.

Bispebrygga-supplement 0301-H33 er godkjent og innlemmet 2026-11-01. Oslo har 37 polygoner / 33 havnegrupper; samlet 817 polygoner / 665 fysiske grupper. Miljøkort MK-06 er geografisk koblet; driftsgrenser og spyleplass er fortsatt uavklart.

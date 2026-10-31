# Porsgrunn – rev-01 godkjent

**56 polygoner / 28 foreløpige anleggsgrupper**, inkludert **3 mulige havner**. Alle avgrensninger har kontrollbehov. Brukeren godkjente revisjonen 2026-10-31T18:15:36Z. Alle 56 polygonene er innlemmet i samledata og nettstedets lokale kartdata. Kjente usikkerheter er beholdt.

Leveranse: `bathavner.geojson` (WGS84) og `metadata.csv` (semikolon, identiske egenskaper per polygon). Fysiske grupper er ikke en juridisk operatøropptelling. `candidate-ledger.json/.csv` dekker 62 OSM-klynger med 152 pirer, 25 supplerende kontrollrammer og delkandidater. Alle kandidatbeslutninger og manuelle pikselomriss er bevart.

259 celler à 500 m / 65 ark er visuelt gjennomgått, inkludert skjærgården og Porsgrunnselva. Marine OSM-kystlinjer har bildedekning: 171276.9 m med 20 m kontrollbelte, 0 m utenfor bildeflisene. Dette er ikke fullstendighetsbevis. Tre historiske Clarity-mosaikker supplerer skyområdene; åtte nordlige buffer-/elvefelt er kontrollert på nytt. Noen svarte landfelt gjenstår. Hele innlandet og alle oppstrøms vannløp er ikke systematisk fullkartlagt.

Havnene omfatter blant annet PMF, Down Town, Østre Brygge, Sundjordkanalen, Bråten, Herøya, Heistad, Døvik, Skjelsvik, Nystrand, Seivall, Brevik, Sandøya og anlegg på øyene. Kilen/Halvarp er foreløpig koblet til Langangen Motorbåtforening gjennom stedsnavn, plassmønster og egne bilder; presis delkobling beholdes åpen. En tidlig brutolkning ved Langangen ble forkastet. Porselænsfabrikkens lille gjestebrygge og Dikkons gjestemolo er åpne uten konstruerte polygoner. Kotøya, Dikkon-campingbrygga og Dåpan er mulige anlegg.

Ingen total nåtidskapasitet oppgis. Avgrensede `capacity_components` bevarer Down Towns 25 gjesteplasser, Herøyas ca.170 i 2019, Brevik-foreningens 460 for hele foreningen og Langangens ulike del-/eierskapsopplysninger. Ventelister, medlemstall, utleiehendelser og eierskapsdeler er ikke summert som båtplasser. PMVs planlagte110 plasser og andre fremtidige utvidelser er ikke digitalisert.

Alle 56 endelige omriss er kontrollert med eksportert GeoJSON som overlegg. Teknisk kontroll: gyldig geometri, unike ID-er, 0 m² utenfor kommunen, ingen intern arealoverlapp eller overlapp med de 760 godkjente polygonene, fullt CSV-samsvar. Se `validation.json`, `visual-review.json`, `coverage.json` og tolv punkter i `open-questions.json`. Godkjent grunnlag ble oppdatert parallelt med Holmsåsen før første Porsgrunn-bygg; opprinnelige og avstemte hasher er bevart i `analysis-config/run.json`. Porsgrunn-arbeidet endret ikke godkjente geometrier.

Originalbilder, native EPSG:3857-bilder/fliser, avledede UTM-mosaikker, rå XML/HTML/PDF og QA ligger lokalt i `work/4001-porsgrunn/` utenfor Git. Bevar denne råpakken separat for identisk etterprøving. `imagery-manifest.json` og `source-manifest.json` bevarer URL-er, georeferering, transformasjonskjeder og SHA-256. Oppskalering gir ikke bedre opptaksoppløsning. Lokal bildedato/nøyaktighet er ikke verifisert for alle polygoner; ett Herøya-metadataoppslag er bare en lokal prøve.

Skript: `work/4001-porsgrunn/build.py`, `qa.py`, `validate.py`, `finalize.py`, `restore_config.py`. Lette innganger er bevart i `analysis-config/`. Ny nedlasting kan gi andre bilder; identisk råpakke trengs for identisk visuell rekonstruksjon. Bygg/finalisering stopper ved godkjent revisjon. Målt veggklokke: 3559 sekunder; tokens og pris er ikke målt.

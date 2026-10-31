# Miljøkort – seks piloter, 31. oktober 2026

Kildebaserte miljøkort med åpne dokumentasjonshull. Ingen befaring eller direkte henvendelser er utført. Ingen samlet miljøscore eller sertifisering. Godkjente havnedata er uendret. Miljøkort er integrert i nettstedets lokale kartvisning som et separat punktlag.

- [Lille Herbern – Oslo Seilforening](lille-herbern.md): opplyst etablert oppsamling og delt rensing.
- [Karenslyst båtopplag](karenslyst.md): leverandørbeskrevet anlegg; kilder spriker om åpningstidspunkt.
- [Revierhavnen](revierhavnen.md): spyleplass omtalt under etablering, ferdigstillelse uavklart.
- [Felles mal](mal.md) for videre havner.

Maskinlesbare kort ligger i cards.json og observasjoner i observations.csv. sources.json registrerer 19 kilder (åtte tiltakskilder og elleve stedfestingskilder), utgiverrolle, dokumentdato, kontrolltidspunkt og SHA-256 for lokale HTML-snapshots i sources/. Råsidene bevares som kildearkiv; dette gir ingen videre rett til publisering av hele nettsider. Avsnittshenvisninger gjør påstandene sporbare. baseline.json identifiserer uendret samlefil.

Ingen bekreftede tiltakshull er funnet: hullene gjelder dokumentasjonen vi har gjennomgått. Temaer som ikke er undersøkt, blant annet naturkartoverlapp, er uavklart. Geografisk kontekst er kontrollert mot navnepunkt, operatørposisjon og publisert adresse. Kobling til 0301-H13, 0301-H02 og 0301-H23 er geografisk kontekst, ikke bekreftede driftsgrenser. Karenslysts punkt er besøksadresse; eksakt spyleplass er uavklart. Revierhavnens posisjon er grovt oppgitt. Sjøpolygoner representerer ikke spyleplasser på land. Delte renseanlegg registreres som relasjoner, ikke kopiert som egne anlegg i hver havn.

Neste steg er datert operatørbekreftelse og driftsbilag for Lille Herbern, prøverapporter og avklart tidslinje for Karenslyst, samt idriftsettelsesstatus for Revierhavnen. Oppfølgingsspørsmål ligger i hvert kort. Ingen kontakt er tatt og ingen frister er avtalt.

Nettstedets meny «Miljøkort», de seks stedspunktene og lenker fra aktuelle havnekort åpner kortene. Kartlag bygges med `python scripts/build_environment_cards.py`, også fra `build_flyover_data.py`. Råsidene inngår ikke i nettstedets data. Delte tjenester vises som kildebelagte relasjoner; anleggenes eksakte posisjon er ikke oppfunnet.

Kortvisningen er forenklet til 3–4 statuslinjer og én neste avklaring. Alle observasjoner, omfang, kildehenvisninger og dokumentdatoer er beholdt under «Kilder og grunnlag». Kildelisten vises én gang per kort.

## Utvidelse: Sonskilen, Skjebergkilens Marina og Bispebrygga

- [Sonskilen](sonskilen.md): sandfang/filter, båtpuss og avfall; drift og måleprøver gjenstår.
- [Skjebergkilens Marina](skjebergkilen.md): vaskestasjon, avfall og septik; renseløsning og måleprøver gjenstår.
- [Bispebrygga](bispebrygga.md): datert ferdigmelding fra 2023 og avfallsrutine; drift i dag og prøver gjenstår.

Totalt seks kort og 25 observasjoner. Nye punkter bygger på publisert besøksadresse eller registeradresse, kontrollert mot Kartverket. De angir ikke nøyaktig spyleplass. Sonskilen er knyttet til 3216-H02 og Skjebergkilen til 3105-H33 som geografisk kontekst. Bispebrygga vises kun ved registeradressen, uten antatt kobling til et sjøpolygon. Ingen befaring eller direkte operatørbekreftelse er gjennomført.

## Prioritering etter forskriftssjekk

Kortene viser nå tre faste temaer: spylevann, båtpuss og arbeidsavfall, samt én neste avklaring. Septik, øvrige tiltak, effekt og full kildehistorikk beholdes under «Kilder og grunnlag». Regulatory-context.json viser at det opprinnelige høringsforslaget er under revisjon, jf. offisiell status 16.10.2026. Verken virkeområde eller regelverksetterlevelse er vurdert for anleggene. Opplysninger om kapasitet i sjø og på land, faktisk vedlikeholdsaktivitet og ansvar må avklares separat.

# Berikelsespilot – Moss, 31. oktober 2026

Status: ferdig kildegjennomgang; brukeren har bedt om publisering i nettstedets havnekort som et separat kildeberikelseslag. Godkjente primærdata endres ikke. Omfang: alle 22 eksisterende anlegg / 26 polygoner og de to åpne kandidatene Sjekta og Refsnes småbåtforening. Pilotens referanse er Moss rev-01. Godkjent geometri, klassifisering og tidligere egenskaper er bevart.

## Resultat

- 22 anlegg har en egen berikelsesrad; en gjennomgått rad betyr ikke at alle felt er avklart.
- 91 observasjoner med felt, verdi, kilde-URL, innhentingstidspunkt, omfang og linjehenvisning i lagret tekstuttrekk.
- 8 anlegg har nye kontrolloppslag som gir tallfestet, publisert kapasitet. Flere verdier var kjent fra før; antallet er ikke åtte nyoppdagede kapasiteter.
- 12 anlegg har en navngitt operatørrelasjon i piloten, med ulik bevisstyrke. Historisk blogg, salgsannonse og fleroperatørgruppe er merket særskilt; dette er ikke 12 bekreftelser på aktuell fysisk drift.
- 4 anlegg har kildestøtte for opplag på land. For Kambo Marina er støtten en tjenestelenke i menyen, svakere enn en eksplisitt kapasitetsbeskrivelse.
- 39 direkte kildeoppslag: 38 vellykkede og ett utilgjengelig nettsted. Dette er kildeoppslag, ikke 39 uavhengige beviskilder; flere sider tilhører samme operatør.
- 10 avvik/avklaringsbehov er registrert. Sjekta og Refsnes er fortsatt åpne, uten nye geometrier.
- Ingen nye landpolygoner, befaringer, bildebaserte tellinger eller direkte operatørhenvendelser er utført. Det finnes ikke tidsfestet bekreftelse på dagens drift eller dagens rensing i piloten.

## Leveranser

| Fil | Innhold |
| --- | --- |
| `harbours.csv` / `harbours.json` | Én rad per eksisterende `harbour_id`; 22 rader. Nye felt er separat fra baselineverdier. |
| `observations.csv` / `observations.json` | Autoritativt bevisregister, inkludert historiske og motstridende opplysninger. |
| `candidates.csv` / `candidates.json` | Sjekta og Refsnes; null `harbour_id` og geometri. |
| `deviations.csv` / `deviations.json` | Avklaringer som kreves før sikker oppdatering av primærdatasettet. |
| `reference-map.geojson` | Kopi av de 26 godkjente geometriene og egenskapene med ett ekstra `enrichment_pilot`-objekt. Dette er et referanseeksport, ikke en ny godkjent kommuneleveranse. |
| `sources.json` | Direkte URL-er, innhentingstid, feil, HTTP-metadata, kontrollsummer og arkivstier. |
| `sources/S*.txt` | Tekstuttrekk fra nettsider; scripts/stiler er fjernet. Dette er ikke gjengitte nettlesersider. |
| `sources/BR*.txt` | Utvalgte organisasjonsfelt fra Enhetsregisterets API. Registeradresse er ikke brukt som havneposisjon. |
| `sources/web-*.json` | Arkiv over søk og sideoppslag som ble brukt til å finne og undersøke kildene. Søkesnutter er ikke alene brukt til promoterte tall. |
| `metrics.json`, `validation.json` | Målbare resultater og kontroller. |
| `baseline.json`, `timing.json` | Kontrollsummer før berikelse og målt veggklokketid fra baselinefangst; innledende rekognosering før dette er ikke medregnet. |

## Viktigste konkrete berikelser

| Anlegg | Kildeopplysning | Tolkning |
| --- | --- | --- |
| Fiske, H01 | 376 båtplasser på operatørens om-side | Eldre avfallsplan har 384. Begge beholdes; faktisk endring er ikke dokumentert uten sammenlignbare referansedatoer. |
| Fuglevik/Rygge, H02 | 409 båtplasser og 7 faste gjesteplasser | Separate observasjoner; summen 416 innføres ikke automatisk som sammenlignbar kapasitet. |
| Kambo båtforening, H03 | Ca. 100 båtplasser; vinteropplag og truck/slipp/rampe | Omtrentlig verdi; eldre 97 bevares. |
| Kambo Marina, H04 | Marina med plass til 300 båter | Kildetallet 300 er kontrollert også på operatørens forside. |
| Betongen, H05 | Ca. 360 på vann og 200 på land for vinterlagring | Landkapasitet er separat. Presisjonsnivået til 200 er ikke entydig formulert og står derfor ukjent. |
| Søly, H10 | 306 båtplasser; gjester bruker ledige medlemsplasser; landopplag og løft/rampe | Gjesteanløp er ikke nødvendigvis ekstra plasser. Historisk oljeutskiller er ikke dokumentasjon på aktuell behandling av bunnstoff. |
| Vansjø, H11 | 168 båtplasser og 16 jolleplasser | Kategoriene holdes adskilt fra eldre tall 185. Anlegget ligger i ferskvann og skal ikke inngå i en ukritisk marin total. |
| Verket, H12 | Verket Havn AS, org.nr. 918686878, oppgir sesong- og gjestetilbud | Eksakt gjesteområde må avstemmes mot polygonet. Siden blander priser for 2027 med vilkår merket 2025. |
| Knutvika/Teibern, H16 | Vindsteg beskriver tre utleiere, ABF har eget tilbud | Ingen samlet kapasitet eller interne operatørgrenser er konstruert. |
| Moss gjestehavn, H19 | Moss Havn beskriver begge kanalsider og Tollbodbrygga | Støtter havnegruppens funksjon, uten ny geometritolkning eller kapasitetstelling. |
| Røedsstranda, H21 | Salgsbeskrivelse angir 16 plasser og felles bryggeanlegg | Uavhengig av den eldre planen som dokument, men det er ikke undersøkt om opplysningene bygger på samme bakgrunn. Ikke likestilt med operatørbekreftelse. |

## Dataskjema og bruk

JSON er kanonisk for typer og nullverdier. CSV bruker UTF-8 med BOM og semikolon; null blir tom celle, mens lister og objekter er JSON i cellen. Tabellene kan kobles via `harbour_id`, observasjonene via `subject_id`. Åpne kandidater får egne `candidate_id` og skal ikke kobles til et eksisterende anlegg uten bevis.

`berths_published` er kildens tall, ikke et verifisert totalt antall faste plasser. Les alltid `berths_scope`, `berths_approximate`, `capacity_quality` og observasjonens note. Tall, jolleplasser, gjesteplasser og opplag summeres ikke i denne leveransen. Hver kapasitet gjelder et anlegg eller en eksplisitt operatørkomponent, aldri hvert delpolygon.

`land_storage_reported`, `lifting_reported` og `ramp_reported` betyr at en kilde beskriver funksjonen; de dokumenterer ikke ny befaring, aktuell tilgjengelighet eller en landgeometri. Null betyr ukjent, ikke nei. `current_operation_verified` og `wastewater_treatment_current` er null for alle anlegg.

`operator_link_status` skiller operatørpublisering, historisk geografisk kobling, salgsopplysninger og fleroperatørgrupper. Et registertreff uten bekreftet kobling er bare en `candidate_registered_entity`-observasjon. Et nytt registrert navn på samme organisasjonsnummer tolkes ikke automatisk som operatørskifte.

`reference_date` er tidspunktet opplysningen gjelder, når kjent. `accessed_utc` er vårt innhentingstidspunkt. Innhentingsdato, oppdateringsdato på nettsiden og copyrightår brukes ikke som dato for kapasitet eller drift. Den eldre avfallsplanens periode er bare anslått til ca. 2020 og står som ukjent eksakt referansedato.

Kvalitet beskrives per dimensjon: identitet, kapasitet, funksjon, tid og geometri. Geometrien er ikke revurdert i denne piloten. Det er ikke laget en samlet poengsum som skjuler forskjellene.

## Hva som gjenstår

Prioriter polygon-/operatørkoblinger i Rørvika, Støtvig, Knutvika og Mossesundet; land-/opptrekksfunksjonen hos de to åpne kandidatene; og referanseår for kapasitet. Felles historisk avfallsplan gir ingen selvstendig ny bekreftelse på nåværende drift for små anlegg uten tilgjengelig operatørside. Nasles gamle blogg dokumenterer aktivitet i 2010–2011, ikke i 2026. Refsnes-nettstedet ble avvist av miljøets proxy; dette er ikke bevis på at foreningen eller nettstedet er nedlagt.

Geometrisk kontroll mot originale bilder er ikke gjort. Originalbildene er ikke tilgjengelige i repoet, og teksten alene avklarer ikke havnegrensene. Berikelsen er rikere på felt og proveniens, men dokumenterer ikke høyere geografisk fullstendighet enn Mepex/SALT.

Kildearkivet under `sources/` er lokalt og utelatt fra Git. De strukturerte faktaene, kilde-URL-ene og kontrollsummene følger repoet; fulltekstuttrekkene gjør det ikke. Kildenes egne rettigheter gjelder. Uttrekk og kontrollsummer er underlag for etterprøving; denne piloten gir ikke tredjeparts tekst og materiale en ny åpen lisens. Avklar rettigheter før eventuell viderepublisering av kildearkivet. Kontaktpersoner fra nettsider er ikke etablert som egne pilotfelt.

## Reproduksjon og kontroll

Kjør fra repoets rot:

```sh
python work/3103-moss/build_enrichment.py
python work/3103-moss/validate_enrichment.py
.venv/bin/python scripts/validate_project.py
```

`collect_enrichment_sources.py` kan hente kildene på nytt, men vil erstatte pilotens kildeuttrekk og kontrollsummer. Ved en ny faglig gjennomgang: kopier arbeidsopplegget til en ny pilot/revisjon og bevar denne kildeversjonen. Byggeskriptet krever at tekstankrene fortsatt finnes og stopper ved endret kildeinnhold. Bare vellykket HTTP-respons er ikke tilstrekkelig for en ny faglig godkjenning.

## Integrasjon med nettstedet

`scripts/build_harbour_enrichment.py` bygger `site/labs/oslofjord-bathavner/data/enrichment.json` direkte fra `harbours.json`, `observations.json` og `sources.json`. Hele nettstedets databygg kaller samme eksportør. Dette krever ikke lokale fulltekstuttrekk. Eksportøren stopper dersom en publisert feltverdi mangler en samsvarende observasjon, eller hvis anleggs-ID-ene avviker fra de godkjente Moss-anleggene.

Havnekortene laster tilleggsdata separat og kobler på `harbour_id`. Hvert publisert felt viser kildelenke, ukjent referansedato der dato mangler, og innhentingsdato. Historiske kapasiteter ligger under «Earlier dataset capacity». Ukjent drift og rensing presenteres som ikke verifisert. Ferskvann, jolleplasser, gjesteplasser, omtrentlige tall og opplag på land holdes eksplisitt adskilt. Operatørgrenser som ikke er avklart merkes i kortet.

Ved feil i tilleggsfilen fungerer kartet fortsatt. Moss-kort viser at kildeberikelsen er utilgjengelig og merker eventuell gammel kapasitet som tidligere datasett med ukjent referanseår. Andre kommuner beholder eksisterende kort. Nye kandidater vises ikke som havner.

Kjør `.venv/bin/python -m unittest discover -s tests -v` for eksportkontroll. `validate_enrichment.py` kontrollerer også de lokale kildeuttrekkene når de finnes; bruk `--require-snapshots` for å kreve hele det opprinnelige kildearkivet. De kan ikke forventes å finnes i en ny klone. Geometridataene valideres med `scripts/validate_project.py`.

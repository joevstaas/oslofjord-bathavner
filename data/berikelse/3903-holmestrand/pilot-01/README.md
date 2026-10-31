# Holmestrand – kilde- og berikelsessjekk 31. oktober 2026

Status: gjennomført kildegjennomgang, til vurdering. Brukeren ba om tilsvarende sjekk som Moss. Denne leveransen er et separat berikelseslag og en avviksliste; den er ikke koblet til nettstedet. Ingen godkjente geometrier, egenskaper eller klassifiseringer er endret.

## Resultat

- Alle **12 anleggsgrupper / 14 polygoner** i den godkjente kommuneleveransen er gjennomgått. Fem grupper har opprinnelig status `ma_avklares`; disse beholder usikkerheten. De øvrige sju har `kart_og_kilde`, ikke en ny klassifisering etter ti-plassregelen.
- **41 observasjoner** med kildelenke, innhentingstid, omfang, status og linjehenvisning til lokalt tekstuttrekk.
- Operatør-/foreningsnavn registrert for **7 grupper**, med eksplisitt skille mellom publisert operatørrelasjon og historisk kommunalt dokument. Dette er ikke sju bekreftelser på fysisk drift i dag.
- **2 kapasitetsgrupper** på tvers av eller uten sikker fordeling til sjøpolygoner. Ingen samlet kapasitet per kommune er beregnet.
- **27 direkte kildeoppslag, 25 tilgjengelige**. Dette er oppslag, ikke uavhengige kilder; flere sider tilhører samme organisasjon. To PDF-adresser kunne ikke hentes.
- **10 avklaringsbehov**. Våle/Frebergsvik er beholdt som et separat, tidligere registrert supplement, uten ny geometri eller godkjenning.
- Tidsfestet driftsmelding finnes for havneselskapets vintertilbud, men er ikke likestilt med befaring eller uavhengig verifisering av alle tilknyttede anlegg.

## Funn per anleggsgruppe

| ID | Gruppe | Kildebasert berikelse | Fortsatt uavklart |
| --- | --- | --- | --- |
| H01 | Holmestrand byhavn, to bassenger | Operatøren oppgir nå Holmestrand Småbåthavn AS. Kommunen oppgir ca. 1100 faste plasser for selskapets samlede tilbud. Gjestehavnen beskrives separat med ca. 50 båter langs 450 meter kai. | 1100 er ikke kapasitet for hvert basseng. Gjestekaiens eksakte forhold til polygonene er ikke kartkontrollert. 450 er meter, ikke plasser. |
| H02 | Hagemann | Samme havneselskap og felles kapasitetsgruppe som byhavna. | Egen kapasitet og andel av totalen 1100 er ukjent. |
| H03 | Nordre Jarlsberg Brygge | NJB Marina-identitet; to kapasitetspubliseringer: 450 på njb.no og 397 på Havneweb. Publisert opplagstilbud, utsettingsrampe og FAQ som sier at havnen ikke har egen kran. | Referanseår og årsak til kapasitetsforskjellen. Ingen enkeltverdi velges. PDF-opplastingsdato brukes ikke som måledato. |
| H04 | Sande & Havna | Foreningens Havneweb og registeridentitet; kommunal anleggsplan beskriver eksisterende småbåthavn. | Havneweb har hovedsakelig plassholdertekst; kapasitet og aktuelle funksjoner er ukjente. |
| H05 | Bjerkøya | Operatøren oppgir 155 medlems-/andelsplasser og 62 utleieplasser. To rampetyper beskrives. Bryggeutvidelse omtales i nyhetsstrømmen. | Katalogens 155 kan være en delmengde, ikke en konflikt. Dagens brygger må sammenholdes med det gamle kartomrisset. Ingen ny aggregert polygonkapasitet beregnes. |
| H06 | Gyltesø | Registrert forening og kommunal anleggsplan 2020–2028 knytter navnet til eksisterende småbåthavn. | Aktuell drift, kapasitet og funksjoner er ikke bekreftet. Kommunalt historisk dokument er ikke en nåtidsbefaring. |
| H07 | Holm Brygge | Operatørens nettside tilbyr båtplasser; Holm Brygge AS er identifisert i registeret. | Antall båtplasser, opplag og aktuelle driftsforhold. |
| K01 | Bekkebrygga | Tidligere kartobservasjon og målrettet navn-/stedssøk gjennomgått. Ingen ny sikker operatørkobling etablert. | Navn/operatør, klasse, kapasitet og omriss. |
| K02 | Sandvika | Tidligere kartobservasjon og navn-/stedssøk gjennomgått; søk gir også treff på badeplasser og andre kommuner. | Ingen kapasitet eller operatør overført fra navnelike steder. |
| K03 | Mathisodden | Kartkandidaten er beholdt separat fra Bjerkøya og Gyltesø. | Nærhet og stedsnavn etablerer ikke operatør eller kapasitet. |
| K04 | Holmsåsen, søndre bryggegruppe | Tidligere kartobservasjon og navn-/stedssøk gjennomgått. | Ingen sikker kobling til campingvirksomhet eller Holm Brygge er etablert. |
| K05 | Torrud, to bryggegrupper | Thorrud Camping annonserer båtplasser ved Eikeren. Ferskvann er eksplisitt registrert. | Tilknytning av begge bryggegruppene til operatøren er ikke bekreftet. 130 gjelder campingplasser, og 1000 kroner er en pris; ingen av delene er båtplasskapasitet. |

## Hva som bør forbedres først

1. **Holmestrand byhavn/Hagemann:** avklar kapasitetens stedlige fordeling og oppdater operatøridentiteten i berikelseslaget. Kommunens nettsider bruker fortsatt DA, mens selskapet oppgir AS. Registeret viser AS 936760600 og gammel DA 985747970 under avvikling. Selskapsstatus er kildebelagt; alle juridiske vilkår ved overgangen er ikke undersøkt.
2. **Bjerkøya:** kontroller den omtalte bryggeutvidelsen mot egnet, datert bilde. Dette kan påvirke både avgrensning og kapasitet, men denne gjennomgangen har ikke tegnet et nytt omriss.
3. **Nordre Jarlsberg Brygge:** avklar forskjellen mellom 397 og 450 og hvilket tidspunkt/område tallene gjelder.
4. **De fem K-gruppene og Våle:** målrettet stedfesting og funksjonsavklaring før eventuell ny geometri eller klassifisering.

## Leveranser og skjema

- `harbours.csv` / `harbours.json`: 12 anleggsrader, koblet med eksisterende `harbour_id`. Kilder og tidligere merknader beholdes.
- `observations.csv` / `observations.json`: autoritativt feltregister med verdi, kilde, omfang, tidsstatus og bevislokator.
- `capacity-groups.csv` / `capacity-groups.json`: de to gruppetallene 1100 og 50, lagret én gang og koblet til relevante anlegg uten automatisk fordeling eller summering.
- `candidates.csv` / `candidates.json`: Våle/Frebergsvik, med peker til det tidligere ikke-godkjente supplementet. Berikelseskandidaten har null geometri og null ny `harbour_id`.
- `deviations.csv` / `deviations.json`: de ti avklaringsbehovene.
- `reference-map.geojson`: samme 14 geometriske objekter og tidligere egenskaper, med et ekstra `enrichment_pilot`-objekt. Kun referanseeksport, ikke ny godkjent kommuneleveranse.
- `sources.json`: URL-er, tidspunkt, HTTP-resultat, kontrollsummer og lokale arkivstier. Fulltekstuttrekk og PDF-er under `sources/` er lokale og utelatt fra Git.
- `baseline.json`, `metrics.json`, `validation.json`, `timing.json`: uendrede originalfiler, nøkkeltall, validering og målt veggklokketid fra baselinefangst.

JSON er kanonisk. CSV er UTF-8 med BOM, semikolon og LF; lister/objekter er JSON i cellene og null er tom celle. `reference_date` er kildens dokumenterte referansetidspunkt, ikke vårt innhentingstidspunkt. Oppdateringsdato på nettsiden og år i filstien etablerer ikke kapasitetens referanseår.

For Bjerkøya ligger 155 og 62 som hver sin `capacity_components` med observasjons-ID. For NJB ligger begge tall i observasjonstabellen og `capacity_quality` er `conflicting_operator_publications`. `berths_published` på anleggsradene er null i denne leveransen: relevante tall er enten konflikter, komponenter eller felles gruppetall, ikke et entydig antall per gammelt sjøomriss. Dette betyr ikke null båtplasser.

Manglende funksjon står som null, ikke nei. Det uttrykkelige nei til egen kran hos NJB er en publisert kildeopplysning i FAQ-en, ikke en ny inspeksjon og ikke et nei til alle eksterne løftetjenester. Vinterplass i boblehavn er sjøbruk; det er ikke landopplag. `current_operation_verified` og `wastewater_treatment_current` er fortsatt null for alle rader.

## Kilder og avgrensninger

De viktigste sidene er operatørenes og kommunens:

- [Holmestrand Småbåthavn](https://holmestrandsmabathavn.no/) og [kommunens havneside](https://holmestrand.kommune.no/innbyggerhjelpen/naring-transport-og-samfunn/parkering-vei-og-havn/havn-og-bobil/smabathavn/).
- [Kommunens gjestehavnbeskrivelse](https://holmestrand.kommune.no/innbyggerhjelpen/naring-transport-og-samfunn/parkering-vei-og-havn/havn-og-bobil/gjestehavn/).
- [NJBs båthavn](https://njb.no/bathavna/) og [NJBs Havneweb-side](https://www.havneweb.no/njb-marina/).
- [Bjerkøyas egen anleggsbeskrivelse](https://bjerkbat.no/OmOss/InformasjonomBjerk%C3%B8yab%C3%A5tforening.aspx).
- [Holm Brygge](https://www.holmbrygge.no/), [Sande & Havna](https://www.havneweb.no/sandehavnabf/) og [Thorrud Camping](https://thorrudcamping.no/fasiliteter/).

Søkene omfattet også navnene Bekkebrygga/Bekkestranda, Sandvika ved Bjerkøya, Mathisodden, Holmsåsen og Våle/Frebergsvik. Treff fra andre kommuner, generelle badestedsbeskrivelser og OSM-gjenbruk er ikke behandlet som nye, uavhengige havnebekreftelser. For enkelte K-grupper gav søkene ingen tilstrekkelig kildekobling; dette er et uavklart resultat, ikke en avkreftelse av anlegget.

Kommunens eldre kunnskapsgrunnlag og et Langøya-planinitiativ ble funnet som søkespor, men direkte dokumenthenting feilet. Ingen kapasitet eller eksisterende havn er etablert fra disse søkesnuttene. Den tilgjengelige anleggsplanen 2020–2028 er bare brukt som historisk dokumentasjon.

Originale pilotbilder er ikke tilgjengelige i repoet. Ingen nye bilder, geometrier, klassifiseringer eller landpolygoner er laget, og ingen operatører er kontaktet. Alle 14 gamle polygoner beholder behovet for ortofotokontroll. Denne sjekken dokumenterer bedre metadata og konkrete kontrollbehov, ikke høyere geografisk fullstendighet eller målenøyaktighet.

## Reproduksjon

Fra repoets rot:

```sh
python work/3903-holmestrand/build_enrichment.py
python work/3903-holmestrand/validate_enrichment.py --require-snapshots
.venv/bin/python scripts/validate_project.py
```

Bygget bruker de lokale kildeuttrekkene og stopper hvis tekstankre ikke lenger finnes. Validering uten `--require-snapshots` kontrollerer strukturer, koblinger og eventuelle tilgjengelige arkiver og rapporterer hvor mange kildeuttrekk som faktisk er kontrollert. Nettinnhentingsskriptet er et revisjonsverktøy; ikke overskriv denne kildeversjonen ved en fremtidig gjennomgang. Kildenes rettigheter videreføres; uttrekkene gir ingen ny lisens til tredjepartsmateriale.

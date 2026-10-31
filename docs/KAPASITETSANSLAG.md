# Arealbaserte kapasitetsanslag – eksperimentell modell v1

Modellen prioriterer videre kildearbeid. Den er ikke en opptelling av båtplasser
og vurderer verken forskriftsvirkeområde eller etterlevelse.
Godkjente sjøpolygoner og publiserte kapasitetstall er uendret.

## Grunnlag og beregning

97 av 664 fysiske havnegrupper har publisert kapasitet som kan brukes.
Disse berører 15 kommuner, men utvalget er skjevt: 62 ligger i Sandefjord.
Kapasitet kan være gammel, omtrentlig eller ha et annet fysisk omfang enn
kartpolygonet. Datagrunnlaget er ikke et tilfeldig eller representativt utvalg.

Areal summeres én gang per fysisk gruppe (`gid`), på tvers av kommunegrenser.
Publiserte kapasitetstall summeres aldri mellom polygoner. Modellen bruker
logaritmisk regresjon av antall plasser mot areal, med lik samlet vekt for hver
primærkommune (første alfabetiske kommune for en delt gruppe). Tilpasset formel:

`plasser ≈ 0,08927 × areal_m²^0,78101`

Ingen treningspunkter er fjernet for å forbedre resultatet. Kommunebalanseringen
hindrer at én kommune dominerer tilpasningen. Modellen sammenlignes med en enkel
referanse: areal multiplisert med median antall publiserte plasser per m².

## Kontroll mot tall holdt utenfor modellen

Hele kommuner holdes utenfor, ikke tilfeldige polygoner. For delte grupper holdes
begge kommunene utenfor treningen samtidig. Dermed lekker ikke deler av samme
havn eller andre havner i testkommunen inn i treningen.

| Modell | Median absolutt prosentavvik | Innenfor en faktor 2 |
|---|---:|---:|
| Kommunebalansert logmodell | 26,4 % | 88,7 % |
| Enkel arealtetthet | 28,0 % | 80,4 % |

Logmodellens gjennomsnittlige absolutte feil er 45 plasser. Enkelthavner kan
bomme mye mer: Huvik har publisert 10 plasser, men anslås til ca. 70 når
Sandefjord holdes utenfor. Areal alene er utilstrekkelig til sikker kapasitet.
Resultatene er utforskende; en ny, uavhengig testmengde er ikke samlet inn.

## Usikkerhet og visning

Et grovt spenn bruker en faktor på ca. 2,08 under/over punktanslaget.
Faktoren er 90-persentilen av absolutte logfeil i kommunebalanserte testresultater.
Dette er en beskrivende kalibrering på de samme testfeilene, **ikke et validert
90 % prediksjonsintervall**. Verken dekning eller sannsynlighet garanteres.
Punktanslag avrundes til ti plasser; spenn avrundes utover.

Modellen har kalibreringsareal 962–99 555 m². Ekstrapolasjoner og anlegg
klassifisert som mulig havn beholder usikker status. Landopplag anslås ikke.

For de 567 gruppene uten etablert publisert kapasitet gir modellen:

- 16 med hele spennet på minst 200: «trolig minst 200».
- 203 med hele spennet under 200: «trolig under 200».
- 348 usikre, inkludert mulige havner og ekstrapolasjoner.

«Trolig» er en praktisk modellkategori, ikke en beregnet sannsynlighet.
Filteret viser publiserte tall som standard (20 grupper ≥200). Brukeren kan
velge å legge til de 16 trolige fra areal, eller også grupper der øvre spenn
når 200. Ukjente og usikre er ikke automatisk små havner. Publiserte tall
har alltid forrang, også når et arealanslag ville gitt en annen kategori.

## Etterprøving

Kjør `.venv/bin/python scripts/build_flyover_data.py` fra prosjektroten.
Modell: `scripts/estimate_harbour_capacity.py`.
`site/labs/oslofjord-bathavner/data/capacity-model.json` inneholder koeffisienter,
kildehenvisning og referanseperiode per treningsgruppe, areal, alle 97
prediksjoner på holdte kommuner, feil og SHA-256 for datagrunnlag og modellkode.
Havnekortet viser anslag, spenn og modellgrunnlag separat fra publisert kapasitet.

Neste kvalitetsløft er flere daterte kapasitetstall utenfor Sandefjord,
kontroll av kildeomfang mot fysisk anlegg og deretter uavhengig validering.

# Småbåthavner i Oslofjorden

Polygoner med sporbare metadata for småbåthavner i kommuner med kystlinje mot indre og ytre Oslofjord.

Godkjent status: **456 polygoner fra 14 kommuner** (Holmestrand, Horten, Tønsberg, Færder, Sandefjord, Larvik, Moss, Råde, Fredrikstad, Bærum, Asker, Lier, Drammen, Oslo). Gjenstår: Nordre Follo, Nesodden, Frogn, Vestby, Hvaler, Sarpsborg, Halden, Porsgrunn, Bamble (Ås uavklart). Se `status.json`.

Datasettet er en bilde- og kildebasert kartlegging, ikke offisielle havne- eller eiendomsgrenser. Godkjenning fjerner ikke klassifiserings- eller geometriusikkerhet.

## Analysemetoden

Full metodikk og kommunelogger står i [`docs/METODIKK.md`](docs/METODIKK.md). Kortversjon (metode 1.2, brukt fra Fredrikstad):

### Hva er en småbåthavn her?

| Klasse | Regel |
|---|---|
| `smabathavn` | Felles anlegg med minst 10 båtplasser, eller dokumentert marina/båtforening med faste plasser |
| `mulig_smabathavn` | Flere sammenhengende brygger, men antall plasser eller felles drift er uklart |
| Utelatt | Spredte private brygger, badebrygger, fergekaier, ramper, rene moloer, planlagte anlegg |

Ti plasser er en prosjektgrense, ikke en juridisk definisjon. En foreningsadresse beviser ikke hvor havna ligger, og et planområde er ikke en eksisterende havn.

### Arbeidsflyt per kommune

1. **Avgrensning og dekning.** Kommunegrensen hentes fra Kartverket. Strandlinjen deles i ruter, og hver rute får flybilder (Esri World Imagery, ca. 0,67 m/piksel) og topografisk kart (Kartverket WMS), lagret med georeferering i EPSG:25833.
2. **Kandidatsøk fra to uavhengige kilder.**
   - *Kart:* OSM-pirer, marinaer og fortøyninger fra Overpass.
   - *Kilder:* Enhetsregisteret (båtforeninger, marinaer), Kartverkets stedsnavn, kommunens havnesider og andre offentlige dokumenter.
3. **Automatisk utkast.** OSM-pirer innen 60 m av hverandre klynges. Hver klynge bufres 12 m og lukkes med 20 m. Resultatet klippes mot vannflaten i det topografiske kartet og mot kommunegrensen. Dette er bare et forslag til geometri.
4. **Visuell vurdering av hver kandidat.** Utkastet tegnes oppå flybildet. Hver kandidat får én beslutning: inkluder, klipp, del, legg til manuell flate, tegn manuelt eller utelat. Hver beslutning har en begrunnelse og ligger i `decisions.py` og kandidatloggen.
5. **Systematisk bildesøk.** Alle fjordnære detaljfliser gjennomgås i kontaktark med kandidatene påtegnet, for å finne anlegg som mangler i OSM. Slike anlegg tegnes manuelt.
6. **Polygonregel.** Polygonet dekker brygger, båtplasser og sjøen mellom dem, ikke hele bukta, landarealer eller foreningens eiendom. Adskilte deler blir egne delpolygoner med felles `harbour_id`. Anlegg som krysser en kommunegrense klippes, merkes `municipality_clipped` og knyttes sammen med `cross_municipality_group_id`.
7. **Kontroll.** Alle eksporterte polygoner kontrolleres som overlegg på flybildet etter siste endring. I tillegg valideres geometri, unike ID-er, kommunegrense, overlapp mot hverandre og mot samlefilen, og at CSV stemmer med GeoJSON.
8. **Godkjenning.** Brukeren godkjenner kommunen (eller en avtalt batch) ved å se på GeoJSON-filen. Først da kopieres leveransen til `data/kommuner/<kode>-<navn>/rev-NN/` og legges inn i samlefilen. Usikre avgrensninger og åpne kandidater beholdes. Nye funn i godkjente kommuner legges i en egen ventelogg (`neighbour-pending.json`).

Hver polygonrad har blant annet klassifisering med begrunnelse, metodefelt (OSM-basert eller manuelt), kilder og OSM-ID-er, bildekilde og oppløsning, og flagg for usikker avgrensning (`needs_orthophoto_review`). Veggklokketid registreres per kommune i `timing.json`.

### Kjente begrensninger

- Bildenes opptaksdato er ukjent. Strukturen er påvist, men ikke at havna er i drift i dag.
- OSM-pirer kan ligge forskjøvet i forhold til bildet. Båter langs kai uten pir i OSM kan falle utenfor polygonet.
- Visuell analyse kan overse små anlegg. Det er ikke gjort befaring eller landmåling.
- Holmestrand og Horten er eldre kartbaserte piloter og er ikke etterprøvd med dagens metode.

## Kom i gang

```bash
git clone https://github.com/joevstaas/oslofjord-bathavner.git
cd oslofjord-bathavner
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/validate_project.py   # skal gi 456 polygoner / 14 kommuner
claude
```

Python 3.11 eller nyere. Claude Code installeres separat.

Flybilder, rådata og QA-ark for godkjente kommuner er ikke med i git (se `.gitignore`). De trengs bare hvis en godkjent kommune skal revideres, og kan hentes på nytt. Valideringen melder derfor 0 kommuner med originalbilder etter kloning.

## Innhold

- `data/samlet/`: godkjent samlefil (GeoJSON, WGS84) og manifest.
- `data/kommuner/<kode>-<navn>/rev-NN/`: godkjente kommuneleveranser med metadata-CSV, kandidatlogg, beslutninger, åpne kandidater, dekning og tidtaking.
- `status.json`: gjeldende status med relative stier.
- `docs/METODIKK.md`: autoritativ metodikk og kommunelogger. `docs/OVERLEVERING.md`: filkart og videreføring.
- `CLAUDE.md`: prosjektinstrukser til Claude Code.
- `work/`: analyseskript per kommune. Den nyeste kommunen (`0301-oslo`) er mal for neste.
- `archive/original/`: historiske leveranser, notater og skript for de første kommunene.
- `scripts/validate_project.py`: lokal kontroll uten nettverk.

Kilder: © Kartverket; Esri, Vantor, Earthstar Geographics and the GIS User Community; © OpenStreetMap contributors (ODbL); Enhetsregisteret.

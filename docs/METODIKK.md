# Kartlegging av småbåthavner – metodikk og overlevering

**Metodeversjon:** 1.1  
**Sist oppdatert:** 2026-10-29  
**Område:** kommuner langs indre og ytre Oslofjord  
**Arbeidsform:** én kommune om gangen; brukeren godkjenner leveransen før neste kommune startes.

Dette dokumentet er prosjektets levende metodebeskrivelse. En annen AI-agent eller fagperson skal kunne videreføre arbeidet uten tilgang til samtalen som startet prosjektet. Dokumentet beskriver både vedtatte regler, praktisk gjennomføring, kjente svakheter og hvordan erfaringer skal legges til.

**Viktig skille:** Brukergodkjenning gjelder en bestemt kommuneleveranse og revisjon. Den fjerner ikke usikkerhet om enkeltanlegg, geometri, bildedato eller fullstendighet. Polygonene er kartleggingsforslag, ikke offisielle havnegrenser eller eiendomsgrenser.

## Innhold

1. [Oppdrag og status](#1-oppdrag-og-status)
2. [Hva regnes som småbåthavn?](#2-hva-regnes-som-småbåthavn)
3. [Datakilder og kildekritikk](#3-datakilder-og-kildekritikk)
4. [Arbeidsflyt for én kommune](#4-arbeidsflyt-for-én-kommune)
5. [Hvordan polygoner tegnes](#5-hvordan-polygoner-tegnes)
6. [Koordinater og georeferering](#6-koordinater-og-georeferering)
7. [Leveranser og dataskjema](#7-leveranser-og-dataskjema)
8. [Kontroll og godkjenning](#8-kontroll-og-godkjenning)
9. [Begrensninger og antagelser](#9-begrensninger-og-antagelser)
10. [Tidsbruk og kostnader](#10-tidsbruk-og-kostnader)
11. [Erfaringer og kommunelogg](#11-erfaringer-og-kommunelogg)
12. [Vedlikehold og instruks til neste agent](#12-vedlikehold-og-instruks-til-neste-agent)

## 1. Oppdrag og status

Målet er et samlet GeoJSON-datasett med polygoner og sporbare metadata for småbåthavner. Et anlegg kan ha flere delpolygoner. Derfor rapporteres alltid både **antall anlegg** (`harbour_id`) og **antall polygonrader** (`id`).

Arbeidet startet med Holmestrand som pilot, deretter Horten og Tønsberg. Tønsberg ble gjennomgått på nytt etter at brukeren viste eksempler på mulige mangler og godkjente en tydeligere avgrensningsregel. Esri World Imagery ble først tatt i bruk i denne nye gjennomgangen.

| Kommune | Kommunenummer | Siste godkjente leveranse | Polygoner | Metodegrunnlag |
|---|---|---|---:|---|
| Holmestrand | 3903 | Pilot | 14 | Topografisk kart og tilleggskilder |
| Horten | 3901 | Pilot | 16 | Topografisk kart og tilleggskilder |
| Tønsberg | 3905 | Revisjon 2 | 20 | Kart, Esri-bilder og tilleggskilder; 17 anlegg, hvorav 2 usikre |
| Færder | 3911 | Revisjon 2 | 35 | Kart, Esri-bilder og kilder; 31 anlegg, inkludert 2 usikre |
| Sandefjord | 3907 | Revisjon 1 | 67 | Metode/skjema 1.1; 65 fysiske anlegg, inkludert 2 usikre kandidater |
| Larvik | 3909 | Revisjon 1 | 32 | 23 anlegg; 15 usikre avgrensninger og åpne kildekandidater |
| Moss | 3103 | Revisjon 1 | 26 | 22 anlegg; én mulig havn og 15 usikre avgrensninger |
| Råde | 3112 | Revisjon 1 | 11 | 11 anlegg; 4 mulige havner, 7 usikre avgrensninger |
| Fredrikstad | 3107 | Revisjon 1 | 69 | 61 anlegg; metode 1.2; 18 mulige havner, 56 usikre avgrensninger |
| Bærum | 3201 | Revisjon 1 | 49 | 42 anlegg; metode 1.2; 20 mulige havner, 40 usikre avgrensninger |
| Asker | 3203 | Revisjon 1 | 60 | 53 anlegg; metode 1.2; 13 mulige havner, 26 usikre avgrensninger |
| Lier | 3312 | Revisjon 1 | 2 | 2 anlegg; metode 1.2 |
| Drammen | 3301 | Revisjon 1 | 19 | 17 anlegg; metode 1.2; 2 mulige havner, 7 usikre avgrensninger |
| Oslo | 0301 | Revisjon 1 | 36 | 32 anlegg; metode 1.2; 11 mulige havner, 16 usikre avgrensninger |
| **Samlet** | | **14 godkjente kommuner** | **456** | Ulik metodehistorikk; se begrensninger |

Samlet antall anlegg på tvers av de sju kommunene oppgis ikke her: de eldste leveransene er ikke harmonisert etter den nye grupperingsregelen.

Færder revisjon 2, Sandefjord revisjon 1, Larvik revisjon 1, Moss revisjon 1, Råde revisjon 1, Fredrikstad revisjon 1 og batchen Bærum, Asker, Lier, Drammen og Oslo (revisjon 1) er godkjent og innlemmet i samlefilen. Samlet fil inneholder 456 polygoner fra 14 kommuner. Ingen neste kommune er startet.

### Prosjektfiler

Stiene nedenfor gjelder dagens arbeidsområde. En ny agent kan bruke andre verktøy eller mapper, men skal bevare sammenhengene mellom leveranser, kilder og godkjenninger.

| Fil/mappe | Rolle |
|---|---|
| `oslofjord-kartlegging/METODIKK.md` | Dette dokumentet |
| `oslofjord-kartlegging/status.json` | Kommunestatus og godkjent revisjon |
| `oslofjord-kartlegging/oslofjorden-bathavner-samlet.geojson` | Bare godkjente kommuneleveranser |
| `oslofjord-kartlegging/samlet-manifest.json` | Avledet oversikt over innholdet i samlet fil |
| `holmestrand-pilot/` og `horten-pilot/` | Eldre piloter med underlag og leveranser |
| `tonsberg-pilot/tonsberg-bathavner-rev2.geojson` | Godkjent Tønsberg-leveranse |
| `tonsberg-pilot/tonsberg-metadata-rev2.csv` | Samme polygonrader som metadatatabell |
| `tonsberg-pilot/tonsberg-endringer-rev2.csv` | Endringer fra Tønsberg revisjon 1 |
| `tonsberg-pilot/revisjon-1/` | Arkivert første leveranse |

Et suppleringsfunn i Holmestrand, Våle båthavn, ligger i `horten-pilot/suppleringsfunn-holmestrand.geojson`. Det er ikke godkjent og skal ikke legges i den samlede filen uten egen behandling.

## 2. Hva regnes som småbåthavn?

Følgende arbeidsregel er **godkjent av brukeren**. Ti plasser er en prosjektgrense, ikke en juridisk definisjon.

| Klasse | Beslutningsregel | Behandling |
|---|---|---|
| `smabathavn` | Felles anlegg med minst 10 båtplasser, **eller** dokumentert marina/båtforening med faste plasser | Inkluderes |
| `mulig_smabathavn` | Flere sammenhengende brygger, men antall plasser eller felles drift er uklart | Inkluderes, tydelig merket som usikker |
| Utelatt | Spredte private brygger uten tydelig felles organisering | Utelates fra havneleveransen; relevante vurderinger loggføres |

### Tolkning i praksis

- «Felles» betyr et samlet båtplassanlegg. Privat eierskap eller stengt adgang utelukker ikke havn; et organisert boligtilknyttet anlegg kan kvalifisere.
- Flere brygger langs samme strand er ikke automatisk et felles anlegg. Separate landfester ved hver sin bolig taler for enkeltbrygger. Ved reell tvil brukes usikker klasse.
- En enkelt lang pir kan ha mer enn ti båtplasser og kvalifisere. Antall pirer er ikke et selvstendig kriterium.
- Ti kartstreker er ikke ti båtplasser. Se etter avgrensede plasser, utriggere eller annet tydelig plassmønster. Fortøyde båter støtter tolkningen, men dokumenterer ikke alene faste plasser eller felles organisering.
- Ikke summer spredte private båtplasser for å passere terskelen.
- Dokumentert båtforening eller marina med faste plasser kan kvalifisere selv med færre enn ti plasser. Et foretaksnavn eller en postadresse alene dokumenterer ikke at riktig sjøanlegg er lokalisert.
- Et sesongstengt anlegg er fortsatt et anlegg. Skill sesongstenging fra nedleggelse.
- Dokumenterte gjestehavner behandles som havneanlegg. Små gjestebrygger som hører til en større havnegruppe kan leveres som delpolygoner. Ikke gi hver liten besøksbrygge status som selvstendig havn uten grunnlag.
- Badebrygger, fergekaier, rene servicekaier, utsettingsramper, opplagsplasser og moloer uten dokumentert båtplassanlegg kvalifiserer ikke alene.
- Planlagte havner holdes adskilt fra observerte anlegg. En reguleringsplan eller et gammelt prospekt må kontrolleres mot bilder før anlegget registreres som bygget.

**Beslutningsrekkefølge:** Finnes et fysisk anlegg? Er riktig sted identifisert? Er det dokumentert felles drift med faste plasser, eller minst ti tydelige plasser i et felles anlegg? Hvis ja, inkluder. Hvis felles anlegg er plausibelt, men grunnlaget uklart, inkluder som usikkert. Ellers utelat og noter begrunnelsen ved behov.

Oppgi hvorfor regelen er oppfylt. Ikke bruk et generelt «høy sikkerhet»-merke som erstatning for begrunnelsen.

## 3. Datakilder og kildekritikk

Kildene utfyller hverandre. Ingen av dem er et komplett register over alle småbåthavner.

| Kilde | Bruk | Begrensning |
|---|---|---|
| Kartverket kommuneinfo / offisiell kommunegeometri | Avgjøre kommune, avgrense arbeidsområdet og kontrollere grensekryssing | Grenser og kommunenumre kan endres; lagre uttrekksdato og oppgitt koordinatsystem |
| Kartverket Topografisk norgeskart | Systematisk oversikt over strandlinje, stedsnavn, brygger og moloer | Kartobjekter kan være generalisert, mangelfulle eller eldre enn situasjonen på bakken |
| Esri World Imagery | Oppdage og avgrense synlige båtplassanlegg; skille bygninger, land, brygger og vann | Mosaikk av ulike opptak, ukjent lokal alder og nøyaktighet; skyer, skygger og sesongforskjeller |
| Daterte ortofoto, dersom tilgjengelig med brukstillatelse | Bedre tidsfestet kontroll og mulig presisering av geometri | Tilgang, dekning og vilkår må undersøkes; ikke forutsett fri tilgang |
| OpenStreetMap | Kandidater, navn, objektreferanser og supplerende geometri | Punkter og områder kan duplisere samme havn; plassering, bruk og grenser kan være feil eller gamle |
| Havneoperatør, båtforening, bryggesameie, kommune | Navn, lokalisering, felles drift, publisert kapasitet og sesonginformasjon | Nettsider og dokumenter kan være utdaterte; opplysninger gjelder ikke nødvendigvis et delpolygon |
| Enhetsregisteret | Bekrefte organisasjon og formål | Registrert kontoradresse er ikke nødvendigvis havnens adresse eller koordinat |
| Sekundære oversikter, f.eks. Sjøsett | Finne kandidater og videre lenker | Kan bygge på samme OSM-data; er da ikke en uavhengig bekreftelse |
| Brukerens eksempler | Avdekke mangler og forbedre metoden | Skjermbilder uten koordinater må stedfestes; eksemplene kan ligge i en annen kommune |

### Tjenester og eksempler

- Kartverkets inngang til kartgrunnlag: <https://www.kartverket.no/api-og-data/kartgrunnlag-fastlands-norge>
- Kommuneinfo, tjenestebase: <https://api.kartverket.no/kommuneinfo/v1/>. Kontroller gjeldende API-dokumentasjon og responsens koordinatsystem før bruk.
- Kartverkets WMS: <https://wms.geonorge.no/skwms1/wms.topo>
- Esri tjenestemetadata: <https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer?f=pjson>
- Esri bildeeksport: <https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export>
- OSM-objekt, eksempel: <https://www.openstreetmap.org/way/38901313>. Bruk gjeldende OSM-API eller annen tillatt uttrekksmetode for maskinlesbare objekter.
- Lokal dokumentasjon fra Tønsberg: <https://www.kloppbat.com/> og <https://www.hsbhavn.com/om-oss/>.

Tjenesteadresser og kapasitetsgrenser kan endres. Manglende tilgang skal loggføres, ikke omgås. Kartverkets/Norge i bilders ortofoto ble ikke hentet i pilotene fordi nødvendig tilgang ikke var tilgjengelig. Dette er en erfaring fra denne kjøringen, ikke en generell påstand om alle tjenester eller brukeres tilgang.

### Hva vi lærte av Esri

I Tønsberg revisjon 2 kunne bildene vise plassmønstre som ikke fremgikk tilstrekkelig av det topografiske kartet. De hjalp også med å holde boligblokker utenfor vannpolygoner og oppdage at et eldre OSM-område ved Kirkegaten ikke fulgte et synlig havneanlegg i bildet.

**Videre praksis:** Bruk kart til oversikt og navn, og georefererte bilder til visuell kontroll og avgrensning fra starten av neste kommune. Søk både systematisk langs strandlinjen og etter dokumenterte anlegg. Ikke begrens bildegranskingen til allerede registrerte havner.

Esri er et nyttig tilgjengelig bildegrunnlag, men ikke automatisk nyere eller mer nøyaktig enn andre kilder. Hvis daterte, egnede ortofoto er tilgjengelige, sammenlign dem. At et bilde kan bestilles med 0,5 meter per piksel betyr ikke at det opprinnelige opptaket har denne detaljgraden eller posisjonsnøyaktigheten.

### Kildelagring og rettigheter

Lagre originalrespons/bilde med filnavn, full forespørsel, dato, faktisk bildeutstrekning, koordinatsystem, dimensjoner og kildehenvisning. Bruk gjerne SHA-256 for å identifisere nøyaktig hvilken fil som er analysert. En dynamisk URL alene sikrer ikke at samme bilde kan hentes senere.

Bevar leverandørens aktuelle kreditering. Esri-tjenesten oppga ved kontroll 2026-10-29: «Source: Esri, Vantor, Earthstar Geographics, and the GIS User Community». OSM skal krediteres, og ODbL må vurderes når data eller geometri gjenbrukes. Kartverket skal krediteres etter gjeldende kildevilkår. Tilgjengelighet via en offentlig URL betyr ikke at råbilder eller avledede data kan gis en vilkårlig åpen lisens. Kontroller vilkår for den planlagte bruken før ekstern publisering eller videredistribusjon.

Ikke utled lokal opptaksdato, oppløsning eller rettigheter fra en generell tjenestebeskrivelse.

## 4. Arbeidsflyt for én kommune

### Trinn 1 – Les status og start en egen kjøring

1. Les dette dokumentet, kommuneloggen og maskinlesbar status.
2. Kontroller hvilken kommune brukeren har bedt om, gjeldende kommunenummer og eventuell tidligere revisjon.
3. Opprett kjørings-ID og registrer metodeversjon, dataskjemaversjon og starttid i UTC.
4. Arkiver tidligere leveranse før revisjon. Den samlede godkjente filen skal ikke endres under analysen.

Verktøyvalg er fritt. Det kreves funksjoner for innhenting av offentlige kilder, bildevisning, koordinattransformasjon, geometrioperasjoner og filskriving. Ingen bestemt AI-leverandør, nettleser eller agentplattform er nødvendig.

### Trinn 2 – Hent kommunegeometri og planlegg dekning

Hent og lagre offisiell kommunegeometri. Bruk kommunegrensen, ikke søkeresultatenes kommunenavn, som geografisk fasit.

Del kysten i navngitte sektorer og dekk også øyer, viker, sund og elvemunninger. Ta med et belte utenfor kommunegrensen for å forstå sammenhengende anlegg, men skill observasjoner utenfor kommunen fra kommunens leveranse. Planlegg innsjøkontroll separat hvis oppdraget omfatter hele kommunen.

Start gjerne med 4 × 4 km oversiktsfliser, som i Tønsberg. Dette er en praktisk startverdi, ikke en tilstrekkelig detaljkontroll. For videre arbeid anbefales om lag 10 % overlapp eller tilsvarende kontroll av alle fliskanter. Tilpass flisestørrelse til bildenes brukbare detaljgrad og skjermvisningen.

**Ikke velg arbeidsområdet bare med en vannfargemaske.** Tønsbergs første uttrekk valgte fliser etter vannpiksler i et oversiktskart. En slik maske kan hjelpe med prioritering, men kan overse små vannflater, smale sund eller annerledes fargede flater. Videre kontroll skal også dokumentere at hele den relevante strandlinjen er dekket.

### Trinn 3 – Gjør to uavhengige søk etter anlegg

**Søk A: systematisk kart- og bildegransking.** Gå langs hver strandsektor, uavhengig av eksisterende havnelister. Registrer kandidat, vurdert utelatelse eller område som ikke kan avgjøres. Et område uten tilgjengelig eller lesbart bilde er «ikke tilstrekkelig kontrollert», ikke «ingen havn».

**Søk B: kildebasert kandidatsøk.** Søk etter marinaer, båtforeninger, bryggesameier, kommunale havner og boligprosjekter med båtplasser. OSM og sekundære lister gir kandidater, men er ikke en komplett kommuneinventering.

Koble funnene sammen. Alle dokumenterte havner skal forsøkes stedfestet i bildene, og alle tydelige bildeanlegg skal vurderes mot regelen også når de mangler navn eller nettkilde.

Oversiktsmontasjer brukes til navigering. Små eller tvetydige anlegg må vises som egne utsnitt i egnet skala. Registrer om et felt bare er grovt screenet eller også detaljkontrollert.

### Trinn 4 – Hent og kontroller bildene

For WMS oppgis blant annet `service=WMS`, `version=1.3.0`, `request=GetMap`, `layers=topo`, `crs`, `bbox`, `width`, `height` og `format=image/png`. Kontroller tjenestens kapabiliteter og akseorden.

For Esri-eksport kan en forespørsel se slik ut:

```text
.../MapServer/export
  ?bbox=<xmin>,<ymin>,<xmax>,<ymax>
  &bboxSR=25833
  &imageSR=25833
  &size=1600,1200
  &format=jpg
  &f=pjson
```

Dette er en mal; bbox og bildets sideforhold må passe sammen. JSON-respons anbefales videre fordi den kan gi faktisk `extent`, dimensjoner og bilde-URL. Hent bildet fra den returnerte URL-en og lagre responsen. Ikke forutsett at ønsket bbox alltid er identisk med returnert utstrekning. I Tønsberg ble `f=image` brukt og forespurt bbox lagret; dette er svakere dokumentasjon av den returnerte utstrekningen.

Ved kontroll 2026-10-29 oppga Esri-tjenesten maksimalt 4096 × 4096 piksler. Les gjeldende tjenestemetadata ved nye kjøringer. Flere små utsnitt er ofte mer hensiktsmessig enn én svært stor eksport.

Kontroller HTTP-status, faktisk filformat, bildedimensjoner, lesbarhet, utstrekning og at innholdet er riktig sted. Tjenester kan returnere XML/JSON-feil med vellykket HTTP-status. Ved timeout eller serverfeil: loggfør, prøv et mindre utsnitt eller en alternativ kilde, og bruk et begrenset antall forsøk. En mislykket nedlasting er ikke et negativt geografisk funn.

### Trinn 5 – Klassifiser og grupper

For hver kandidat:

1. Dokumenter observasjonen og kildene.
2. Avgjør klasse etter seksjon 2, med en konkret begrunnelse.
3. Skill publisert kapasitet fra visuell observasjon. Kapasitet for hele havnen skal ikke kopieres som kapasitet for hvert delpolygon.
4. Slå sammen OSM-punkt og OSM-område dersom de beskriver samme anlegg. Bevar begge objektreferansene som kilder.
5. Bruk samme `harbour_id` for delområder som hører til samme havnegruppe. Beskriv grupperingsgrunnlaget; samme øy eller nærhet alene dokumenterer ikke felles operatør.
6. Bruk beskrivende navn hvis navnet er ukjent. Merk dette eksplisitt.

Ved motstrid mellom kilder: beskriv konflikten og bevar usikkerhet. Et topografisk kart, en gammel plan og et flybilde kan beskrive forskjellige tidspunkter.

### Trinn 6 – Tegn og kontroller polygonene

Følg seksjon 5 og 6. Se hvert polygon som overlegg på det faktiske bildegrunnlaget før godkjenning. En matematisk gyldig polygon kan fortsatt ligge feil eller inkludere en boligblokk.

### Trinn 7 – Eksporter og lever til godkjenning

Lever GeoJSON og metadata-CSV, eventuelt en kort endrings-CSV ved revisjoner. Brukeren har bedt om polygoner og metadata; HTML-kart, skjermbildepakker og lange rapporter er ikke standardleveranser. Underlag og kontrollogger beholdes internt for etterprøvbarhet.

Oppgi antall anlegg, polygoner, usikre anlegg og vesentlige begrensninger. Stopp etter kommuneleveransen og vent på godkjenning.

### Trinn 8 – Registrer godkjenning og slå sammen

Når brukeren godkjenner en bestemt revisjon, registrer dato og status i kommuneleveranse, CSV og prosjektstatus. Oppdater samlet GeoJSON med denne revisjonen og regenerer manifestet. Bevar klassifisering og usikkerhet.

Ved revisjon skal kommunens tidligere godkjente polygonsett erstattes som et sett, også når polygoner er fjernet. Ren tilføyelse/oppdatering etter ID kan etterlate utgåtte polygoner. Kontroller dette særskilt. Ikke start neste kommune før brukeren har bedt om det.

## 5. Hvordan polygoner tegnes

Polygonet representerer **brygger, tilhørende båtplasser og sjøen mellom dem**. Det representerer ikke hele den skjermede bukten, foreningens eiendom, et planformål eller alle tilgjengelige tjenester på land.

- Følg synlig struktur, med ytterkant utenfor båtplassene. Ikke bruk en stor vilkårlig buffersone rundt et kartpunkt.
- Avgrens havneinnløpet med en begrunnet linje mellom relevante ytterpunkter. Ikke inkluder store deler av åpen fjord eller gjennomgående farled uten behov.
- Følg strand-/kaikanten. Hold boligblokker, veier, parkeringsplasser, opplagsområder og større landflater utenfor.
- Kartografisk forenkling skal ikke klippe bort tydelige bryggearmer eller føye inn store landflater. Detaljgrad skal stå i forhold til kildegrunnlaget.
- Bruk flere delpolygoner når anlegget har adskilte sjøområder. Det anbefalte leveranseformatet er én `Polygon` per rad og felles `harbour_id`. Ikke trekk et polygon over land for å forbinde delene.
- Hull kan brukes for landøyer/bygninger der det gir en faglig rimelig avgrensning. Ikke bruk automatiske «reparasjoner» som ukritisk endrer det observerte området.
- Dokumenter hvilken kilde som bestemmer grensen, og hvilke kilder som bare støtter navn, drift eller kapasitet.

Ved grensekryssing: avgrens kommunens del med offisiell kommunegeometri, merk `municipality_clipped=true`, og bevar referanse til det opprinnelige anlegget. Dersom klipping gir flere polygoner, gi dem egne del-ID-er. Bruk ved behov en felles `cross_municipality_group_id` for sammenhengen på tvers av kommuneleveranser. Et suppleringsfunn i en annen godkjent kommune skal legges i en egen ventelogg, ikke innlemmes automatisk.

### ID-er og revisjoner

Eksempel: `3905-H22-B02` betyr kommune 3905, havnegruppe H22, delpolygon B02.

- `id` er globalt unik per polygonrad.
- `harbour_id` er felles for anleggets delpolygoner.
- Bevar ID når samme objekt forbedres. Ikke nummerer alle anlegg på nytt ved et tillegg.
- Utgåtte ID-er skal ikke gjenbrukes til et annet anlegg.
- Ved sammenslåing/splitting loggføres tidligere og nye ID-er og begrunnelse.

## 6. Koordinater og georeferering

**Leveranse:** GeoJSON etter RFC 7946, WGS84, koordinatrekkefølge `[lengdegrad, breddegrad]`. Ikke legg til en gammel GeoJSON `crs`-egenskap som endrer dette.

**Arbeidskoordinater i Oslofjorden:** ETRS89 / UTM sone 33N (`EPSG:25833`) er brukt for bildeuttrekk, arealer og geometrioperasjoner. Velg og dokumenter et egnet projisert koordinatsystem ved bruk andre steder i Norge. Ikke beregn kvadratmeter direkte fra lengde-/breddegrader.

Kommuneinfo kan oppgi `EPSG:4258` (ETRS89 geografisk). Les responsen og transformer eksplisitt; ikke omdøp kildekoordinater til WGS84 uten dokumentasjon. Forskjellen er vanligvis liten sammenlignet med denne kartleggingens usikkerhet, men koordinatsystemene skal fortsatt registreres korrekt.

For et nordvendt bilde uten rotasjon, med faktisk bbox `(xmin, ymin, xmax, ymax)`, bredde `W` og høyde `H`, gjelder for pikselkantkoordinater `(u, v)` fra øvre venstre hjørne:

```text
x = xmin + (u / W) × (xmax − xmin)
y = ymax − (v / H) × (ymax − ymin)
```

For sentrene i heltallspiksler brukes `u + 0,5` og `v + 0,5`. En georeferert rasterfil kan i stedet ha en affin transformasjon med rotasjon; bruk da denne.

Hvis bildet vises nedskalert, må koordinatene omregnes fra **faktisk visningsstørrelse** til originalbildet. Utsnitt krever også at utsnittets offset legges til. Ikke anta at en bildeviser viste originalstørrelsen. Ta høyde for marger og eventuell skalering som endrer sideforhold.

Lagre originalbildet, metadata og eventuelt world-fil/GeoTIFF. Merkede forhåndsvisninger holdes adskilt fra originalene. Ikke bruk genererte eller rekonstruerte bilder som geografisk belegg.

**Oppløsning er ikke nøyaktighet:** `image_resolution_m_per_pixel` beskriver det leverte rasterets pikselstørrelse. Den dokumenterer verken opptakets opprinnelige detaljgrad eller polygonets posisjonsnøyaktighet. Ukjent nøyaktighet skal stå som `null`.

## 7. Leveranser og dataskjema

### Filstruktur for videre arbeid

```text
prosjekt/
  METODIKK.md
  status.json
  samlet.geojson
  samlet-manifest.json
  kommuner/<kommunenummer>/
    raw/                       # Originale API-svar og dokumenter
    images/                    # Originalbilder og metadata
    archive/rev-001/           # Tidligere leveranse
    coverage.json              # Sektorer, fliser, kvalitet og mangler
    candidates.json            # Inkluderte og vurdert utelatte kandidater
    timing.json                # Tidsbruk og avbrudd
    result-rev-002.geojson
    metadata-rev-002.csv
    changes-rev-002.csv
```

Dette er en anbefalt struktur. Dagens pilotmapper flyttes ikke som del av metodearbeidet.

### Felles feltskjema, versjon 1.1 (utvidet fra 1.0)

Tabellen med tilleggene nedenfor er normen for **nye leveranser**. Versjon 1.1 er tatt i bruk for Sandefjord; tidligere leveranser er ikke etterendret. Dagens samlede fil har eldre feltvarianter og er ikke automatisk migrert til dette skjemaet. Endring av gamle godkjente data krever en sporbar migrering; ny semantisk klassifisering krever faktisk gjennomgang.

| Felt | Type | Betydning / regel |
|---|---|---|
| `id` | string | Stabil, globalt unik polygon-ID |
| `harbour_id` | string | Stabil anleggs-/gruppe-ID; brukes ved telling av anlegg |
| `name` | string | Dokumentert eller tydelig beskrivende navn |
| `name_is_descriptive` | boolean | `true` når navnet er laget for kartleggingen |
| `municipality` | string | Offisielt kommunenavn |
| `municipality_code` | string | Firesifret kommunenummer; ikke talltype |
| `classification` | enum | `smabathavn` eller `mulig_smabathavn` |
| `classification_basis` | string | Konkret grunnlag for klassifisering etter regelen |
| `approval_status` | enum | `til_godkjenning`, `godkjent_av_bruker` eller `avvist` |
| `approved_utc` | string/null | ISO 8601 i UTC; null før godkjenning |
| `revision` | integer | Kommuneleveransens revisjonsnummer |
| `method_version` | string | Metodeversjon brukt under gjennomgangen |
| `schema_version` | string | Versjon av feltskjema |
| `geometry_role` | string | Som standard `brygger_batplasser_og_mellomliggende_sjo` |
| `method` | string | Metode brukt for geometri og kontroll |
| `area_m2` | number | Beregnet i dokumentert projisert koordinatsystem |
| `area_crs` | string | Eksempel `EPSG:25833` |
| `longitude`, `latitude` | number | Representativt punkt inne i polygonet; ikke nødvendigvis inngang eller kai |
| `sources` | array of strings | Sporbare kilde-URL-er; behold kilde-ID-er i underlaget |
| `osm_ids` | array of strings | `node/...`, `way/...`, `relation/...`; tom liste hvis ingen |
| `imagery_source` | string/null | Bildetjeneste og tilgjengelig lokal kildeinformasjon |
| `imagery_retrieved_date` | string/null | Dato bildet ble hentet, `YYYY-MM-DD` |
| `source_observation_date` | string/null | Dokumentert lokal opptaksdato; **ikke** nedlastingsdato |
| `image_resolution_m_per_pixel` | number/null | Leverert rasteroppløsning; ikke posisjonsnøyaktighet |
| `estimated_accuracy_m` | number/null | Bare et tall når det finnes en begrunnet vurdering; ellers null |
| `needs_orthophoto_review` | boolean | Om egnet detaljert bilde-/ortofotokontroll fortsatt gjenstår |
| `needs_dated_imagery_review` | boolean | Om kontroll mot tidsfestet bildegrunnlag gjenstår |
| `current_operation_verified` | boolean | Om drift på et oppgitt tidspunkt er dokumentert; synlig bildeanlegg alene er ikke nok |
| `reviewed_date` | string | Dato for denne vurderingen |
| `berth_count_published` | integer/null | Kapasitet oppgitt i kilde; ikke et automatisk bildeestimat |
| `berth_count_source` | string/null | Kilde til publisert kapasitet |
| `berth_count_approximate` | boolean/null | Om kilden sier «ca.»; null når kapasitet mangler |
| `berth_count_scope` | string/null | Om kapasiteten gjelder hele anlegget eller et bestemt delområde |
| `municipality_clipped` | boolean | Om polygonet er klippet ved kommunegrensen |
| `cross_municipality_group_id` | string/null | Valgfri kobling mellom deler i forskjellige kommuner |
| `attribution` | string | Korrekt kreditering for brukte kilder |
| `note` | string | Begrensninger, konflikter, gruppetolkning og andre vesentlige forhold |

For ukjente verdier brukes `null`, ikke `0`, tomt årstall eller oppdiktet tall. En usikker kandidat kan være godkjent av brukeren uten å skifte klasse.

Flagget `needs_orthophoto_review=false` betyr i Tønsberg revisjon 2 at visuell kontroll mot Esri-bilder er gjort. Det innebærer ikke kjent opptaksdato eller dokumentert landmålingsnøyaktighet; derfor er `needs_dated_imagery_review=true` og nøyaktighet/dato fortsatt ukjent.

### Feltvarianter i eksisterende data

| Eldre/parallelle felt | Videre anbefaling |
|---|---|
| `kommunenummer` og `municipality_code` | Bruk `municipality_code`; behold sporbarhet ved migrering |
| `status`: `kart_og_kilde`, `ma_avklares`, `kart_og_kildeunderbygget`, `bilde_og_kildeunderbygget`, `usikker_kandidat` | Bevar historisk verdi. Vurder klasse eksplisitt etter regelen; ikke anta at en gammel «kart og kilde»-status oppfyller den |
| `approval_status`, `municipality_delivery_status`, `approval_scope` | Skill leveransegodkjenning fra faglig klasse; ikke overskriv usikkerheten |
| `osm_id` og `osm_ids` | Samle alle referanser i `osm_ids` |
| `positional_accuracy_m` og `estimated_accuracy_m` | Harmoniser felt, men ikke fyll inn tall uten grunnlag |
| `retrieved`, `retrieved_date`, `imagery_retrieved_date` | Skill generell innhenting fra dato for konkret bilde |
| `reviewed` og `reviewed_date` | Standardiser til `reviewed_date` |
| `attribution` og `map_attribution` | Standardiser til `attribution`, med aktuelle kilders kreditering |

### Syntetisk GeoJSON-eksempel

Dette eksempelet viser struktur, ikke en virkelig havn. Det skal ikke importeres i det faktiske datasettet.

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "id": "DEMO-H01-B01",
        "harbour_id": "DEMO-H01",
        "name": "Eksempelvika – mulig småbåthavn",
        "name_is_descriptive": true,
        "municipality": "Eksempelkommune",
        "municipality_code": "0000",
        "classification": "mulig_smabathavn",
        "classification_basis": "Sammenhengende brygger; faste plasser og drift er uklare",
        "approval_status": "til_godkjenning",
        "approved_utc": null,
        "revision": 1,
        "method_version": "1.0",
        "schema_version": "1.0",
        "source_observation_date": null,
        "estimated_accuracy_m": null,
        "needs_dated_imagery_review": true,
        "current_operation_verified": false,
        "berth_count_published": null,
        "sources": ["https://example.org/kilde"]
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[10.40,59.26],[10.401,59.26],[10.401,59.261],[10.40,59.261],[10.40,59.26]]]
      }
    }
  ]
}
```

Eksempelet viser et utvalg felt. Nye faktiske leveranser skal følge tabellen og ha reelle kildehenvisninger.

### CSV og intern dokumentasjon

CSV har én rad per polygon og samme `id` som GeoJSON. Bruk UTF-8, gjerne BOM for regneark, og semikolon som skilletegn. Lister lagres som JSON i cellen. CSV har ikke geometri; den kobles til GeoJSON via `id`. En tom CSV-celle for en nullable verdi skal leses som ukjent, ikke null kapasitet.

Intern flis-/kildemetadata bør minst inneholde:

```text
image_id, source_url, retrieved_utc, observation_date,
source_crs, actual_bbox, requested_bbox, width, height,
pixel_size_x, pixel_size_y, file_hash, attribution,
review_level, image_quality, uncovered_or_unclear_reason
```

`review_level` kan være `oversikt`, `detaljkontroll` eller `ikke_kontrollert`. Kandidatloggen bør inneholde kandidat-ID, sted, observasjon, vedtak, begrunnelse, kilder, berørte polygon-ID-er og dato. Endringsloggen skal ha minst tidligere/ny ID, handling og begrunnelse. Ikke tegn presise polygoner rundt funn som ikke er tilstrekkelig stedfestet.

### Tillegg i skjema 1.1

| Felt | Type | Betydning |
|---|---|---|
| `candidate_id` | string | Referanse til vurdert kandidat i kandidatloggen |
| `source_register_objectid` | integer/null | Unik objekt-ID fra kommunalt register; foretrekkes fremfor navn/dupliserte etiketter |
| `source_register_number` | string/null | Kildens egen etikett; kan være feil eller duplisert |
| `source_register_members` | array[integer] | Alle registerobjekter representert i dette fysiske havneområdet |
| `capacity_components` | array[object] | Separate kildetall/navn når summering eller delgrense ikke er forsvarlig; ikke automatisk additivt |
| `berth_count_reference_period` | string/null | Oppgitt referanseperiode eller eksplisitt ukjent; hentedato er ikke observasjonsdato |

`method` skal angi bildeverifisert OSM-omriss der dette brukes. Polygonene skal ikke omtales som fullt nydigitaliserte når geometri er gjenbrukt fra en kilde. Overlapp langs kaier kan tilpasses etter visuell kontroll, med kilde og begrunnelse; ikke utfør generell automatisk fjerning av overlapp mellom ukjente operatører.

## 8. Kontroll og godkjenning

### Geografisk og teknisk kontroll

Før leveranse skal følgende være kontrollert:

- Gyldig GeoJSON, lukkede polygonringer og konsistent koordinatrekkefølge.
- Ingen selvkryss, tomme polygoner eller åpenbare georefereringsfeil.
- Unike polygon-ID-er; stabil kobling mellom anlegg og delpolygoner.
- Polygonene ligger i kommunen, eller grenseklipping er dokumentert.
- Areal beregnes i meterbasert projeksjon; representativt punkt ligger inne i polygonet.
- Duplikate OSM-punkter/-områder er ikke blitt separate havner.
- Ingen uforklarte overlapper mellom havnepolygoner. I Tønsberg ble overlapp under 1 m² brukt som numerisk toleranse, og avvik utenfor grensen under 0,02 m² som transformasjonstoleranse. Disse er tekniske toleranser, ikke påstander om kartleggingsnøyaktighet.
- CSV og GeoJSON har identiske ID-sett og radantall.
- Hvert polygon er sett som overlegg på bildet etter siste geometriendring. Kontroller særlig smale kanaler, bygninger, land, farled og bryggeender.

### Innholdskontroll

- Hver kandidat har konkret klassifiseringsgrunnlag etter gjeldende regel.
- Publisert kapasitet har kilde og riktig omfang; visuell vurdering presenteres ikke som publisert kapasitet.
- Ukjent bildedato/nøyaktighet står som ukjent.
- Uklare, skydekte og ufullstendig undersøkte sektorer er dokumentert.
- Godkjente eldre kommuner er ikke blitt endret av et nytt nabofunn.
- Antall anlegg og polygoner rapporteres hver for seg.
- En fullstendighetspåstand er ikke sterkere enn dokumentert dekning. Ikke skriv «alle havner funnet» på grunnlag av en visuell gjennomgang alene.

### Ved godkjenning

Oppdater status, godkjenningsdato, kommuneleveranse, CSV, samlet fil og manifest konsistent. Kontroller at samlet fil inneholder riktig kommuneversjon og at fjernede ID-er ikke lever videre. Godkjenning skal kunne spores til revisjonen brukeren faktisk vurderte. Ta vare på tidligere revisjoner.

## 9. Begrensninger og antagelser

| Tema | Konsekvens og håndtering |
|---|---|
| Ukjent opptaksdato | Man kan påvise struktur i bildet, men ikke uten videre dagens situasjon. Lagre null og bevar kontrollbehov |
| Mosaikk og skiftende kilder | Nabofelt kan vise ulike årstider eller år; sjekk sømmer og kildeopplysninger |
| Skyer, skygger, vinter og tomme plasser | Fravær av synlige båter dokumenterer ikke fravær av havn |
| Oppskalering av bilde | Flere eksportpiksler skaper ikke nye detaljer; unngå falsk presisjon |
| Manuell digitalisering | Grensene har tolknings- og plasseringsusikkerhet; koordinatdesimaler er ikke nøyaktighetsbevis |
| Visuell AI-analyse | Små anlegg kan overses eller feiltolkes. Dokumenter dekning og kontroller med kilder og overlegg |
| Avhengige kilder | OSM og nettsteder som gjenbruker OSM er ikke to uavhengige bekreftelser |
| Kildekonflikter og historiske dokumenter | Prioriter tidsfestet, stedsspesifikt belegg. Bevar tvil og ikke lat som planlagt anlegg er eksisterende |
| Felles drift kan ikke sees direkte | Gruppér med begrunnelse. Samme kyststrekning, øy eller boligområde er ikke alene bevis |
| Kommunegrenser i sjø | En nærliggende havn kan høre til nabokommunen; bruk geometri, ikke stedssøk alene |
| Land- og sjøareal | Publisert havneareal kan omfatte opplag og bygninger; det er ikke direkte sammenlignbart med våre vannpolygoner |
| Ulik historisk metode | Godkjente Holmestrand/Horten er ikke etterprøvd med den nye Esri-metoden og ti-plassregelen |
| Innsjøer | Tønsberg har topografisk innsjøscreening, ikke full flybildekontroll av alle innsjøstrender. Oppgi tilsvarende omfang for hver kommune |

Arbeidsantagelser som skal følge leveransen:

1. Dette er en visuell og kildebasert kartlegging uten befaring eller uavhengig landmålingskontroll.
2. Anlegg kan inkluderes med ukjent kapasitet dersom dokumentert felles drift med faste plasser oppfyller regelen.
3. Registreringen er av havneanlegg, ikke et datasett over samtlige private båtplasser.
4. Geometrien viser en begrunnet fysisk avgrensning, ikke juridisk råderett eller navigasjonssikkerhet.
5. Brukeren avgjør godkjenning av kommuneleveransen. Usikre kandidater forblir usikre etter godkjenning.

## 10. Tidsbruk og kostnader

Registrer for hver kjøring:

- Start/slutt i UTC, og metode-/dataskjemaversjon.
- Veggklokketid, avbrudd og venting på brukeren hver for seg.
- Nettverksventing, gjenbrukte bilder, nye nedlastinger og antall detaljkontroller der dette kan måles.
- Førstegangsarbeid og revisjonsarbeid separat.
- Antall sektorer, kandidater, polygoner og usikre anlegg.
- Token-/API-forbruk hvis tilgjengelig; ellers «ikke målt». Ikke estimer dette som om det var målt.

**Registrert historikk:** Horten 20 min 31 sek; Tønsberg første gjennomgang 26 min 34 sek. Tønsberg revisjon 2 har registrert veggklokketid 2 t 39 min 10 sek, med søk, innhenting, venting og ny digitalisering. Den siste tiden er ikke et mål på aktiv analysetid alene. Kjøringene har forskjellig metode og er ikke et robust grunnlag for lineær prognose for resten av fjorden.

Det tidligere Horten-estimatet brukte 26 kommuner som planleggingsantagelse. Det er ikke en kvalitetssikret avgrensning av dette prosjektets kommuneliste, og skal ikke videreføres som en fast premiss uten avklaring.

For et bedre estimat: mål flere kommuner med samme metode og sammenlign etter kystkompleksitet, antall kandidater og tilgjengelig bildedekning. Hold brukerens godkjenningsventing utenfor produksjonsestimatet.

For lavere forbruk: gjenbruk identiske georefererte utsnitt, søk målrettet etter at kandidatene er funnet, hent detaljer ved behov, og gi korte statusmeldinger. Ikke spar bort detaljkontroll eller skjul udekkede områder for å få et lavt token- eller tidsestimat.

## 11. Erfaringer og kommunelogg

### Tønsberg: dokumentert metodeforbedring

Revisjon 1 leverte 19 polygoner: 11 kart-/kildeunderbyggede og 8 usikre kandidater. Brukerens tilbakemelding viste at kandidatfangsten og grensen mot enkeltbrygger måtte forbedres.

I revisjon 2 ble 35 topografiske fliser gjennomgått på nytt og 15 Esri-bildeutsnitt brukt som underlag. Innsjøene ble screenet i kart; flybildekontrollen rettet seg mot kystanlegg. Det var delvis skydekke langs Slagen-kysten.

Resultatet ble 20 polygoner for 17 anlegg: 15 klassifisert som småbåthavn og 2 som mulig småbåthavn. Seks delpolygoner ble lagt til, fire tidligere kandidater fjernet og ett polygon samlet med et annet. Sluttantallet alene skjuler derfor omfanget av forbedringen.

Sentrale endringer:

- Klopp båthavn ble tatt inn. Operatøren oppgir ca. 160 plasser.
- Husøy Småbåthavn SA ble tatt inn med sjøavgrensning ved Myrasundet. Operatøren oppgir 75 plasser.
- Vestre og østre båtanlegg ved Husøy Havn ble registrert som to delpolygoner med felles havne-ID.
- Nordre del av Tønsberg gjestehavn ble lagt til under samme havne-ID som den søndre delen.
- Nordre bryggeanlegg i Jarlsøsundet ble tatt inn som usikker kandidat.
- Kaldnes Brygge ble samlet til ett anlegg, med bedre skille mellom vann og boligblokker.
- Et eldre OSM-område ved Kirkegaten ble tatt ut som feil avgrensning. Mulige moloområder ved Ringshaugodden, Furustrand og Karlsvika ble tatt ut fordi regelen ikke var dokumentert oppfylt.

**Overførbar læring:** Kombiner systematisk bildegransking med kildesøk, før klassifisering og digitalisering. Bruk eksisterende havnelister som supplement. Kontroller geometri visuelt også etter at den har bestått geometriske tester.

Dette dokumenterer forbedringer i Tønsberg, men er ikke en målt presisjons-/dekningsprosent. Det finnes ingen komplett fasit eller statistisk evaluering i prosjektet ennå.

### Kommunelogg

| Kommune / revisjon | Regel og bildegrunnlag | Resultat / godkjenning | Åpne forhold |
|---|---|---|---|
| Holmestrand pilot | Før dagens eksplisitte regel; topografisk kart | 14 polygoner; godkjent pilot | Ikke etterkontrollert med ny metode; suppleringsfunn Våle venter |
| Horten pilot | Før dagens eksplisitte regel; topografisk kart | 16 polygoner; godkjent | Ikke etterkontrollert med ny metode |
| Tønsberg rev. 1 | Topografisk kart; kriterier senere presisert | 19 polygoner; erstattet av rev. 2 | Beholdt som arkiv og endringsgrunnlag |
| Tønsberg rev. 2 | Godkjent arbeidsregel; kart og Esri-bilder | 17 anlegg / 20 polygoner, 2 usikre anlegg; godkjent 2026-10-29 | Ukjent lokal bildedato/nøyaktighet; delvis skyer; dagens drift ikke generelt verifisert |

### Mal som fylles ut etter hver kommune

```markdown
### <Kommune> – revisjon <n>

- Kommunenummer:
- Metodeversjon / skjemaversjon:
- Start/slutt UTC; veggklokketid; avbrudd:
- Siste leveranse og status: til godkjenning / godkjent / avvist
- Godkjenningsdato og godkjent revisjon:
- Antall anlegg / polygoner / usikre anlegg:
- Undersøkt omfang: fastland, øyer, elvemunninger, innsjøer:
- Dekning: antall sektorer/fliser, detaljkontroll og eventuelle hull:
- Kilder og lokale opptaksdatoer (eller ukjent):
- Nye funn, utelatelser og endringer fra tidligere revisjon:
- Hva fungerte / hva ble oversett eller feiltolket:
- Nye antagelser, konflikter og begrensninger:
- Konkret forbedring for neste kommune:
- Funn i nabokommuner som venter på egen behandling:
- Filreferanser: GeoJSON, CSV, endringer, kontrollogger:
```

## 12. Vedlikehold og instruks til neste agent

### Oppdateringsregler

- Les kommuneloggen før ny analyse og oppdater den etter hver leveranse/revisjon. Registrer godkjenningen når den foreligger.
- Nye erfaringer skal angi kommune, dato, faktisk observasjon og hvilken endring som foreslås. Skill observert forbedring fra en hypotese som ennå ikke er prøvd.
- Oppdater metodeversjon når arbeidsflyt eller kvalitetskrav endres. Oppdater skjemaversjon ved endrede felt eller feltbetydninger.
- Endringer i brukerens ti-plassregel eller hva som skal inkluderes skal foreslås for brukeren før de brukes. Vanlige implementasjonsvalg innenfor denne metoden krever ikke ny godkjenning.
- Ikke beskriv en ny metode som allerede gjennomført på gamle kommuner. En etterkontroll er en ny revisjon som skal godkjennes.
- Hold status, faktisk GeoJSON og manifest i samsvar. Ved uenighet: undersøk filene og godkjenningshistorikken; ikke stol blindt på en gammel opptelling.
- Hold dokumentet forståelig: oppdater hovedteksten når en anbefaling blir etablert praksis, og bevar begrunnelsen i endringsloggen.

### Kort overleveringsinstruks

> Les METODIKK.md og statusfilen. Arbeid bare på kommunen brukeren har bestilt. Bruk godkjent klassifiseringsregel. Dekk strandlinjen systematisk med kart og georefererte bilder; suppler med kilder om drift og faste båtplasser. Loggfør uklare og utilgjengelige områder. Tegn polygoner rundt brygger, båtplasser og mellomliggende sjø, med felles havne-ID for delområder. Bevar ukjente datoer, ukjent nøyaktighet og usikker klasse. Kontroller hvert overlegg visuelt og valider eksporten. Lever GeoJSON og metadata-CSV kortfattet. Vent på kommunevis godkjenning, oppdater samlet datasett og manifest etterpå, og ikke start neste kommune uten bestilling. Legg erfaringen inn i kommuneloggen og foreslå eventuelle regelendringer eksplisitt.

### Endringslogg for metodikken

| Dato | Versjon | Endring |
|---|---|---|
| 2026-10-29 | 1.0 | Første samlede, agentuavhengige metodebeskrivelse. Dokumenterer godkjent klassifiseringsregel, Esri-læring fra Tønsberg rev. 2, geometri-/kildekontroll, felles skjemaforslag, historiske avvik og mal for løpende kommunelogg. Metoden er ikke etteranvendt på de eldre pilotene. |


### Færder – revisjon 1, 2026-10-29

- Kommunenummer 3911; metode/skjema 1.0. Status: **til godkjenning**. Ikke innlemmet i godkjent samlet datasett.
- Resultat: **30 anlegg / 34 polygoner**, inkludert 2 mulige småbåthavner (Langvikveien og Hagakilen). Hella og Grimestad har i tillegg usikker geometri.
- Omfang: Nøtterøy, Føynland, Tjøme, Hvasser, Veierland, Bolærne og øvrige øyer i den kartlagte kystsonen. 62 overlappende topografiske fliser kontrollert; målrettede Esri-detaljbilder supplert med brede kystutsnitt. Dette er ikke en dokumentasjon av heldekkende høyoppløselig bildedekning.
- Kilder: offisiell kommunegrense, Kartverkets topografiske WMS, Esri World Imagery, individuelt hentede OSM-objekter, kommunens syv småbåthavner og tre gjestehavner, operatører/foreninger. Lokale bildedatoer og nøyaktighet er ukjente.
- Overpass/brede OSM-forespørsler feilet. Kandidater fra OSM måtte suppleres med systematisk kartlesing, bilder og primærkilder. Alle syv kommunalt oppførte småbåthavner og tre gjestehavner er representert, men dette beviser ikke at alle private anlegg er funnet.
- Esri kunne returnere tom href eller null bildedimensjoner selv ved HTTP 200. Endret utsnitt/størrelse og direkte bildeeksport fungerte i mange tilfeller. Kontroller faktisk eksportert extent og dimensjoner før pixelkoordinater omregnes. Ett bredt utsnitt (coast-1-6) feilet; detaljbilder dekker flere aktuelle anlegg i sektoren. Dekningshullet beholdes i kontrolloggen.
- Læring: båtrekker på land ved Vestskogen nord var opplag, ikke ny havn. Kjøpmannskjær/Vrengensundet-kildene pekte til samme fysiske bryggekompleks; interne operatørgrenser er ukjente. Teie/Rosanes og Tangen/arbeidsnavnet Vestgården er heller ikke dobbelttelt. Deler av samme havn deler harbour_id.
- Forbedring neste kommune: bruk land-/kystgeometri for å velge søkefliser. En enkel fargemaske valgte unødvendig mange sjøfliser. Fortsett å kontrollere øyer, og ikke la optimaliseringen skjule små anlegg.
- Geometrikontroll: alle 34 polygoner visuelt kontrollert som overlegg av den eksporterte geometrien på kildebildene; gyldige polygoner, innen kommunegrensen, ingen innbyrdes overlapp større enn 1 m². Dette er en teknisk kontroll, ikke dokumentasjon av landmålingsnøyaktighet.
- Leveranse: `/workspace/faerder-pilot/faerder-bathavner.geojson`, `faerder-metadata.csv`. Sporbarhet: `manual-digitization.json`, `coverage.json`, `images/qa-*.jpg` og `timing.json` i samme mappe.
- Tids-/kostnadsregnskap finnes i timing.json. Faktiske tokens og fakturert beløp er utilgjengelige. Et token-/prisregneeksempel må aldri presenteres som målt kostnad eller validert estimat.

- Start 2026-10-29T13:52:15Z; slutt 2026-10-29T14:40:22Z; veggklokketid 48 min 7 sek. Ingen isolert måling av aktiv behandlingstid.

### Færder – revisjon 2, 2026-10-29

Brukeren påpekte Sundene/Søndre Strandvei, som ble oversett i rev. 1. Kildebildet sundene var allerede hentet og viser et sammenhengende molo-/bryggeanlegg med mer enn ti båtplasser. Ingen loggført eksklusjonsvurdering foreligger. Dette var en utelatelse i gjennomgangen. Tilføyd som 3911-H31-B01; navn er beskrivende og operatør ukjent. Nå 31 anlegg / 35 polygoner; fortsatt to mulige anlegg og to øvrige usikre geometrier. Rev. 1 arkivert i faerder-pilot/archive-rev1. Færder avventer fortsatt godkjenning. Korrigert polygon visuelt kontrollert og eksport validert på nytt.

Forbedring neste komplette kontroll: opprett kandidatliste fra hver detaljflis, med eksplisitt inkluderings-/eksklusjonsgrunn for hver sammenhengende bryggegruppe. «Bilde sett» er utilstrekkelig kontroll. Denne forbedringen er ikke etteranvendt på hele Færder nå; komplettheten er fortsatt usikker. Opprinnelig tidsmåling 48,1 minutter inkluderer ikke rettingen.


### Færder – godkjenning 2026-10-29

Brukeren godkjente revisjon 2: 31 anlegg / 35 polygoner. Godkjenningsstatus oppdatert i GeoJSON og CSV, og leveransen innlemmet i samlet GeoJSON (85 polygoner / fire kommuner). Klassifiserings-, bilde- og geometriusikkerheter er beholdt. Sandefjord foreslått som neste kommune; ikke startet.


### Sandefjord – revisjon 1, 2026-10-29

- Kommunenummer 3907; metode/skjema **1.1**. Status: **til godkjenning**. Samlefilen inneholder fortsatt bare 85 godkjente polygoner fra fire kommuner.
- Resultat: **65 fysiske havneområder / 67 polygoner**, inkludert to mulige småbåthavner: Nedre Solnes og Framnæs Maritime nord. **19 polygoner** har usikker avgrensning; dette er en annen type usikkerhet enn kandidatklassifisering.
- Grunnlag: kommunens småbåthavnutredning (22.12.2022, vedtatt 28.02.2023), offentlig ArcGIS-kartlag med 66 punktobjekter, 22 OSM-kandidater hentet individuelt, operatører og kommunens nåværende havnesider. 66 kommunale detaljbilder, 22 brede Esri-utsnitt og 24 topografiske søkefliser er gjennomgått. Grovkontroll av Goksjø inngår. Dette er ikke heldekkende detaljkontroll av alle innlandsvann eller hele sjøterritoriet.
- Kandidatlogg: alle 66 kommunale OBJECTID-er er koblet til leveransen. Alle 22 OSM-kandidater har vurdering og kobling. To ekstra anlegg er registrert, og fire konkrete tillegg er vurdert utelatt. Totalt 94 loggrader; det betyr ikke 94 ulike havner. Spredte private enkeltbrygger er også vurdert på sektornivå; loggen er ikke en uttømmende individuell registrering av hver private brygge.
- Nyttig funn: kommunens PDF lenket til et digitalt informasjonskart. Den offentlige FeatureServer ga koordinatfestede kandidater som reduserte risikoen for mangler. Undersøk slike kartlenker før bare tekst-/navnesøk brukes neste gang.
- Kildekonflikt: kartgeometrien og attributtene x/y avvek vesentlig for blant annet Mefjorden båtforening, Mefjordveien og Namløs. Kartgeometrien er brukt og kontrollert mot bildene. Nr-etiketter er også duplisert/avvikende; OBJECTID brukes som entydig kilde-ID.
- Kapasitet: normalt hentet fra kommunens punktlag, hvis referanseår er ukjent. Tallene kan avvike fra PDF og nettsider. Kildelenke og referanseusikkerhet følger hvert polygon. Kildetall som gjelder hele anlegget gjentas ikke som additive delpolygonkapasiteter.
- Sammensatte områder: Roabukta omfatter fire registerobjekter/navn (Roa, Roabrygga, Vindal og Asnespynten) i ett sammenhengende fysisk havneområde. Kapasitetskomponentene bevares separat, uten sum, og interne operatørgrenser er ikke påstått. Hesteskoen/MiljøMarina og Sandefjord gjestehavn/La Scala er heller ikke talt dobbelt. Langebys bryggefordeling ble derimot beskrevet konkret i rapporten og er brukt til å skille anleggene.
- Ny kandidat: Huvik Eiendom AS oppgir 32 faste utleieplasser. Denne er skilt fra kommunens ti-plassers Huvik-kandidat. Framnæs nord har tydelige fingerbrygger, men fast bruk versus serviceplasser er uavklart; beholdt som mulig.
- Utelatelser: planlagte store utvidelser ved Nedre Solnes er ikke tegnet som eksisterende havn. Et særskilt åtteplassers anlegg nord ved Natholmen, spredte private pirer i Folehavna-/Vøra-utsnittene og rene servicekaier ved Framnæs er loggført utelatt. Det ekstra bildet med arbeidsnavn varnes var feilsentrert og teller ikke som detaljkontroll av Vårnes.
- Geometri: nye bildebaserte omriss, samt tre uttrykkelig kildeangitte og bildeverifiserte OSM-omriss. Alle eksporterte polygoner er projisert tilbake på kildebildene og kontrollert visuelt. To anlegg har delpolygoner (Berganodden og Stub brygger AS). Delte kai-/molokanter er koordinert etter visuell gjennomgang, og små justeringer er omtalt i notatfeltet. En kontrollert rest på 4,6 m² ved motorbåtforeningens nordkant er utelatt som avgrensningsartefakt. Dette er ingen garanti for landmålingsnøyaktighet.
- Begrensning: ukjente lokale bildedatoer og ukjent oppgitt posisjonsnøyaktighet. Vinterbilder kan vise tomme plasser og utydelige fortøyninger. Historiske bøye-/wireplasser kan være ufullstendig avgrenset. Dagens drift og komplettheten er ikke generelt verifisert.
- Leveranse: `/workspace/sandefjord-pilot/sandefjord-bathavner.geojson` og `sandefjord-metadata.csv`. Kontrollgrunnlag i samme mappe: `candidate-ledger.json/csv`, `sector-review.json`, `coverage.json`, `source-notes.json`, `manual-digitization.json`, `images/qa-0.jpg` til `qa-7.jpg`, originaldata under `raw/`, og `timing.json`.

### Metodeendring 1.1 – anvendt på Sandefjord, ikke etteranvendt på eldre kommuner

1. Hent og vurder kommunale temakart/registre før bildesøk; bruk dem som kandidater, ikke som fullstendighetsbevis eller polygonfasit.
2. Gi kjente og nye kandidater en eksplisitt beslutning med kobling til eksport-ID. Loggfør også sammenslåtte navn, planlagte anlegg og relevante utelatelser. Skill individuell kandidatkontroll fra sektorscreening av private enkeltbrygger.
3. Kryssjekk koordinatattributter mot faktisk geometri, bilder og beskrivelse. Bevar kildens entydige objekt-ID.
4. Bevar separate kapasitetsopplysninger ved overlappende navn/operatører. Ikke lag interne grenser eller summer som kilden og bildet ikke underbygger.
5. Oppgi uttrykkelig om et omriss er manuelt tegnet eller hentet fra OSM og kontrollert visuelt. Kontroller hele eksporten som bildeoverlegg, samt gyldighet, kommunegrense, overlapp og CSV-samsvar.

Disse kontrollendringene endrer ikke brukerens ti-plassregel. Et dokumentert fast småbåthavnanlegg kan fortsatt inkluderes med færre plasser, eksempelvis La Scala. En privat pir med åtte plasser blir ikke automatisk en dokumentert småbåthavn fordi den nevnes i en rapport.

- Tidsmåling Sandefjord: 2026-10-29T14:54:46Z–2026-10-29T15:57:22Z, 62.6 minutter veggklokketid. 117 georefererte kildebilder ble lastet ned. Aktiv beregningstid og faktisk token-/faktureringsregnskap er ikke tilgjengelig.


### Sandefjord – godkjenning 2026-10-29

Brukeren godkjente revisjon 1: 65 anlegg / 67 polygoner. Godkjenningsstatus er oppdatert i kommuneleveransens GeoJSON og CSV. Samlefilen inneholder nå 152 polygoner fra fem godkjente kommuner; manifest og status er oppdatert. To usikre kandidater, 19 polygoner med usikker avgrensning og øvrige forbehold er beholdt. Ingen neste kommune er startet. Godkjenning registrert 2026-10-29T16:01:59Z.


### Larvik – revisjon 1, 2026-10-29, til godkjenning

- Resultat: 23 fysiske anlegg / 32 polygoner. Ingen leverte polygoner er klassifisert som mulig havn; 15 polygoner har usikker avgrensning. Dette innebærer ikke at kandidatgrunnlaget er komplett. Samlefilen er fortsatt 152 godkjente polygoner fra fem kommuner.
- Alle 19 OSM-kandidater er bilde-/kildekontrollert og koblet til leveransen. To OSM-punkter ved Kjerringvik Nordhavna er samordnet. Karistranda/Vadskjæret er ett fysisk anlegg. Larvik Havns liste dekker kommunale anlegg og er ikke en fullstendig privat havneoversikt. Ingen fullstendig kommunal punktdatabase ble funnet.
- 100 georefererte bilder er hentet. 31 brede topografiske søkefliser, 21 brede Esri-utsnitt, 19 opprinnelige detaljutsnitt og målrettede tillegg inngår. Dekning gjelder kystscreening, nedre Lågen og målrettet Farris-kontroll; ikke heldekkende detaljkontroll av alle innlandsvann eller hele sjøterritoriet. Kandidatlogg og sektorlogg følger leveransen.
- Flere navngitte foreninger er ikke sikkert stedfestet: Tvedalen, Storehamn, Hovet og Kaupang. Fritzøe Brygge er omtalt som gjestehavn, men fikk ikke en pålitelig polygonavgrensning. Naverfjorden og mulig Lille Ranvika beholdes uten polygon i kandidatloggen. Svenner er ikke avklart som kvalifiserende bryggeanlegg. Disse åpne kandidatene begrenser komplettheten.
- Læring: kontakt-/kontoradresser ga flere feilplasserte detaljbilder. En juridisk foreningsadresse skal ikke automatisk brukes som havneposisjon. Operatørens egen kartlenke ga derimot en presis kandidat for Farris båtforening i Kilen. Stedsnavn fra andre kommuner må filtreres geografisk.
- Agnes er delt i tre sjø-/bryggepolygoner slik at store landarealer ikke inngår. Oppgitt kapasitet rundt 100 gjelder hele gruppen og ligger bare på første rad. Bjønnesstranda har 143 kildeoppgitte plasser. Stavern-foreningens 757 plasser brukes ikke som sum for hele det sammensatte fysiske havneområdet. Interne operatørgrenser ved Stavern, Hølen og Ødegården er ikke kartlagt.
- Alle eksporterte omriss er kontrollert som bildeoverlegg. Flere foreløpige omriss ble korrigert eller trukket ved denne kontrollen. En delt grense i Stavern ble samordnet ved å fjerne 20,79 m² dobbelt avgrensning innen samme havnegruppe. Geometrier er gyldige, innen kommunegrensen, uten overlapp over 1 m², og CSV har én rad per polygon. Dette dokumenterer teknisk kontroll, ikke landmålingsnøyaktighet.
- Begrensninger: kraftig sjørefleks, ukjent opptaksdato og ukjent oppgitt posisjonsnøyaktighet. Dagens drift er ikke generelt bekreftet. Utbyggingsplaner og historiske nautiske oversikter brukes ikke som dagens avgrensning. Fullstendighet krever oppfølging av kandidatloggen.
- Tid: 40.0 minutter veggklokketid. Faktiske tokens og kostnad er utilgjengelige; bilde-/kallantall er arbeidsmengdemål, ikke tokenregnskap.
- Leveranse: `/workspace/larvik-pilot/larvik-bathavner.geojson`, `larvik-metadata.csv`, `candidate-ledger.json/csv`, `coverage.json`, `sector-review.json`, `source-notes.json`, `manual-digitization.json`, `images/qa-*.jpg` og `timing.json`. Neste kommune avventer brukerens godkjenning.


### Larvik – godkjenning 2026-10-29

Brukeren godkjente revisjon 1: 23 anlegg / 32 polygoner. Godkjenningsstatus er oppdatert i GeoJSON og CSV, og Larvik er innlemmet i samlefilen: 184 polygoner fra seks godkjente kommuner. De 15 usikre avgrensningene og uavklarte kandidatene er beholdt. Ingen neste kommune er startet. Godkjenning registrert 2026-10-29T16:53:23Z.


### Moss – revisjon 1, 2026-10-29, til godkjenning

- Kommunenummer 3103, inkludert Jeløya og tidligere Rygge. Metode/skjema 1.1. Resultat: 22 fysiske anlegg / 26 polygoner, hvorav ett mulig anlegg (Støtvig østre brygge) og 15 usikre avgrensninger. Godkjent samlefil er uendret: 184 polygoner / seks kommuner.
- Kildegrunnlag: felles avfallsplan publisert hos Kambo Marina med 24 navngitte havner, 17 sekundærkandidater fra OSM/Sjøsett (ett slettet OSM-objekt svarte 410), kommunens kartinngang og operatørsider. Alle 24 planrader og 17 OSM-kandidater har beslutning i kandidatloggen. Kildelisten er ikke bevis på kompletthet.
- Dekning: 34 brede topografiske og 34 brede Esri-fliser er gjennomgått, pluss 16 opprinnelige detaljkandidater, 16 topografiske detaljutgaver og målrettede tillegg. Totalt 119 georefererte bilder. Dette er bred kommunescreening og målrettet detaljkontroll, ikke uttømmende høyoppløselig kontroll av hver private brygge. Enkelte nordøstlige innlandsoversikter har skyfelt.
- Læring: oppgitt antall i en avfallsplan må få referanseperiode. Nettsiden er tilgjengelig nå, men tallene er rundt 2020. Fuglevik/Rygge oppgir nå 409 plasser og 7 gjesteplasser mot eldre 412/10. Søly oppgir litt over 300 faste plasser mot planens 380; ikke angi et presist aktuelt tall. Landopplag skal ikke legges til kapasitet på vann.
- Sjekta og Refsnes småbåtforening er dokumenterte kildehavner, men en tilstrekkelig begrunnet sjøflate til faste plasser ble ikke identifisert ved omrissene. Land-/opptrekksanlegg er ikke tegnet som sjøpolygoner. Oppføringene beholdes i loggen; de er ikke erklært nedlagt. Dette avgrenser polygonleveransens omfang og krever egen vurdering dersom landplasser senere skal inngå.
- Fuglevik er tvetydig: Fuglevikbryggen på Jeløya er skilt fra Fuglevik båthavn/Rygge båtforening. Riktig Jeløy-brygge ble funnet ved å følge kysten fra bredt georeferert bilde; gårdspunktet traff land. Røedsstranda ble stedfestet via Rødstranda/Billmannsbakken og konkret sameiebeskrivelse av steinmolo/trebrygge med 16 plasser. Feilsentrerte søkeutsnitt er loggført og regnes ikke som kontroll av havnen.
- OSM-omriss for Betongen, Søly og Vansjø omfattet betydelig land, parkering eller opplag. Disse er erstattet med bildebaserte sjø-/bryggeavgrensninger. Fiske beholder et kildeangitt bildeverifisert OSM-omriss. Tre Verket-oppføringer er samordnet til samme fysiske bryggegruppe.
- Knutvika/Teibern har flere utleiere i samme bukt; individuelle driftsgrenser er ikke konstruert. Rørvikas vestre aktører/fiskermolo er heller ikke juridisk fordelt. Kildefigurer er bevart uten sum. Moss Marina og Fleischer Brygge har foreløpige geografiske navnekoblinger; kapasiteten er ikke automatisk overført til hele omrissene. Lersbauen-navnet er uavklart mot Støtvig østre brygge.
- Moss gjestehavn er avgrenset som tre smale brygge-/kaibelter langs kanalen og Tollbodbrygga; seilingsleden, brua og ferjekaiene er ikke havnepolygoner. Felles ytterkant mot Fleischer-området er justert etter bildeoverlegg for å unngå dobbeltregistrering av gjestepontongen.
- Alle eksporterte polygoner er kontrollert som overlegg på kildebildet. Gyldighet, positivt areal, kommunegrense, unike ID-er, overlapp over 1 m² og én CSV-rad per polygon er kontrollert. Bildedato, oppgitt posisjonsnøyaktighet, dagens drift og kompletthet er ikke generelt verifisert.
- Tid: 24.3 minutter veggklokketid. Faktiske tokens og kostnad er utilgjengelige; ingen målt pengepris er oppgitt.
- Leveranse: `/workspace/moss-pilot/moss-bathavner.geojson` og `moss-metadata.csv`; kandidat-/sektorlogg, kilde-/dekningsnotater, digitaliseringsgrunnlag og tidtaking i samme mappe. Neste kommune avventer brukerens godkjenning.


### Moss – godkjenning 2026-10-29

Brukeren godkjente revisjon 1: 22 anlegg / 26 polygoner. Godkjenningsstatus er oppdatert i GeoJSON og CSV, og Moss er innlemmet i samlefilen: 210 polygoner fra sju godkjente kommuner. Én mulig havn, 15 usikre avgrensninger og åpne kildekandidater er beholdt. Ingen neste kommune er startet. Godkjenning registrert 2026-10-29T17:49:50Z.


### Prosjektomfang – brukerbeslutning 2026-10-29

Prosjektet omfatter alle kommuner med kystlinje mot indre eller ytre Oslofjord. Brukeren godkjenner hver ferdig analyserte kommune ved å se på GeoJSON-filen, og neste kommune startes bare etter brukerens beskjed. Den eldre planleggingsantagelsen om 26 kommuner er ikke kvalitetssikret og erstattes av denne avgrensningen. Den konkrete kommunelisten er ennå ikke fastsatt.


### Råde – revisjon 1, 2026-10-29, til godkjenning

- Kommunenummer 3112; metode/skjema 1.1. Første kjøring med Claude Code lokalt. Arbeidsmappe: `work/3112-rade/`. Samlefilen er uendret: 210 polygoner / 7 kommuner.
- Resultat: **11 fysiske anlegg / 11 polygoner**, hvorav 4 mulige småbåthavner (Fuglevik vestre brygge, Krokstadfjorden kai ved båtverksted, Nordre Tasken og Grimstadstøa) og 7 polygoner med usikker avgrensning.
- Kilder: offisiell kommunegrense (Kommuneinfo, EPSG:4326), OSM via Overpass-speil, Enhetsregisteret, Råde båtforening (402 plasser), Saltnes båtforening (220 bryggeplasser), kommunedelplan for Saltnesområdet 2007 (historiske tall 280/190), eiendomsannonse for Nordre Tasken. Ingen kommunal havnedatabase eller fullstendig havneliste ble funnet.
- Dekning: 26 topografiske og 26 Esri-oversiktsfliser på 4 km. 105 Esri-detaljfliser på 1,1 km, valgt fra 1 km-ruter med 2–99 % vann i kartet og kontrollert mot oversiktsmosaikken. 13 zoomutsnitt på 0,67 m/px. Sjøkysten, Kurefjorden, Krokstadfjorden og Søsterøyene er detaljkontrollert. Vansjø-delen og elveløpet i sørøst er bare kontrollert på oversiktsnivå, med zoom ved OSM-slipper og Grimstadstøa. Vansjø-bildene er vårbilder uten båter.
- Kommunegrensen krysser Saltholmen båthavn. Bare Råde-delen er levert (`municipality_clipped=true`, `cross_municipality_group_id=X-SALTHOLMEN-3112-3107`). Søndre del ligger i Fredrikstad og står i `neighbour-pending.json`, sammen med et Fredrikstad-funn og et Moss-funn ved Larkollen. Godkjent Moss er ikke endret.
- Gruppering: Åven vestre og indre basseng, og Krokstadfjordens østre bryggeanlegg og kaien ved verkstedet, har egne havne-ID-er. Nærhet dokumenterer ikke felles operatør. Krogstad båtforening og Grimstadbukta bryggeforening er koblet geografisk via registeradresse, ikke via dokumentert anleggsplassering.
- Utelatt: spredte private brygger langs Saltnes og Krokstadfjordens nordside, flere brygger under terskelen og slipper. Øketangen bryggeforening ligger i Sarpsborg. Kandidatloggen har 34 rader.
- Alle eksporterte polygoner er kontrollert som overlegg på kildebildet. Tre omriss ble justert etter kontrollen (Saltholmen, Åven indre, Krokstad kai). Gyldighet, kommunegrense, ID-er, overlapp internt og mot samlefilen, og CSV-samsvar er kontrollert (`validation.json`).
- Læring: Esri-eksport på 0,5 m/px ga tom `href` og HTTP 500; 0,67 m/px fungerte. Overpass-hovedtjenesten svarte 406/502; speilet `overpass.private.coffee` fungerte. Kontaktark med 50/100 m-rutenett og koordinatetiketter gjorde digitaliseringen sporbar i meter. Kommunegrensen må alltid legges på zoombildet: den kan dele et bryggeanlegg.
- Begrensninger: ukjent bildedato og posisjonsnøyaktighet. Dagens drift er ikke verifisert. Vansjø-strendene kan ha små fellesbrygger som ikke er sett.
- Tid: se `work/3112-rade/timing.json`. Faktiske tokens og kostnad er ikke målt.
- Leveranse: `work/3112-rade/rade-bathavner.geojson` og `rade-metadata.csv`. Kontrollgrunnlag i samme mappe: `candidate-ledger.json/csv`, `coverage.json`, `source-notes.json`, `manual-digitization.json`, `validation.json`, `qa/qa-*.jpg`, `images/`, `raw/`.
- Kontroll etter brukerinnspill (samme dag): Brukerens eksempel ved Engholmveien ligger i Moss og er dekket av godkjent `3103-H07-B01`. Som ny kontroll ble alle OSM-pirer og -moloer i Råde hentet med geometri og sjekket mot polygonene. Alle udekkede klynger er vurdert i zoom, og ingen nye kvalifiserende anlegg ble funnet. **Forbedring for neste kommune:** kryssjekk OSM-pirer med geometri mot polygonene før leveranse. Klynger som ikke dekkes av et polygon, skal ha en loggført vurdering. Overpass-speil kan svikte; prøv flere.


### Råde – godkjenning 2026-10-29

Brukeren godkjente revisjon 1: 11 anlegg / 11 polygoner. Godkjenningsstatus er oppdatert i GeoJSON og CSV, og Råde er innlemmet i samlefilen: 221 polygoner fra åtte godkjente kommuner. Kommuneuttrekk og kontrollgrunnlag ligger i `data/kommuner/3112-rade/rev-01/`. Arbeidsmappe, bilder og rådata er beholdt i `work/3112-rade/`. Fire mulige havner, sju usikre avgrensninger, grenseklippingen ved Saltholmen og ventelisten for nabokommuner er beholdt. Ingen neste kommune er startet. Godkjenning registrert 2026-10-29T19:10:25Z.


### Metodeendring 1.2 – tatt i bruk for Fredrikstad, ikke etteranvendt

Begrunnelse: Fredrikstad har om lag 120 km kyst og 735 OSM-pirer. Ren manuell digitalisering per anlegg ville ikke skalere. Ti-plassregelen og klassifiseringen er uendret.

1. **Kandidatpolygoner fra OSM-pirer:** Pirer innen 60 m av hverandre klynges. Hver klynge bufres 12 m og lukkes med 20 m, og resultatet klippes mot vannflaten i Kartverkets topografiske kart (utvidet 4 m) og mot kommunegrensen. Dette er bare et utkast til geometri.
2. **Visuell vurdering:** Hver klynge vurderes på Esri-bilde med pirer og utkast påtegnet. Utfallet blir inkluder, klipp, del, legg til manuell flate eller utelat. Alle beslutninger og begrunnelser ligger i `decisions.py` og kandidatloggen.
3. **Systematisk bildesøk:** Alle detaljfliser gjennomgås i kontaktark med kandidatene påtegnet, slik at anlegg uten OSM-pir fanges opp. Slike anlegg tegnes manuelt i meter (EPSG:25833).
4. **Metodefelt:** `method` viser om geometrien er OSM-pir-basert, manuelt tillagt eller manuelt tegnet.
5. **Overleggskontroll:** Alle eksporterte polygoner kontrolleres som overlegg på bildet etter siste endring.

Svakhet: Polygonene følger pirene. Båter langs kai uten pir i OSM kan derfor falle utenfor polygonet, og land kan bli med der kartets vannkant er grov. Usikker avgrensning er derfor flagget hyppigere enn før.


### Fredrikstad – revisjon 1, 2026-10-29, til godkjenning

- Kommunenummer 3107, metode 1.2, skjema 1.1. Arbeidsmappe: `work/3107-fredrikstad/`. Samlefilen er uendret: 221 polygoner fra 8 kommuner.
- **Resultat:** 61 fysiske anlegg og 69 polygoner. 18 anlegg er klassifisert som mulig småbåthavn, og 56 polygoner har usikker avgrensning.
- **Kilder:**
  - offisiell kommunegrense
  - OSM fra Overpass-speil, hentet i ni delruter fordi én samlet spørring tidsavbrøt
  - Enhetsregisteret med 117 båt-, brygge- og marinaenheter
  - stedsnavn-API
  - operatørsider med kapasitet: Onsøy Båthavn 300, Gressvik båtforening ca. 220, Nøkledypet/Kråkerøy båtforening 285, Saltnes båtforening 220, Øra båtforening 76 (sistnevnte er ikke satt på polygonet fordi koblingen er usikker)
  - Statsforvalterens mudringstillatelse for Fredrikstad Motorbåtforening
  - Ingen kommunal havneliste ble funnet.
- **Dekning:** 65 + 65 oversiktsfliser, 282 detaljfliser og 19 zoomutsnitt. 181 kandidater ble vurdert: 177 OSM-klynger, OSM-merker uten pir og manuelle tillegg. Ett anlegg ble funnet bare i det systematiske bildesøket.
- **Bildesvikt:** Esri-mosaikken er gråskjær og uskarp over Torsnes, Ødegårdskilen, Skjærviken og Singlefjorden. Anlegg der er flagget usikre. Bildetidspunktene varierer fra vinter til sommer.
- **Grenser:**
  - Saltholmen-delen i Fredrikstad er klippet ved kommunegrensen og har samme `cross_municipality_group_id` som godkjent `3112-H02-B01`.
  - Singlefjorden vest ligger rett ved grensen.
  - Marinaen ved brua sør for Kjøkøy ligger i Hvaler og står i `neighbour-pending.json`.
- **Grupperinger og delinger:** Gressvik båtforening og Onsøy Båthavn er skilt etter den geografiske plasseringen av OSM-punktet, ikke etter dokumentert driftsgrense. Hankø Marina og Hankø Yacht Club/hotellet har flere delpolygoner hver. Vikane med Fredrikstad Seilforening og Hankøsund båthavn er levert som ett havneområde.
- **Åpne kandidater:** 36 registrerte foreninger er ikke sikkert koblet til et polygon (se `source-notes.json`). Flere av dem ligger trolig i de beskrivende navngitte anleggene.
- **Kontroll:** Overleggskontrollen førte til tre rettelser: Saltholmen-klippingen, ytre L-brygge ved Hankø Yacht Club og vestkanten av Kjøkøy øst. Teknisk validering er bestått (`validation.json`): ingen overlapp og ingen ID-kollisjon med samlefilen.
- **Tid:** se `timing.json`. Tokens og kostnad er ikke målt.


### Fredrikstad – godkjenning 2026-10-29

Brukeren godkjente revisjon 1 (61 anlegg, 69 polygoner). Godkjenningsstatus er oppdatert i GeoJSON og CSV, og Fredrikstad er innlemmet i samlefilen, som nå har 290 polygoner fra ni godkjente kommuner. Kommuneuttrekk, beslutningsfil og kontrollgrunnlag ligger i `data/kommuner/3107-fredrikstad/rev-01/`. Bilder og rådata ligger i `work/3107-fredrikstad/`. Følgende er beholdt uendret: 18 mulige havner, 56 usikre avgrensninger, svakt bildegrunnlag i sørøst, 36 foreninger uten sikker kobling til et polygon og nabofunnet i Hvaler. Ingen neste kommune er startet. Godkjenning registrert 2026-10-29T20:48:04Z.


### Prosjektomfang – presisering 2026-10-29

Brukeren har bestemt at Halden, Porsgrunn og Bamble skal være med. Etter omgangen Bærum–Asker–Lier–Drammen–Oslo gjenstår disse kommunene:

- Nordre Follo, Nesodden, Frogn, Vestby, Hvaler, Sarpsborg, Halden, Porsgrunn og Bamble.
- Ås er ikke avklart: det er ennå ikke kontrollert mot kommunegrensen om kommunen har kystlinje.

Den samme listen ligger i `status.json`.


### Batch Bærum–Asker–Lier–Drammen–Oslo – revisjon 1, 2026-10-29/30

Alle fem er laget med metode 1.2 og skjema 1.1. Arbeidsmappene ligger i `work/<kode>-<navn>/`. Samlefilen er uendret: 290 polygoner fra 9 kommuner.

| Kommune | Anlegg | Polygoner | Mulige | Usikre avgrensninger | Kandidater |
|---|---:|---:|---:|---:|---:|
| Bærum 3201 | 42 | 49 | 20 | 40 | 112 |
| Asker 3203 | 53 | 60 | 13 | 26 | 159 |
| Lier 3312 | 2 | 2 | 0 | 0 | 5 |
| Drammen 3301 | 17 | 19 | 2 | 7 | 44 |
| Oslo 0301 | 32 | 36 | 11 | 16 | 123 |
| **Sum** | **146** | **166** | | | |

- **Kilder:**
  - OSM fra Overpass-speil, hentet i 3 × 3 delruter.
  - Enhetsregisteret.
  - Kartverkets stedsnavn ved hver kandidat.
  - Lokalhistoriewikis havnelister for Bærum og Asker, med plasstall fra rundt 2011. De står bare i notatfeltet og er ikke satt som publisert kapasitet.
  - Asker kommunes havneside: Holmsbu har 250 faste plasser og Filtvet 73.
  - Statsforvalterens mudringstillatelse for Berger båtforening.
- **Systematisk bildesøk:** Bare detaljfliser langs Oslofjorden og Drammensfjorden er gjennomgått. Søket fant ett nytt anlegg utenfor OSM: Sandtaket sør i Asker. Innsjøer, Tyrifjorden/Holsfjorden og elver oppstrøms er utenfor omfanget eller bare grovt kontrollert.
- **Grenseanlegg:**
  - Gyssestad er delt mellom Bærum og Asker (`X-GYSSESTAD-3201-3203`).
  - Hvervenbukta er delt mellom Oslo og Nordre Follo (`X-HVERVEN-0301-3207`). Nordre Follo-delen venter.
  - Engersand havn er levert i Lier.
- **Overleggskontroll:** Den førte til flere rettelser. Tre OSM-omriss i Drammen ble tegnet manuelt i stedet (Muusøya, Solumstrand og Bokerøya). Ett omriss i Asker og tre i Oslo ble utelatt fordi OSM-pirenes plassering ikke stemte med bildet. Disse står som åpne kandidater i `neighbour-pending.json`.
- **Teknisk validering:**
  - gyldige polygoner
  - 0 m² utenfor kommunegrensene
  - ingen overlapp internt, mellom de fem kommunene eller mot samlefilen
  - unike ID-er på tvers av alle fem
  - CSV-filen stemmer med GeoJSON-filen
- **Læring:**
  1. OSM-pirer kan ligge forskjøvet i forhold til Esri-bildet. Der det skjer, er manuelt omriss bedre.
  2. Esri ga avkortede JPEG-filer ved parallell nedlasting. Bilder skal derfor kontrolleres med `Image.load()` før bruk.
  3. Tidtaking per kommune i en batch måler ikke nedlastingen som går parallelt. Veggklokketiden for hele batchen er 20:50 → 00:00 UTC, inkludert brukerens meldinger underveis.
- **Tid:** Se `timing.json` per kommune. Tokens og kostnad er ikke målt.

#### Godkjenning av batchen

Brukeren godkjente hele batchen samlet: 146 anlegg og 166 polygoner. Godkjenningsstatus er oppdatert i GeoJSON og CSV i `work/`. Kommuneuttrekk, beslutningsfiler og kontrollgrunnlag ligger i `data/kommuner/<kode>-<navn>/rev-01/`. Samlefilen har nå 456 polygoner fra 14 kommuner. Før innlemming ble ID-kollisjon og overlapp kontrollert mot samlefilen, uten funn. Følgende er beholdt uendret: mulige havner, usikre avgrensninger, åpne kandidater i `neighbour-pending.json` (blant annet Gilhusbukta, Sjursøya, Sørenga, Ulvøya og Nordre Follo-delen av Hvervenbukta) og grensegruppene. Innlemmingen ble gjort med `work/approve_batch.py`. Klassifiseringstellingen i manifestet ble fullført i et eget steg, fordi Holmestrand- og Horten-pilotene ikke har feltet `classification`. Ingen neste kommune er startet. Godkjenning registrert 2026-10-30T05:46:52Z.


### Moss – separat berikelsespilot 2026-10-31

Brukeren ba om en berikelsespilot i Moss etter sammenligning med Mepex-rapporten «Utslipp til Oslofjorden fra småbåthavner» (30.10.2024). Piloten ligger i `data/berikelse/3103-moss/pilot-01/`, med arbeids-/reproduksjonsskript i `work/3103-moss/`.

Omfang: 22 eksisterende anlegg / 26 godkjente polygoner samt åpne kandidater Sjekta og Refsnes småbåtforening. Eksisterende kommuneleveranse, CSV, godkjenningsstatus og samlefil er ikke endret. Metodeversjon for geometrien og ti-plassregelen er uendret. Berikelsen er til vurdering og ikke innlemmet i godkjente leveranser.

Pilotpraksis: én rad per anlegg og egne observasjoner per felt, med kilde-URL, tidspunkt for innhenting, eksplisitt kildeomfang, eventuell referansedato og linjehenvisning til lagret tekstuttrekk. Kildeverdier fra eldre avfallsplan bevares som historiske komponenter, også når nye kilder oppgir andre tall. Faste/ordinære plasser, jolleplasser, gjestebruk og opplag på land holdes adskilt. Organisasjonsidentitet er ikke alene bevis på stedfesting eller aktuell drift; fleroperatørgrupper splittes ikke uten belegg. Ukjent funksjon registreres som null, ikke nei.

Resultat: 91 observasjoner; åtte anlegg med tallfestede kapasitetsopplysninger kontrollert i tilgjengelige nettkilder; fire med publisert landopplagsfunksjon, med ulik bevisstyrke. Dette er ikke åtte nyoppdagede kapasiteter eller uavhengig verifiserte kapasitetsmålinger. 10 avklaringsbehov er registrert. Ingen nye landpolygoner, bildebaserte tellinger eller direkte operatørhenvendelser er utført. Tidsfestet dokumentasjon på aktuell fysisk drift og dagens rensing er fortsatt ukjent. Ingen fullstendighetspåstand mot Mepex/SALT fremsettes.

Se pilotens README for feltskjema, avvik, gjenstående kontrollbehov og reproduksjon. Berikelsesmetoden skal vurderes etter piloten før eventuell anvendelse på andre kommuner.

### Moss – berikelse i nettstedets havnekort, 2026-10-31

Brukeren har bedt om at piloten kobles til nettstedet. Bare kildebelagte opplysninger eksporteres til en separat `enrichment.json`, koblet med `harbour_id`. Kildehenvisning, innhentingsdato, ukjent referansedato og feltets omfang følger visningen. Eldre kapasitet beholdes som sammenleggbar historikk. Ukjent drift og rensing merkes som ikke verifisert. Ingen nye kandidater eller geometriske endringer innlemmes. Primærdatasettets tidligere godkjenning og metodeversjon er uendret.

### Holmestrand – separat kilde- og berikelsessjekk 2026-10-31

Brukeren ba om tilsvarende sjekk som Moss. Leveransen ligger i `data/berikelse/3903-holmestrand/pilot-01/`, med arbeids-/reproduksjonsskript i `work/3903-holmestrand/`. Alle 12 anleggsgrupper / 14 polygoner er dekket; sju har tidligere status `kart_og_kilde` og fem `ma_avklares`. Disse statusene er ikke harmonisert til nyere klasseverdier. Originalgeometri, egenskaper, godkjent kommuneleveranse, metadata-CSV og samlet datasett er uendret. Våle/Frebergsvik forblir et ikke-godkjent supplement.

41 observasjoner er lagret. Særlig viktig: kommunens ca. 1100 faste plasser lagres én gang på operatør-/gruppenivå, ikke som kapasitet for hvert basseng eller Hagemann. Gjestehavnas ca. 50 båter og 450 meter longside er ulike størrelser og er ikke summert med faste plasser. NJB oppgir 450 på én side og 397 på Havneweb; begge beholdes uten valg av en enkelt kapasitet. Bjerkøya oppgir 155 andelsplasser og 62 utleieplasser, beholdt som separate komponenter. Katalogens 155 kan være en delmengde. Publisert bryggeutvidelse er et kontrollbehov, ikke en ny geometri.

Operatøren Holmestrand Småbåthavn oppgir nå AS, og registeret viser den eldre DA-en under avvikling; kommunesider bruker fortsatt DA. Rolle, selskapsform og havnegrense holdes adskilt. Thorrud/Torrud merkes som ferskvann; campingkapasitet og pris overføres ikke til antall båtplasser. K-gruppenes operatørkoblinger er fortsatt uavklarte. Det er registrert ti avklaringsbehov og utført struktur-/provenienskontroll. Ingen nettsideendring eller innlemming i primærdata er gjort i denne oppgaven. Ingen nye bilder eller befaring er utført; eksisterende behov for ortofotokontroll gjelder fortsatt.


### Nordre Follo – revisjon 1 til godkjenning, 2026-10-31

Brukeren ba om Nordre Follo alene. Leveransen ligger i `data/kommuner/3207-nordre-follo/rev-01/`: to polygoner / to lokale anleggsgrupper, hvorav én dokumentert saltvannshavn (Oppegård Båtforening/Ljansbruket, Nordre Follo-del) og én mulig ferskvannshavn (Gjevika ved Langen). Ingen innlemming i samlefil eller nettsted. Ingen neste kommune startet.

Metode 1.2 / skjema 1.1, manuell bildedigitalisering med OSM- og kildekontroll. 14 overlappende kystbilder dekker den innhentede OSM-kystlinjen, ca. 10,96 km; 17 innlandsbilder er bare kandidatsjekk, ikke komplett innsjøkartlegging. 58 registrerte brygger er vurdert. Ett vellykket detaljbilde gir totalt 32 originalbilder lokalt. Alle to eksportomriss er visuelt kontrollert; geometri, kommunegrense, ID-er, CSV og overlapp er validert. Samlet datasett og manifest er kontrollert uendret: 456 polygoner / 14 kommuner.

Oppegårds publiserte 350 plasser gjelder hele grenseanlegget, ikke dette kommuneuttrekket, og må ikke dobbelttelles med Oslo. Kildens referanseperiode er ukjent. Grensegruppe `X-HVERVEN-0301-3207` beholdes; eksisterende Oslo-navn og geometri endres ikke. Gjevika beholder mulig-klasse fordi eksakt operatørkobling og faste plasser er uavklart. Registeradresser for fire andre kildekandidater gir ingen polygon. Se leveransens README, kandidatlogg og kildeproveniens.

Læring: behold ferskvannskandidater eksplisitt atskilt fra fjordhavner. En grensehavn kan gi en ny kommunerad uten å være et nytt fysisk anlegg; kapasitet og senere anleggstelling må følge samme grensegruppe. Originalbilder/georeferering og QA ligger i arbeidsmappen og må følge med ved maskinflytting. Bildedato, nøyaktighet og dagens drift er fortsatt ukjent; tidsbruk er målt veggklokketid, tokens/pris er ikke målt.

#### Godkjenning og innlemming av Nordre Follo

Brukeren godkjente revisjon 1 med «Godkjent» 2026-10-31. Begge polygonene er innlemmet; samlet 458 polygoner fra 15 godkjente kommuner. Alle 456 eldre features er bevart uendret. Mulig-klasse for Gjevika, ferskvannsmerking, ukjent bildedato, åpne kildekandidater og grensegruppe er beholdt. Nettstedets lokale kartdata og kommunestatus er oppdatert; publisering skjer først ved senere utrulling. Globale havnetall bruker grensegruppe som felles nøkkel (også den eksisterende Gyssestad-gruppen), mens kommunekort beholder lokale ID-er. Dette gir 402 anleggsgrupper inkludert mulige havner, ikke 404 kommunale grupper telt hver for seg. Publiserte 350 plasser er fortsatt bare en hel-havn-opplysning i primærdata; de vises ikke som kapasitet for Nordre Follo-delen. Ingen neste kommune er startet.


### Nesodden – revisjon 1 til godkjenning, 2026-10-31

Brukeren ba om neste kommune; Nesodden (3212) ble valgt fra rekkefølgen i status.json. Leveransen ligger i `data/kommuner/3212-nesodden/rev-01/`: 11 anleggsgrupper / 11 polygoner, inkludert tre mulige (to på Ildjernet og ett ved Kavringstrand). Fem har eksplisitt usikker avgrensning. Alle venter på godkjenning; godkjent samlefil og nettsted er uendret, fortsatt 458 polygoner / 15 kommuner. Ingen neste kommune startet.

Metode 1.2 / skjema 1.1. Alle omriss er manuelt digitalisert i georefererte bilder. 65 kystfliser dekker ca. 55,15 km OSM-kystlinje innen kommunen med grensemargin, inkludert øyer. Kontaktark er gjennomgått uavhengig av kandidatsøket; 310 kartlagte bryggeobjekter er vurdert i 84 klynger. Totalt 72 vellykkede originalbilder, hvorav seks ekstra detaljbilder og ett supplerende innlandsutsnitt. Innlandet er ikke systematisk fullkartlagt. Alle 11 eksportomriss er kontrollert visuelt; geometri, grense, ID-er, CSV og overlapp er validert uten funn.

Oksvals ca. 290 ordinære plasser og Spros ca. 180 publiserte plasser bevares med kilde og ukjent referanseperiode. Medlemmer og tilgjengelige gjesteplasser er ikke brukt som total kapasitet. Spro vises med fysisk molo og brygger; publiserte 2026-tilbud og omtalt ferdigstillelse/fornyelse daterer ikke selve bildet. Steilene krever også kontroll mot datert ortofoto etter fornyelse. Bomansvik beholdes som åpen kildekandidat uten polygon; manglende sikker geometri er ikke fravær av havn. Kavringstrands operatørkobling og mulig felles fysisk havnegruppe med Kavringen er uavklart. Industri-/treningskaier ved Svestad, rutebåt-/frilufts-/badebrygger og separate private landfester kvalifiserer ikke alene.

Læring: et OSM-marina-merke i nærheten av en privat brygge eller servicekai beviser ikke havnetilhørighet. Pirklynger er bare søkehjelp, ikke ferdige havnegrupper. Nye utbygginger kan finnes i bildet selv om landarealene fortsatt fremstår under arbeid; kildeoppgitt ferdigstillelse og bildeopptaksdato må holdes adskilt. Se README, åpne spørsmål og kildeproveniens. Tidsbruk er målt veggklokketid inkludert nettventing; tokens/pris er ikke målt.

#### Godkjenning og innlemming av Nesodden

Brukeren godkjente revisjon 1 med «Godkjent» 2026-10-31. Alle 11 polygoner er innlemmet, inkludert de tre mulige havnene; samlet 469 polygoner fra 16 godkjente kommuner. De 458 tidligere godkjente features er kontrollert uendret med kanonisk SHA-256. Fem usikre avgrensninger, ukjent bildeopptaksdato og åpne spørsmål om Bomansvik, Kavringstrand, Ildjernet og Steilene beholdes. Godkjenning er ikke verifikasjon av fullstendighet, dagens kapasitet eller operatørgrenser. Nettstedets lokale kartdata/kommunestatus er oppdatert; publisering krever senere utrulling. Ingen neste kommune er startet.


### Frogn – rev-01 til godkjenning 2026-10-31

Brukeren ba om neste kommune etter merge av PR #6; Frogn (3214) er kartlagt på egen branch fra main 30cd3d9. Leveransen i `data/kommuner/3214-frogn/rev-01/` har 24 polygoner / 18 fysiske anleggsgrupper, én mulig havn (Bergholmen, to deler) og ti usikre avgrensninger. 256 OSM-pirer i 81 klynger er visuelt kontrollert, i tillegg til uavhengig gjennomgang av 79 kystfliser og åtte detaljfliser. Solbergstrand og Bergholmen har fått egne bildekandidater uten OSM-pirer. Et duplikat mellom bildeutsnitt ble fjernet ved overlappskontroll. Alle endelige omriss er visuelt kontrollert etter eksport.

Dragsunds to brygger grupperes med koordinat- og kildebelegg; Tåjebukta holdes atskilt. Vindfangerbukta/Husvikholmen deles i sjøpolygoner rundt land uten å hevde eksklusive operatørgrenser. Gylteåsen-kapasiteten på 70 er ikke stedfestet til delbrygger og er derfor ikke påført hele gruppen. Publiserte faste/gjesteplasser holdes atskilt; Tåjebuktas leverandørverdi er prosjektopplysning med ukjent referanseperiode. Solbukta beholdes åpen uten nåtidspolygon på grunn av udatert bilde og motstridende skadereferat; referatets hendelsesår må avklares. Foreningsadresse alene stedfester ikke Torkildstranda eller Fløyspjeld.

Gyldighet, unike ID-er, kommunegrense, overlapp mot alle 469 godkjente polygoner, metadata og bildehash/dekoding er validert. Ukjent opptaksdato/posisjonsnøyaktighet, ti usikre avgrensninger, fem åpne kildeavklaringer og manglende systematisk innlandssøk er beholdt. Samledata, manifest og nettsted er uendret. Frogn venter på brukergodkjenning; Vestby er ikke startet. Målt veggklokketid finnes i leveransen; ingen målt token-/kostnadspåstand.


### Frogn – godkjent og innlemmet 2026-10-31

Brukeren godkjente rev-01 og ba om commit, push og PR. Alle 24 polygoner / 18 anleggsgrupper er innlemmet, inkludert mulig Bergholmen. Samlefilen har 493 polygoner fra 17 kommuner. De 469 tidligere features er bevart uendret, kontrollert med kanonisk SHA-256 i `approval.json`. Ti usikre avgrensninger, ukjent opptaksdato/posisjonsnøyaktighet og fem åpne kildeavklaringer beholdes, inkludert Solbukta uten nåtidspolygon og uavklarte operatørgrenser. Godkjenning er ikke verifikasjon av dagens kapasitet, drift eller fullstendighet. Nettstedets lokale kartdata og kommunestatus er oppdatert; publisering krever merge/utrulling. Vestby er ikke startet.


### Vestby – rev-01 til godkjenning 2026-10-31

Brukeren ba om neste kommune etter merge av PR #7. Vestby (3216) er kartlagt på egen branch fra main 0463f63. Leveransen i `data/kommuner/3216-vestby/rev-01/` har 9 sjøpolygoner / 8 anleggsgrupper, inkludert 3 mulige (Andersbrygga, Sonsbuktas vestside og Kjøvangen). Alle ni avgrensninger har kontrollbehov. Fire komplette Overpass-delruter ga 68 grensenære pirer i 16 klynger. Alle ble visuelt kontrollert, sammen med uavhengig gjennomgang av 31 kystfliser og ett detaljbilde; Hvitsten nord og Kjøvangen er ekstra bildekandidater uten egne OSM-pirer. Son-hovedbassenget og molobrygga ble samlet i ett sjøpolygon etter overlappskontroll.

Kapasitet bevares feltvis: Sonskilens 679 og 775 står i konflikt, og Søndre Breviks 141 andelsplasser står mot Havnewebs 150–200 båter ekskl. joller. Son Gjestehavns 65 forhåndsreserverbare plasser er en delmengde, ikke total. Ingen entydig scalar kapasitet påføres; komponentenes omfang og ukjente referanseperiode følger dataene. Son havn nord/Sonskilen behandles som fysisk fleroperatørgruppe; SC ved Son Spa unntas uttrykkelig fra kommunalt operatøransvar uten at det skaper en udokumentert eiendomsgrense.

Operatørkart fra 2025 brukes til navne-/inndelingskontroll, ikke som bevis på bygget geometri. Datert ortofoto trengs ved omtalte bryggeendringer. Båtplasser oppstrøms i Hølenselva/Såna er beholdt som åpen avklaring uten ekstra polygon. Bade-/anløpskaier og separate private brygger er utelatt. Alle endelige omriss er visuelt kontrollert etter eksport; teknisk kontroll av geometri, grense, unike ID-er, overlapp mot 493 godkjente polygoner, CSV og bildehash/dekoding bestått. Samledata, manifest og nettsted er uendret. Vestby venter på godkjenning; Hvaler er ikke startet. Målt veggklokketid ligger i leveransen; ingen målt token-/kostnadspåstand.


### Vestby – godkjent og innlemmet 2026-10-31

Brukeren godkjente rev-01 og ba om commit, merge og PR. Alle 9 polygoner / 8 anleggsgrupper er innlemmet, inkludert 3 mulige. Samlet 502 polygoner fra 18 kommuner. De 493 tidligere features er kontrollert uendret med kanonisk SHA-256 i `approval.json`. Alle ni avgrensningers kontrollbehov, kapasitetskonflikter, fire åpne kildeavklaringer og ukjent bildeopptaksdato beholdes. Godkjenning er ikke verifikasjon av dagens drift, kapasitet eller fullstendighet. Nettstedets lokale kartdata og kommunestatus er oppdatert. Hvaler er ikke startet.


### Hvaler – rev-01 til godkjenning 2026-10-31

Etter merge av Vestby PR #8 ba brukeren om neste kommune. Hvaler (3110) er kartlagt på `data/hvaler-analysis` fra main `6a9fa50`. Leveransen i `data/kommuner/3110-hvaler/rev-01/` har 69 sjøpolygoner / 66 foreløpige fysiske anleggsgrupper, inkludert 20 mulige. 68 avgrensninger trenger kontroll mot daterte ortofoto; bildeopptaksdato og absolutt nøyaktighet er ukjent. Ingen påstand om fullstendighet eller verifisert antall operatører.

Alle 335 OSM-bryggeklynger (948 pirer) har eksplisitte beslutninger. 274 kystfliser er gjennomgått uavhengig av OSM-klyngene, med 19 supplerende bilder; én ekstra mulig fingerbrygge er registrert. Private nabobrygger er ikke summert, og rene fiskeri-/ferge-/bade-/servicekaier er ikke inkludert som havner uten båtplassgrunnlag. Sju åpne kildeavklaringer beholdes.

Kommunens havneside, Borg Havn og operatørkilder brukes til navn og bruk. Havneplan 2018–2028 er historisk; framtidige utvidelser er ikke kartlagt som bygget. Borgs 2024-liste gjelder delanlegg, inkludert næringsplasser. Kapasiteter for foreninger, fritidsplasser og gjesteplasser holdes atskilt. Skjærhaldens 37 reserverbare gjesteplasser er en delmengde av ca.100; operatørgrensene mellom gjestehavn, forening og Lorentzenhavna må avklares. Papperhavn, vestre Vikerhavn og Stokken/Listranda har også åpne geografiske koblinger.

Alle eksporterte omriss er visuelt kontrollert etter eksport, og korrigerte omriss kontrollert på nytt. Teknisk kontroll av geometri, grense, ID-er, overlapp mot 502 godkjente polygoner, CSV og bildehash/dekoding består. Målt veggklokketid ligger i leveransen; tokenforbruk og pris er ikke målt. Samledata, manifest og nettsted er uendret. Hvaler venter på godkjenning; Sarpsborg er ikke startet.


### Hvaler – godkjent og innlemmet 2026-10-31

Brukeren godkjente rev-01 og ba om commit, push og PR. Alle 69 polygoner / 66 foreløpige anleggsgrupper er innlemmet, inkludert 20 mulige. Samlet 571 polygoner fra 19 kommuner. De 502 tidligere features er kontrollert uendret med kanonisk SHA-256 i `approval.json`. 68 avgrensningers kontrollbehov, sju åpne kildeavklaringer og ukjent bildeopptaksdato beholdes. Operatørgrenser, kapasitet og fullstendighet er ikke verifisert av godkjenningen. Nettstedets lokale kartdata og kommunestatus er oppdatert. Sarpsborg er ikke startet.


### Bamble – revisjon 1 til godkjenning, 2026-10-31

Brukeren ba om Bamble (4012). Leveransen ligger i `data/kommuner/4012-bamble/rev-01/`: **38 anleggsgrupper / 43 polygoner** etter to rettingsrunder, inkludert sju mulige havner og 17 usikre avgrensninger. Den venter på godkjenning; samlefil og nettsted er uendret (469 polygoner / 16 kommuner). Ingen neste kommune er startet.

Metode 1.2 / skjema 1.1. Omrissene er tegnet manuelt i georefererte bilder. 130 kystfliser dekker ca. 224 km OSM-kystlinje uten hull, og alle er gjennomgått på kontaktark uavhengig av OSM. 52 kandidater er vurdert enkeltvis: 40 OSM-pirklynger og 12 bildefunn. I tillegg er 12 registrerte foreninger eller havner uten sikker stedfesting loggført som åpne kildekandidater. To bryggeanlegg like utenfor kommunegrensen står i `neighbour-pending.json`. Overpass-delrute 6 måtte deles i fire etter gjentatte tidsavbrudd.

Læring:
1. OSM-dekningen av pirer var svak (144 pirer). Flere store anlegg fantes bare i det systematiske bildesøket. Kontaktark må derfor gjennomgås selv når OSM ser fullstendig ut.
2. Første overleggskontroll avdekket forskyvning eller land i omkring 20 omriss. Rettingen gikk raskere med et zoomverktøy som tegner gjeldende omriss på et forstørret panelrutenett (`work/4012-bamble/zoom.py`). Dette anbefales fra starten neste gang.
3. Beskrivende navn bør hentes fra Kartverkets stedsnavn-API (`/punkt`) ved anlegget, ikke fra hukommelse eller nærliggende fjordnavn. Søkeparameteren for kommune er `knr`, ikke `kommunenummer`.
4. Flere kommunale PDF-lenker svarte 404, og visitnorway.no avviste automatisk henting (403). Kildeopplysningene er derfor tatt fra kommunens egne havnesider, lokalhistoriewiki, Enhetsregisteret og KNBF, med eksplisitt referanseusikkerhet.

Bildeopptaksdato, nøyaktighet og dagens drift er ukjent. Tidsbruk er målt veggklokketid, 51,8 minutter fram til ferdigstillingsskriptet, inkludert nettventing; tokens og pris er ikke målt.

#### Brukerinnspill før godkjenning (samme dag)

Brukeren påviste to oversette havner: Stranda ved Grosholmen og Havparadiset på Kjønnøya (Kjønnøyaveien ca. 217–226). Begge er små kaianlegg der båtene ligger langs steinkai eller i et lite basseng ved en T-brygge, uten OSM-pir. På kontaktark med ca. 1,8 m/px var de ikke synlige som bryggeanlegg. De er lagt til som H31 og H32 (kandidat M13 og M14), med brukerens identifikasjon som grunnlag og usikker avgrensning. Rev-01 er oppdatert før godkjenning; ingen godkjent revisjon er overskrevet.

Forbedring for neste kommune: kontaktark alene fanger ikke opp anlegg langs kai. Følgende kontroller skal derfor gjøres i tillegg:
1. Gå gjennom detaljutsnitt på ca. 0,7 m/px langs bebygd strandlinje (adressepunkter nær sjø), ikke bare kontaktark.
2. Søk i adresseregisteret etter samlinger av adresser ved sjø og naust.
3. Merk «båter langs kai» som egen kandidattype.

Førstegangsarbeidet tok 51,8 minutter. Tiden for rettingen er registrert separat i `timing.json`; ventetid på brukeren er ikke produksjonstid.

#### Brukerinnspill runde 2 (samme dag)

Brukeren viste elleve steder til, og var selv usikker på størrelsen for flere av dem. Utfall:
- **Seks nye anlegg (H33–H38):** Sauøya, Grunnsundveien, Hafsundveien, Trolldalen, Rognstranda og Vinjekilen. Sauøya (C026) var først utelatt som under ti plasser.
- **Omklassifisert:** Vinjestranda (H11) er oppgradert fra mulig til småbåthavn.
- **Utenfor kommunen:** Stråholmen ligger i Kragerø og står som nabofunn.
- **Fortsatt utelatt, nå med begrunnelse i loggen:** Vaterlands gate (private brygger med hver sin landfeste) og en liten brygge ved Rognstranda.
- **Ikke stedfestet:** et molobasseng ved «Kyststien».

Havne-ID-ene fra forrige utkast er beholdt, og nye anlegg er nummerert bakerst.

Samlet læring fra de to rundene:
1. **Kontaktark er for grove.** Ved ca. 1,8 m/px ble brygger med 10–20 båter oversett, særlig når båtene ligger langs kai, i skygge eller ved små molobasseng.
2. **Neste kommune: detaljbilder langs bebygd strand.** Gjør en systematisk gjennomgang i ca. 0,7 m/px (zoompaneler) langs all strandlinje med bebyggelse, hyttefelt eller vei. Kontaktark brukes bare til oversikt.
3. **Revurder grensetilfeller.** Brygger som er utelatt fordi de har «under ti synlige plasser», skal revurderes i høyere oppløsning. Én mosaikk kan vise færre båter enn virkeligheten, for eksempel i en annen sesong.
4. **Vurder å stoppe opp tidlig.** Når brukeren påviser mange mangler, er en full ny gjennomgang i detaljoppløsning mer effektiv enn å rette punkt for punkt. For Bamble er den ikke gjort; fullstendigheten er fortsatt usikker.


### Bamble – revisjon 2 etter fullført detaljgjennomgang, 2026-10-31

Brukeren ba om å ferdigstille ny gjennomgang etter brukerinnspill. Rev-02 ligger i `data/kommuner/4012-bamble/rev-02/` og venter på godkjenning: **53 anleggsgrupper / 59 polygoner**, inkludert **13 mulige havner og 33 usikre avgrensninger**. Dette er **15 nye grupper / 16 nye polygoner** fra rev-01. De 43 tidligere polygonene og ID-ene er bevart; rev-01 er ikke overskrevet. Samledata og nettsted er uendret.

Detaljsøket omfatter 255 kystceller à 500 m, 64 ark, med kildeflisene vist i ca. 0,73 m/px. En bevart, påbegynt gjennomgang hadde allerede kontrollert ark 25–63 og notert 12 funn. Ark 0–24 er fullført nå. Alle de 12 funnene, pluss seks nye kontrollfunn, har fått eksplisitte beslutninger i egne georefererte detaljpaneler. I tillegg er 17 tidligere utelatte kandidater kontrollert på nytt, med eksisterende polygoner som overlegg for å unngå dubletter.

Fem tidligere utelatelser er omgjort: C013 (Skjerkebukta nord), C029 (Bunes), M05 (Ekstrand båtbyggeri/Kuskjær), C019 (Vinjestranda øst) og C020 (Høvika). C013/C029/C019/C020 viser tydelige anlegg over ti-plassgrensen; tidligere vurdering som små enkeltbrygger var feil. Ved båtbyggeriet er faste fritidsbåtplasser ikke skilt sikkert fra service-/salgsplasser, derfor mulig. H45 ved Håvøyveien har to sjøpolygoner med felles landtilkomst; ingen polygon er trukket over land for å binde dem sammen.

Det trekantede molobassenget ved Kruksdalen/Krukodden er stedfestet som H39. Formen passer beskrivelsen av brukerens «Kyststien»-basseng; identitet med originalskjermbildet er ikke bekreftet og beholdes som åpen avklaring. Nye beskrivende navn er støttet av Kartverkets punkt-API, med lagrede svar og proveniens. Navnestøtte er ikke dokumentasjon av operatør.

De 16 nye eksportomrissene er visuelt kontrollert som overlegg etter geometrirettinger. Teknisk kontroll viser gyldige polygoner, unike ID-er, 0 m² utenfor kommunen, ingen intern overlapp eller overlapp mot samledata og fullstendig CSV-samsvar. Bildehashene stemmer. SHA-256-kontroll bekrefter at rev-01, godkjente samledata og nettsted er uendret.

**Kontrollhull beholdes:** Skydekte deler av industrikysten i G024/G028/G030/G031 er ikke tilstrekkelig visuelt kontrollert. Ukjent opptaksdato/nøyaktighet, dagens drift, driftsgrensene Valle/Stoa og ikke-systematisk kartlagt innland er fortsatt begrensninger. «Fullført detaljgjennomgang» betyr at alle feltene er behandlet og begrensningene er loggført, ikke at fullstendighet er bevist.

Læring: Tidligere kandidatpaneler må kontrolleres med eksisterende omriss som overlegg. Et panel kan vise både en liten utelatt brygge og en stor havn som allerede er inkludert. Omvendt må faktisk antall utriggere leses i detalj; en generell «under ti»-begrunnelse kan skjule tydelige større anlegg. Småbåter langs sammenhengende kai skal vurderes på samme måte som flytebrygger, med usikker klasse når faste plasser eller felles drift ikke er dokumentert.

Ny veggklokketid er registrert separat i `rev-02/timing.json`, fra opprettelsen av detaljpanelverktøyet. Innledende fil-/bildekontroll før målepunktet og den tidligere delgjennomgangen er ikke målt i dette intervallet. Tokens og pris er ikke målt. Ingen neste kommune er startet.


### Bamble – revisjon 2 godkjent og innlemmet 2026-10-31

Brukeren godkjente rev-02 og ba om commit, push og PR. Alle 59 polygoner / 53 anleggsgrupper er innlemmet, inkludert 13 mulige havner og 33 usikre avgrensninger. Samlet 630 polygoner fra 20 kommuner. De 571 tidligere godkjente features, inkludert Frogn, Vestby og Hvaler fra siste main, er bevart med kanonisk SHA-256 i `data/kommuner/4012-bamble/rev-02/approval.json`. Rev-01 er bevart som historisk, ikke-godkjent leveranse. Skydekte deler av industrikysten, ukjent bildedato/drift og øvrige åpne avklaringer beholdes. Godkjenning verifiserer ikke fullstendighet eller antall operatører. Nettstedets kartdata og kommunestatus er oppdatert. Ingen neste kommune er startet.

/* Source-owned UI translations. Source documents and place names retain their original language. */
(function(root) {
  'use strict';
  const messages = {
  "feedback.title": {"nb": "Meld inn feil eller mangler", "en": "Report an error or missing harbour"},
  "feedback.help": {"nb": "Kjenner du en havn vi mangler, eller noe som bør rettes? Send sted, forslag til endring og gjerne en kilde via GitHub Issues. Du trenger en GitHub-konto. Innspill blir offentlige og vurderes før datasettet oppdateres. Unngå personopplysninger.", "en": "Know a missing harbour or something that needs correcting? Send the location, proposed change and a source if available via GitHub Issues. A GitHub account is required. Submissions are public and reviewed before the dataset is updated. Avoid personal information."},
  "feedback.href": {"nb": "https://github.com/joevstaas/oslofjord-bathavner/issues/new?template=kartinnspill.yml", "en": "https://github.com/joevstaas/oslofjord-bathavner/issues/new?template=kartinnspill.yml"},

  "publication.status": {"nb": "Første KI-støttede kartlegging", "en": "First AI-assisted mapping"},
  "publication.notice": {"nb": "Kartleggingen bygger på kart, flybilder og offentlige kilder. Den inneholder usikre kandidater, kan ha mangler og er ikke uavhengig faglig kvalitetssikret. Bildeopptaksdato og aktuell drift er ikke bekreftet.", "en": "This mapping uses maps, aerial imagery and public sources. It includes uncertain candidates, may omit facilities and has not undergone independent professional review. Image acquisition dates and current operation are unverified."},
  "publication.approval": {"nb": "Brukergodkjenning betyr at prosjekteieren har kontrollert og tatt inn en kommuneleveranse. Det er ikke en myndighetsgodkjenning eller uavhengig fagkontroll. Flere polygoner kan tilhøre samme havnegruppe; gruppene er foreløpige og kan inkludere mulige havner.", "en": "User approval means the project owner has reviewed and included a municipal delivery. It is not official approval or independent professional validation. Several polygons may belong to one harbour group; groups are provisional and may include possible harbours."},
  "publication.short": {"nb": "Første KI-støttede kartlegging · Ikke uavhengig fagkontrollert", "en": "First AI-assisted mapping · No independent professional review"},

  "s0": {
    "nb": "Kartlegger fjorden…",
    "en": "Charting the fjord…"
  },
  "s1": {
    "nb": "Småbåthavner i Oslofjorden",
    "en": "Oslofjord small-boat harbours"
  },
  "s2": {
    "nb": "Havner i Oslofjorden",
    "en": "Oslofjord harbours"
  },
  "s4": {
    "nb": "Drevet av Ocean Data Platform ↗",
    "en": "Powered by the Ocean Data Platform ↗"
  },
  "s6": {
    "nb": "Småbåthavn",
    "en": "Harbour"
  },
  "s7": {
    "nb": "Mulig havn",
    "en": "Possible"
  },
  "s9": {
    "nb": "Ikke kartlagt",
    "en": "Not yet mapped"
  },
  "s10": {
    "nb": "KURS",
    "en": "HDG"
  },
  "s12": {
    "nb": "HØYDE",
    "en": "ALT"
  },
  "s13": {
    "nb": "POS",
    "en": "POS"
  },
  "s14": {
    "nb": "Fri flyging",
    "en": "Free flight"
  },
  "s17": {
    "nb": "fremover / bakover",
    "en": "forward / back"
  },
  "s20": {
    "nb": "sving venstre / høyre",
    "en": "turn left / right"
  },
  "s23": {
    "nb": "opp / ned",
    "en": "climb / descend"
  },
  "s26": {
    "nb": "vipp kameraet",
    "en": "tilt view"
  },
  "s28": {
    "nb": "raskere ·",
    "en": "boost ·"
  },
  "s30": {
    "nb": "avslutt",
    "en": "exit"
  },
  "s32": {
    "nb": "200+ båtplasser",
    "en": "200+ berths"
  },
  "s33": {
    "nb": "Grunnlag",
    "en": "Basis"
  },
  "s34": {
    "nb": "Kun publisert kapasitet",
    "en": "Published capacity only"
  },
  "s35": {
    "nb": "Publisert + trolig ≥200 fra areal",
    "en": "Published + likely ≥200 from area"
  },
  "s36": {
    "nb": "Også mulig ≥200 (usikre anslag)",
    "en": "Also possibly ≥200 (uncertain estimates)"
  },
  "s37": {
    "nb": "Kun publiserte tall. Ukjent kapasitet utelates.",
    "en": "Published counts only. Unknown capacity is excluded."
  },
  "s38": {
    "nb": "Publiserte tall kan være eldre. Arealanslag er grove og vises separat. Ingen vurdering av forskriftskrav.",
    "en": "Published counts may be old. Area estimates are rough and shown separately. No assessment of regulatory requirements."
  },
  "s39": {
    "nb": "Om arealanslagene",
    "en": "About area estimates"
  },
  "s40": {
    "nb": "Modell testet ved å holde hele kommuner utenfor beregningen. Spennet er veiledende, uten garantert dekning.",
    "en": "Tested by holding entire municipalities out of training. Ranges are indicative, with no guaranteed coverage."
  },
  "s41": {
    "nb": "Havnestørrelse og båtstørrelser varierer. Ukjent kapasitet er ikke det samme som under 200. Utenfor modellens arealområde og for mulige havner beholdes usikker status.",
    "en": "Harbour layouts and boat sizes vary. Unknown capacity does not mean fewer than 200 berths. Extrapolations and possible harbours retain uncertain status."
  },
  "s42": {
    "nb": "Modellgrunnlag og testresultater ↗",
    "en": "Model basis and test results ↗"
  },
  "s43": {
    "nb": "Bakgrunnskart",
    "en": "Base map"
  },
  "s44": {
    "nb": "Satellitt",
    "en": "Satellite"
  },
  "s45": {
    "nb": "Sjøkart",
    "en": "Sea chart"
  },
  "s46": {
    "nb": "Topografi",
    "en": "Topo"
  },
  "s47": {
    "nb": "Kartlag",
    "en": "Overlays"
  },
  "s48": {
    "nb": "Kommunegrenser",
    "en": "Municipality boundaries"
  },
  "s49": {
    "nb": "Havnenavn",
    "en": "Harbour names"
  },
  "s50": {
    "nb": "Terrengforsterkning ×2",
    "en": "Terrain relief ×2"
  },
  "s51": {
    "nb": "Om kartet",
    "en": "About"
  },
  "s52": {
    "nb": "Småbåthavner i Oslofjorden",
    "en": "Small-boat harbours of the Oslofjord"
  },
  "s53": {
    "nb": "Kartet viser omrisset av småbåthavnene som er funnet så langt i kommunene langs indre og ytre Oslofjord: brygger, båtplasser og vannet mellom dem.",
    "en": "This map shows the physical outline of every small-boat harbour found so far in the municipalities around the inner and outer Oslofjord: piers, berths and the water between them."
  },
  "s54": {
    "nb": "816 polygoner fra 23 kommuner",
    "en": "816 polygons from 23 municipalities"
  },
  "s55": {
    "nb": "er kartlagt. Kommunene merket",
    "en": "are mapped; the municipalities marked"
  },
  "s56": {
    "nb": "ikke kartlagt",
    "en": "not yet mapped"
  },
  "s57": {
    "nb": "står for tur.",
    "en": "are next."
  },
  "s58": {
    "nb": "Flyrute",
    "en": "Flyover route"
  },
  "s59": {
    "nb": "Start i Oslo, følg fjorden sørover langs vestsiden og kryss over før turen går nordover igjen.",
    "en": "Start in Oslo, head south-west down the fjord, then cross over and fly north again."
  },
  "s60": {
    "nb": "Hva regnes som en småbåthavn?",
    "en": "What counts as a harbour"
  },
  "s61": {
    "nb": "Et fellesanlegg med minst ti båtplasser, eller en dokumentert marina eller båtforening med faste båtplasser. Spredte private brygger, badebrygger, ferjekaier og planlagte anlegg er utelatt.",
    "en": "A shared facility with at least 10 berths, or a documented marina or boat club with permanent berths. Scattered private piers, bathing piers, ferry quays and planned facilities are left out."
  },
  "s62": {
    "nb": "Mulig småbåthavn",
    "en": "Possible harbour"
  },
  "s63": {
    "nb": "Pilot (kartbasert)",
    "en": "Pilot (map-based)"
  },
  "s64": {
    "nb": "Slik ble kartet laget",
    "en": "How it was made"
  },
  "s65": {
    "nb": "Finn kandidater",
    "en": "Collect candidates"
  },
  "s66": {
    "nb": "fra to uavhengige kilder: brygger og marinaer i OpenStreetMap, og offentlige registre, stedsnavn og kommunale havnesider.",
    "en": "from two independent sources: OpenStreetMap piers and marinas, and public registers, place names and municipal harbour pages."
  },
  "s67": {
    "nb": "Lag foreløpige omriss automatisk:",
    "en": "Draft outlines automatically:"
  },
  "s68": {
    "nb": "nærliggende brygger grupperes, bufres og klippes mot vannarealet i Kartverkets topografiske kart og mot kommunegrensen.",
    "en": "nearby piers are clustered, buffered and clipped to the water area of Kartverket’s topographic map and to the municipal boundary."
  },
  "s69": {
    "nb": "Gjennomgå hver kandidat",
    "en": "Review every candidate"
  },
  "s70": {
    "nb": "mot georefererte flybilder. Hver kandidat tas med, justeres, deles, tegnes på nytt eller utelates, og begrunnelsen loggføres.",
    "en": "against georeferenced aerial imagery. Each one is included, trimmed, split, redrawn by hand or excluded, and the reason is logged."
  },
  "s71": {
    "nb": "Gjennomgå alle bildeflisene",
    "en": "Sweep all imagery tiles"
  },
  "s72": {
    "nb": "langs kysten for å finne havner som mangler i OpenStreetMap, og tegn dem for hånd.",
    "en": "along the shore to catch harbours that are missing from OpenStreetMap, and draw them by hand."
  },
  "s73": {
    "nb": "Kvalitetssikre og godkjenn",
    "en": "Quality-check and approve"
  },
  "s74": {
    "nb": "hver kommune med bildeoverlegg, geometri- og grensekontroller og manuell godkjenning før innlemming i datasettet.",
    "en": "each municipality: overlays on the imagery, geometry and boundary checks, and a manual approval before anything enters the combined dataset."
  },
  "s75": {
    "nb": "Kilder, full metode og KI-modeller →",
    "en": "Data sources, full method and AI models →"
  },
  "s76": {
    "nb": "Begrensninger",
    "en": "Limitations"
  },
  "s77": {
    "nb": "Bildenes opptaksdato er ukjent, det er ikke gjennomført befaring, og små anlegg kan være oversett. Omrissene er kartleggingsanslag, ikke offisielle havne- eller eiendomsgrenser. Usikre omriss er merket i havnekortet.",
    "en": "Image acquisition dates are unknown, no field survey has been made, and small facilities may be missed. Outlines are mapping estimates, not official harbour or property boundaries. Uncertain outlines are flagged in each harbour card."
  },
  "s78": {
    "nb": "Bidragsytere",
    "en": "Credits"
  },
  "s79": {
    "nb": "Laget av",
    "en": "Created by"
  },
  "s81": {
    "nb": "Full metode, data og kode på GitHub ↗",
    "en": "Full method, data and code on GitHub ↗"
  },
  "s82": {
    "nb": "Drevet av",
    "en": "Powered by the"
  },
  "s84": {
    "nb": "fra",
    "en": "from"
  },
  "s87": {
    "nb": "Kilder: © Kartverket (topografisk kart, sjøkart og kommunegrenser); bilder © Esri, Vantor og Earthstar Geographics; © OpenStreetMap-bidragsytere (ODbL); Brønnøysundregistrene; terreng: Mapzen / AWS Terrain Tiles.",
    "en": "Sources: © Kartverket (topographic map, sea chart, municipal boundaries); imagery © Esri, Vantor, Earthstar Geographics; © OpenStreetMap contributors (ODbL); Brønnøysund Register Centre; terrain: Mapzen / AWS Terrain Tiles."
  },
  "s88": {
    "nb": "Metode",
    "en": "Methodology"
  },
  "s89": {
    "nb": "Slik ble havnene kartlagt",
    "en": "How the harbours were mapped"
  },
  "s90": {
    "nb": "En KI-agent kartla havnene kommunevis etter en skriftlig metode. Et menneske godkjente hver kommune ved å kontrollere GeoJSON-filen før den ble tatt inn i datasettet.",
    "en": "An AI agent mapped the harbours one municipality at a time, following a written methodology. A person approved every municipality by inspecting its GeoJSON before it was added to the dataset."
  },
  "s91": {
    "nb": "Datakilder",
    "en": "Data sources"
  },
  "s92": {
    "nb": "Analyse",
    "en": "Analysis"
  },
  "s93": {
    "nb": "KI-modeller",
    "en": "AI models"
  },
  "s94": {
    "nb": "Kvalitet",
    "en": "Quality"
  },
  "s95": {
    "nb": "Nøkkeltall",
    "en": "Numbers"
  },
  "s97": {
    "nb": "Fly- og satellittbilder eksportert som georefererte fliser med ca. 0,67–0,83 m/piksel i EPSG:25833. Dette er hovedgrunnlaget for hvert omriss. Opptaksdatoene er ukjente.",
    "en": "Aerial and satellite imagery, exported as georeferenced tiles at about 0.67–0.83 m/pixel in EPSG:25833. This is the main evidence for every outline. Acquisition dates are unknown."
  },
  "s99": {
    "nb": "Brygger, moloer, marinaer og fortøyninger. Brukes til å finne kandidater og som utgangspunkt for foreløpige omriss. © OpenStreetMap-bidragsytere, ODbL.",
    "en": "Piers, breakwaters, marinas and moorings. Used to find candidates and as the skeleton of draft outlines. © OpenStreetMap contributors, ODbL."
  },
  "s101": {
    "nb": "Kommunegrenser (Kommuneinfo API), topografisk kart (WMS) for kystlinje, vannareal og stedsnavn, og stedsnavnregisteret. Sjøkartet brukes bare i denne visningen.",
    "en": "Municipal boundaries (Kommuneinfo API), the topographic map (WMS) for shoreline, water area and place names, and the place-name register. The sea chart is used only in this viewer."
  },
  "s102": {
    "nb": "Brønnøysundregistrene",
    "en": "Brønnøysund Register Centre"
  },
  "s103": {
    "nb": "Enhetsregisteret: båtforeninger, marinaer og bryggelag. En foreningsadresse er aldri i seg selv bevis for havnens plassering.",
    "en": "The Central Coordinating Register for Legal Entities (Enhetsregisteret): boat clubs, marinas and pier associations. A club’s address is never treated as the harbour’s location."
  },
  "s104": {
    "nb": "Offentlige dokumenter",
    "en": "Public documents"
  },
  "s105": {
    "nb": "Kommunale havnesider, operatørnettsider, avfallsplaner og plandokumenter. Brukes til å dokumentere drift og publisert antall båtplasser.",
    "en": "Municipal harbour pages, operator websites, waste-management plans for harbours and planning documents. Used for operation and published berth counts."
  },
  "s106": {
    "nb": "Analyse, steg for steg",
    "en": "Analysis, step by step"
  },
  "s107": {
    "nb": "Dekning.",
    "en": "Coverage."
  },
  "s108": {
    "nb": "Kommunegrensen konverteres til EPSG:25833, og kystlinjen deles inn i ruter. Oversiktsbilder og detaljfliser på 1,1 × 1,1 km lagres med avgrensning, hentetidspunkt og SHA-256-kontrollsum.",
    "en": "The municipal boundary is converted to EPSG:25833 and the shoreline is split into cells. Overview and 1.1 × 1.1 km detail tiles are stored with their bounding box, retrieval date and SHA-256 checksum."
  },
  "s109": {
    "nb": "Kandidater.",
    "en": "Candidates."
  },
  "s110": {
    "nb": "OpenStreetMap søkes i 3 × 3 delområder. Registeret og stedsnavn undersøkes separat slik at kildene kan kontrollere hverandre.",
    "en": "OpenStreetMap is queried in 3 × 3 sub-areas. The register and place names are searched separately, so the two sources can check each other."
  },
  "s111": {
    "nb": "Foreløpige omriss",
    "en": "Draft outlines"
  },
  "s112": {
    "nb": "(metode 1.2). Brygger innen",
    "en": "(method 1.2). Piers within"
  },
  "s114": {
    "nb": "fra hverandre grupperes, bufres med",
    "en": "of each other are clustered, buffered by"
  },
  "s116": {
    "nb": "og lukkes med",
    "en": "and closed by"
  },
  "s118": {
    "nb": ". Resultatet klippes mot kartets vannareal (+",
    "en": ". The result is clipped to the map’s water area (+"
  },
  "s120": {
    "nb": ") og mot kommunegrensen.",
    "en": ") and to the municipal boundary."
  },
  "s121": {
    "nb": "Visuell gjennomgang.",
    "en": "Visual review."
  },
  "s122": {
    "nb": "Kontrollark viser forslaget (rødt), OSM-brygger (gult) og kommunegrensen på flybildet. Hver kandidat tas med, justeres, deles, utvides, tegnes på nytt eller utelates, og begrunnelsen loggføres. Klassifiseringen følger ti-plassregelen.",
    "en": "Review sheets show the draft (red), OSM piers (yellow) and the boundary on the imagery. Each candidate is included, trimmed, split, extended, redrawn by hand or excluded, and the reason is written down. Classification follows the ten-berth rule."
  },
  "s123": {
    "nb": "Søk etter manglende havner.",
    "en": "Gap sweep."
  },
  "s124": {
    "nb": "Kontaktark med alle kystflisene gjennomgås for å finne havner som mangler i OpenStreetMap. Disse tegnes for hånd, i meter.",
    "en": "Contact sheets of all shoreline tiles are checked for harbours missing from OpenStreetMap. These are drawn by hand, in metres."
  },
  "s125": {
    "nb": "Polygonregel.",
    "en": "Polygon rule."
  },
  "s126": {
    "nb": "Et omriss dekker bryggene, båtplassene og vannet mellom dem. Det dekker ikke hele bukten, landareal eller foreningens eiendom. Havner som krysser en kommunegrense klippes og kobles på tvers av grensen.",
    "en": "An outline covers the piers, berths and water between them. It does not cover the bay, land or club property. Harbours that cross a municipal boundary are clipped and linked across the boundary."
  },
  "s127": {
    "nb": "Metoden har utviklet seg. Holmestrand og Horten er tidlige piloter tegnet etter topografisk kart. Fra Tønsberg til Råde ble omrissene tegnet for hånd på flybilder (metode 1.0–1.1). Fra Fredrikstad ble OSM-baserte forslag kontrollert mot bilder (metode 1.2).",
    "en": "The method changed over time. Holmestrand and Horten are early pilots traced from the topographic map. Tønsberg to Råde were drawn by hand on aerial imagery (method 1.0–1.1). From Fredrikstad onwards, OSM-assisted drafts were reviewed against imagery (method 1.2)."
  },
  "s128": {
    "nb": "KI-modeller og verktøy",
    "en": "AI models and tools"
  },
  "s129": {
    "nb": "KI-modeller:",
    "en": "AI models:"
  },
  "s130": {
    "nb": "kartleggingen ble utført med en blanding av Anthropic Claude Opus 5.5 og OpenAI GPT-6.1 Sol. Begge fulgte samme metode og instrukser.",
    "en": "the mapping was done with a mix of Anthropic Claude Opus 5.5 and OpenAI GPT-6.1 Sol. Both models followed the same methodology and the same instructions."
  },
  "s131": {
    "nb": "Dette gjorde KI-agenten:",
    "en": "What the AI did:"
  },
  "s132": {
    "nb": "skrev og kjørte behandlingsskript, hentet kilder, gjennomgikk bildefliser og kontrollark med innebygd bildeforståelse, klassifiserte kandidater, justerte omriss og loggførte alle beslutninger.",
    "en": "it wrote and ran the processing scripts, retrieved the sources, looked at imagery tiles and review sheets with its built-in image understanding to classify candidates and adjust outlines, and logged every decision."
  },
  "s133": {
    "nb": "Dette ble ikke gjort:",
    "en": "What it did not do:"
  },
  "s134": {
    "nb": "ingen objektdeteksjons- eller segmenteringsmodell ble trent eller brukt, og ingen havn ble klassifisert automatisk fra piksler. Alle geometrioperasjoner er vanlig, repeterbar kode (Python med Shapely, PyProj og Pillow).",
    "en": "no object-detection or segmentation model was trained or used, and no harbour was classified automatically from pixels. All geometry operations are ordinary, repeatable code (Python with Shapely, PyProj and Pillow)."
  },
  "s135": {
    "nb": "Menneskets rolle:",
    "en": "Human role:"
  },
  "s136": {
    "nb": "et menneske fastsatte reglene, godkjente hver kommune og påpekte oversette havner. Disse innspillene førte til metodeendringer, blant annet kryssjekking mot OpenStreetMap-brygger.",
    "en": "a person set the rules, approved every municipality and pointed out harbours that had been missed. Those corrections led to method changes, such as cross-checking against OpenStreetMap piers."
  },
  "s137": {
    "nb": "Kvalitetskontroll",
    "en": "Quality control"
  },
  "s138": {
    "nb": "Etter siste endring kontrolleres hvert eksportert omriss som bildeoverlegg. Automatiske kontroller omfatter gyldig geometri, unike ID-er, 0 m² utenfor kommunegrensen, ingen overlapp internt, med nabokommuner eller med samlefilen, og samsvar mellom CSV og GeoJSON. Usikre omriss og åpne kandidater beholdes og merkes.",
    "en": "After the last edit, every exported polygon is checked as an overlay on the imagery. The automated checks are: valid geometry, unique IDs, 0 m² outside the municipal boundary, no overlap within a municipality, with neighbours or with the combined file, and CSV matching GeoJSON. Uncertain outlines and open candidates are kept and flagged, not removed."
  },
  "s139": {
    "nb": "Les mer",
    "en": "Read more"
  },
  "s140": {
    "nb": "Metodesammendrag (README) ↗",
    "en": "Method summary (README) ↗"
  },
  "s141": {
    "nb": "Full metode og kommunelogger, på norsk ↗",
    "en": "Full methodology and municipal logs, in Norwegian ↗"
  },
  "s142": {
    "nb": "Data: GeoJSON, CSV og kandidatlogger ↗",
    "en": "Data: GeoJSON, CSV and candidate ledgers ↗"
  },
  "s143": {
    "nb": "Forrige stopp",
    "en": "Previous stop"
  },
  "s144": {
    "nb": "Spill av flyturen",
    "en": "Play flyover tour"
  },
  "s145": {
    "nb": "Neste stopp",
    "en": "Next stop"
  },
  "s146": {
    "nb": "Flytur",
    "en": "Tour"
  },
  "s149": {
    "nb": "Turhastighet",
    "en": "Tour speed"
  },
  "s151": {
    "nb": "Bytt 2D / 3D",
    "en": "Switch 2D / 3D"
  },
  "s152": {
    "nb": "Fri flyging (tastatur)",
    "en": "Free flight (keyboard)"
  },
  "s153": {
    "nb": "Finn en havn",
    "en": "Find a harbour"
  },
  "s154": {
    "nb": "Metode",
    "en": "Method"
  },
  "s155": {
    "nb": "Kartlag",
    "en": "Layers"
  },
  "s156": {
    "nb": "Oslofjorden · Norge",
    "en": "Oslofjord · Norway"
  },
  "s157": {
    "nb": "Se alle småbåthavnene i Oslofjorden",
    "en": "See all small-boat harbours in the Oslofjord"
  },
  "s158": {
    "nb": "Utforsk Oslofjorden",
    "en": "Explore the Oslofjord"
  },
  "s159": {
    "nb": "Kartlagt fra flybilder, OpenStreetMap og offentlige registre. Start i Oslo, følg fjorden sørover langs vestsiden og kryss over før turen går nordover igjen.",
    "en": "Mapped from aerial imagery, OpenStreetMap and public registers. Start in Oslo, head south-west down the fjord, then cross over and fly north again."
  },
  "s160": {
    "nb": "Oppdag kartlagte småbåthavner i 3D.",
    "en": "Discover mapped small-boat harbours in 3D."
  },
  "s161": {
    "nb": "Start flyturen",
    "en": "Start the flyover"
  },
  "s162": {
    "nb": "Start turen",
    "en": "Start tour"
  },
  "s163": {
    "nb": "Utforsk fritt",
    "en": "Explore freely"
  },
  "s164": {
    "nb": "Utforsk kartet",
    "en": "Explore map"
  },
  "s165": {
    "nb": "Hvordan ble dette kartlagt? Kilder, metode og KI-modeller →",
    "en": "How was this mapped? Data sources, method and AI models →"
  },
  "s166": {
    "nb": "Om kartleggingen →",
    "en": "About the mapping →"
  },
  "Close": {
    "nb": "Lukk",
    "en": "Close"
  },
  "Map layers": {
    "nb": "Kartlag",
    "en": "Map layers"
  },
  "About this map": {
    "nb": "Om kartet",
    "en": "About this map"
  },
  "Methodology, data sources and AI models": {
    "nb": "Metode, datakilder og KI-modeller",
    "en": "Methodology, data sources and AI models"
  },
  "Controls": {
    "nb": "Kartkontroller",
    "en": "Controls"
  },
  "Find a harbour": {
    "nb": "Finn en havn",
    "en": "Find a harbour"
  },
  "Find harbour": {
    "nb": "Finn havn",
    "en": "Find harbour"
  },
  "Find a harbour or municipality…": {
    "nb": "Finn en havn eller kommune…",
    "en": "Find a harbour or municipality…"
  },
  "Reset north": {
    "nb": "Vend kartet mot nord",
    "en": "Reset north"
  },
  "Toggle municipality boundaries": {
    "nb": "Vis eller skjul kommunegrenser",
    "en": "Toggle municipality boundaries"
  },
  "Toggle harbour names": {
    "nb": "Vis eller skjul havnenavn",
    "en": "Toggle harbour names"
  },
  "Toggle terrain exaggeration": {
    "nb": "Slå terrengforsterkning av eller på",
    "en": "Toggle terrain exaggeration"
  },
  "Play tour": {
    "nb": "Spill av turen",
    "en": "Play tour"
  },
  "Pause tour": {
    "nb": "Sett turen på pause",
    "en": "Pause tour"
  },
  "Previous stop": {
    "nb": "Forrige stopp",
    "en": "Previous stop"
  },
  "Next stop": {
    "nb": "Neste stopp",
    "en": "Next stop"
  },
  "Tour speed": {
    "nb": "Turhastighet",
    "en": "Tour speed"
  },
  "Tour progress": {
    "nb": "Fremdrift i turen",
    "en": "Tour progress"
  },
  "Toggle 2D/3D": {
    "nb": "Bytt mellom 2D og 3D",
    "en": "Toggle 2D/3D"
  },
  "Free flight mode": {
    "nb": "Fri flyging",
    "en": "Free flight mode"
  },
  "3D map of the Oslofjord": {
    "nb": "3D-kart over Oslofjorden",
    "en": "3D map of the Oslofjord"
  },
  "Could not load data": {
    "nb": "Kunne ikke laste kartdata",
    "en": "Could not load data"
  },
  "harbours": {
    "nb": "havner",
    "en": "harbours"
  },
  "polygons": {
    "nb": "polygoner",
    "en": "polygons"
  },
  "municipalities": {
    "nb": "kommuner",
    "en": "municipalities"
  },
  "municipalities approved": {
    "nb": "godkjente kommuner",
    "en": "municipalities approved"
  },
  "last update": {
    "nb": "sist oppdatert",
    "en": "last update"
  },
  "No harbours found": {
    "nb": "Ingen havner funnet",
    "en": "No harbours found"
  },
  "Journey complete": {
    "nb": "Turen er fullført",
    "en": "Journey complete"
  },
  "Back in Oslo": {
    "nb": "Tilbake i Oslo",
    "en": "Back in Oslo"
  },
  "Flyover tour": {
    "nb": "Flytur",
    "en": "Flyover tour"
  },
  "Largest:": {
    "nb": "Størst:",
    "en": "Largest:"
  },
  "possible": {
    "nb": "mulige",
    "en": "possible"
  },
  "Water area": {
    "nb": "Sjøareal",
    "en": "Water area"
  },
  "Published berths": {
    "nb": "Publiserte båtplasser",
    "en": "Published berths"
  },
  "Basis": {
    "nb": "Grunnlag",
    "en": "Basis"
  },
  "Outline": {
    "nb": "Omriss",
    "en": "Outline"
  },
  "Boundary": {
    "nb": "Avgrensning",
    "en": "Boundary"
  },
  "Uncertain": {
    "nb": "Usikker",
    "en": "Uncertain"
  },
  "Provisional": {
    "nb": "Foreløpig",
    "en": "Provisional"
  },
  "Note": {
    "nb": "Merknad",
    "en": "Note"
  },
  "Clipped at municipal border": {
    "nb": "Klippet ved kommunegrensen",
    "en": "Clipped at municipal border"
  },
  "Capacity:": {
    "nb": "Kapasitet:",
    "en": "Capacity:"
  },
  "Source": {
    "nb": "Kilde",
    "en": "Source"
  },
  "Method": {
    "nb": "Metode",
    "en": "Method"
  },
  "Earlier mapping note:": {
    "nb": "Tidligere kartleggingsnotat:",
    "en": "Earlier mapping note:"
  },
  "Reference year unknown": {
    "nb": "Referanseår ukjent",
    "en": "Reference year unknown"
  },
  "Original mapping note (Norwegian)": {
    "nb": "Opprinnelig kartleggingsnotat (norsk)",
    "en": "Original mapping note (Norwegian)"
  },
  "Reference date unknown": {
    "nb": "Referansedato ukjent",
    "en": "Reference date unknown"
  },
  "Reference:": {
    "nb": "Referanse:",
    "en": "Reference:"
  },
  "Checked": {
    "nb": "Kontrollert",
    "en": "Checked"
  },
  "Reported": {
    "nb": "Oppgitt",
    "en": "Reported"
  },
  "Reported unavailable": {
    "nb": "Oppgitt utilgjengelig",
    "en": "Reported unavailable"
  },
  "Earlier source": {
    "nb": "Tidligere kilde",
    "en": "Earlier source"
  },
  "unknown": {
    "nb": "ukjent",
    "en": "unknown"
  },
  "approximately 2020 (unconfirmed)": {
    "nb": "omtrent 2020 (ubekreftet)",
    "en": "approximately 2020 (unconfirmed)"
  },
  "Moss · source review": {
    "nb": "Moss · kildegjennomgang",
    "en": "Moss · source review"
  },
  "Source review is loading.": {
    "nb": "Kildegjennomgangen lastes.",
    "en": "Source review is loading."
  },
  "Source review is unavailable. Try reloading the page.": {
    "nb": "Kildegjennomgangen er utilgjengelig. Prøv å laste siden på nytt.",
    "en": "Source review is unavailable. Try reloading the page."
  },
  "Freshwater harbour · Vansjø": {
    "nb": "Ferskvannshavn · Vansjø",
    "en": "Freshwater harbour · Vansjø"
  },
  "No additional operator, capacity or service information could be established for this harbour.": {
    "nb": "Ingen flere opplysninger om operatør, kapasitet eller tjenester kunne fastslås for denne havnen.",
    "en": "No additional operator, capacity or service information could be established for this harbour."
  },
  "Boat-place capacity: not established in this review.": {
    "nb": "Antall båtplasser ble ikke fastslått i denne gjennomgangen.",
    "en": "Boat-place capacity: not established in this review."
  },
  "Current operation and wastewater treatment: not verified. Unlisted services are unknown.": {
    "nb": "Dagens drift og behandling av avløpsvann er ikke verifisert. Tjenester som ikke er oppgitt, er uavklart.",
    "en": "Current operation and wastewater treatment: not verified. Unlisted services are unknown."
  },
  "Earlier dataset capacity": {
    "nb": "Kapasitet i tidligere datasett",
    "en": "Earlier dataset capacity"
  },
  "Historical or undated values. Categories and scopes may differ; do not add these to the figures above.": {
    "nb": "Historiske eller udaterte tall. Kategorier og omfang kan variere; ikke legg dem til tallene over.",
    "en": "Historical or undated values. Categories and scopes may differ; do not add these to the figures above."
  },
  "Operator / association": {
    "nb": "Operatør / forening",
    "en": "Operator / association"
  },
  "Reported boat places": {
    "nb": "Oppgitt antall båtplasser",
    "en": "Reported boat places"
  },
  "Dedicated guest places": {
    "nb": "Egne gjesteplasser",
    "en": "Dedicated guest places"
  },
  "Dinghy places": {
    "nb": "Jolleplasser",
    "en": "Dinghy places"
  },
  "Boat lifting": {
    "nb": "Båtløft",
    "en": "Boat lifting"
  },
  "Launching ramp": {
    "nb": "Utsettingsrampe",
    "en": "Launching ramp"
  },
  "Storage on land": {
    "nb": "Opplag på land",
    "en": "Storage on land"
  },
  "Winter storage on land": {
    "nb": "Vinteropplag på land",
    "en": "Winter storage on land"
  },
  "Operator website": {
    "nb": "Operatørens nettside",
    "en": "Operator website"
  },
  "Property listing": {
    "nb": "Eiendomsannonse",
    "en": "Property listing"
  },
  "Harbour": {
    "nb": "Småbåthavn",
    "en": "Harbour"
  },
  "Possible harbour": {
    "nb": "Mulig småbåthavn",
    "en": "Possible harbour"
  },
  "Pilot (map-based)": {
    "nb": "Pilot (kartbasert)",
    "en": "Pilot (map-based)"
  },
  "Manual, aerial image": {
    "nb": "Manuelt tegnet fra flybilde",
    "en": "Manual, aerial image"
  },
  "Manual, topographic map": {
    "nb": "Manuelt tegnet fra topografisk kart",
    "en": "Manual, topographic map"
  },
  "OSM piers + image review": {
    "nb": "OSM-brygger og bildekontroll",
    "en": "OSM piers + image review"
  },
  "OSM outline + image review": {
    "nb": "OSM-omriss og bildekontroll",
    "en": "OSM outline + image review"
  },
  "Map and sources (pilot)": {
    "nb": "Kart og kilder (pilot)",
    "en": "Map and sources (pilot)"
  },
  "Documented operator + visible berths": {
    "nb": "Dokumentert operatør og synlige båtplasser",
    "en": "Documented operator + visible berths"
  },
  "Documented harbour with permanent berths": {
    "nb": "Dokumentert havn med faste båtplasser",
    "en": "Documented harbour with permanent berths"
  },
  "Documented guest harbour": {
    "nb": "Dokumentert gjestehavn",
    "en": "Documented guest harbour"
  },
  "At least ~10 visible berths in one facility": {
    "nb": "Minst ca. ti synlige plasser i ett anlegg",
    "en": "At least ~10 visible berths in one facility"
  },
  "Several piers; shared use or capacity unclear": {
    "nb": "Flere brygger; felles bruk eller kapasitet uavklart",
    "en": "Several piers; shared use or capacity unclear"
  },
  "Shared berthing area; permanent berths or operation unverified": {
    "nb": "Felles bryggeområde; faste plasser eller drift ikke verifisert",
    "en": "Shared berthing area; permanent berths or operation unverified"
  },
  "Shared jetties; permanent berth count or organisation unclear": {
    "nb": "Fellesbrygger; antall faste plasser eller organisering uklart",
    "en": "Shared jetties; permanent berth count or organisation unclear"
  },
  "Shared visitor jetties; permanent berth count unclear": {
    "nb": "Felles gjestebrygger; antall faste plasser uklart",
    "en": "Shared visitor jetties; permanent berth count unclear"
  },
  "Shared boat jetty; permanent berth count and operator link unclear": {
    "nb": "Felles båtbrygge; antall faste plasser og operatørkobling uklart",
    "en": "Shared boat jetty; permanent berth count and operator link unclear"
  },
  "stats": {
    "nb": "{harbours} havner · {polygons} polygoner · {municipalities} kommuner",
    "en": "{harbours} harbours · {polygons} polygons · {municipalities} municipalities"
  },
  "stats.mobile": {
    "nb": "{harbours} havner · {municipalities} kommuner",
    "en": "{harbours} harbours · {municipalities} municipalities"
  },
  "about.stats": {
    "nb": "{polygons} polygoner ({harbours} havner) fra {municipalities} kommuner",
    "en": "{polygons} polygons ({harbours} harbours) from {municipalities} municipalities"
  },
  "candidates": {
    "nb": "kandidater loggført ({count} kommuner)",
    "en": "candidates logged ({count} municipalities)"
  },
  "stop": {
    "nb": "Stopp {current} av {total}",
    "en": "Stop {current} of {total}"
  },
  "harbour.summary": {
    "nb": "{harbours} havner, {municipalities} kommuner",
    "en": "{harbours} harbours, {municipalities} municipalities"
  },
  "tour.home": {
    "nb": "Tilbake over Oslo. Utforsk de kartlagte havnene rundt fjorden.",
    "en": "Back over Oslo. Explore the mapped harbours around the fjord."
  },
  "tour.filtered": {
    "nb": "Tur med kapasitetsfilter. Publiserte tall og valgfrie arealanslag vises separat i hvert havnekort.",
    "en": "Capacity-filtered tour. Published counts and optional area estimates are shown separately in each harbour card."
  },
  "tour.todo": {
    "nb": "En del av prosjektområdet. Havner her legges til i en senere gjennomgang.",
    "en": "Part of the project scope. Harbours here will be added in a later review."
  },
  "tour.filteredCount": {
    "nb": "{count} havner i kapasitetsfilteret",
    "en": "{count} harbours in capacity filter"
  },
  "parts": {
    "nb": "{count} deler",
    "en": "{count} parts"
  },
  "estimate.row": {
    "nb": "≈{count} plasser",
    "en": "≈{count} berths"
  },
  "estimate.range": {
    "nb": "grovt spenn {low}–{high}",
    "en": "rough range {low}–{high}"
  },
  "estimate.kind": {
    "nb": "Arealanslag",
    "en": "Area estimate"
  },
  "estimate.title": {
    "nb": "Estimert · ikke publisert kapasitet",
    "en": "Estimated · not published capacity"
  },
  "estimate.likely_ge_200": {
    "nb": "Trolig minst 200",
    "en": "Likely at least 200"
  },
  "estimate.likely_lt_200": {
    "nb": "Trolig under 200",
    "en": "Likely fewer than 200"
  },
  "estimate.uncertain": {
    "nb": "Usikkert antall plasser",
    "en": "Uncertain berth count"
  },
  "estimate.basis": {
    "nb": "Beregnet fra hele anleggsgruppens kartlagte sjøareal ({area} m²), også på tvers av kommunegrenser.",
    "en": "Calculated from the entire facility group’s mapped water area ({area} m²), including across municipal boundaries."
  },
  "estimate.outside": {
    "nb": "Arealet ligger utenfor modellens kalibreringsområde. Anslaget er ekstra usikkert.",
    "en": "The area is outside the model’s calibration range. This estimate is especially uncertain."
  },
  "estimate.possible": {
    "nb": "Anlegget er klassifisert som mulig havn; antall faste plasser er uavklart.",
    "en": "The facility is a possible harbour; its number of permanent berths is unresolved."
  },
  "estimate.caveat": {
    "nb": "Veiledende spenn, uten garantert dekning. Landopplag er ikke beregnet.",
    "en": "Indicative range with no guaranteed coverage. Storage ashore is not estimated."
  },
  "filter.show": {
    "nb": "Viser",
    "en": "Showing"
  },
  "filter.selection": {
    "nb": "Filterutvalg:",
    "en": "Filter selection:"
  },
  "filter.published": {
    "nb": "publisert",
    "en": "published"
  },
  "filter.likely": {
    "nb": "trolig fra areal",
    "en": "likely from area"
  },
  "filter.uncertain": {
    "nb": "usikre",
    "en": "uncertain"
  },
  "filter.mobile": {
    "nb": "{count} havner med publisert kapasitet ≥200",
    "en": "{count} harbours with published capacity ≥200"
  },
  "filter.hits": {
    "nb": "{count} kjente treff",
    "en": "{count} known matches"
  },
  "filter.on": {
    "nb": "Slå på kapasitetsfilter",
    "en": "Enable capacity filter"
  },
  "filter.off": {
    "nb": "Slå av kapasitetsfilter",
    "en": "Disable capacity filter"
  },
  "filter.label": {
    "nb": "Vis havner med minst 200 båtplasser",
    "en": "Show harbours with at least 200 berths"
  },
  "model.summary": {
    "nb": "Kalibrert på {harbours} havner i {municipalities} kommuner. Medianavvik {error} % når hele kommuner holdes utenfor. Enkelthavner kan avvike mye mer. Spennet har ingen garantert dekning.",
    "en": "Calibrated on {harbours} harbours in {municipalities} municipalities. Median error {error}% when entire municipalities are held out. Individual harbours may differ much more. The range has no guaranteed coverage."
  },
  "enrichment.review": {
    "nb": "Gjennomgått {date}. Kildeopplysninger som ikke er uavhengig verifisert. Havneomrisset er uendret.",
    "en": "Reviewed {date}. Source-reported information; not independently verified. Harbour outline unchanged."
  },
  "enrichment.earlier": {
    "nb": "Tidligere datasett: {count} oppgitte båtplasser; referanseår ukjent.",
    "en": "Earlier dataset: {count} reported boat places; reference year unknown."
  },
  "enrichment.baseline": {
    "nb": "{count} oppgitte båtplasser · referanseperiode {period}",
    "en": "{count} reported boat places · reference period {period}"
  },
  "language": {
    "nb": "Språk / Language",
    "en": "Language / Språk"
  },
  "title": {
    "nb": "Havner i Oslofjorden",
    "en": "Oslofjord Harbours"
  },
  "description": {
    "nb": "Utforsk småbåthavnene i Oslofjorden i 3D: 816 polygoner fra 23 kommuner.",
    "en": "Explore the mapped small-boat harbours of the Oslofjord in 3D: 816 polygons from 23 municipalities."
  },
  "text.269": {
    "nb": "Miljøkort",
    "en": "Environmental card"
  },
  "text.270": {
    "nb": "Lukk miljøkort",
    "en": "Close environmental card"
  },
  "text.271": {
    "nb": "Laster miljøkort…",
    "en": "Loading environmental cards…"
  },
  "text.272": {
    "nb": "Miljøkortene kunne ikke lastes. Last siden på nytt for å prøve igjen. Havnekartet kan fortsatt brukes.",
    "en": "Environmental cards could not be loaded. Reload to try again. The harbour map remains available."
  },
  "text.273": {
    "nb": "Stedspunkter, ikke miljøvurdering av hele havnen.",
    "en": "Location markers, not an environmental assessment of the entire harbour."
  },
  "text.274": {
    "nb": "Gjelder et bestemt anlegg eller en tjeneste i området; se kortets omfang.",
    "en": "Applies to a specific facility or service in the area; see the card’s scope."
  },
  "text.275": {
    "nb": "Kildeopplysninger · kontrollert",
    "en": "Source-reported information · checked"
  },
  "text.276": {
    "nb": "Neste avklaring",
    "en": "Next question"
  },
  "text.277": {
    "nb": "Kilder og grunnlag",
    "en": "Sources and evidence"
  },
  "text.278": {
    "nb": "Ingen befaring eller direkte operatørbekreftelse. Ukjent betyr ikke at tiltak mangler. Ingen målt økologisk effekt er dokumentert.",
    "en": "No site visit or direct operator confirmation. Unknown does not mean measures are absent. No measured ecological effect has been documented."
  },
  "text.279": {
    "nb": "Regelverk",
    "en": "Regulatory context"
  },
  "text.280": {
    "nb": "Forskriftsforslag under revisjon. Om anlegget omfattes, og om krav oppfylles, er ikke vurdert.",
    "en": "The proposed regulation is under revision. Applicability to this facility and compliance have not been assessed."
  },
  "text.281": {
    "nb": "Plassering og omfang",
    "en": "Location and scope"
  },
  "text.282": {
    "nb": "Omfang:",
    "en": "Scope:"
  },
  "text.283": {
    "nb": "Dokumentasjonshull:",
    "en": "Evidence gap:"
  },
  "text.284": {
    "nb": "Neste steg:",
    "en": "Next step:"
  },
  "text.285": {
    "nb": "Finn avsnitt:",
    "en": "Find section:"
  },
  "text.286": {
    "nb": "Delte tjenester",
    "en": "Shared services"
  },
  "text.287": {
    "nb": "Kilder",
    "en": "Sources"
  },
  "text.288": {
    "nb": "Dokumentdato:",
    "en": "Document date:"
  },
  "text.289": {
    "nb": "Hentet:",
    "en": "Retrieved:"
  },
  "text.290": {
    "nb": "Ingen henvendelse er sendt.",
    "en": "No enquiry has been sent."
  },
  "text.291": {
    "nb": "Kildetitler, avsnittsnavn og opprinnelige kartleggingsnotater beholdes på originalspråket.",
    "en": "Source titles, section names and original mapping notes retain their original language."
  },
  "text.292": {
    "nb": "Opplyst etablert",
    "en": "Reported installed"
  },
  "text.293": {
    "nb": "Rutine publisert",
    "en": "Procedure published"
  },
  "text.294": {
    "nb": "Ukjent i gjennomgåtte kilder",
    "en": "Unknown in reviewed sources"
  },
  "text.295": {
    "nb": "Påstand uten målerapport",
    "en": "Claim without measurement report"
  },
  "text.296": {
    "nb": "Kildeavvik",
    "en": "Conflicting sources"
  },
  "text.297": {
    "nb": "Under etablering, ifølge operatør",
    "en": "Being established, according to the operator"
  },
  "text.298": {
    "nb": "Tilgang opplyst",
    "en": "Access reported"
  },
  "text.299": {
    "nb": "Spylevann",
    "en": "Wash water"
  },
  "text.300": {
    "nb": "Båtpuss",
    "en": "Boat maintenance"
  },
  "text.301": {
    "nb": "Arbeidsavfall",
    "en": "Maintenance waste"
  },
  "text.302": {
    "nb": "Slipestøv",
    "en": "Sanding dust"
  },
  "text.303": {
    "nb": "Farlig avfall",
    "en": "Hazardous waste"
  },
  "text.304": {
    "nb": "Renseeffekt og naturtilstand",
    "en": "Treatment performance and ecological condition"
  },
  "text.305": {
    "nb": "Renseeffekt",
    "en": "Treatment performance"
  },
  "text.306": {
    "nb": "Tidslinje",
    "en": "Timeline"
  },
  "text.307": {
    "nb": "Oppsamling og felles rensing opplyst etablert.",
    "en": "Collection and shared treatment reported installed."
  },
  "text.308": {
    "nb": "Rutine for støvoppsamling publisert.",
    "en": "Dust-collection procedure published."
  },
  "text.309": {
    "nb": "Levering med kvittering/deklarasjon beskrevet.",
    "en": "Waste delivery with receipt/declaration described."
  },
  "text.310": {
    "nb": "Bekreft drift i 2026 og innhent renseprøver.",
    "en": "Confirm operation in 2026 and obtain treatment test results."
  },
  "text.311": {
    "nb": "Oppsamling og mobil rensing opplyst etablert.",
    "en": "Collection and mobile treatment reported installed."
  },
  "text.312": {
    "nb": "Støvoppsamling er ikke avklart.",
    "en": "Dust collection is unresolved."
  },
  "text.313": {
    "nb": "Leveringsordning er ikke avklart.",
    "en": "Waste-delivery arrangements are unresolved."
  },
  "text.314": {
    "nb": "Avklar oppstartsdato og innhent prøverapport.",
    "en": "Clarify the start-up date and obtain the test report."
  },
  "text.315": {
    "nb": "Under etablering ifølge foreningen.",
    "en": "Being established, according to the association."
  },
  "text.316": {
    "nb": "Miljøcontainer og deklarert levering oppgitt.",
    "en": "Waste container and declared waste delivery reported."
  },
  "text.317": {
    "nb": "Er spyleplassen på Østslippen satt i drift?",
    "en": "Is the wash-down area at Østslippen in operation?"
  },
  "text.318": {
    "nb": "Sandfang og filterrensing opplyst etablert.",
    "en": "Sediment trap and filtration reported installed."
  },
  "text.319": {
    "nb": "Oppsamling av bunnstoff beskrevet.",
    "en": "Collection of antifouling residues described."
  },
  "text.320": {
    "nb": "Levering av bunnstoffrester beskrevet.",
    "en": "Delivery of antifouling residues described."
  },
  "text.321": {
    "nb": "Bekreft dagens drift og innhent renseprøver.",
    "en": "Confirm current operation and obtain treatment test results."
  },
  "text.322": {
    "nb": "Vaskestasjon med rensing opplyst etablert.",
    "en": "Wash station with treatment reported installed."
  },
  "text.323": {
    "nb": "Avfallsavtale oppgitt; renseavfall uavklart.",
    "en": "Waste agreement reported; treatment waste is unresolved."
  },
  "text.324": {
    "nb": "Avklar dagens renseløsning og innhent prøverapport.",
    "en": "Clarify the current treatment system and obtain the test report."
  },
  "text.325": {
    "nb": "Renseanlegg opplyst ferdigstilt i 2023.",
    "en": "Treatment plant reportedly completed in 2023."
  },
  "text.326": {
    "nb": "Flytende avfall håndteres; fast avfall er brukeransvar.",
    "en": "Liquid waste is handled; solid waste is the user’s responsibility."
  },
  "text.327": {
    "nb": "Bekreft dagens drift, vedlikehold og renseprøver.",
    "en": "Confirm current operation, maintenance and treatment test results."
  },
  "text.328": {
    "nb": "Kartverkets navnepunkt på øya. Tilknyttet nærliggende kartgruppe 0301-H13 som geografisk kontekst; det generiske gruppenavnet er ikke endret. Punktet angir ikke spyleplass.",
    "en": "Kartverket’s place-name point on the island. Linked to nearby mapped group 0301-H13 for geographic context; the generic group name is unchanged. The marker does not locate the wash-down area."
  },
  "text.329": {
    "nb": "Publisert besøksadresse, kontrollert mot Kartverkets adressepunkt. Dette er et landpunkt, ikke nøyaktig plassering av spyleplass. Sjølyst-gruppen er geografisk kontekst; brukere og ansvarsgrenser er ikke kartlagt. Kartverket oppgir stedfestingverifisert=false.",
    "en": "Published visiting address checked against Kartverket’s address point. This is a land location, not the exact wash-down area. The Sjølyst group provides geographic context; users and responsibility boundaries have not been mapped. Kartverket marks the geolocation as unverified."
  },
  "text.330": {
    "nb": "Foreningens publiserte posisjon; lengdegrad oppgitt med hele minutter og derfor grov. Hovedøya-gruppen omfatter flere foreninger. Kortet gjelder Revierhavnen, ikke hele kartgruppen. Østslippen er ikke presist stedfestet.",
    "en": "The association’s published position; longitude is given in whole minutes and is therefore approximate. The Hovedøya group includes several associations. This card concerns Revierhavnen, not the entire mapped group. Østslippen has not been precisely located."
  },
  "text.331": {
    "nb": "Publisert besøksadresse Kolåsveien 30 kontrollert mot Kartverkets adressepunkt. Punktet viser ikke nøyaktig spyleplass. Kartgruppen 3216-H02 omfatter flere aktører; kortet gjelder Sonskilen, ikke alle brygger i gruppen.",
    "en": "Published visiting address Kolåsveien 30 checked against Kartverket’s address point. The marker does not show the exact wash-down area. Mapped group 3216-H02 includes several operators; the card concerns Sonskilen, not every jetty in the group."
  },
  "text.332": {
    "nb": "Operatørens besøksadresse Ullerøyveien 338 kontrollert mot Kartverkets adressepunkt. Sjøpolygonene 3105-H33 gir geografisk kontekst. Punktet viser ikke eksakt vaskestasjon, septikmottak eller driftsgrenser.",
    "en": "The operator’s visiting address Ullerøyveien 338 checked against Kartverket’s address point. Water polygons 3105-H33 provide geographic context. The marker does not precisely locate the wash station, sewage reception or operating boundaries."
  },
  "text.333": {
    "nb": "Kartpunktet viser registrert forretningsadresse Grønsundveien 16, kontrollert mot Kartverket. En registeradresse er ikke bevis for havneposisjon. Ingen sikker kobling til godkjent sjøpolygon er etablert; punktet angir ikke renseanlegg eller spyleplass.",
    "en": "The marker shows the registered business address Grønsundveien 16, checked against Kartverket. A registered address does not establish the harbour’s location. No reliable link to an approved water polygon has been established; the marker does not locate a treatment plant or wash-down area."
  },
  "text.334": {
    "nb": "Kapasitet på sjøen; opplag på land er separat.",
    "en": "Capacity afloat; storage on land is separate."
  },
  "text.335": {
    "nb": "Kapasitet for hele fellesanlegget. Oppgitt i en eiendomsannonse, ikke verifisert med operatør.",
    "en": "Capacity for the whole shared facility. Reported in a property listing, not verified with the operator."
  },
  "text.336": {
    "nb": "Kapasitet på land, ikke båtplasser på sjøen. Kilden oppgir ikke nøyaktighet.",
    "en": "Capacity on land, not boat places afloat. Precision is not specified by the source."
  },
  "text.337": {
    "nb": "Barnejolleplasser; holdes separat fra vanlige båtplasser.",
    "en": "Children’s dinghy places; kept separate from ordinary places."
  },
  "text.338": {
    "nb": "Egne gjesteplasser, holdt separat fra andre tall.",
    "en": "Dedicated guest places, kept separate from other counts."
  },
  "text.339": {
    "nb": "Gjesteplasser oppgis separat; tallene summeres ikke.",
    "en": "Guest places are reported separately; counts are not added."
  },
  "text.340": {
    "nb": "Gjester bruker ledige medlemsplasser; ikke ekstra kapasitet.",
    "en": "Guests use available member places; not additional capacity."
  },
  "text.341": {
    "nb": "Historiske innlegg fra 2010–2011; dagens drift er ikke verifisert.",
    "en": "Historical website posts from 2010–2011; current operation is not verified."
  },
  "text.342": {
    "nb": "Identitet oppgitt i en eiendomsannonse; ikke direkte bekreftet med operatør.",
    "en": "Identity reported in a property listing; not confirmed directly with the operator."
  },
  "text.343": {
    "nb": "Vanlige båtplasser; jolleplasser er separate.",
    "en": "Ordinary places; dinghy places are separate."
  },
  "text.344": {
    "nb": "Publisert operatøridentitet; driftsgrensene er ikke kartlagt.",
    "en": "Published operator identity; operating boundaries have not been surveyed."
  },
  "text.345": {
    "nb": "Tjenestelenke på operatørens nettside; kapasitet og landareal er ikke dokumentert.",
    "en": "Service link on the operator website; capacity and land area are not documented."
  },
  "text.346": {
    "nb": "Flere operatører deler denne havnegruppen; interne grenser er uavklart.",
    "en": "Several operators share this harbour group; internal boundaries are unresolved."
  },
  "text.347": {
    "nb": "Felles rampe i bukten; plasseringen er ikke kartlagt separat.",
    "en": "Shared ramp in the bay; its location has not been mapped separately."
  },
  "text.348": {
    "nb": "Det oppgis ikke om gjesteplasser inngår.",
    "en": "Whether guest places are included is not specified."
  },
  "environment.MK-01-01.claim": {
    "nb": "Foreningen beskriver oppsamling via sandfang/pumpekum og tankflåte, med transport til felles rensing på Hovedøya.",
    "en": "The association describes collection through a sediment trap/pump chamber and tank barge, with transport to shared treatment on Hovedøya."
  },
  "environment.MK-01-01.scope": {
    "nb": "Oppsamling på Lille Herbern; rensing på Hovedøya.",
    "en": "Collection at Lille Herbern; treatment on Hovedøya."
  },
  "environment.MK-01-01.missing_evidence": {
    "nb": "Driftsbekreftelse for 2026, mengder, kapasitet og behandlingskvitteringer.",
    "en": "Confirmation of operation in 2026, volumes, capacity and treatment receipts."
  },
  "environment.MK-01-01.next_action": {
    "nb": "Be operatøren om siste driftslogg og dokumentasjon fra mottak/rensing.",
    "en": "Ask the operator for the latest operating log and reception/treatment documentation."
  },
  "environment.MK-01-02.claim": {
    "nb": "Plastunderlag eller støvsuging foreskrives; rester leveres til miljøstasjonen.",
    "en": "Plastic sheeting or vacuum collection is prescribed; residues are delivered to the waste station."
  },
  "environment.MK-01-02.scope": {
    "nb": "Båtpuss på land.",
    "en": "Boat maintenance ashore."
  },
  "environment.MK-01-02.missing_evidence": {
    "nb": "Etterlevelse og hvor mye som faktisk fanges opp.",
    "en": "Compliance and the quantity actually collected."
  },
  "environment.MK-01-02.next_action": {
    "nb": "Kontroller rutine og gjennomføring ved neste vedlikeholdssesong.",
    "en": "Check the procedure and its implementation during the next maintenance season."
  },
  "environment.MK-01-03.claim": {
    "nb": "Miljøstasjon og levering med kvittering/deklarasjon beskrives.",
    "en": "A waste station and delivery with receipts/declarations are described."
  },
  "environment.MK-01-03.scope": {
    "nb": "Miljøstasjon og levering fra Lille Herbern.",
    "en": "Waste station and delivery from Lille Herbern."
  },
  "environment.MK-01-03.missing_evidence": {
    "nb": "Nyeste leveringsbilag og mengder; offentlig plan viser også eldre innsendingsdato.",
    "en": "Latest delivery records and volumes; the public plan also shows an older submission date."
  },
  "environment.MK-01-03.next_action": {
    "nb": "Be om siste deklarasjoner og avklar planens revisjons-/godkjenningshistorikk.",
    "en": "Request the latest declarations and clarify the plan’s revision/approval history."
  },
  "environment.MK-01-04.claim": {
    "nb": "Ingen anleggsspesifikke analyser eller naturmålinger funnet i gjennomgått kilde.",
    "en": "No facility-specific analyses or ecological measurements were found in the reviewed source."
  },
  "environment.MK-01-04.scope": {
    "nb": "Ingen effekt overføres fra renseprodukt til havn.",
    "en": "No treatment-product performance is attributed to the harbour."
  },
  "environment.MK-01-04.missing_evidence": {
    "nb": "Innløps-/utløpsprøver, vannmengder og separat naturundersøkelse.",
    "en": "Inlet/outlet samples, water volumes and a separate ecological survey."
  },
  "environment.MK-01-04.next_action": {
    "nb": "Innhent prøver med metode, dato og driftsforhold; vurder behov for naturfaglig oppfølging.",
    "en": "Obtain samples with methods, dates and operating conditions; assess the need for ecological follow-up."
  },
  "environment.MK-02-01.claim": {
    "nb": "Leverandøren beskriver tett oppsamling til tank og mobil rensing på stedet.",
    "en": "The supplier describes contained collection into a tank and mobile treatment on site."
  },
  "environment.MK-02-01.scope": {
    "nb": "Spyleplass ved Karenslyst; ikke alle havne- eller opplagsarealer.",
    "en": "The wash-down area at Karenslyst; not all harbour or storage areas."
  },
  "environment.MK-02-01.missing_evidence": {
    "nb": "Oppdatert drift, dekningsgrad og driftsavvik.",
    "en": "Current operation, coverage and operational deviations."
  },
  "environment.MK-02-01.next_action": {
    "nb": "Be operatøren om driftslogg og tegning av området som samles opp.",
    "en": "Ask the operator for an operating log and a drawing of the collection area."
  },
  "environment.MK-02-02.claim": {
    "nb": "Presseomtalen gjengir høy rensegrad, men tilgjengelig omtale inneholder ikke prøveresultater for anlegget.",
    "en": "Press coverage reports high removal rates, but the available coverage contains no test results for the facility."
  },
  "environment.MK-02-02.scope": {
    "nb": "Produkt-/pressepåstand er ikke målt lokal effekt.",
    "en": "A product/press claim is not a measured local effect."
  },
  "environment.MK-02-02.missing_evidence": {
    "nb": "Analyser, prøvetakingsmetode, vannmengder og driftsbetingelser.",
    "en": "Analyses, sampling methods, water volumes and operating conditions."
  },
  "environment.MK-02-02.next_action": {
    "nb": "Be Bymiljøetaten/operatør om rapportene fra omtalt prøvetaking.",
    "en": "Ask the City Environment Agency/operator for the reports from the sampling mentioned."
  },
  "environment.MK-02-03.claim": {
    "nb": "Leverandøren omtaler åpning i oktober 2025; presseomtalen oppgir en åpning i juni 2026.",
    "en": "The supplier reports an opening in October 2025; press coverage gives an opening in June 2026."
  },
  "environment.MK-02-03.scope": {
    "nb": "Datoene beholdes hver for seg.",
    "en": "The dates are retained separately."
  },
  "environment.MK-02-03.missing_evidence": {
    "nb": "Om dette er ulike trinn, ny åpning eller feil i omtalen.",
    "en": "Whether these refer to different stages, a reopening or an error in the coverage."
  },
  "environment.MK-02-03.next_action": {
    "nb": "Be operatøren avklare idriftsettelse og senere oppgraderinger.",
    "en": "Ask the operator to clarify commissioning and subsequent upgrades."
  },
  "environment.MK-02-04.claim": {
    "nb": "Spylevannsomtalen gir ikke et fullstendig bilde av støvoppsamling, avfallsleveranser eller naturtilstand.",
    "en": "The wash-water coverage does not give a complete picture of dust collection, waste deliveries or ecological condition."
  },
  "environment.MK-02-04.scope": {
    "nb": "Ikke en konklusjon om at tiltak mangler.",
    "en": "This is not a finding that measures are absent."
  },
  "environment.MK-02-04.missing_evidence": {
    "nb": "Rutiner og leveringsbilag samt eventuell miljøovervåking.",
    "en": "Procedures and delivery records, plus any environmental monitoring."
  },
  "environment.MK-02-04.next_action": {
    "nb": "Innhent miljø-/avfallsplan og siste leveringsbilag.",
    "en": "Obtain the environmental/waste plan and latest delivery records."
  },
  "environment.MK-03-01.claim": {
    "nb": "Foreningen beskriver en mobil oppsamlings-/renseløsning med Østslippen som første etablering høsten 2026.",
    "en": "The association describes a mobile collection/treatment system, with Østslippen as its first installation in autumn 2026."
  },
  "environment.MK-03-01.scope": {
    "nb": "Østslippen; ikke automatisk hele havnen.",
    "en": "Østslippen; not automatically the entire harbour."
  },
  "environment.MK-03-01.missing_evidence": {
    "nb": "Bekreftet ferdigstillelse og faktisk drift.",
    "en": "Confirmed completion and actual operation."
  },
  "environment.MK-03-01.next_action": {
    "nb": "Be om datert idriftsettelsesbekreftelse og første driftslogg.",
    "en": "Request dated commissioning confirmation and the first operating log."
  },
  "environment.MK-03-02.claim": {
    "nb": "Foreningen beskriver miljøcontainer og sortert, deklarert levering.",
    "en": "The association describes a waste container and sorted, declared waste delivery."
  },
  "environment.MK-03-02.scope": {
    "nb": "Foreningens miljøcontainer.",
    "en": "The association’s waste container."
  },
  "environment.MK-03-02.missing_evidence": {
    "nb": "Aktuelle bilag og mengder.",
    "en": "Current records and quantities."
  },
  "environment.MK-03-02.next_action": {
    "nb": "Be om siste leveringsbekreftelser og avfallsplan.",
    "en": "Request the latest delivery confirmations and waste plan."
  },
  "environment.MK-03-03.claim": {
    "nb": "Miljøgruppe og øremerket miljøavgift beskrives.",
    "en": "An environmental group and earmarked environmental fee are described."
  },
  "environment.MK-03-03.scope": {
    "nb": "Organisering er ikke dokumentasjon av miljøeffekt.",
    "en": "Organisational arrangements do not document environmental effects."
  },
  "environment.MK-03-03.missing_evidence": {
    "nb": "Gjeldende tiltaksplan, ansvar og fremdrift.",
    "en": "Current action plan, responsibilities and progress."
  },
  "environment.MK-03-03.next_action": {
    "nb": "Be om årets tiltaksplan med ansvarlig funksjon.",
    "en": "Request this year’s action plan with the responsible role identified."
  },
  "environment.MK-03-04.claim": {
    "nb": "Foreningen viser til kommunalt tømmepunkt i bukta og mobil tjeneste.",
    "en": "The association refers to a municipal sewage reception point in the bay and a mobile service."
  },
  "environment.MK-03-04.scope": {
    "nb": "Tilgang i nærområdet, ikke eget anlegg bekreftet.",
    "en": "Access nearby; an association-owned facility is not confirmed."
  },
  "environment.MK-03-04.missing_evidence": {
    "nb": "Eksakt mottakssted, eier, tilgjengelighet og driftsstatus.",
    "en": "Exact reception location, owner, availability and operating status."
  },
  "environment.MK-03-04.next_action": {
    "nb": "Kontroller hos kommunen; registrer mottaket som separat tjeneste.",
    "en": "Check with the municipality; register the reception point as a separate service."
  },
  "environment.MK-03-05.claim": {
    "nb": "Gjennomgått side inneholder ikke måleresultater for renseeffekt eller lokal naturtilstand.",
    "en": "The reviewed page contains no measurements of treatment performance or local ecological condition."
  },
  "environment.MK-03-05.scope": {
    "nb": "Ingen effekt beregnet.",
    "en": "No effect has been calculated."
  },
  "environment.MK-03-05.missing_evidence": {
    "nb": "Prøveopplegg og eventuelle naturmålinger.",
    "en": "Sampling design and any ecological measurements."
  },
  "environment.MK-03-05.next_action": {
    "nb": "Avklar prøvetaking etter idriftsettelse og behov for naturfaglig oppfølging.",
    "en": "Clarify post-commissioning sampling and the need for ecological follow-up."
  },
  "environment.MK-04-01.claim": {
    "nb": "Operatøren beskriver en spyleplass med sandfang og filter, samt levering av oppsamlet avfall.",
    "en": "The operator describes a wash-down area with a sediment trap and filter, plus delivery of collected waste."
  },
  "environment.MK-04-01.scope": {
    "nb": "Sonskilens spyleplass; ikke hele Son havn.",
    "en": "Sonskilen’s wash-down area; not the whole of Son harbour."
  },
  "environment.MK-04-01.missing_evidence": {
    "nb": "Datert driftsbekreftelse, dekningsgrad og vedlikeholdslogg.",
    "en": "Dated confirmation of operation, coverage and maintenance log."
  },
  "environment.MK-04-01.next_action": {
    "nb": "Be om siste drifts- og vedlikeholdslogg.",
    "en": "Request the latest operating and maintenance logs."
  },
  "environment.MK-04-02.claim": {
    "nb": "Underlag og oppsamling ved skraping beskrives; sand- og tørrisblåsing tillates ikke.",
    "en": "Protective sheeting and collection during scraping are described; sandblasting and dry-ice blasting are prohibited."
  },
  "environment.MK-04-02.scope": {
    "nb": "Bunnstoffarbeid hos Sonskilen.",
    "en": "Antifouling work at Sonskilen."
  },
  "environment.MK-04-02.missing_evidence": {
    "nb": "Etterlevelse i praksis.",
    "en": "Compliance in practice."
  },
  "environment.MK-04-02.next_action": {
    "nb": "Kontroller gjennomføring ved vedlikehold.",
    "en": "Check implementation during maintenance."
  },
  "environment.MK-04-03.claim": {
    "nb": "Mottak for utvalgte avfallstyper og levering av bunnstoffrester til avfallsmottaker beskrives.",
    "en": "Reception of selected waste types and delivery of antifouling residues to a waste receiver are described."
  },
  "environment.MK-04-03.scope": {
    "nb": "Utvalgte avfallstyper; siden henviser andre fraksjoner til eksternt mottak.",
    "en": "Selected waste types; the page directs other fractions to external reception."
  },
  "environment.MK-04-03.missing_evidence": {
    "nb": "Nyeste deklarasjoner og mottaksbilag.",
    "en": "Latest declarations and reception records."
  },
  "environment.MK-04-03.next_action": {
    "nb": "Be om avfallsplan og leveringsbilag.",
    "en": "Request the waste plan and delivery records."
  },
  "environment.MK-04-04.claim": {
    "nb": "Ingen lokal målerapport eller naturundersøkelse følger miljøbeskrivelsen.",
    "en": "The environmental description includes no local measurement report or ecological survey."
  },
  "environment.MK-04-04.scope": {
    "nb": "Ingen utslippsreduksjon eller økologisk effekt er beregnet.",
    "en": "No emission reduction or ecological effect has been calculated."
  },
  "environment.MK-04-04.missing_evidence": {
    "nb": "Prøver med dato, metode og vannmengder.",
    "en": "Samples with dates, methods and water volumes."
  },
  "environment.MK-04-04.next_action": {
    "nb": "Innhent representative prøver før og etter rensing.",
    "en": "Obtain representative samples before and after treatment."
  },
  "environment.MK-05-01.claim": {
    "nb": "Operatøren omtaler vaskestasjon med rensing av vann og spyleavfall.",
    "en": "The operator describes a wash station treating water and wash-down waste."
  },
  "environment.MK-05-01.scope": {
    "nb": "Marinaens vaskestasjon; påstanden om å være først er ikke kontrollert.",
    "en": "The marina’s wash station; its claim to be the first has not been checked."
  },
  "environment.MK-05-01.missing_evidence": {
    "nb": "Teknisk løsning, idriftsettelse og aktuell drift.",
    "en": "Technical system, commissioning and current operation."
  },
  "environment.MK-05-01.next_action": {
    "nb": "Be om anleggsbeskrivelse og datert driftslogg.",
    "en": "Request a system description and dated operating log."
  },
  "environment.MK-05-02.claim": {
    "nb": "Miljøcontainere og samarbeid med Norsk Gjenvinning omtales.",
    "en": "Waste containers and cooperation with Norsk Gjenvinning are described."
  },
  "environment.MK-05-02.scope": {
    "nb": "Marinaens avfallsordning.",
    "en": "The marina’s waste arrangements."
  },
  "environment.MK-05-02.missing_evidence": {
    "nb": "Avfallsplan og siste leveringsbilag.",
    "en": "Waste plan and latest delivery records."
  },
  "environment.MK-05-02.next_action": {
    "nb": "Innhent dokumentasjon av levering og avfallstyper.",
    "en": "Obtain documentation of deliveries and waste types."
  },
  "environment.MK-05-03.claim": {
    "nb": "Operatøren oppgir eget tømmesystem for fritidsbåt og bobil.",
    "en": "The operator reports a dedicated sewage disposal system for leisure boats and motorhomes."
  },
  "environment.MK-05-03.scope": {
    "nb": "Tjenestetilbud; ikke tilgjengelighetsbekreftelse for dagens dato.",
    "en": "An advertised service; not confirmation of availability today."
  },
  "environment.MK-05-03.missing_evidence": {
    "nb": "Eksakt punkt, tilgjengelighet og aktuell driftsstatus.",
    "en": "Exact location, availability and current operating status."
  },
  "environment.MK-05-03.next_action": {
    "nb": "Kontroller mottakssted og drift med operatøren.",
    "en": "Check the reception location and operation with the operator."
  },
  "environment.MK-05-04.claim": {
    "nb": "Omtalen av full rensing ledsages ikke av målerapporter.",
    "en": "The description of complete treatment is not accompanied by measurement reports."
  },
  "environment.MK-05-04.scope": {
    "nb": "Full rensing er en operatørpåstand, ikke et verifisert måleresultat.",
    "en": "Complete treatment is an operator claim, not a verified measurement."
  },
  "environment.MK-05-04.missing_evidence": {
    "nb": "Representative analyser og eventuelle naturmålinger.",
    "en": "Representative analyses and any ecological measurements."
  },
  "environment.MK-05-04.next_action": {
    "nb": "Innhent renseprøver med metode, dato og driftsbetingelser.",
    "en": "Obtain treatment samples with methods, dates and operating conditions."
  },
  "environment.MK-06-01.claim": {
    "nb": "Datert melding fra juni 2023 beskriver ferdigstilt spyle- og renseanlegg med bilder av første båtvask.",
    "en": "A dated announcement from June 2023 describes a completed wash-down and treatment facility, with photographs of the first boat wash."
  },
  "environment.MK-06-01.scope": {
    "nb": "Foreningens eget anlegg; historisk ferdigmelding.",
    "en": "The association’s own facility; a historical completion announcement."
  },
  "environment.MK-06-01.missing_evidence": {
    "nb": "Bekreftelse på drift i 2026 og vedlikehold.",
    "en": "Confirmation of operation in 2026 and maintenance."
  },
  "environment.MK-06-01.next_action": {
    "nb": "Be om aktuell driftsstatus og vedlikeholdslogg.",
    "en": "Request current operating status and the maintenance log."
  },
  "environment.MK-06-02.claim": {
    "nb": "Foreningen oppgir håndtering av flytende miljøfarlige stoffer; fast miljøfarlig avfall er den enkelte brukers ansvar.",
    "en": "The association reports handling liquid environmentally hazardous substances; each user is responsible for solid hazardous waste."
  },
  "environment.MK-06-02.scope": {
    "nb": "Ikke et bekreftet mottak for alle typer farlig avfall.",
    "en": "Reception of all hazardous-waste types is not confirmed."
  },
  "environment.MK-06-02.missing_evidence": {
    "nb": "Hvilke væsker tas imot og hvor fast avfall skal leveres.",
    "en": "Which liquids are accepted and where solid waste must be delivered."
  },
  "environment.MK-06-02.next_action": {
    "nb": "Avklar avfallstyper og leveringsordning.",
    "en": "Clarify waste types and delivery arrangements."
  },
  "environment.MK-06-03.claim": {
    "nb": "Foreningen oppgir rensing før utslipp, men publiserer ingen analyser i de gjennomgåtte kildene.",
    "en": "The association reports treatment before discharge, but publishes no analyses in the reviewed sources."
  },
  "environment.MK-06-03.scope": {
    "nb": "Ingen renseprosent er overført fra produkt eller presseomtale.",
    "en": "No treatment percentage has been taken from product information or press coverage."
  },
  "environment.MK-06-03.missing_evidence": {
    "nb": "Prøver og vannmengder for anlegget.",
    "en": "Samples and water volumes for the facility."
  },
  "environment.MK-06-03.next_action": {
    "nb": "Innhent representative renseprøver og opplysninger om filtervedlikehold.",
    "en": "Obtain representative treatment samples and information on filter maintenance."
  },
  "environment.MK-06-04.claim": {
    "nb": "Ingen målt endring i naturtilstand er dokumentert i sidene som er gjennomgått.",
    "en": "No measured change in ecological condition is documented in the reviewed pages."
  },
  "environment.MK-06-04.scope": {
    "nb": "Etablert utstyr dokumenterer ikke økologisk effekt.",
    "en": "Installed equipment does not document ecological effects."
  },
  "environment.MK-06-04.missing_evidence": {
    "nb": "Eventuelle lokale miljøundersøkelser.",
    "en": "Any local environmental surveys."
  },
  "environment.MK-06-04.next_action": {
    "nb": "Avklar om det foreligger naturfaglig oppfølging.",
    "en": "Clarify whether ecological follow-up exists."
  },
  "extra.449": {
    "nb": "Naturtilstand",
    "en": "Ecological condition"
  },
  "extra.450": {
    "nb": "Organisering",
    "en": "Organisation"
  },
  "extra.451": {
    "nb": "Septik",
    "en": "Sewage"
  },
  "extra.452": {
    "nb": "Slipestøv, avfall og naturtilstand",
    "en": "Sanding dust, waste and ecological condition"
  },
  "extra.453": {
    "nb": "leverandør",
    "en": "supplier"
  },
  "extra.454": {
    "nb": "operatør",
    "en": "operator"
  },
  "extra.455": {
    "nb": "presse; bygger på pressemelding fra foreningen",
    "en": "press; based on the association’s press release"
  },
  "extra.456": {
    "nb": "registeradresse_ikke_havnegrense",
    "en": "registered address, not a harbour boundary"
  },
  "extra.457": {
    "nb": "stedfestingskilde",
    "en": "location source"
  },
  "extra.458": {
    "nb": "Axon-anlegg på Hovedøya",
    "en": "Axon facility on Hovedøya"
  },
  "extra.459": {
    "nb": "opplyst av operatør",
    "en": "reported by operator"
  },
  "extra.460": {
    "nb": "opplyst av leverandør",
    "en": "reported by supplier"
  },
  "extra.461": {
    "nb": "Samarbeid med Arbeidernes båtforening. Ikke likestilt med Revierhavnens eget tiltak.",
    "en": "Cooperation with Arbeidernes båtforening. This is distinct from Revierhavnen’s own measure."
  },
  "Harbours:": {
    "nb": "Havner:",
    "en": "Harbours:"
  },
  "by": {
    "nb": "av",
    "en": "by"
  },
  "Toggle attribution": {
    "nb": "Vis eller skjul kildehenvisninger",
    "en": "Toggle attribution"
  },
  "Powered by the": {
    "nb": "Drevet av",
    "en": "Powered by the"
  },
  "og.title": {
    "nb": "Havner i Oslofjorden – flytur i 3D",
    "en": "Oslofjord Harbours – 3D flyover"
  },
  "environment.menu": {
    "nb": "Miljøkort",
    "en": "Environmental cards"
  }
};

  let language = 'nb';
  try { if (root.localStorage?.getItem('oslofjord-language') === 'en') language = 'en'; } catch {}
  const bySource = new Map();
  for (const [key, entry] of Object.entries(messages)) { bySource.set(entry.nb, key); bySource.set(entry.en, key); }
  function t(key, values = {}) {
    const template = messages[key]?.[language] ?? key;
    return template.replace(/\{(\w+)\}/g, (match, name) => values[name] == null ? match : String(values[name]));
  }
  function text(source) { return t(bySource.get(source) ?? source); }
  function apply() {
    if (!root.document) return;
    root.document.documentElement.lang = language;
    root.document.title = t('title');
    const description = root.document.querySelector('meta[name="description"]');
    if (description) description.content = t('description');
    for (const element of root.document.querySelectorAll('[data-i18n]')) element.textContent = t(element.dataset.i18n);
    for (const attribute of ['aria-label', 'title', 'placeholder', 'content', 'href']) {
      for (const element of root.document.querySelectorAll(`[data-i18n-${attribute}]`)) element.setAttribute(attribute, t(element.getAttribute(`data-i18n-${attribute}`)));
    }
    const selector = root.document.getElementById('language');
    if (selector) { selector.value = language; selector.onchange = () => setLanguage(selector.value); }
  }
  function setLanguage(value) {
    if (!['nb', 'en'].includes(value)) return;
    language = value;
    try { root.localStorage?.setItem('oslofjord-language', value); } catch {}
    apply();
    root.dispatchEvent?.(new Event('site-language-change'));
  }
  root.I18n = {t, text, apply, setLanguage, messages, get language() { return language; },
    number: value => Number(value).toLocaleString(language === 'nb' ? 'nb-NO' : 'en-GB')};
  if (root.document) {
    root.document.documentElement.lang = language;
    if (root.document.readyState === 'loading') root.document.addEventListener('DOMContentLoaded', apply, {once:true});
    else apply();
  }
})(typeof window === 'undefined' ? globalThis : window);

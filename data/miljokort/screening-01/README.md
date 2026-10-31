# Hvor mange av de 664 anleggsgruppene kan få miljøkort?

Kontrollert 31. oktober 2026. **Dokumentert nedre grense: 69 av 664 grupper (10,4 %).** Dette er en kildescreening, ikke en full miljøkartlegging eller et endelig maksimum.

| Resultat | Grupper | Hva det betyr |
| --- | ---: | --- |
| Konkret tiltak, tjeneste eller lokal rutine omtalt | 50 | Kildegrunnlag for et enkelt kort med tydelig utgiver, dato og omfang. Aktuell drift og effekt er ikke uavhengig bekreftet. |
| Kun eldre felles avfallsplaner funnet | 19 | Kort kan vise historisk ordning og konkrete avklaringer, men må merkes med kildens alder. |
| Uavklart i screeningen | 595 | Verken positiv eller negativ konklusjon. Flere kan ha tilstrekkelig grunnlag som ennå ikke er funnet. |

## Avgrensning og etterprøving

Alle 664 offentlige `gid` er inventert, med kobling til de 816 polygonene. Grensekryssende grupper telles én gang. 281 grupper hadde fra før offentlige kildelenker utover kart/bilder/register; dette er ikke antall publiserbare kort.

Registerets kilder og utvalgte miljø-, HMS-, avfalls- og septiksider er kontrollert. Totalt 306 kildeoppslag er loggført, inkludert delte sider, alternative URL-er og to offentlige septiklag. 24 tilgangsfeil og seks gjenværende PDF-lesefeil er registrert. Dette er ikke 306 uavhengige kilder. Automatisk søkeordtreff er bare kandidatsøk; de 69 positive koblingene er valgt og begrunnet separat.

Det er gjort målrettede nettsøk og gjennomgang av offentlige oversikter, **ikke fullstendig individuelt nettsøk for alle 664 navn**. Tallet 595 betyr derfor uavklart, ikke «kan ikke få miljøkort» eller «har ingen tiltak». Naturkartoverlapp og økologisk tilstand er ikke undersøkt her. Generelle miljøslagord, forskriftskrav, vedlikeholdsareal eller spyleplass alene er ikke likestilt med dokumentert rensing.

Miljødirektoratets septiklag ble funnet via Færder kommunes lenke til det offentlige kartet. Navn, punkt og nærhet er kontrollert mot kartgruppene. Punkt i eller nær en gruppe dokumenterer stedlig tjeneste, ikke at båtforeningen driver eller eier den. Tvetydige treff og steder utenfor datasettet er utelatt fra denne opptellingen. Se `septic-matching-review.json`.

Moss-planens stedskoblinger som allerede er bilde-/kildekontrollert i grunnlaget, er brukt. Foreløpige navnekoblinger teller ikke. Fredrikstad-planen fra 2022 er tabellkontrollert, med visuell kontroll av PDF-side 15; bare entydig navngitte grupper med deltakelse er brukt. Manglende deltakelse i en fellesplan tolkes ikke som manglende miljøarbeid.

De seks eksisterende miljøkortene er ikke seks sikkert koblede grupper i nevneren: fem er koblet til grupper som er med her; Bispebrygga står foreløpig ved registeradressen og mangler sikker kobling til en av de 664. Bispebrygga er derfor ikke lagt til tellingen.

## Filer

- `assessment.csv` og `assessment.json`: én rad per gruppe, status, kilder kontrollert og neste steg.
- `reviewed-evidence.json`: 77 begrunnede evidensposter med URL, avsnitt/tabellrad, fysisk omfang og gruppe-ID.
- `source-screening.json`: kildeoppslag, tidspunkt, SHA-256, feil og relative stier til lokalt kildearkiv.
- `septic-matching-review.json`: alle vurderte punkter, avstand, aksept/avvisning.
- `summary.json` og `validation.json`: opptelling og konsistenskontroller.
- `work/miljokort-screening/`: skript og lokale råkilder. Råpakken er utenfor Git; bevar den for identisk etterprøving. Ny henting kan gi annet innhold.

Ingen nye kort er publisert eller lagt til nettstedet i denne screeningen. Godkjente havnepolygoner er uendret. Før flere kort lages, må hvert kort beholde kildenes forbehold og skille delt tjeneste fra eget havneanlegg.

## Grupper med funnet kortgrunnlag

| Gruppe | Navn | Kommune | Grunnlag | Kilde |
| --- | --- | --- | --- | --- |
| 3203-H06 | Holmsbu havn | Asker | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3203-H09 | Leangbukta båtforening | Asker | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3203-H12 | Vollen – molo og brygge sør | Asker | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3203-H34 | Lagahølet – Røyken båtforening | Asker | Tiltak/tjeneste/rutine | [Kilde](https://www.lagaholet.no/dokumenter/Bl%C3%A5boka%202022.pdf) |
| 4012-H21 | Langesund gjestehavn – Kongshavn | Bamble | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3201-H04 | Sandvikselva vest – lang kai med båtplasser | Bærum | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3201-H09 | Solvik og Blommenholm båtforeninger | Bærum | Tiltak/tjeneste/rutine | [Kilde](https://www.no17.no/3228/) |
| 3201-H19 | Fornebu Marina / Oksenøya Marina | Bærum | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3201-H21 | Sarbuvollen båtforening / Bærum Seilforening | Bærum | Tiltak/tjeneste/rutine | [Kilde](https://sarbis.no/wp-content/uploads/2024/02/Avfalls-og-beredskapsplan-for-Sarbuvollen-Batforening-Rev.-2.-09.01.2024.pdf) |
| 3107-H21 | Hubukta – felles brygge | Fredrikstad | Eldre fellesplan | [Kilde](https://www.fredrikstad-seilforening.no/wp-content/uploads/2023/02/Godkjent-30.03.2022-Felles-avfallsplan-for-smabathavner-i-Fredrikstad-kommune-2022-versjon-II.docx.pdf) |
| 3107-H24 | Marnet Marine Park / Marnetvika | Fredrikstad | Eldre fellesplan | [Kilde](https://www.fredrikstad-seilforening.no/wp-content/uploads/2023/02/Godkjent-30.03.2022-Felles-avfallsplan-for-smabathavner-i-Fredrikstad-kommune-2022-versjon-II.docx.pdf) |
| 3107-H33 | Langøen båtforening | Fredrikstad | Eldre fellesplan | [Kilde](https://www.fredrikstad-seilforening.no/wp-content/uploads/2023/02/Godkjent-30.03.2022-Felles-avfallsplan-for-smabathavner-i-Fredrikstad-kommune-2022-versjon-II.docx.pdf) |
| 3107-H37 | Fjeldberg båthavn / Fredrikstad Motorbåtforening | Fredrikstad | Eldre fellesplan | [Kilde](https://www.fredrikstad-seilforening.no/wp-content/uploads/2023/02/Godkjent-30.03.2022-Felles-avfallsplan-for-smabathavner-i-Fredrikstad-kommune-2022-versjon-II.docx.pdf) |
| 3107-H38 | Fredrikstad gjestehavn – vestre brygger | Fredrikstad | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3107-H40 | Isegran og Gamlebyen – brygger rundt øya | Fredrikstad | Eldre fellesplan | [Kilde](https://www.fredrikstad-seilforening.no/wp-content/uploads/2023/02/Godkjent-30.03.2022-Felles-avfallsplan-for-smabathavner-i-Fredrikstad-kommune-2022-versjon-II.docx.pdf) |
| 3107-H48 | Nabbetorp båtforening | Fredrikstad | Eldre fellesplan | [Kilde](https://www.fredrikstad-seilforening.no/wp-content/uploads/2023/02/Godkjent-30.03.2022-Felles-avfallsplan-for-smabathavner-i-Fredrikstad-kommune-2022-versjon-II.docx.pdf) |
| 3107-H49 | Øra – båthavn ved industriområdet | Fredrikstad | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3214-H09 | Vindfangerbukta / Husvikholmen – østre brygger | Frogn | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3214-H10 | Drøbak Båtforening – nordre båthavn | Frogn | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3214-H11 | Drøbak Gjestehavn | Frogn | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3911-H03 | Arås Båtforening | Færder | Tiltak/tjeneste/rutine | [Kilde](https://www.araas.no/avfallshandtering/) |
| 3911-H07 | Tenvik – nordre småbåtbasseng | Færder | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3911-H11 | Krukehavn/Sandøsund – indre basseng | Færder | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3911-H14 | Østre Bolæren gjestehavn – nordre brygger | Færder | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3911-H15 | Verdens Ende gjestehavn | Færder | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3911-H18 | Knarberg Båtforening | Færder | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3911-H22 | Kjøpmannskjær/Vrengensundet – flytebryggeanlegg | Færder | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3101-H13 | Halden gjestehavn – Kongens brygge | Halden | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3901-H04 | Bankløkka båthavn | Horten | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3901-H12 | Åsgårdstrand – nordre basseng / seilforeningen | Horten | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3110-H01 | Vestre Hvaler – molo- og båtplassområde ved sundet | Hvaler | Tiltak/tjeneste/rutine | [Kilde](https://www.xn--utgrdskilenbtforening-u2bj.no/nyheter-og-aktuelt-16702s.html) |
| 3909-H16 | Stavern – nordre havnebrygger | Larvik | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3103-H01 | Fiske båthavn | Moss | Eldre fellesplan | [Kilde](https://www.kambomarina.no/kambo_marina/avfallsplan) |
| 3103-H02 | Fuglevik båthavn / Rygge båtforening | Moss | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3103-H03 | Kambo båtforening | Moss | Eldre fellesplan | [Kilde](https://www.kambomarina.no/kambo_marina/avfallsplan) |
| 3103-H04 | Kambo Marina | Moss | Eldre fellesplan | [Kilde](https://www.kambomarina.no/kambo_marina/avfallsplan) |
| 3103-H05 | Moss motorbåtforening / Betongen | Moss | Eldre fellesplan | [Kilde](https://www.kambomarina.no/kambo_marina/avfallsplan) |
| 3103-H07 | Nasle bryggesameie – Rørvika øst | Moss | Eldre fellesplan | [Kilde](https://www.kambomarina.no/kambo_marina/avfallsplan) |
| 3103-H08 | Støtvig – indre båthavn | Moss | Eldre fellesplan | [Kilde](https://www.kambomarina.no/kambo_marina/avfallsplan) |
| 3103-H10 | Søly båthavn / Moss Seilforening | Moss | Eldre fellesplan | [Kilde](https://www.kambomarina.no/kambo_marina/avfallsplan) |
| 3103-H11 | Vansjø båtforening | Moss | Eldre fellesplan | [Kilde](https://www.kambomarina.no/kambo_marina/avfallsplan) |
| 3103-H13 | Kippenes hyttegrend – felles båtbrygge | Moss | Eldre fellesplan | [Kilde](https://www.kambomarina.no/kambo_marina/avfallsplan) |
| 3103-H14 | Sildebaugen – nordre båtbrygge | Moss | Eldre fellesplan | [Kilde](https://www.kambomarina.no/kambo_marina/avfallsplan) |
| 3103-H15 | Refsnes Gods / Refsnes bryggeforening – båtbrygge | Moss | Eldre fellesplan | [Kilde](https://www.kambomarina.no/kambo_marina/avfallsplan) |
| 3103-H16 | Knutvika / Teibern – felles havneområde | Moss | Eldre fellesplan | [Kilde](https://www.kambomarina.no/kambo_marina/avfallsplan) |
| 3103-H21 | Sameiet Røedsstranda – molo og båtbrygge | Moss | Eldre fellesplan | [Kilde](https://www.kambomarina.no/kambo_marina/avfallsplan) |
| 3212-H01 | Steilene – Nesodden Seilforenings havn | Nesodden | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3212-H07 | Oksval Båthavn | Nesodden | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 0301-H02 | Bestumkilen – Sjølyst Marina | Oslo | Tiltak/tjeneste/rutine | [Kilde](https://toxiclean.no/karenslyst-batopplag-med-nytt-toxiclean-anlegg/) |
| 0301-H04 | Bestumkilen – Maritim båtforening | Oslo | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 0301-H08 | Frognerkilen – KNS, Frognerkilens Båtforening av 1860 og Kongen Marina | Oslo | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 0301-H09 | Dronninghavna – Kongelig Norsk Seilforening | Oslo | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 0301-H13 | Bygdøy – Huk/Paradisbukta marina | Oslo | Tiltak/tjeneste/rutine | [Kilde](https://www.osloseilforening.no/next/p/14151/hms) |
| 0301-H23 | Hovedøya småbåthavn | Oslo | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 0301-H29 | Padda småbåthavn | Oslo | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 4001-H05 | Porsgrunn gjestebrygge – Østre Brygge | Porsgrunn | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 4001-H14 | Brevik indre havn – båtplasser og gjestebrygger | Porsgrunn | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 4001-H15 | Sandøya Småbåthavn – Breistranda | Porsgrunn | Tiltak/tjeneste/rutine | [Kilde](https://www.havneweb.no/sandoyabatforening/) |
| 4001-H16 | Langangen Motorbåtforening – Kilen / Halvarp | Porsgrunn | Tiltak/tjeneste/rutine | [Kilde](https://elvoghav.no/prosjekter/kystlotteriet/her-kan-du-levere-hente-sekk/) |
| X-SALTHOLMEN-3112-3107 | Saltholmen båthavn / Saltnes båtforening – Råde-del | Råde, Fredrikstad | Tiltak/tjeneste/rutine | [Kilde](https://saltnesbf.no/?page_id=233) |
| 3907-H32 | Ormestad motorbåtforening | Sandefjord | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3907-H65 | Framnæs Maritime – nordre bryggeanlegg | Sandefjord | Tiltak/tjeneste/rutine | [Kilde](https://www.framnes-maritime.no/) |
| 3105-H33 | Skjebergkilens marina | Sarpsborg | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3105-H36 | Grimsøy marina | Sarpsborg | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3905-H03 | Tønsberg gjestehavn – Brygga | Tønsberg | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3905-H06 | Vallø Småbåthavn | Tønsberg | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3216-H02 | Son havn nord / Sonskilen – vestre brygger | Vestby | Tiltak/tjeneste/rutine | [Kilde](https://services1.arcgis.com/ThExf1r1eIhz35uv/arcgis/rest/services/Septik_(ny_og_gammel)/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json&returnGeometry=true) |
| 3216-H05 | Søndre Brevik båthavn – Son Båtforening | Vestby | Tiltak/tjeneste/rutine | [Kilde](https://www.sonbaat.no/avfallshandtering/) |
| 3216-H06 | Son Gjestehavn – sentrumsbrygger | Vestby | Tiltak/tjeneste/rutine | [Kilde](https://www.sonhavn.no/son-gjestehavn/priser-2/) |

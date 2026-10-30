import json
from pathlib import Path
P=Path(__file__).parent
REPORT='https://www.sandefjord.kommune.no/engasjer-deg/planer/miljo-naring-landbruk/smabathavnutredning/'
SERVICE='https://services3.arcgis.com/dLSgnt8bVopEJNp3/arcgis/rest/services/B%C3%A5thavner/FeatureServer/0'
MP='https://www.sandefjord.kommune.no/miljo-naring-landbruk/sandefjord-havn/leie-batplass/'
municipal={f['properties']['OBJECTID']:f for f in json.loads((P/'raw/municipal-harbour-points.geojson').read_text())['features']}
rows=[]
def add(n,pts,note='',uncertain=False,part=None):
 f=municipal[n];p=f['properties'];rows.append(dict(candidate_id=f'MUN-{n:02d}',name=p['Navn'],image=f'p{n:02d}',display_width=600,display_height=600,pixels=pts,group=f'mun-{n}',capacity=p['antall_bå'],sources=[REPORT,SERVICE]+([MP] if n<=12 else []),name_is_descriptive=False,possible=False,basis='kommunalt_dokumentert_smabathavn_med_faste_batplasser',note=note,geometry_uncertain=uncertain,municipal_objectid=n,municipal_source_number=p['Nr'],part=part))
add(1,[(270,288),(310,285),(314,330),(293,337),(282,353),(269,350)],'Avgrenser synlige brygger ved Flautangen. Rapportens 52 plasser omfatter også 12 private plasser ved nordre brygge. Yttergrense for alle fortøyninger er uklar.',True)
add(2,[(253,310),(302,302),(304,329),(291,338),(288,324),(252,328)],'Kommunal brygge ved Granholmen. Privat anlegg i Berganbukta nord for holmen er separat.')
add(3,[(238,286),(266,264),(302,251),(329,255),(389,305),(244,374),(229,337)],'Hesteskoen/MiljøMarina: samme fysiske basseng. Gjestehavnfunksjon er ikke talt som et ekstra anlegg. Intern fordeling av kommunale/andre plasser er ikke kartlagt.',True)
add(4,[(297,292),(327,303),(328,317),(303,307)],'Ti dokumenterte plasser langs Huvik-kaien; foreløpig smalt belte.',True)
add(5,[(268,285),(299,274),(322,332),(301,340),(279,304)],'Dokumentert kommunal småbåthavn med under ti plasser: inkludert etter regelens unntak for dokumenterte faste havneplasser. Rapport 2022 oppgir 6, kommunens nåværende nettside 5. Kapasitet i tabellen er historisk, ikke dagens kapasitet.')
add(6,[(241,296),(299,284),(337,272),(344,282),(300,297),(244,308)],'Smalt belte langs nordkaien i Kamfjordkilen. Naboforeningens flytebrygger er eget anlegg.')
add(7,[(247,288),(291,284),(306,337),(296,359),(247,338)],'Kommunens nordre brygger ved Langeby. Søndre bryggelag kartlagt separat.')
add(8,[(252,265),(293,274),(311,316),(304,344),(244,325),(246,309)],'Avgrenser Roa kommunale brygger. Roabrygga, Vindal og Asnespynten er egne navngitte kandidater.')
add(9,[(290,284),(326,275),(332,287),(321,320),(306,317)],'Synlige brygger ved Skjellvika. Ikke alle historisk oppgitte plasser kan identifiseres tydelig i vinterbildet.',True)
add(10,[(229,287),(239,279),(268,265),(283,279),(249,302),(230,312)],'Kommunal brygge ved Stub. Hjertnes og Stub brygger AS holdes adskilt.')
add(11,[(281,275),(319,283),(325,341),(283,341)],'Kommunalt bryggeanlegg på vestre side av Tangenbukta. Private enkeltbrygger på motsatt side er ikke innlemmet.')
add(12,[(282,291),(332,238),(344,243),(298,303)],'Kommunens midtre brygge ved Enge. Fergeanløpet er del av samme fysiske brygge; tilstøtende forening og Engø er egne anlegg.')
add(13,[(248,291),(351,238),(364,257),(261,315)],'Lang brygge langs Fjellvik-kaien. Gokstad kystlags U-anlegg sørvest er separat.')
add(14,[(271,273),(343,266),(356,332),(276,342)])
add(15,[(269,251),(296,255),(334,318),(280,329),(270,304),(260,299)],'Søndre vifteformede anlegg innenfor Hjertnes båtforenings lokalitet. Kommunale Stub og Ulabrand holdes adskilt.')
add(16,[(214,297),(350,254),(358,269),(228,319)],'Langstrakt flytebrygge langs Kilen Brygge; kommunal nordkai og motorbåtforening øst for dette er separate.')
add(17,[(405,260),(422,266),(459,317),(427,330),(423,313),(381,323),(378,308),(418,299)],'Østre flytebrygger ved Sandefjord motorbåtforening. Nærliggende Kilen Brygge er separat.')
add(18,[(269,264),(360,225),(378,225),(376,325),(268,322)],'Hovedanlegget ved Thorøya. Ikke hele industri-/opplagsområdet på land.')
add(19,[(218,307),(260,289),(280,331),(251,356),(230,354)],'Ulabrands dokumenterte brygge ved moloen. Hesteskoen, Stub og Hjertnes er separate lokaliteter.')
add(20,[(286,288),(373,253),(385,296),(299,320)])
add(21,[(297,224),(394,246),(399,260),(385,284),(375,281),(352,380),(282,355),(286,289),(303,271)])
add(22,[(270,280),(343,278),(372,371),(304,381)],'Hovedbryggene i Melsomvik. Nordre mindre brygge kartlagt som delpolygon i samme anlegg.')
add(22,[(269,238),(282,239),(293,268),(283,273),(277,251)],'Nordre brygge; inngår i samme dokumenterte havn, ikke nytt anlegg.',part='nordre')
add(23,[(274,283),(324,285),(324,264),(363,268),(363,331),(274,327)])
add(24,[(243,270),(319,283),(320,304),(241,288)],'Nordre separate flytebrygge ved Roa. Nabobrygger kartlagt under sine respektive kandidater.')
add(25,[(281,319),(323,324),(324,342),(281,340)],'Synlig bryggegruppe ved Berganodden. Fortøyningsutstrekning i rapporten er ikke fullstendig identifiserbar i bildet.',True)
add(26,[(258,281),(303,285),(344,367),(331,377),(289,301),(257,298)])
add(27,[(279,296),(351,240),(370,250),(291,315)],'Sørøstre brygge ved Enge. Kommunens midtbrygge og nordre Engø er ikke tatt inn i dette polygonet.')
add(28,[(275,283),(324,218),(337,222),(290,293)],'Nordre brygge ved Engø. Kildene omtaler tre ulike anlegg ved samme landadkomst.')
add(29,[(242,270),(296,276),(328,311),(330,326),(250,329)],'Søndre båthavn ved Framnæs. Nordre separate brygger kontrolleres mot egen operatørkilde.',True)
add(30,[(259,267),(293,279),(300,299),(268,341),(250,332),(247,318),(262,294)],'Gokstad kystlags U-formede bryggeanlegg ved Huvik.')
add(31,[(280,291),(340,252),(351,271),(364,278),(364,295),(297,301)])
add(32,[(270,284),(315,281),(322,316),(301,324),(275,311)],'Søndre brygger ved Langeby bryggelag; kommunens nordre brygger er separat.')
add(33,[(292,288),(319,269),(331,289),(319,315),(345,303),(355,310),(340,331),(310,322)],'Avgrenser Ormestad motorbåtforenings felles brygger. Nabobrygger ved Nordre Holtan holdes utenfor.')
add(34,[(277,277),(334,318),(323,330),(274,285)],'Hellanoddens diagonale brygge; andre navngitte brygger i bukta er separate.')
add(35,[(282,293),(309,301),(309,311),(280,304)],'Kortere midtre brygge ved Vindal, mellom Roabrygga og Roa kommunale brygger.')
add(36,[(267,297),(300,283),(314,294),(287,316),(279,324),(267,318)])
add(37,[(264,274),(305,276),(306,300),(331,312),(328,323),(263,310)],'Brunstad båtforenings søndre anlegg. OCCs nordre brygge er separat.')
add(38,[(275,273),(337,290),(335,305),(278,289)],'Nordre brygge ved Oslofjorden Convention Center. Båtforeningens søndre brygger er separat.')
add(39,[(255,285),(271,294),(277,313),(260,320),(249,308)],'Søndre mindre anlegg på Asnespynten; de tre større bryggene nord for dette er egne kandidater.')
add(40,[(244,272),(319,276),(333,295),(319,317),(261,323),(249,304)],'Brygge og fortøyningsområde innerst i Bentsrødbukta. Alle historiske plasser er ikke tydelige i bildet.',True)
add(41,[(288,286),(309,289),(304,316),(285,317)],'Lite dokumentert fellesanlegg ved Eianbukta. Bildet viser få detaljer; foreløpig snever avgrensning.',True)
add(42,[(256,270),(298,258),(304,269),(259,283)])
add(43,[(266,293),(313,287),(319,303),(268,309)])
add(44,[(273,290),(300,305),(306,317),(295,326),(277,313)],'Søndre fellesbrygge i Ormestadvika. Motorbåtforeningens nordre anlegg er eget polygon/anlegg.')
add(45,[(278,285),(309,293),(328,303),(322,314),(297,305),(278,298)],'Fellesbrygge ved Lofterødveien. Spredte private nabobrygger utelatt.')
add(46,[(271,286),(321,288),(320,298),(274,299)],'Lystad fellesbrygge; nabokandidaten Hystadveien 189 kontrolleres separat.')
add(47,[(295,289),(339,295),(340,305),(294,302)],'Dokumentert mindre bryggeanlegg ved Hystadveien 189. Intern fordeling ved tettliggende nabobrygger er foreløpig.',True)
add(48,[(281,283),(332,272),(336,288),(292,299)],'Natholmen brygge AS er ett av tre navngitte anlegg ved samme sund. Ikke automatisk slått sammen.')
add(49,[(276,290),(315,266),(327,280),(286,306)])
add(50,[(288,287),(296,299),(331,314),(327,326),(298,316),(286,303)])
add(51,[(287,273),(301,301),(320,299),(322,311),(286,315),(279,279)])
add(52,[(269,285),(311,311),(309,327),(292,326),(280,308),(263,295)],'Småbåtplasser ved Stub brygger AS. Kommunale Stub nord for dette er eget anlegg.')
add(53,[(294,285),(314,293),(312,329),(302,331)],'Felles flytebrygge sør for Thorsholmen.')
add(54,[(281,290),(324,285),(329,317),(301,322),(293,307),(280,306)],'Rapportens overskrift er Årøtangen 46, mens kartlaget sier Årøtangen 26. Stedet identifisert ved kartgeometri; adressen er ikke avklart.',True)
add(55,[(291,291),(329,291),(330,305),(292,304)])
add(56,[(283,283),(325,277),(324,290),(285,298)])
add(57,[(297,291),(318,312),(319,323),(300,315),(296,304)])
add(58,[(279,286),(303,278),(321,307),(313,318),(292,305)],'Dokumentert anlegg langs Hagaløkka. Full utstrekning av historiske bøye-/wireplasser er uklar.',True)
add(59,[(289,288),(315,267),(322,277),(297,298)])
add(60,[(247,268),(282,294),(296,279),(303,290),(281,308),(244,280)],'Østre Nes: søndre vinkelformede brygger. Ikke hele bukten mellom andre navngitte anlegg.')
add(61,[(299,290),(341,296),(338,331),(298,327)],'Kartgeometrien viser bryggene innerst i Mefjorden. Lagrede x/y-attributter peker feil og er ikke brukt.')
add(62,[(290,292),(336,301),(335,313),(290,304)])
add(63,[(273,285),(304,288),(309,300),(272,296)],'Kartgeometri brukt: x/y-attributtene i kilden peker til et annet anlegg. Mindre brygge og fortøyningsområde er foreløpig avgrenset.',True)
add(64,[(274,292),(306,290),(309,302),(277,304)],'Riktig plassering på Østerøya fra kartgeometrien. Kildens y-attributt peker ca. 2,7 km nordover og er ikke brukt. Full fortøyningsutstrekning usikker.',True)
add(65,[(299,286),(316,292),(315,306),(298,301)])
add(66,[(293,290),(344,292),(347,307),(298,312)],'Dokumentert småbåtanlegg ved Herreportveien. Yttergrense for alle historiske plasser er uklar.',True)

# Final tracing corrections following exported-geometry overlays and report detail pages.
fix={
2:[(293,275),(307,275),(309,322),(288,323),(287,314),(296,310)],
4:[(268,288),(287,267),(305,275),(288,297),(279,306),(267,300)],
6:[(240,306),(295,296),(339,278),(343,286),(299,307),(242,319)],
7:[(269,309),(299,309),(306,342),(277,345),(263,337)],
10:[(299,293),(340,267),(349,279),(312,301),(317,309),(309,315)],
15:[(302,266),(351,277),(350,313),(372,332),(364,355),(294,340)],
19:[(278,277),(344,245),(398,326),(328,358),(300,314)],
22:[(270,280),(347,278),(378,402),(304,414)],
25:[(287,253),(296,253),(297,295),(288,296)],
28:[(276,309),(322,253),(336,264),(290,320)],
30:[(239,318),(278,325),(303,294),(310,299),(281,336),(235,325)],
33:[(295,291),(335,313),(345,303),(363,311),(338,341),(291,307)],
38:[(267,289),(279,285),(283,276),(295,278),(290,292),(331,304),(329,322),(264,304)],
42:[(260,242),(286,229),(293,239),(264,252)],
44:[(281,295),(308,279),(317,288),(294,310),(310,317),(319,311),(326,320),(310,334),(286,313)],
50:[(291,291),(302,290),(311,326),(333,321),(338,337),(301,344)],
51:[(279,261),(290,256),(310,291),(320,289),(323,300),(273,317),(268,308),(299,295)],
52:[(280,267),(296,264),(305,288),(289,292)],
54:[(290,290),(328,266),(339,279),(297,305)],
56:[(288,295),(334,281),(341,296),(294,308)],
57:[(291,246),(304,240),(311,253),(305,263),(311,266),(312,279),(295,285)],
59:[(280,311),(306,289),(315,298),(286,323)],
60:[(244,268),(259,257),(300,285),(308,288),(299,304),(281,307),(241,280)],
63:[(291,288),(324,284),(326,300),(292,306)],
65:[(308,291),(322,293),(322,306),(315,326),(304,323),(310,302)]}
for r in rows:
 n=r['municipal_objectid']
 if n in fix:r['pixels']=fix[n]
# Melsomvik's first tracing accidentally marked land north of the piers. One enclosing
# polygon now includes the actual five-pier complex; no extra land polygon is retained.
rows[:]=[r for r in rows if not (r['municipal_objectid']==22 and r.get('part'))]
r=next(r for r in rows if r['municipal_objectid']==22);r['note']='Samlet synlig bryggekompleks i Melsomvik; planformål og fremtidige utvidelser er ikke brukt som havnegrense.'
# Langeby operator allocation is explicitly described on report page 50.
r=next(r for r in rows if r['municipal_objectid']==32);r['image']='p07';r['pixels']=[(256,258),(291,256),(302,308),(262,307)];r['note']='Midtre brygge tilhører Langeby bryggelag. Nordre private brygge inngår i rapportens 55 plasser. De to søndre kommunale bryggene er eget polygon.'
# Roabukta contains several operators whose historic allocation cannot safely be
# matched to every pier in this image. Deliver one physical harbour, preserve sources.
r=next(r for r in rows if r['municipal_objectid']==8);r.update(name='Roabukta – Roa, Roabrygga, Vindal og Asnespynten',pixels=[(224,310),(253,246),(281,257),(288,235),(348,254),(348,272),(312,284),(315,316),(309,343),(281,346),(222,326)],capacity=None,geometry_uncertain=True,source_register_members=[8,24,35,39],capacity_components=[{'objectid':n,'name':municipal[n]['properties']['Navn'],'berths_in_register':municipal[n]['properties']['antall_bå']} for n in [8,24,35,39]],note='Ett sammenhengende fysisk båthavnområde i Roabukta, med fire kommunalt registrerte navn/forvaltere. Interne brygge-/operatørgrenser er ikke pålitelig identifisert i kildebildet. Ingen summering av kapasitet; de fire kildetallene beholdes separat. Dette er ikke en påstand om felles juridisk drift.')
rows[:]=[r for r in rows if r['municipal_objectid'] not in [24,35,39]]
# Split small jetties around land rather than drawing through the peninsula.
add(25,[(297,319),(353,323),(353,334),(300,335)],'Søndre brygge i samme dokumenterte anlegg ved Berganodden.',True,part='sor')
add(52,[(310,294),(322,294),(331,326),(318,331)],'Søndre brygge ved Stub brygger AS; tilhører samme havne-ID som nordre brygge.',part='sor')
r=next(r for r in rows if r['municipal_objectid']==48);r['image']='p56';r['pixels']=[(302,309),(358,294),(367,311),(310,327)];r['note']='Søndre lange brygge ved Natholmen. Den midtre og den korte nordre bryggen er andre navngitte anlegg.'
r=next(r for r in rows if r['municipal_objectid']==57);r.update(possible=True,basis='eksisterende_smabrygger_men_planlagt_hovedanlegg_ikke_verifisert',geometry_uncertain=True,note='Rapport side 82 omtaler et planlagt større anlegg. Bare eksisterende småbrygger i bildet er avgrenset; planarealet er ikke inkludert. Kommunalt punktlag oppgir 30 plasser, men dagens felles drift/kapasitet er uklar.')
r=next(r for r in rows if r['municipal_objectid']==19);r['geometry_uncertain']=True;r['note']='Avgrenser bryggene ved det historiske Strømbadet. Intern avgrensning mot tilgrensende Hesteskoen/Hjertnes trenger kontroll; ikke en offisiell operatørgrense.'
# Where available, use the independently mapped OSM outline as a reference geometry
# and explicitly retain its provenance; it is visually checked on the same imagery.
import xml.etree.ElementTree as ET
import sys
sys.path.insert(0,str(P/'deps'))
from pyproj import Transformer
T=Transformer.from_crs(4326,25833,always_xy=True)
r=next(r for r in rows if r['municipal_objectid']==17);root=ET.parse(P/'raw/osm-way-1218866789.osm').getroot();ns={n.get('id'):(float(n.get('lon')),float(n.get('lat'))) for n in root.findall('node')};way=root.find("way[@id='1218866789']");m=json.loads((P/'images/p17.json').read_text());a,b,c,d=m['bbox'];r['pixels']=[((x-a)/(c-a)*600,(d-y)/(d-b)*600) for x,y in (T.transform(*ns[z.get('ref')]) for z in way.findall('nd'))];r['osm_ids']=['way/1218866789'];r['basis']='kommunalt_dokumentert_smabathavn_og_bildekontrollert_osm_omriss';r['note']='OSM-omriss kontrollert mot Esri-bildet; bevarer sjøområdet innenfor bryggene. Naboforeninger er separate.';r['tracing_method']='osm_polygon_bildekontrollert'

r=next(r for r in rows if r['municipal_objectid']==4);r['pixels']=[(252,263),(268,271),(292,277),(300,281),(285,311),(274,315),(242,294)]
r=next(r for r in rows if r['municipal_objectid']==30);r['pixels']=[(272,258),(317,279),(286,321),(241,313)];r['note']='Gokstad kystlags langstrakte midtre anlegg. Den kommunale Huvik-bryggen i sør og Huvik Eiendom AS i nord er separate dokumenterte kandidater.'
# Additional operator: not the municipal ten-berth Huvik site.
def osm_pixels(osmid,key):
 root=ET.parse(P/'raw'/('osm-'+osmid.replace('/','-')+'.osm')).getroot();typ,num=osmid.split('/');w=root.find(typ+f"[@id='{num}']");ns={n.get('id'):(float(n.get('lon')),float(n.get('lat'))) for n in root.findall('node')};m=json.loads((P/'images'/f'{key}.json').read_text());a,b,c,d=m['bbox'];return [((x-a)/(c-a)*600,(d-y)/(d-b)*600) for x,y in (T.transform(*ns[z.get('ref')]) for z in w.findall('nd'))]
rows.append(dict(candidate_id='EXT-HUVIK',name='Huvik Eiendom AS – båthavn',image='p13',display_width=600,display_height=600,pixels=osm_pixels('way/1218301840','p13'),group='huvik-eiendom',capacity=32,sources=['https://www.huvik.no/b%C3%A5tplasser'],name_is_descriptive=False,possible=False,basis='operator_dokumenterer_32_faste_batplasser',note='Operatøren oppgir 32 plasser i Framnæsveien 3 B, nær Gokstad kystlag. OSM-navnet Huvik er ikke brukt til å slå dette sammen med kommunens separate Huvik-kandidat. OSM-omriss kontrollert mot bilde.',geometry_uncertain=False,osm_ids=['way/1218301840'],tracing_method='osm_polygon_bildekontrollert'))
# Sandefjord guest harbour and La Scala share the same immediate quay/basin.
r=next(r for r in rows if r['municipal_objectid']==5);r.update(name='Sandefjord gjestehavn / La Scala',pixels=osm_pixels('way/1079317965','p05'),osm_ids=['way/1079317965'],capacity=None,capacity_components=[dict(name='La Scala',berths_in_register=6,source=SERVICE),dict(name='Sandefjord gjestehavn',published_guest_berths=60,source='https://www.sandefjord.kommune.no/miljo-naring-landbruk/sandefjord-havn/gjeste-og-fiskerihavner/')],source_register_members=[5],tracing_method='osm_polygon_bildekontrollert',geometry_uncertain=True,note='Dokumentert gjestehavn ved samme kai som La Scala. Kildenes plasser kan ikke fordeles sikkert til delgrenser; ingen summering. Den kommunale La Scala er dokumentert selv om den har færre enn ti plasser. Kildetallene beholdes separat.');r['sources'].append('https://www.sandefjord.kommune.no/miljo-naring-landbruk/sandefjord-havn/gjeste-og-fiskerihavner/')
rows.append(dict(candidate_id='EXT-FRAMNES-NORD',name='Framnæs Maritime – nordre bryggeanlegg',image='framnes-nord',display_width=1000,display_height=1000,pixels=[(479,389),(532,390),(536,520),(471,520)],group='framnes-nord',capacity=None,sources=['https://www.framnes-maritime.no/'],name_is_descriptive=True,possible=True,basis='flere_fingerbrygger_men_fast_batplassbruk_versus_service_uklar',note='To tydelige fingerbrygger innenfor molo nord for Framnæs Båthavn AS. Operatøren beskriver service, opptak og samarbeid med båthavnen i sør. Fast utleie versus serviceplasser er ikke avklart; beholdt som mulig småbåthavn. Rene servicekaier nord for bassenget er ikke inkludert.',geometry_uncertain=False,osm_ids=['node/2088640421']))
r=next(r for r in rows if r.get('municipal_objectid')==1);r['pixels'][0]=(270,273);r['pixels'][1]=(308,271)
r=next(r for r in rows if r.get('municipal_objectid')==11);r['pixels']=[(278,256),(320,270),(325,341),(283,341)]
r=next(r for r in rows if r.get('municipal_objectid')==8);r['pixels']=[(224,310),(253,246),(281,257),(289,204),(372,217),(374,242),(348,256),(348,272),(312,284),(315,316),(309,343),(281,346),(222,326)]
r=next(r for r in rows if r.get('municipal_objectid')==52 and r.get('part')=='sor');r['pixels']=[(298,310),(313,298),(321,325),(304,330),(293,322)]

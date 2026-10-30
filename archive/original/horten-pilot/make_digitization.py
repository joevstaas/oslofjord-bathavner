import json,pathlib
p=pathlib.Path(__file__).parent
common='https://www.hortenhavn.no/fritidsbaat/'
a=[]
def add(h,b,name,img,frame,pts,osm=None,sources=None,status='kart_og_kilde',note=None):
 a.append(dict(id=f'{h}-B{b:02d}',harbour_id=h,name=name,image=img,frame=frame,vertices=pts,osm_id=osm,sources=sources if sources is not None else [common],status=status,note=note))
add('H01',1,'Våle båthavn / Frebergsvik','frebergsvik',[1400,1400],[[628,744],[654,706],[693,672],[776,832],[732,849]],'node/9963302233',sources=['https://www.openstreetmap.org/node/9963302233'])
add('H02',1,'Solviken småbåthavn','indre-vest',[1400,1400],[[529,438],[706,484],[794,585],[683,635],[490,504]],'way/1216920501')
add('H03',1,'Båtforeningen Pluggen','indre-vest',[1400,1400],[[935,858],[1107,872],[1141,897],[1111,925],[1075,988],[958,1004],[941,968]],'way/1216417052')
add('H04',1,'Bankløkka båthavn','sykehus-banklokka',[1400,884],[[316,356],[476,361],[479,514],[455,555],[419,555],[419,535],[300,540]],sources=['https://www.hortenhavn.no/fritidsbaat/bankloekka-baathavn/','https://www.hortenhavn.no/hvor-er-hva/'])
add('H05',1,'Sykehusbrygga gjestehavn','sykehus-banklokka',[1400,884],[[901,352],[1036,357],[1011,410],[1000,419],[904,410]],sources=['https://www.hortenhavn.no/fritidsbaat/sykehusbrygga-gjestehavn/','https://www.hortenhavn.no/hvor-er-hva/'])
add('H06',1,'Fyllinga båthavn','fyllinga',[1400,1400],[[399,451],[611,597],[683,687],[647,754],[739,755],[626,878],[483,866],[371,542],[380,505]],'node/679140414')
add('H07',1,'Horten gjestehavn','sentrum-ost',[900,1500],[[441,747],[477,743],[513,785],[539,803],[511,848],[464,855],[431,840],[421,809],[429,778]],'way/1216306785',sources=['https://www.hortenhavn.no/fritidsbaat/horten-gjestehavn/','https://www.hortenhavn.no/hvor-er-hva/'])
add('H08',1,'Strandparken båtforening','sentrum-ost',[900,1500],[[268,1391],[330,1392],[357,1413],[333,1416],[327,1448],[311,1470],[286,1469],[267,1458]])
add('H09',1,'Steinsneshavn','steinsnes',[1400,1400],[[857,507],[981,517],[1039,557],[1033,585],[990,640],[851,591],[860,542]])
add('H10',1,'Horten Seilforening / Rørestrand','steinsnes',[1400,1400],[[688,896],[749,906],[838,927],[846,994],[870,1010],[850,1040],[838,1052],[793,1045],[736,1022],[689,993]],'node/5107343404')
add('H11',1,'Steinbrygga båthavn – hovedbasseng','steinbrygga',[1400,1400],[[516,699],[642,582],[663,565],[682,580],[776,711],[746,742],[724,762],[643,802],[616,786]],'way/1216709953')
add('H12',1,'Åsgårdstrand – nordre basseng / seilforeningen','asgardstrand',[1250,1500],[[425,626],[505,592],[537,558],[578,684],[578,724],[483,750],[442,641]],'way/1216198612',sources=['https://www.hortenhavn.no/fritidsbaat/aasgaardstrand-smaabaathavn/'])
add('H12',2,'Åsgårdstrand – midtre basseng','asgardstrand',[1250,1500],[[482,758],[578,733],[603,751],[626,780],[619,875],[544,904],[507,831]],sources=['https://www.hortenhavn.no/fritidsbaat/aasgaardstrand-smaabaathavn/'],note='Bassengavgrensning. Gjesteplasser kan ligge i samme basseng som faste plasser; dette er ikke operatør- eller leiegrenser.')
add('H12',3,'Åsgårdstrand – søndre basseng','asgardstrand',[1250,1500],[[549,914],[618,888],[625,803],[657,819],[699,972],[571,1001]],'way/1217376960',sources=['https://www.hortenhavn.no/fritidsbaat/aasgaardstrand-gjestehavn/'])
add('H13',1,'RS Noatun – marina','noatun-full',[1400,1400],[[522,547],[642,546],[742,629],[700,666],[675,708],[432,645],[485,613],[520,601]],sources=['https://www.rs-noatun.no/nb'],note='Tilbyder opplyser om egen marina. Kurs-/konferanseanlegg; ikke automatisk klassifisert som ordinær offentlig gjestehavn.')
add('K01',1,'Drasund / Løvøya – bryggegruppe','lovoya',[1350,1500],[[501,461],[579,403],[619,466],[590,510],[567,501]],sources=['https://lovoyaoslofjord.no/','https://velihavn.no/gjestehavner/vestfold/lovoya-bathavn'],status='ma_avklares',note='Bryggegruppe synlig i kart. Løvøya har dokumentert båthavn, men koblingen til akkurat disse bryggene er ikke bekreftet. Ikke likestilt med båtfølget kommunen fjernet i august 2026.')
add('K02',1,'Steinbrygga – nordre moloområde','steinbrygga',[1400,1400],[[731,550],[805,482],[840,476],[933,598],[865,629],[781,664]],sources=[common],status='ma_avklares',note='Nordre moloområde er synlig i kart; faste småbåtplasser og avgrensning mot hovedanlegget må avklares.')
a=[d for d in a if d['id']!='H01-B01']
(p/'digitization.json').write_text(json.dumps(a,ensure_ascii=False,indent=2))
print(len(a),'polygoner')

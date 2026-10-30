"""Beslutninger for automatiske kandidater (A###) og manuelle tillegg (M###), Fredrikstad rev. 1.
action: inc = inkluder auto-geometri; clip = auto-geometri klippet med box (EPSG:25833); add = union med ekstra polygon;
man = manuell geometri (koordinater i EPSG:25833); exc = utelatt (begrunnelse). group samler delpolygoner i én havn."""
D = {}
def d(cid, action, **kw): D[cid] = dict(action=action, **kw)
EXC_SMALL = 'Enkeltbrygge(r) med få synlige båter; ikke dokumentert felles anlegg med minst 10 plasser.'
EXC_PRIV = 'Spredte private brygger ved separate eiendommer; ikke summert.'
d('A001', 'exc', why=EXC_SMALL); d('A002', 'exc', why='Lang brygge/molo ved Rauøy uten synlig båtplassanlegg.')
d('A003', 'clip', box=[257400, 6579600, 258100, 6579900], group='saltholmen', name='Saltholmen båthavn / Saltnes båtforening – Fredrikstad-del', cls='smabathavn',
  basis='operator_dokumenterer_faste_batplasser', capacity=220, cap_source='https://saltnesbf.no/?page_id=19', cross='X-SALTHOLMEN-3112-3107', unc=True, descr=False,
  note='Søndre del av Saltnes båtforenings anlegg. Kommunegrensen krysser bryggene; Råde-delen er godkjent som 3112-H02-B01. Kapasitet gjelder hele havna.')
d('A004', 'inc', group='saltholmen-sor', name='Sør for Saltholmen – lang felles brygge', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg',
  note='Én lang brygge med rundt 20 synlige båter på begge sider. Operatør ikke dokumentert.')
d('A005', 'exc', why=EXC_SMALL); d('A006', 'exc', why=EXC_SMALL); d('A007', 'exc', why=EXC_SMALL); d('A008', 'exc', why=EXC_PRIV)
d('A009', 'inc', group='lervik', name='Lervik båthavn', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg',
  note='Stor marina med åtte–ni lange brygger og mange hundre synlige plasser. Navn beskrivende; operatør ikke sikkert dokumentert.')
d('A010', 'inc', group='lervik-ost', name='Lervik østside – felles brygger', cls='mulig_smabathavn', basis='flere_brygger_men_felles_drift_eller_kapasitet_uklar', unc=True,
  note='Flere brygger med 5–15 båter hver langs østsiden. Felles drift ikke dokumentert.')
d('A011', 'exc', why=EXC_SMALL); d('A012', 'exc', why='Fem–seks korte brygger med 3–8 båter hver langs vikens østside; felles drift ikke dokumentert.')
d('A013', 'add', extra=[[256843, 6575960], [256870, 6575960], [256872, 6576150], [256848, 6576150]], group='engelsviken-nord', name='Engelsviken – indre havn',
  cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', unc=True, descr=True,
  note='Indre havnebasseng med flere brygger på østsiden og båter langs vestre kai. Engelsviken båtforening har adresse Moloveien 22 ved søndre havn; operatørgrenser i havna er ikke kartlagt.',
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/996223183'])
d('A014', 'inc', group='engelsviken-sor', name='Engelsviken – søndre havn og gjestehavn', cls='smabathavn', basis='operator_dokumenterer_gjestehavn_og_synlige_faste_plasser', unc=True, descr=True,
  note='Lang brygge med mange båter innenfor moloen og mindre brygger nordover. Engelsviken gjestehavn drives av Engelsviken båtforening (9–11 gjestebåter). Båter langs moloens vestside er ikke tatt med.',
  sources=['https://visitfredrikstadhvaler.com/no/sted/engelsviken-gjestehavn-fredrikstad', 'https://virksomhet.brreg.no/nb/oppslag/enheter/996223183'])
for c in ['A015', 'A016', 'A017', 'A018', 'A019', 'A022']: d(c, 'exc', why=EXC_SMALL)
d('A020', 'inc', group='gaustad', name='Gaustad båtforening', cls='smabathavn', basis='forening_registrert_og_minst_10_synlige_plasser', descr=False,
  note='Fire brygger med utriggere og mange båter innerst i kilen. Gaustad båtforening har adresse Engelsvikenveien 208 like ved; koblingen er geografisk.',
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/993400246'])
d('A021', 'inc', group='hankosund-nord', name='Hankøsund nordside – felles brygge', cls='mulig_smabathavn', basis='flere_brygger_men_felles_drift_eller_kapasitet_uklar', unc=True,
  note='Brygge med rundt ti båter på begge sider, blant flere private brygger. Felles drift ikke dokumentert.')
d('A023', 'inc', group='vikane-hankosund-n', name='Hankøsund nord ved Vikaneveien – bryggerekke', cls='mulig_smabathavn', basis='flere_brygger_men_felles_drift_eller_kapasitet_uklar', unc=True,
  note='Sammenhengende rekke brygger med mange båter langs strandkanten nord for Hankø Marina. Kan omfatte flere private eiere; felles drift og faste plasser er ikke dokumentert.')
for c in ['A024', 'A025', 'A031']: d(c, 'exc', why=EXC_SMALL)
HM = ['https://virksomhet.brreg.no/nb/oppslag/enheter/985210128', 'https://virksomhet.brreg.no/nb/oppslag/enheter/992108770']
d('A027', 'inc', group='hanko-marina', name='Hankø Marina – hovedbrygger', cls='smabathavn', basis='marina_og_minst_10_synlige_plasser', descr=False, sources=HM, osm=['way/1518774721'],
  note='Lang dobbel brygge med utriggere og mange båter. OSM-flate «Hankø Marina». Hankø Marina AS og Hankø Marina Bryggeplasser AS (Vikaneveien 409).')
d('A026', 'inc', group='hanko-marina', name='Hankø Marina – brygger ved parkeringen', cls='smabathavn', basis='del_av_marina', descr=False, sources=HM, unc=True,
  note='To korte brygger med båter i bukta ved marinaens parkering. Gruppert med Hankø Marina etter nærhet og OSM-flate; driftsgrense ikke dokumentert.')
d('A028', 'inc', group='hanko-marina', name='Hankø Marina – brygger ved Vikaneveien', cls='smabathavn', basis='del_av_marina', descr=False, sources=HM, unc=True,
  note='To brygger med båter langs veien øst for marinaen. Gruppert med Hankø Marina; driftsgrense ikke dokumentert.')
d('A029', 'inc', group='hanko-yc', name='Hankø – Yacht Club og hotellets gjestehavn, vestre del', cls='smabathavn', basis='flere_brygger_med_minst_10_synlige_plasser', descr=False, unc=True,
  osm=['way/1539664077', 'way/1539664076'], note='Brygger ved Hankø Yacht Club og Hankø hotell (kro og gjestehavn) på Hankø. Fordeling mellom klubb-, gjeste- og faste plasser er ikke dokumentert.')
d('A030', 'add', extra=[[259520, 6571316], [259533, 6571315], [259554, 6571266], [259520, 6571212], [259510, 6571215], [259542, 6571264]], group='hanko-yc', name='Hankø – Yacht Club og hotellets gjestehavn, østre del', cls='smabathavn', basis='flere_brygger_med_minst_10_synlige_plasser', descr=False, unc=True,
  osm=['way/1539664076'], note='Lange brygger og molo øst for hotellet; ytre L-brygge manuelt tillagt etter overleggskontroll. Samme havnegruppe som vestre del.')
for c in ['A032', 'A033', 'A034', 'A035', 'A037', 'A038', 'A039']: d(c, 'exc', why=EXC_SMALL)
d('A036', 'inc', group='hanko-nv', name='Hankø nordvest – bryggeanlegg i vika', cls='mulig_smabathavn', basis='flere_brygger_men_felles_drift_eller_kapasitet_uklar', unc=True,
  note='Åtte–ti brygger med båter rundt en lun vik på Hankø. Mange plasser samlet, men bryggene kan tilhøre enkelte hytter; felles drift ikke dokumentert.')
d('A040', 'inc', group='vikane', name='Vikane – Fredrikstad Seilforening og Hankøsund båthavn', cls='smabathavn', basis='foreninger_og_marina_registrert_og_mange_synlige_plasser', descr=False, unc=True,
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/977478367', 'https://virksomhet.brreg.no/nb/oppslag/enheter/989347535'],
  note='Sammenhengende havneområde med mange brygger langs Vikane. Fredrikstad Seilforening (Vikaneveien 359) og Hankøsund Båthavn AS (Vikaneveien 315) har adresser her; interne operatørgrenser er ikke kartlagt.')
for c in ['A041', 'A045', 'A046', 'A048', 'A049']: d(c, 'exc', why=EXC_SMALL)
d('A042', 'exc', why='Tre lange brygger med få synlige båter; kan være fellesbrygger, men minst ti plasser eller felles drift er ikke dokumentert.')
d('A043', 'inc', group='a043', name='Bukta sør for Vikane – marina med fire brygger', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg',
  note='Fire lange brygger med utriggere og mange båter. Operatør ikke dokumentert.')
d('A044', 'inc', group='a044', name='Slevikkilen vest – marina med fem brygger', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', unc=True,
  note='Fem lange brygger med utriggere og mange båter. Operatør ikke dokumentert; Slevik og Ramseklo båtforening har tilknytning til området, men koblingen er ikke fastslått.')
d('A047', 'inc', group='oksrodkilen', name='Oksrødkilen – bryggeanlegg', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', unc=True,
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/816914302'],
  note='T-formet hovedbrygge med mange båter og flere korte brygger innerst i kilen. Østre Oksrød brygge (forening) er registrert ved Østre Oksrødkilen; koblingen er geografisk.')
for c in ['A050', 'A052', 'A055', 'A058']: d(c, 'exc', why=EXC_SMALL)
d('A057', 'exc', why='Brygge uten synlige båter i bildet; ikke dokumentert båtplassanlegg.')
d('A051', 'inc', group='a051', name='Smalt sund nord for Dypeklo – lang bryggerekke', cls='mulig_smabathavn', basis='lang_brygge_med_mange_synlige_baater_grovt_bilde', unc=True,
  note='Om lag 270 m brygge/kai langs et smalt sund med mange båter. Bare kontrollert i grovt oversiktsbilde (2,5 m/px); felles drift og plassantall ikke dokumentert.')
d('A053', 'inc', group='dypeklo', name='Dypeklo båtplass / Tyskerbrygga', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', descr=False, unc=True,
  osm=['way/1461597625', 'way/1352197007', 'way/1352197008'],
  note='Flere brygger og kai med mange båter. OSM-navn «Dypeklo båtplass» og «Tyskerbrygga». Operatør ikke dokumentert.')
d('A054', 'inc', group='a054', name='Helleskilen nord – brygge og kai', cls='mulig_smabathavn', basis='brygge_med_rundt_10_synlige_plasser', unc=True,
  note='Brygge med rundt ti båter og båter langs kaien nord for den (kaistrekningen er ikke tatt med). Helleskilen småbåthavn SA er registrert i området; koblingen er ikke fastslått.',
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/917765243'])
d('A056', 'inc', group='hubukta', name='Hubukta – felles brygge', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', descr=False, osm=['node/1924834873'],
  note='Lang brygge med rundt 15 båter. OSM-punkt «Hubukta» (marina). Operatør ikke dokumentert.')
for c in ['A059', 'A060', 'A061', 'A062']: d(c, 'exc', why=EXC_SMALL)
d('A063', 'inc', group='a063', name='Øyenkilen nord – brygger med utriggere', cls='smabathavn', basis='minst_10_synlige_plasser_utriggere', unc=True,
  note='Lang brygge med rundt 20 utriggerplasser og en kortere brygge. Vårbilde med få båter. Operatør ikke dokumentert; Øienkilen båtforening er registrert i området, koblingen er ikke fastslått.',
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/995705850'])
d('A064', 'inc', group='marnet', name='Marnet Marine Park / Marnetvika', cls='smabathavn', basis='marina_og_minst_10_synlige_plasser', descr=False, osm=['node/5134133052'],
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/818861052', 'https://virksomhet.brreg.no/nb/oppslag/enheter/913569113'],
  note='Flere lange brygger med utriggere. OSM «Marnet Marine Park»; Marnet Marina AS og Marnetvika båtforening AS er registrert her. Opplag på land er utelatt.')
d('A065', 'add', extra=[[262735, 6566470], [262785, 6566482], [262808, 6566420], [262800, 6566380], [262745, 6566385]], group='stranda', name='Stranda Marina, Øyenkilen',
  cls='smabathavn', basis='marina_og_minst_10_synlige_plasser', descr=False, unc=True, osm=['way/59396155'],
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/991443967'],
  note='Hovedbrygge med utriggere (OSM) og to sørlige brygger/kaier med båter (manuelt tillagt, ikke i OSM). Stranda Marina tar båter 10–35 fot.')
for c in ['A067', 'A068', 'A069', 'A070', 'A073']: d(c, 'exc', why=EXC_SMALL)
d('A071', 'inc', group='langoen', name='Langøen båtforening', cls='smabathavn', basis='forening_og_minst_10_synlige_plasser', descr=False, osm=['way/196876018'],
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/988115371'], note='Flere lange brygger med utriggere og mange båter. OSM-flate «Langøen Båtforening».')
d('A072', 'inc', group='a072', name='Langøya vest – brygger ved boligblokkene', cls='mulig_smabathavn', basis='flere_brygger_men_felles_drift_eller_kapasitet_uklar', unc=True,
  note='Tre T-brygger langs boligblokker; kan være boligsameiets felles anlegg. Felles drift og antall plasser ikke dokumentert. Bare kontrollert i grovt bilde.')
d('A074', 'inc', group='vikerkilen', name='Vikerkilen – båtforening og slipp', cls='smabathavn', basis='forening_og_minst_10_synlige_plasser', descr=False, osm=['node/5134159182'],
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/917118655'], unc=True,
  note='Flere brygger med båter innerst i Vikerkilen. Vikerkilen båtforening er registrert; OSM «Vikerkilen Slipp». Grensen mellom slipp/verksted og båtplasser er ikke kartlagt.')
for c in ['A075', 'A076', 'A078', 'A079', 'A080', 'A081']: d(c, 'exc', why=EXC_SMALL)
d('A077', 'inc', group='a077', name='Langøya sør – brygger med utriggere', cls='smabathavn', basis='minst_10_synlige_plasser_utriggere', unc=True,
  note='To brygger med mange utriggerplasser (vårbilde, få båter) og en kaistrekning nordover. Operatør ikke dokumentert.')
d('A082', 'inc', group='a082', name='Sandvika (Kråkerøy) – brygge med utriggere', cls='mulig_smabathavn', basis='brygge_med_rundt_15_utriggerplasser_uten_baater_i_bildet', unc=True,
  note='Én brygge med rundt 15 utriggerplasser; vårbilde uten båter. Sameiet Sandvika brygge er registrert i kommunen; koblingen er ikke fastslått.',
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/918795979'])
for c in ['A083', 'A084', 'A085', 'A086', 'A087', 'A088', 'A093']: d(c, 'exc', why=EXC_SMALL)
d('A089', 'inc', group='a089', name='Vesterelva nordvest – brygge ved industriområdet', cls='mulig_smabathavn', basis='flere_brygger_men_felles_drift_eller_kapasitet_uklar', unc=True,
  note='Brygge med få båter i kanalen; utriggere langs boligene på vestsiden er ikke tatt med. Felles drift og plassantall ikke dokumentert.')
d('A090', 'inc', group='a090', name='Vesterelva nord – lang brygge (Bjølstad)', cls='mulig_smabathavn', basis='lang_brygge_grovt_bilde', unc=True,
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/913700260'],
  note='Om lag 190 m brygge i kanal. Bjølstad motorbåtforening har adresse i nærheten; koblingen er geografisk. Bare grovt bilde.')
d('A092', 'inc', group='a092', name='Vesterelva vest – marina ved verkstedområdet', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', unc=True,
  note='Fire–fem brygger med utriggere og båter langs vestbredden. Operatør ikke dokumentert (flere marina- og verkstedforetak i området).')
for c in ['A094', 'A098', 'A101', 'A103', 'A105', 'A107']: d(c, 'exc', why=EXC_SMALL)
d('A100', 'inc', group='a100', name='Ålestranda / Bruket – brygger langs verkstedkaia', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', unc=True,
  note='Flere brygger med båter langs kaia ved båtverksteder og opplag. Flere marina- og verkstedforetak (bl.a. Gressvik Marina AS, Kjøkøysund Marina AS) har adresse på Bruket; operatørgrenser er ikke kartlagt. Opplag på land er utelatt.',
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/915773966', 'https://virksomhet.brreg.no/nb/oppslag/enheter/971594861'])
d('A104', 'inc', group='a104', name='Kjøkøy nord – båthavn med fire brygger', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', osm=['node/5105877544'],
  note='Fire brygger med båter. OSM-punkt «Småbåtshavn». Operatør ikke dokumentert; Kjøkøya båtforening er registrert i kommunen.',
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/995694549'])
for c in ['A109', 'A110', 'A112', 'A113', 'A114', 'A115', 'A116', 'A117']: d(c, 'exc', why=EXC_SMALL)
d('A111', 'inc', group='a111', name='Kjøkøy vest – båthavn med åtte brygger', cls='smabathavn', basis='flere_brygger_og_osm_smaabaathavn', unc=True, osm=['node/5106029772'],
  note='Sju–åtte brygger langs en lun vik; OSM-punkt «Småbåtshavn». Vårbilde med få båter, så plassantall er ikke talt. Operatør ikke dokumentert.')
for c in ['A118', 'A119', 'A120', 'A121', 'A122', 'A124', 'A125', 'A126', 'A127']: d(c, 'exc', why=EXC_SMALL + ' Hyttebrygger på Kjøkøy/Ålekjær-området.')
d('A134', 'exc', why=EXC_PRIV + ' Kråkerøy østside mot Glomma: 15–18 korte brygger langs boligtomter.')
for c in ['A135', 'A137', 'A138', 'A140', 'A141', 'A142']: d(c, 'exc', why=EXC_SMALL)
d('O1', 'exc', why='OSM «Hankøhavna» er en naturhavn/ankringsplass med oppankrede båter, ikke et båtplassanlegg med brygger.')
d('O3', 'exc', why='OSM mooring-områder i naturhavn; båter fortøyd til fjell, ikke båtplassanlegg.')
d('M001', 'man', coords=[[268097, 6563650], [268115, 6563655], [268150, 6563630], [268150, 6563600], [268140, 6563560], [268100, 6563560], [268093, 6563590]],
  group='kjokoy-ost', name='Kjøkøy øst – båthavn med to brygger', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', unc=True, osm=['node/5105877539'],
  note='To brygger med til sammen 12–14 synlige båter og båter ved land. OSM-punkt «Småbåtshavn»; brygger ikke i OSM, omriss tegnet manuelt i meter.')
GBF = ['https://www.havneweb.no/gressvik-bf/?mod=omhavnen', 'https://virksomhet.brreg.no/nb/oppslag/enheter/993774146']
OBH = ['https://www.havneweb.no/onsoy-bathavn/', 'https://virksomhet.brreg.no/nb/oppslag/enheter/968659405']
d('A066', 'split', parts=[
  dict(box=[265840, 6570440, 266200, 6570700], group='gressvik-bf', name='Gressvik båtforening – Vesterelven', cls='smabathavn', basis='operator_dokumenterer_faste_batplasser',
       descr=False, unc=True, sources=GBF, osm=['node/5134150525'], capacity=220, cap_source=GBF[0], cap_approx=True,
       note='Brygger innenfor moloen øst i Østkilen ved OSM-punkt «Gressvik Båtforening». Foreningen oppgir ca. 220 båtplasser i Vesterelven. Koblingen mellom foreningens plasser og dette bassenget er geografisk; nabobassenget i vest er registrert som Onsøy Båthavn.'),
  dict(minus=[265840, 6570440, 266200, 6570700], group='onsoy-bathavn', name='Onsøy Båthavn – Østkilen', cls='smabathavn', basis='operator_dokumenterer_faste_batplasser',
       descr=False, unc=True, sources=OBH, capacity=300, cap_source=OBH[0],
       note='Stor marina i Østkilen og bryggene sørover langs vestbredden. Onsøy Båthavn AS (Østkilen 5) oppgir 300 båtplasser i Vesterelven vest for Huthholmen. Grensen mot Gressvik båtforening er ikke dokumentert.')])
for c in ['A132', 'A133']: d(c, 'exc', why=EXC_SMALL)
d('A130', 'inc', group='isegran', name='Isegran og Gamlebyen – brygger rundt øya', cls='smabathavn', basis='flere_brygger_med_minst_10_synlige_plasser', unc=True,
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/893762302'],
  note='Flere brygger og kaier rundt Isegran og mot Gamlebyen med til sammen mange båter. Gamlebyens båtforening (Kongens brygge) og veteranbåtmiljøet på Isegran har tilknytning; operatørgrenser er ikke kartlagt.')
d('A131', 'inc', group='nokledypet', name='Nøkledypet båthavn / Kråkerøy båtforening', cls='smabathavn', basis='operator_dokumenterer_faste_batplasser', descr=False, osm=['node/367678069'],
  sources=['https://www.nokledypet.no/gjestehavn-2', 'https://virksomhet.brreg.no/nb/oppslag/enheter/971253312'], capacity=285, cap_source='https://www.nokledypet.no/gjestehavn-2', unc=True,
  note='Lange brygger langs Nøkledypet. Kråkerøy båtforening oppgir 285 båtplasser og gjestehavn. Opplag på land er utelatt. Nordre del av bryggene kan ligge utenfor polygonet.')
d('A136', 'inc', group='ora', name='Øra – båthavn ved industriområdet', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', osm=['way/69855707'], unc=True,
  sources=['https://www.havneweb.no/orabat/?mod=omhavnen', 'https://virksomhet.brreg.no/nb/oppslag/enheter/997027000'],
  note='Tre brygger med utriggere og båter; OSM «Småbåtshavn». Sannsynlig Øra båtforening (76 plasser ifølge foreningen), men koblingen er geografisk og kapasiteten er derfor ikke satt på polygonet.')
d('A091', 'inc', group='fjeldberg', name='Fjeldberg båthavn / Fredrikstad Motorbåtforening', cls='smabathavn', basis='forening_og_minst_10_synlige_plasser', descr=False, osm=['node/3638020925'],
  sources=['https://www.statsforvalteren.no/siteassets/fm-oslo-og-viken/miljo-og-klima/forurensning/mudring-ved-mosseveien-15/fredrikstad-motobatforening-tillatelse.pdf', 'https://virksomhet.brreg.no/nb/oppslag/enheter/971247916'],
  note='Stor marina med fem lange brygger. OSM «Fjeldberg båthavn». Fredrikstad Motorbåtforening har båtanlegg ved Mosseveien 15 like ved (mudringstillatelse fra Statsforvalteren); koblingen er geografisk.')
GH = 'Fredrikstad gjestehavn (OSM). Gjestehavn i sentrum; fast- og gjesteplassfordeling er ikke dokumentert.'
d('A095', 'add', extra=[[267220, 6570980], [267355, 6570980], [267355, 6571045], [267220, 6571045]], group='gjestehavn', name='Fredrikstad gjestehavn – vestre brygger', cls='smabathavn',
  basis='dokumentert_gjestehavn', descr=False, unc=True, osm=['node/5134112334'], note='Fire brygger langs kaia. ' + GH)
d('A096', 'inc', group='gjestehavn', name='Fredrikstad gjestehavn – østre brygge', cls='smabathavn', basis='dokumentert_gjestehavn', descr=False, unc=True, note='Brygge ved bygningene øst for de vestre bryggene. ' + GH)
d('A097', 'inc', group='a097', name='Vesterelva – bryggeanlegg ved boligene (Bruket)', cls='mulig_smabathavn', basis='flere_brygger_men_felles_drift_eller_kapasitet_uklar', unc=True,
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/922737037'],
  note='Basseng med flere brygger ved boligblokker. Bruket Brygge Marina AS er registrert på Bruket; koblingen og plassantall er ikke fastslått. Grovt bilde.')
d('A099', 'inc', group='vaerste', name='Værste – brygger ved boligene', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', unc=True,
  note='Fire brygger med utriggere og båter langs kaia ved Værste. Flere boligsameier (Værste brygge) er registrert; operatør ikke fastslått.')
d('A102', 'inc', group='rod', name='Rød båtforening', cls='smabathavn', basis='forening_og_minst_10_synlige_plasser', descr=False, osm=['node/3653923708'],
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/996181634'], note='Mange korte brygger med båter langs vestsiden av Kråkerøy ved OSM-punkt «Rød Båtforening».')
d('A106', 'inc', group='a106', name='Kjøkøy – bryggerekke langs vestsiden', cls='mulig_smabathavn', basis='flere_brygger_men_felles_drift_eller_kapasitet_uklar', unc=True, osm=['node/5105877544'],
  note='Rad med mange korte brygger; OSM-punkt «Småbåtshavn» i nærheten. Kan være private brygger ved hytter; felles drift ikke dokumentert.')
for c in ['A108', 'A123']: d(c, 'exc', why=EXC_SMALL)
d('A128', 'inc', group='kiaers-bruk', name='Kiærs Bruk marina', cls='smabathavn', basis='forening_og_minst_10_synlige_plasser', descr=False, osm=['node/3638019542'],
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/919891254'], note='Flere brygger langs Glomma ved OSM «Kiærs Bruk Marina»; Kiærs Bruk båtforening er registrert.')
d('A139', 'inc', group='a139', name='Kjøkøysund – bryggerekke ved brua', cls='mulig_smabathavn', basis='flere_brygger_men_felles_drift_eller_kapasitet_uklar', unc=True, osm=['node/5106029772'],
  note='Rad med korte brygger langs sundet; OSM «Småbåtshavn». Kan være private brygger; felles drift ikke dokumentert. Grovt bilde.')
d('A146', 'inc', group='a146', name='Glomma østside ved Selbak/Lisleby – lang brygge', cls='mulig_smabathavn', basis='lang_brygge_med_faa_baater_i_vaarbilde', unc=True,
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/991180400', 'https://virksomhet.brreg.no/nb/oppslag/enheter/918911871'],
  note='Om lag 180 m brygge med få båter i vårbildet. Selbak båtforening og Lisleby båtforening er registrert i området; koblingen er ikke fastslått.')
for c in ['A129', 'A143', 'A144', 'A145', 'A147', 'A148']: d(c, 'exc', why=EXC_SMALL)
d('A150', 'inc', group='nabbetorp', name='Nabbetorp båtforening', cls='smabathavn', basis='forening_og_minst_10_synlige_plasser', descr=False, osm=['node/3655591339'],
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/994522299'], note='Tre lange T-brygger med båter langs Glomma ved OSM «Nabbetorp Båtforening».')
d('A152', 'inc', group='a152', name='Øra sør – brygge med båter', cls='mulig_smabathavn', basis='brygge_med_rundt_10_synlige_plasser_svakt_bilde', unc=True,
  note='Brygge med rundt ti–femten båter. Bildet er gråskjært og uskarpt i dette området; felles drift ikke dokumentert.')
for c in ['A149', 'A151', 'A153', 'A154', 'A155', 'A156', 'A157']: d(c, 'exc', why=EXC_SMALL)
GREY = ' Bildet i dette området er gråskjært/uskarpt (mosaikkfeil); geometri og telling er usikre.'
ODK = ['https://virksomhet.brreg.no/nb/oppslag/enheter/991210849', 'https://virksomhet.brreg.no/nb/oppslag/enheter/990390746']
d('A160', 'inc', group='odegardskilen-n', name='Ødegårdskilen – lang felles brygge', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', unc=True, sources=ODK,
  note='Lang brygge med rundt 20 båter. Sameiet Ødegårdskilen brygge og Nordre Ødegårdkilen bryggeforening er registrert; hvilken som drifter denne bryggen er ikke fastslått.' + GREY)
d('A161', 'inc', group='odegardskilen-o', name='Ødegårdskilen øst – brygge', cls='mulig_smabathavn', basis='brygge_med_rundt_10_synlige_plasser', unc=True, sources=ODK,
  note='Brygge med rundt ti–tolv båter.' + GREY)
d('A163', 'inc', group='odegardskilen-s', name='Ødegårdskilen sørvest – brygge', cls='mulig_smabathavn', basis='brygge_med_rundt_10_synlige_plasser', unc=True,
  note='Kort brygge med rundt ti båter.' + GREY)
d('A164', 'inc', group='a164', name='Ødegårdskilen sør – brygge langs strandenga', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', unc=True,
  note='Brygge med rundt 15 båter langs land.' + GREY)
d('A165', 'inc', group='a165', name='Herretangen – dobbel brygge', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', unc=True,
  sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/930157961'],
  note='Brygge med båter på begge sider, rundt 20 plasser. Herretangen bryggeforening er registrert; koblingen er geografisk.' + GREY)
for c in ['A158', 'A159', 'A162', 'A166']: d(c, 'exc', why=EXC_SMALL)
for c in ['A167', 'A168', 'A171', 'A173']: d(c, 'exc', why=EXC_SMALL)
SKJ = ['https://virksomhet.brreg.no/nb/oppslag/enheter/991240535']
d('A169', 'inc', group='a169', name='Skjærviken vest – lang brygge', cls='mulig_smabathavn', basis='lang_brygge_uten_baater_i_bildet', unc=True, sources=SKJ,
  note='Om lag 220 m brygge uten synlige båter i bildet. Kan høre til Skjærviken båtforening; ikke dokumentert.' + GREY)
d('A170', 'inc', group='skjaerviken', name='Skjærviken båthavn', cls='smabathavn', basis='forening_og_minst_10_synlige_plasser', descr=True, unc=True, sources=SKJ,
  note='Tre–fire brygger med mange båter. Skjærviken båtforening har adresse Båthavnveien i Skjærviken; koblingen er geografisk.' + GREY)
d('A172', 'inc', group='a172', name='Torsnes øst – båthavn med lang brygge', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', unc=True,
  note='Lang brygge med utriggere og mange båter, og båter ved land. Operatør ikke dokumentert.' + GREY)
d('A174', 'inc', group='singlefjord-v', name='Singlefjorden vest – båthavn langs land, nordre del', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', unc=True,
  note='Rekke brygger med mange båter langs vestbredden av Singlefjorden, like ved kommunegrensen mot Hvaler/Sarpsborg. Operatør ikke dokumentert (flere foreninger på Torsnes).' + GREY)
d('A175', 'inc', group='singlefjord-v', name='Singlefjorden vest – båthavn langs land, søndre del', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', unc=True,
  note='Tre brygger med mange båter. Samme havnegruppe som nordre del; mellomliggende båter ved land er ikke tatt med.' + GREY)
for c in ['A176', 'A177']: d(c, 'exc', why=EXC_SMALL)
d('M002', 'man', coords=[[276762, 6565812], [276784, 6565816], [276842, 6565898], [276832, 6565916], [276812, 6565912], [276758, 6565834]],
  group='m002', name='Ødegårdskilen nordøst – brygge med båter ved gårdsvei', cls='smabathavn', basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', unc=True,
  note='Funnet i systematisk bildesøk (ikke i OSM): én brygge med rundt 15 båter og parkering/opplag ved land. Operatør ikke dokumentert.' + GREY)

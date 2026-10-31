"""Reproduce a field-level enrichment pilot from reviewed evidence, offline."""
import collections,csv,datetime,hashlib,json,pathlib,time
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=ROOT/'data/berikelse/3103-moss/pilot-01'
BASE=ROOT/'data/kommuner/3103-moss/rev-01'
def read(p):return json.loads(p.read_text())
def write(name,data): (OUT/name).write_text((json.dumps(data,ensure_ascii=False,separators=(',', ':')) if name.endswith('.geojson') else json.dumps(data,ensure_ascii=False,indent=2))+'\n')
def csvwrite(name,rows):
 if not rows:return
 with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';',lineterminator='\n');w.writeheader()
  for r in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else '' if v is None else v for k,v in r.items()})
fc=read(BASE/'bathavner.geojson'); groups=collections.defaultdict(list)
for f in fc['features']:groups[f['properties']['harbour_id']].append(f)
sources={s['source_id']:s for s in read(OUT/'sources.json')}
rows={};obs=[];issues=[]
for hid,fs in sorted(groups.items()):
 ps=[f['properties'] for f in fs];p=ps[0]
 rows[hid]=dict(harbour_id=hid,name_baseline=p['name'],polygon_ids=[p['id'] for p in ps],classification_baseline=p['classification'],water_environment='freshwater' if hid=='3103-H11' else 'marine',pilot_status='reviewed_not_approved',reviewed_date='2026-10-31',operator_name=None,operator_org_no=None,operator_link_status='unresolved',berths_published=None,berths_approximate=None,berths_scope=None,guest_berths_published=None,dinghy_berths_published=None,winter_storage_berths_published=None,land_storage_reported=None,lifting_reported=None,ramp_reported=None,wash_area_reported=None,wastewater_treatment_current=None,operation_evidence_status='not_verified',current_operation_verified=None,reference_date=None,baseline_berth_values=[{'polygon_id':p['id'],'value':p.get('berth_count_published'),'source':p.get('berth_count_source'),'reference_period':p.get('berth_count_reference_period'),'scope':p.get('berth_count_scope')} for p in ps if p.get('berth_count_published') is not None],baseline_notes=[p.get('note','') for p in ps],source_ids=['S14'] if any('avfallsplan' in u for p in ps for u in p.get('sources',[])) else [],observation_ids=[],geometry_review_status='not_reassessed',identity_quality='unresolved',capacity_quality='unknown',function_quality='unknown',temporal_quality='unknown')
def observation(hid,field,value,sid,anchor,note='',scope='whole_harbour',status='published_undated',reference_date=None,approximate=None,promote=True):
 source=sources[sid];assert source['retrieval_status']=='retrieved',sid
 text=(ROOT/source['snapshot_path']).read_text();lines=text.splitlines();hits=[i+1 for i,l in enumerate(lines) if anchor.lower() in l.lower()];assert hits,(sid,anchor)
 oid=f'OBS-{len(obs)+1:03}'
 o=dict(observation_id=oid,subject_id=hid,field=field,value=value,unit='berths' if 'berths' in field else None,approximate=approximate,scope=scope,status=status,reference_date=reference_date,source_id=sid,source_url=source['url'],accessed_utc=source['accessed_utc'],evidence_lines=hits,note=note)
 obs.append(o)
 if hid in rows:
  r=rows[hid];r['observation_ids'].append(oid)
  if sid not in r['source_ids']:r['source_ids'].append(sid)
  if promote and field in r:r[field]=value
 return oid
def operator(hid,sid,name,org=None,link='operator_published_baseline_location',anchor=None):
 observation(hid,'operator_name',name,sid,anchor or name,scope='operator_relation')
 r=rows[hid];r['operator_link_status']=link;r['identity_quality']=link
 if org:
  j=read(ROOT/sources['BR'+org]['snapshot_path']);observation(hid,'registered_entity_name',j['navn'],'BR'+org,'"navn"',scope='organisation_only',status='register_verified',note='Registeridentitet dokumenterer ikke alene stedfesting eller faktisk drift.')
  r['operator_org_no']=org
 r['operation_evidence_status']='operator_service_published_date_unknown'
def cap(hid,n,sid,anchor,approx=False,scope='published_berth_capacity_guest_inclusion_unknown',note=''):
 observation(hid,'berths_published',n,sid,anchor,note,scope,approximate=approx)
 rows[hid].update(berths_approximate=approx,berths_scope=scope,capacity_quality='source_published_reference_date_unknown',temporal_quality='accessed_2026-10-31_reference_date_unknown')
def issue(hids,kind,description,next_step,sids):
 issues.append(dict(issue_id=f'MOSS-E-{len(issues)+1:02}',harbour_ids=hids,kind=kind,status='open',description=description,next_step=next_step,source_ids=sids))
operator('3103-H01','S01','Fiske Båtforening',anchor='Fiske Båtforening ble stiftet')
cap('3103-H01',376,'S01','Foreningen har 376')
observation('3103-H01','lifting_reported',True,'S01','ny kran',note='Kranopplysning viser til utbedring i 2006; dagens tilgjengelighet ikke kontrollert.',status='historical',reference_date='2006',promote=False)
observation('3103-H01','winter_afloat_reported',True,'S01','utleie av båtplasser for vinter',note='Vinterplass i sjø; ikke opplag på land.')
operator('3103-H02','S02','Rygge Båtforening',anchor='Rygge Båtforening eier og driver')
cap('3103-H02',409,'S02','409 båtplasser',scope='operator_published_berths_separately_lists_7_guest',note='409 og 7 beholdes separat; ingen automatisk summering.')
observation('3103-H02','guest_berths_published',7,'S02','7 faste gjesteplasser',approximate=False,scope='dedicated_guest_berths')
observation('3103-H02','lifting_capacity_tonnes_historical',8,'S02','kran inntil 8 tonn',status='historical',reference_date='2006',note='Ikke nåverifisert teknisk kapasitet.')
operator('3103-H03','S03','Kambo Båtforening','996958663',anchor='Kambo Båtforening ligger')
cap('3103-H03',100,'S03','ca. 100 båtplasser',True)
for field,anchor in [('land_storage_reported','vinteropplagsmuligheter'),('lifting_reported','moderne truck'),('ramp_reported','utsettingsrampe')]:observation('3103-H03',field,True,'S03',anchor)
observation('3103-H03','guest_service_reported',True,'S03','ledige gjesteplasser',note='Antall gjesteplasser er ikke dokumentert.')
operator('3103-H04','S04','Kambo Marina AS','958467362',anchor='Kambo Marina AS er')
cap('3103-H04',300,'S04','marina med plass til 300')
observation('3103-H04','land_storage_reported',True,'S04','Båtopplag',note='Tjeneste lenket i operatørens navigasjon; kapasitet og landavgrensning ikke bekreftet.')
operator('3103-H05','S05','Moss Motorbåtforening','883336402',anchor='Moss Motorbåtforening ligger')
cap('3103-H05',360,'S05','ca 360 båter på vann',True,scope='boats_afloat_capacity')
observation('3103-H05','winter_storage_berths_published',200,'S05','200 båter på land',approximate=None,scope='land_winter_storage',note='Kildesetningen bruker ca. om sjøkapasitet; presisjonsnivået for 200 landplasser er ikke uttrykkelig avklart.')
observation('3103-H05','land_storage_reported',True,'S05','200 båter på land')
# Geography and operator allocations in Rørvika remain unresolved.
for org in ['913241045','917198616']:
 j=read(ROOT/sources['BR'+org]['snapshot_path']);observation('3103-H06','candidate_registered_entity',{'org_no':org,'name':j['navn']},'BR'+org,'"navn"',scope='candidate_operator_only',status='register_verified',note='Kildekobling til akkurat dette sjøpolygonet er ikke bekreftet.',promote=False)
operator('3103-H07','S06','Nasle Bryggesameie','985441464',link='historical_operator_baseline_geographic_link',anchor='Bryggesameie')
rows['3103-H07']['operation_evidence_status']='historical_website_2010_2011_only';rows['3103-H07']['temporal_quality']='historical_2010_2011'
observation('3103-H07','historical_website_activity','2011-08-13','S06','august 13, 2011',status='historical',reference_date='2011-08-13')
observation('3103-H08','hotel_berth_booking_reported',True,'S16','booke plass på bryggen',scope='hotel_marina_internal_extent_unverified',note='Tjenestetilbud, ikke bevis på Fische AS som nåværende operatør eller kapasitet 70.')
rows['3103-H08']['operation_evidence_status']='hotel_service_published_extent_unverified';rows['3103-H08']['source_ids'].append('BR990894116')
operator('3103-H10','S07','Moss Seilforening','882921662',anchor='Moss Seilforening og vår havn')
cap('3103-H10',306,'S07','306 båtplasser',scope='operator_published_berths_guest_use_of_members_places',note='Litt over 300 faste plasser på S08 støtter størrelsesorden; gjestebruk er ikke ekstra kapasitet.')
for field,anchor in [('land_storage_reported','vinteropplag på land'),('lifting_reported','løft med truck'),('ramp_reported','sjøsettingsrampe')]:observation('3103-H10',field,True,'S08',anchor)
observation('3103-H10','guest_service_reported',True,'S07','medlemmenes faste plasser',note='Ingen ekstra gjesteplasskapasitet lagt til.')
observation('3103-H10','wash_area_historical',True,'S14','Oljeutskiller er montert ved spyleplass',status='historical',scope='plan_row_6',note='Historisk plan ca. 2020, eksakt referansedato ukjent. Oljeutskiller dokumenterer ikke dagens rensing av bunnstoff/metaller.')
operator('3103-H11','S09','Vansjø Båtforening','983392229',anchor='Vansjø Båtforening:')
cap('3103-H11',168,'S09','168 båtplasser',scope='ordinary_berths_excluding_separately_reported_dinghy_berths')
observation('3103-H11','dinghy_berths_published',16,'S09','16 jolleplasser',scope='children_dinghy_berths',approximate=False,note='Holdes separat; 168+16 presenteres ikke som 184 sammenlignbare faste plasser.')
operator('3103-H12','S10','Verket Havn AS','918686878',anchor='Utleier er Verket Havn AS')
observation('3103-H12','guest_service_reported',True,'S10','DROP-IN GJESTEHAVN',note='Gjesteområdet beskrives utenfor småbåthavna og nord for Rabben; eksakt samsvar med baselinepolygonet krever kartkontroll.')
observation('3103-H12','launching_permitted_historical',False,'S10','Utsetting og opptak av båt tillates ikke',status='historical',reference_date='2025',note='Vilkår merket sesong 2025, mens pristabellen er for 2027; ikke fylt som någjeldende nei til rampe.')
# These register matches enrich identity without confirming geographic operator limits.
for hid,org in [('3103-H13','995878321'),('3103-H14','922347034'),('3103-H15','930391204'),('3103-H17','982743354'),('3103-H18','912159515'),('3103-H22','920520111')]:
 j=read(ROOT/sources['BR'+org]['snapshot_path']);observation(hid,'candidate_registered_entity',{'org_no':org,'name':j['navn']},'BR'+org,'"navn"',scope='candidate_operator_only',status='register_verified',note='Navn/organisasjon verifisert; operatørens geografiske omfang er ikke bekreftet på nytt.',promote=False)
 rows[hid]['identity_quality']='register_entity_found_geographic_link_unresolved'
operator('3103-H16','S11','Vindsteg AS; Arbeidernes Båtforening Moss; tredje utleier uavklart',link='multiple_operators_internal_boundaries_unresolved',anchor='Vindsteg AS er én av dem')
for org,sid,anchor in [('991373721','S11','Vindsteg AS er én av dem'),('979250029','S12','Arbeidernes Båtforening Moss')]:
 j=read(ROOT/sources['BR'+org]['snapshot_path']);observation('3103-H16','operator_component',{'org_no':org,'name':j['navn']},sid,anchor,scope='suboperator',note='Ikke eksklusiv operatør for hele havnegruppen.')
 observation('3103-H16','registered_entity_name',j['navn'],'BR'+org,'"navn"',scope='organisation_only',status='register_verified')
observation('3103-H16','ramp_reported',True,'S11','Rampa er gratis',scope='bay_shared_ramp_location_not_digitised')
observation('3103-H16','winter_berthing_reported',True,'S11','Vinterplass',scope='Vindsteg_only',note='Oppgitt vinterplass er ikke dokumentasjon på vinteropplag på land.')
operator('3103-H19','S13','Moss Havn KF',anchor='Moss Gjestehavn har båtplasser')
observation('3103-H19','guest_service_reported',True,'S13','Moss Gjestehavn har båtplasser',note='Kilden beskriver begge sider av kanalen og Tollbodbrygga; ingen ny oppmåling eller kapasitetstelling.')
operator('3103-H21','S17','Sameiet Røedsstranda','993100544',link='sales_listing_and_baseline_location',anchor='Sameiet Røedsstranda har i over 30 år')
cap('3103-H21',16,'S17','brygge og 16 båtplasser',scope='whole_shared_facility',note='Salgsopplysning, ikke operatørbekreftelse; oppgitt sist endret 2026-09-08, ukjent faktisk tellingstidspunkt.')
# Preserve every old capacity assertion at its original component scope, including unallocated records.
for hid,fs in groups.items():
 seen=set()
 for f in fs:
  for c in f['properties'].get('source_register_members',[]):
   n=c.get('number');key=json.dumps(c,sort_keys=True)
   if key in seen:continue
   seen.add(key)
   observation(hid,'historical_capacity_component',{'source_name':c.get('name'),'berths':c.get('berth_count'),'guest_berths':c.get('guest_count'),'link_status':c.get('link_status')},'S14',c.get('name','').split(' (')[0].replace('Fuglevik Båthavn v/Rygge Båtforening','Fuglevik Båthavn v/Rygge Båtforening'),scope='avfallsplan_row_'+str(n),status='historical',note='Historisk plan ca. 2020, dato ikke bekreftet. Kildens rad er ikke en bekreftet geografisk operatørgrense. Ingen automatisk summering.',promote=False)
# New service candidate is recorded without assigning it to the neighbouring boat association.
observation('SERVICE-fuglevik','land_storage_reported',True,'S18','vinteropplag i mossedistriktet',scope='separate_service_operator',note='Fuglevik Båtservice er ikke automatisk Rygge Båtforening eller dens kapasitet.')
candidates=[]
for cid,name,org,n in [('C-SJEKTA','Båtforeningen Sjekta','990798664',4),('C-REFSNES','Refsnes småbåtforening','916250258',5)]:
 j=read(ROOT/sources['BR'+org]['snapshot_path']);observation(cid,'registered_entity_name',j['navn'],'BR'+org,'"navn"',scope='organisation_only',status='register_verified')
 anchor='Sjekta AS' if n==4 else 'Refsnes småbåtfore'
 observation(cid,'historical_plan_capacity',169 if n==4 else 80,'S14',anchor,scope='avfallsplan_row_'+str(n),status='historical',note='Plasstype og eventuell kobling til sjø-/landanlegg er uavklart; ikke lagt til totalsum.')
 candidates.append(dict(candidate_id=cid,name=name,org_no=org,baseline_candidate_ids=['AVP-'+str(n),'OSM-way/'+('29593396' if n==4 else '1513385299')],harbour_id=None,geometry=None,status='unresolved_no_new_geometry',identity_status='registered_entity_verified',operation_status='not_verified',capacity_current=None,land_function_status='hypothesis_not_verified',next_action='Dokumenter operatørens faktiske anlegg og funksjon mot datert bilde eller stedsspesifikk primærkilde; registeradresse gir ikke sjøposisjon.'))
issue(['3103-H01'],'capacity_difference','Operatørens udaterte side oppgir 376; eldre avfallsplan oppgir 384.','Behold begge observasjoner. Innhent referanseår før forskjellen tolkes som faktisk endring.',['S01','S14'])
issue(['3103-H10'],'capacity_precision','Havneweb oppgir 306; operatørens hovedside litt over 300; eldre plan 380.','Bruk 306 som kildeoppgitt, udatert verdi i pilot. Ikke erklær en målt nedgang eller legg gjestebruk til faste plasser.',['S07','S08','S14'])
issue(['3103-H11'],'capacity_categories','Operatøren skiller 168 båtplasser og 16 jolleplasser; eldre plan har 185 uten samme kategorisering.','Bevar separate kategorier og ferskvannsattributt. Avklar om kildene dekker samme anlegg og tidspunkt.',['S09','S14'])
issue(['3103-H06','3103-H20'],'operator_allocation','Rørvika har flere aktører og uavklarte interne grenser. Org.nr. 913241045 heter nå FJELLSMELL AS i registeret.','Dokumenter sammenhengen mellom registerenhet, brygger og kildens 29+29 plasser; ikke summer eller fordel nå.',['S14','BR913241045','BR917198616'])
issue(['3103-H08','3103-H09'],'operator_change_or_name_change','Org.nr. 990894116 fra den eldre Fische-raden har nå navnet LARKOLLVEIEN 801 AS. Hotellet tilbyr båtplassbooking; dette avklarer ikke polygonenes operatørgrenser.','Kontroller eier-/driftsrelasjon og stedfestet marinaoversikt før navne- eller kapasitetsendring.',['S14','S16','BR990894116'])
issue(['3103-H16'],'multi_operator','Vindsteg beskriver tre utleiere; ABF beskriver egne sesongplasser i samme bukt.','Bevar felles fysisk havnegruppe; registrer kapasitet på operatørnivå når omfang er kjent.',['S11','S12','S14'])
issue(['3103-H12'],'mixed_reference_periods','Verket-nettsiden blander leiepriser for 2027 og vilkår merket 2025.','Ikke erklær alle tjenester eller restriksjoner som gjeldende i 2026. Kontroller også gjesteområdene utenfor eksisterende polygon.',['S10'])
issue(['3103-H17','3103-H18'],'identity_boundary','Moss Marina og Sameie Fleischer Brygge Båthavn er bekreftede registerenheter. Registertreff bekrefter ikke interne sjøgrenser.','Stedfestet operatørkart eller dokument med bryggereferanser kreves før 125 og 34 plasser kan knyttes sikkert til polygonene.',['BR982743354','BR912159515','S14'])
issue([],'open_candidates','Sjekta og Refsnes småbåtforening finnes i registeret, men sjøpolygon og nåværende plasstype er fortsatt uavklart. Refsnes-nettstedet var utilgjengelig i dette miljøet.','Følg opp C-SJEKTA og C-REFSNES separat fra godkjente anlegg. Ingen automatisk innlemming.',['BR990798664','BR916250258','S14','S15'])
issue(['3103-H02'],'separate_land_service','Fuglevik Båtservice tilbyr vinteropplag nær Fuglevik båthavn. Det er en separat tjenesteaktør.','Avklar kobling og landlokasjon; ikke tilordne servicebedriftens opplag til båtforeningens sjøpolygon.',['S02','S18'])
# Each row's explicit unknown fields remain unknown. Published services never prove physical present-day operation.
for r in rows.values():
 if any(o['subject_id']==r['harbour_id'] and o['field'] in ['land_storage_reported','lifting_reported','ramp_reported'] and o['status']=='published_undated' for o in obs):r['function_quality']='some_services_published_reference_date_unknown'
 r['source_ids']=list(dict.fromkeys(r['source_ids']))
write('harbours.json',list(rows.values()));csvwrite('harbours.csv',list(rows.values()));write('observations.json',obs);csvwrite('observations.csv',obs);write('candidates.json',candidates);csvwrite('candidates.csv',candidates);write('deviations.json',issues);csvwrite('deviations.csv',issues)
# Reference export copies baseline geometry verbatim; metadata is explicitly a pilot overlay.
joined=json.loads(json.dumps(fc))
for f in joined['features']:
 r=rows[f['properties']['harbour_id']]
 f['properties']['enrichment_pilot']={k:v for k,v in r.items() if k not in ['baseline_notes','baseline_berth_values']}
joined['name']='Moss approved geometry with unapproved enrichment pilot overlay'
write('reference-map.geojson',joined)
baseline=read(OUT/'baseline.json');unchanged=all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in baseline['files'].items());assert unchanged
assert len(rows)==22 and len(fc['features'])==26
metrics=dict(harbours_reviewed=len(rows),baseline_polygons=len(fc['features']),open_candidates=len(candidates),observations=len(obs),sources_attempted=len(sources),sources_retrieved=sum(s['retrieval_status']=='retrieved' for s in sources.values()),sources_failed=sum(s['retrieval_status']=='failed' for s in sources.values()),harbours_with_newly_checked_numeric_berth_claim=sum(r['berths_published'] is not None for r in rows.values()),harbours_with_operator_name_recorded=sum(r['operator_name'] is not None for r in rows.values()),harbours_with_land_storage_publication=sum(r['land_storage_reported'] is True for r in rows.values()),harbours_with_dated_current_operation_verification=0,harbours_with_current_treatment_verification=0,land_polygons_created=0,approved_files_unchanged=unchanged,deviations=len(issues))
write('metrics.json',metrics)
write('timing.json',dict(started_utc=baseline['started_utc'],finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_wall_seconds=round(time.time()-baseline['started_unix'],1),scope='Baseline capture through last build; excludes initial reconnaissance before baseline capture. No token or cost measurement.'))
print(json.dumps(metrics,ensure_ascii=False,indent=2))

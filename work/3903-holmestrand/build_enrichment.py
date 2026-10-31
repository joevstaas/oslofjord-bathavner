"""Offline Holmestrand source review. Never modifies approved geometry or website data."""
import collections,csv,datetime,hashlib,json,pathlib,time
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=ROOT/'data/berikelse/3903-holmestrand/pilot-01';BASE=ROOT/'data/kommuner/3903-holmestrand/rev-01'
def read(p):return json.loads(p.read_text())
def save(name,data):
 (OUT/name).write_text((json.dumps(data,ensure_ascii=False,separators=(',',':')) if name.endswith('.geojson') else json.dumps(data,ensure_ascii=False,indent=2))+'\n')
def table(name,rows):
 save(name+'.json',rows)
 if rows:
  with (OUT/(name+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';',lineterminator='\n');w.writeheader()
   for r in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else '' if v is None else v for k,v in r.items()})
sources={s['source_id']:s for s in read(OUT/'sources.json')};fc=read(BASE/'bathavner.geojson');groups=collections.defaultdict(list)
for f in fc['features']:groups[f['properties']['harbour_id']].append(f)
rows={};observations=[];deviations=[]
for hid,fs in sorted(groups.items()):
 p=fs[0]['properties'];rows[hid]=dict(harbour_id=hid,name_baseline=p['name'],polygon_ids=[f['properties']['id'] for f in fs],legacy_status=p['status'],classification_baseline=p.get('classification'),pilot_status='source_review_not_geometry_approval',reviewed_date='2026-10-31',water_environment='freshwater' if hid=='3903-K05' else 'marine',operator_name=None,operator_org_no=None,operator_link_status='unresolved',berths_published=None,berths_approximate=None,capacity_components=[],capacity_group_ids=[],guest_berths_published=None,land_storage_reported=None,ramp_reported=None,own_crane_reported=None,wash_area_reported=None,wastewater_treatment_current=None,current_operation_verified=None,operation_evidence_status='not_verified',reference_date=None,source_ids=[],observation_ids=[],identity_quality='unresolved',capacity_quality='unknown',function_quality='unknown',geometry_review_status='not_reassessed_topographic_pilot',needs_orthophoto_review=True,baseline_notes=[f['properties'].get('note','') for f in fs])
def obs(subject,field,value,sid,anchor,scope='whole_harbour_operator_publication',status='published_undated',date=None,approximate=None,note='',promote=False):
 source=sources[sid];assert source['retrieval_status']=='retrieved',(sid,field)
 lines=(ROOT/source['snapshot_path']).read_text().splitlines();hits=[i+1 for i,l in enumerate(lines) if anchor.lower() in l.lower()];assert hits,(sid,anchor)
 oid=f'HS-OBS-{len(observations)+1:03}'
 observations.append(dict(observation_id=oid,subject_id=subject,field=field,value=value,scope=scope,status=status,reference_date=date,approximate=approximate,source_id=sid,source_url=source['url'],accessed_utc=source['accessed_utc'],evidence_lines=hits,note=note))
 if subject in rows:
  r=rows[subject];r['observation_ids'].append(oid)
  if sid not in r['source_ids']:r['source_ids'].append(sid)
  if promote:r[field]=value
 return oid
def op(hid,name,org,sid,anchor,link='operator_published_baseline_location'):
 obs(hid,'operator_name',name,sid,anchor,scope='operator_relation',promote=True)
 j=read(ROOT/sources['BR'+org]['snapshot_path']);obs(hid,'registered_entity_name',j['navn'],'BR'+org,'"navn"',scope='organisation_only',status='register_verified',note='Registeridentitet gir ikke alene havneposisjon eller faktisk drift.')
 rows[hid].update(operator_org_no=org,operator_link_status=link,identity_quality=link,operation_evidence_status='source_published_not_field_verified')
def issue(hids,kind,description,next_step,sids):
 deviations.append(dict(issue_id=f'HOLMESTRAND-E-{len(deviations)+1:02}',harbour_ids=hids,kind=kind,status='open',description=description,next_step=next_step,source_ids=sids))
for hid in ['3903-H01','3903-H02']:
 op(hid,'Holmestrand Småbåthavn AS','936760600','HS01','Daglig leder og styret i Holmestrand Småbåthavn AS',link='operator_published_multiple_sites_no_internal_allocation')
 rows[hid]['capacity_group_ids']=['HS-GROUP-CITY-OPERATOR']
 obs(hid,'dated_operation_notice','Vinterhavn 2026/27; oppdatert 06.10.2026','HS01','Oppdatering 06.10.2026.',scope='operator_wide_not_every_polygon',status='dated_operator_notice',date='2026-10-06',note='Datering gjelder kun den konkrete publiserte meldingen, ikke alle kapasitets- eller driftsopplysninger.')
 rows[hid]['operation_evidence_status']='dated_operator_notice_not_field_verified'
obs('HS-GROUP-CITY-OPERATOR','berths_published',1100,'HS02','rundt 1100 faste båtplasser',scope='municipal_operator_total_multiple_sites_no_allocation',approximate=True,note='Ikke 1100 på hvert anlegg eller hvert delpolygon. Kapasitetens referanseår er ukjent; nettsidens endringsdato er noe annet.')
obs('HS-GROUP-CITY-OPERATOR','winter_afloat_reported',True,'HS02','vinterhavn i bobleanlegg',scope='operator_wide_no_allocation',note='Vinterhavn i sjø er ikke landopplag.')
obs('HS-GROUP-CITY-OPERATOR','legacy_operator_name','Holmestrand Småbåthavn DA','HS02','drives av Holmestrand Småbåthavn DA',scope='operator_relation',note='Kommunens side har eldre selskapsform enn operatørens melding; navn holdes som motstridende kildeopplysning.')
obs('HS-GROUP-CITY-OPERATOR','registered_legacy_entity_status',{'org_no':'985747970','underAvvikling':True},'BR985747970','"underAvvikling": true',scope='organisation_only',status='register_verified')
obs('HS-GROUP-CITY-GUEST','guest_berths_published',50,'HS03','omtrent 50 båter',scope='city_guest_quays_longside_capacity_depends_on_boat_size',approximate=True,note='Gjelder gjestekai i sentrum; eksakt kobling til de to bassengpolygonene er ikke kontrollert. Ikke tillegg til 1100 uten avklaring av omfang.')
obs('HS-GROUP-CITY-GUEST','guest_quay_length_m',450,'HS03','450 meter med longside',scope='guest_quays_not_berth_count',note='450 er meter kailengde, ikke 450 båtplasser.')
obs('HS-GROUP-CITY-OPERATOR','association_allocates_places',False,'HS17','tildeler ikke båtplasser',scope='Holmestrand_Baatforening_only',note='Båtforeningen viser til havneselskapet for plass; forening og operatør er ikke samme rolle.')
rows['3903-H01']['capacity_group_ids'].append('HS-GROUP-CITY-GUEST')
capacity_groups=[dict(group_id='HS-GROUP-CITY-OPERATOR',name='Holmestrand Småbåthavn – operatørens samlede tilbud',related_harbour_ids=['3903-H01','3903-H02'],berths_published=1100,approximate=True,scope='operator_total_not_allocated_to_basins_or_sites',reference_date=None,observation_ids=[o['observation_id'] for o in observations if o['subject_id']=='HS-GROUP-CITY-OPERATOR'],mapping_status='related_existing_sites_exact_capacity_extent_unverified'),dict(group_id='HS-GROUP-CITY-GUEST',name='Holmestrand gjestekai i sentrum',related_harbour_ids=['3903-H01'],berths_published=50,approximate=True,scope='guest_boat_capacity_depends_on_boat_size_not_added_to_fixed_places',reference_date=None,observation_ids=[o['observation_id'] for o in observations if o['subject_id']=='HS-GROUP-CITY-GUEST'],mapping_status='exact_quay_to_polygon_allocation_unverified')]
op('3903-H03','Nordre Jarlsberg Brygge Marina AS','912886786','HS05','Nordre Jarlsberg Brygge Marina AS')
for sid,n in [('HS04',450),('HS05',397)]:obs('3903-H03','berths_published',n,sid,f'{n}',scope='NJB_operator_publication',approximate=False,note='To operatørpubliseringer gir ulike tall uten sammenlignbar referansedato; ingen enkeltverdi er valgt.')
rows['3903-H03']['capacity_quality']='conflicting_operator_publications'
obs('3903-H03','guest_service_reported',True,'HS04','liten gjestebrygge',note='Antall gjesteplasser er ikke oppgitt.')
obs('3903-H03','ramp_reported',True,'HS06','benytte utsettingsrampen',promote=True)
obs('3903-H03','own_crane_reported',False,'HS06','Nei det har vi',note='Operatørens udaterte FAQ svarer nei på egen kran; kranfirma kan kontaktes. Dette er ikke fravær av løftetjenester i området.',promote=True)
obs('3903-H03','storage_offer_reported',True,'HS18','Opplagspriser',note='Publisert opplagstilbud; antall og landgeometri er ikke oppgitt. Filnavnets 20260605 brukes ikke som observasjonsdato.')
obs('3903-H03','land_storage_reported',True,'HS06','Bobil på opplagsplass',note='FAQ bekrefter landbasert opplags-/parkeringsareal; bobilparkering er ikke båtkapasitet.',promote=True)
rows['3903-H03']['function_quality']='published_service_claims_reference_date_unknown'
op('3903-H04','Sande & Havna Båtforening','997317599','HS09','Sande & Havna Båtforening')
obs('3903-H04','historical_municipal_facility','Eksisterende småbåthavn','HS15','Sande Båtforening',scope='municipal_inventory_row',status='historical',date='2020',note='Anleggsplan 2020–2028, PDF-side 18. Ikke nåverifisert kapasitet eller omriss.')
op('3903-H05','Bjerkøya Båtforening','896548972','HS07','Bjerkøya båtforening har')
components=[]
for field,n,anchor in [('member_share_places',155,'155 medlemsplasser'),('rental_places',62,'62 plasser')]:
 oid=obs('3903-H05',field,n,'HS07',anchor,scope='operator_capacity_component',approximate=False,note='Kilden sier at 62 utleieplasser kommer i tillegg til 155 andelsplasser. Begge kategorier beholdes separat; ingen samlet polygonkapasitet konstrueres.')
 components.append({'kind':field,'value':n,'observation_id':oid})
rows['3903-H05']['capacity_components']=components;rows['3903-H05']['capacity_quality']='separate_published_components_no_aggregate'
obs('3903-H05','directory_berths_published',155,'HS16','155',scope='directory_unspecified_capacity',approximate=False,note='155 i katalogen kan være delmengden andelsplasser; ikke nødvendigvis motstrid med operatørens 155+62.')
obs('3903-H05','ramp_reported',True,'HS07','utkjøringsrampe',promote=True)
obs('3903-H05','lifting_ramp_reported',True,'HS07','rampe for å løfte',note='Rampe for større båter er ikke i seg selv dokumentasjon på egen kran.')
obs('3903-H05','expansion_reported','Bryggeutvidelse omtalt som beregnet klar for sesong 2026','HS08','sesongen 2026',scope='operator_plan_and_news',status='planned_or_progress_publication',note='Nyere bryggeomtale krever bildekontroll før pilotens gamle kartomriss kan revurderes.')
rows['3903-H05']['function_quality']='published_ramps_no_geometry_review'
op('3903-H06','Gyltesø Båtforening','912086275','HS15','Gyltesø Småbåthavn',link='historical_municipal_operator_and_register_baseline_location')
# Correct the source status: the municipal facility document is historical, not a current operator publication.
for o in observations:
 if o['subject_id']=='3903-H06' and o['field']=='operator_name':o.update(status='historical',reference_date='2020',note='Anleggsplan 2020–2028, PDF-side 22. Ikke bevis på drift i dag.')
rows['3903-H06']['operation_evidence_status']='historical_municipal_record_and_current_registry_only'
op('3903-H07','Holm Brygge AS','987352965','HS10','Vi tilbyr båtplasser')
# Existing possible facilities retain uncertain classifications and do not inherit neighbouring operators.
obs('3903-K05','candidate_operator_offer','Thorrud Camping tilbyr båtplasser','HS11','Sikre fortøyninger',scope='camping_offer_not_allocated_to_two_baseline_polygons',note='Nord/sør-bryggene kan ikke tilordnes operatøren sikkert fra tekstkilden; operator_name er fortsatt null.')
obs('3903-K05','non_boat_capacity',130,'HS12','130 faste plasser',scope='camping_seasonal_pitches_not_boat_places',approximate=False,note='130 gjelder campingplasser. Dette tallet er eksplisitt utelatt fra båtplasskapasitet.')
obs('3903-K05','berth_price_nok',1000,'HS13','Bryggeplass for båt',scope='price_not_capacity',note='Pris er ikke antall båtplasser. Kapasiteten er ukjent.')
# Preserve the previously recorded supplement without adopting its polygon or inventing a new harbour ID.
org=read(ROOT/sources['BR915094821']['snapshot_path'])
obs('C-VALE','registered_entity_name',org['navn'],'BR915094821','"navn"',scope='organisation_only',status='register_verified',note='Ingen ny stedfesting eller kapasitet er bekreftet.')
candidates=[dict(candidate_id='C-VALE',name='Våle båthavn / Frebergsvik',harbour_id=None,geometry=None,baseline_supplement_path='archive/original/horten-pilot/suppleringsfunn-holmestrand.geojson',candidate_org_no='915094821',identity_status='registered_entity_found_geographic_relation_unverified',status='existing_supplement_still_not_approved',capacity_current=None,source_ids=['BR915094821'],next_action='Kontroller operatørtilknytning, kommuneplassering og omriss mot egnet bilde og offisiell grense før eventuell separat revisjon.')]
issue(['3903-H01','3903-H02'],'shared_capacity','Kommunen oppgir ca. 1100 faste plasser for operatørens samlede tilbud. Omfanget er ikke fordelt på byhavnas to bassenger og Hagemann.','Bevar tallet én gang som gruppeobservasjon; avklar fordeling før anleggsvis publisering.',['HS01','HS02'])
issue(['3903-H01','3903-H02'],'operator_legal_form','Kommunesidene viser fortsatt DA; operatøren oppgir AS. Enhetsregisteret viser AS 936760600 og gammel DA 985747970 under avvikling.','Bruk kildebelagt AS-identitet i berikelsen, men behold avviket og ikke utled alle juridiske overdragelsesvilkår.',['HS01','HS02','BR936760600','BR985747970'])
issue(['3903-H01'],'guest_scope','Gjestehavna beskrives som ca. 50 båter langs 450 meter longsidekai. Eksakt polygonkobling og forhold til faste plasser er ikke kontrollert.','Ikke registrer 450 båtplasser eller summer 50 med 1100 uten belegg.',['HS03'])
issue(['3903-H03'],'capacity_conflict','NJBs nettside oppgir 450, mens operatørens Havneweb oppgir 397 båtplasser.','Behold begge kildetall og la entydig kapasitet stå null til referanseperiode og omfang er avklart.',['HS04','HS05'])
issue(['3903-H05'],'capacity_categories_and_expansion','155 andelsplasser og 62 utleieplasser beskrives av operatøren, mens katalogen viser 155. Bryggeutvidelse omtales også.','Bevar kategorier; kontroller om dagens fysiske anlegg avviker fra pilotens topografiske omriss.',['HS07','HS08','HS16'])
issue(['3903-K01','3903-K02','3903-K03','3903-K04'],'unresolved_baseline_candidates','Bekkebrygga, Sandvika, Mathisodden og Holmsåsen har fortsatt uavklart operatør, klasse og kapasitet. Stedssøk gir også navnelikhet med andre kommuner og badeanlegg.','Kontroller stedsspesifikt mot datert bilde og primærkilde; ikke overfør naboanleggenes kapasitet eller operatør.',[])
issue(['3903-K05'],'freshwater_and_camping','Torrud-gruppen ligger ved Eikeren. Thorrud annonserer båtplasser, men to bryggegruppers operatørkobling er uavklart; 130 plasser gjelder camping og 1000 er pris.','Behold ferskvann som egen dimensjon. Ikke tilordne 130 eller 1000 som båtplasskapasitet.',['HS11','HS12','HS13'])
issue([],'unapproved_supplement','Våle/Frebergsvik ligger allerede som et ikke-godkjent suppleringsfunn fra Horten-gjennomgangen.','Bevar C-VALE separat; ingen automatisk innlemming i Holmestrand eller samlefilen.',['BR915094821'])
issue(list(rows),'topographic_pilot_geometry','Alle 14 polygoner er eldre topografiske pilotomriss. Denne kildegjennomgangen gir ikke ny ortofoto- eller geometrikontroll.','Behold eksisterende usikkerhet og behov for ortofotokontroll; eventuelle geometriendringer krever ny revisjon og godkjenning.',[])
issue([],'unavailable_primary_documents','Kommunens kunnskapsgrunnlag-URL og Langøya-planinitiativ kunne ikke hentes direkte.','Søkesnutter er bare spor til videre undersøkelse. Ingen nye kapasiteter eller eksisterende Langøya-havn er utledet fra dem.',['HS14','HS19'])
for name,data in [('harbours',list(rows.values())),('observations',observations),('capacity-groups',capacity_groups),('candidates',candidates),('deviations',deviations)]:table(name,data)
reference=read(BASE/'bathavner.geojson')
for f in reference['features']:f['properties']['enrichment_pilot']=rows[f['properties']['harbour_id']]
reference['name']='Holmestrand approved pilot geometry with separate source-review overlay';save('reference-map.geojson',reference)
baseline=read(OUT/'baseline.json');assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha for p,sha in baseline['files'].items())
metrics=dict(harbours_reviewed=len(rows),baseline_polygons=len(fc['features']),legacy_unresolved_harbour_groups=sum(r['legacy_status']=='ma_avklares' for r in rows.values()),observations=len(observations),operator_names_recorded=sum(r['operator_name'] is not None for r in rows.values()),capacity_groups=len(capacity_groups),harbours_with_conflicting_operator_capacity=1,harbours_with_separate_capacity_components=1,open_supplements=len(candidates),sources_attempted=len(sources),sources_retrieved=sum(s['retrieval_status']=='retrieved' for s in sources.values()),deviations=len(deviations),geometry_reassessed=False,approved_files_unchanged=True,website_changed=False)
save('metrics.json',metrics);save('timing.json',dict(started_utc=baseline['started_utc'],finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_wall_seconds=round(time.time()-baseline['started_unix'],1),scope='Baseline capture through build; includes source research, no token/cost measurement.'))
print(json.dumps(metrics,ensure_ascii=False,indent=2))

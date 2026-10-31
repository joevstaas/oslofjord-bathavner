"""Reviewed evidence assignments. Scope is environmental-card eligibility, not eco-rating."""
from pathlib import Path
import json,hashlib,csv,datetime,collections,urllib.parse
from shapely.geometry import shape,Point
from shapely.ops import transform
from pyproj import Transformer
R=Path(__file__).resolve().parents[2];O=R/'data/miljokort/screening-01';rows=json.loads((O/'inventory.json').read_text());groups={g['group_id']:g for g in rows}
hid_to_gid={hid:g['group_id'] for g in rows for hid in g['harbour_ids']}
ss=json.loads((O/'source-screening.json').read_text());sources={r['url']:r for r in ss}
evidence=[]
def add(hid,url,topic,claim,locator,level='kortgrunnlag',scope='Hele gruppens driftsgrenser er ikke bekreftet; kildeopplysningen gjelder bare navngitt anlegg eller tjeneste.'):
 assert hid in hid_to_gid,hid
 assert url in sources,url
 evidence.append(dict(group_id=hid_to_gid[hid],harbour_id=hid,source_id=sources[url]['id'],url=url,topic=topic,claim=claim,locator=locator,eligibility=level,scope=scope,measured_effect_verified=False))
# Official public map: reviewed point/name associations. No automatic nearest-neighbour acceptance.
assign={1:'3203-H09',2:'3203-H12',3:'3201-H04',4:'3201-H19',6:'3107-H49',7:'3911-H15',8:'3101-H13',10:'3214-H10',11:'3214-H11',12:'3214-H09',13:'3105-H33',15:'3103-H02',16:'3212-H07',17:'3212-H01',19:'3909-H16',21:'3905-H03',22:'3905-H06',23:'3901-H04',24:'3901-H12',26:'3216-H02',28:'4001-H05',29:'4001-H14',30:'4012-H21',34:'0301-H04',35:'0301-H08',36:'0301-H23',37:'0301-H29',38:'3911-H22',39:'3911-H07',40:'3911-H15',41:'3911-H14',44:'3911-H18',48:'3203-H06'}
new_assign={49:'3105-H36',50:'3203-H06',51:'0301-H09',52:'3911-H11',53:'3107-H38',None:'3907-H32'}
spatial=[];T=Transformer.from_crs(4326,25833,always_xy=True).transform
fc=json.loads((R/'data/samlet/oslofjorden-bathavner-samlet.geojson').read_text());geoms=collections.defaultdict(list)
for f in fc['features']:geoms[f['properties']['harbour_id']].append(transform(T,shape(f['geometry'])))
for name,assignment in [('Septik_(ny_og_gammel)',assign),('Septik_(ny)',new_assign)]:
 sid='official-'+name;src=next(s for s in ss if s['id']==sid)
 for f in json.loads((R/'work/miljokort-screening'/('septic-'+name+'.json')).read_text())['features']:
  a=f['attributes'];oid=a.get('ObjectID');hid=assignment.get(oid);pt=transform(T,Point(f['geometry']['x'],f['geometry']['y']))
  status='accepted_context' if hid else 'not_counted'
  note='' if hid else ('Utenfor de 664 eller tvetydig steds-/navnekobling; ikke automatisk tilordnet.')
  if hid:
   distance=min(g.distance(pt) for g in geoms[hid]);assert distance<300,(hid,distance)
   add(hid,src['url'],'septikmottak',f"Offentlig kartlag oppfører {a['Havn']} med status {a.get('Eksisterende_foreslått')}. Dette bekrefter kartoppføringen, ikke drift i dag.",f"{name}: ObjectID={oid}; Havn={a['Havn']}")
  else:distance=None
  spatial.append(dict(layer=name,object_id=oid,name=a['Havn'],municipality=a.get('Kommune'),coordinates=f['geometry'],harbour_id=hid,distance_to_polygon_m=round(distance,1) if distance is not None else None,status=status,note=note))
# Additional direct source checks. Specific operations / routines, never generic green branding.
entries=[
('0301-H13','https://www.osloseilforening.no/next/p/14151/hms','spylevann','Oppsamling og transport til felles rensing beskrives.','Høytrykkspyling av båter og rensing av spylevann'),
('0301-H02','https://toxiclean.no/karenslyst-batopplag-med-nytt-toxiclean-anlegg/','spylevann','Leverandøren beskriver oppsamling og mobil rensing ved Karenslyst.','Karenslyst-anlegget; gjelder landanlegg, ikke hele Sjølyst-gruppen'),
('0301-H23','https://1853.no/miljotiltak','planlagt tiltak','Revierhavnen oppgir etablering ved Østslippen og avfallsordning.','Etablering av spyleplass / farlig avfall'),
('3216-H02','https://www.sonskilen.no/miljo','spylevann og avfall','Operatøren beskriver sandfang/filter og mottak for utvalgt farlig avfall.','Rensing av spylevann / Mottaksstasjon'),
('3105-H33','https://www.skjebergmarinesenter.no/aktuelt/hoy-miljoprofil','spylevann','Vaskestasjon og renseordning oppgis av operatøren.','Først i Norge'),
('3201-H09','https://www.no17.no/3228/','spylevann','Prosjektpartner beskriver demonstrasjon av mobil rensing hos Blommenholm.','Demonstrasjon hos Blommenholm; ikke all aktivitet i Solvik/Blommenholm'),
('3201-H21','https://sarbis.no/wp-content/uploads/2024/02/Avfalls-og-beredskapsplan-for-Sarbuvollen-Batforening-Rev.-2.-09.01.2024.pdf','avfall','Datert lokal plan beskriver avfallsmottak og henteavtaler.','Revisjon 2, 09.01.2024, side 1'),
('3203-H34','https://www.lagaholet.no/dokumenter/Bl%C3%A5boka%202022.pdf','spylevann','Foreningens håndbok beskriver oppsamling og renseanlegg.','Blåboka 2022: spyleplass ved servicekai'),
('3911-H03','https://www.araas.no/avfallshandtering/','avfall','Foreningen publiserer lokale rutiner for avfallshåndtering.','Avfallshåndtering; spyleplass alene er ikke bevis for rensing'),
('3907-H65','https://www.framnes-maritime.no/','spylevann','Operatøren beskriver rensing ved dokkanlegget og oppsamling av pussestøv.','MILJØ; ikke automatisk overført til nabogruppen Framnæs båthavn AS'),
('X-SALTHOLMEN-3112-3107','https://saltnesbf.no/?page_id=233','avfall og planer','Foreningen beskriver miljø-/avfallsplan og kommende lokale tiltak.','Havneregler, vedtekter og miljø; ferdigstillelse uavklart'),
('3216-H05','https://www.sonbaat.no/avfallshandtering/','spylevann og avfall','Oppsamlingskum ved opptaksplattform og avfallsordning beskrives.','Avfallshåndtering; oppsamling er ikke dokumentert full rensing'),
('3216-H06','https://www.sonhavn.no/son-gjestehavn/priser-2/','septik og avfall','Gjestehavnen tilbyr mottak for miljøfarlig avfall og septik.','Priser/tjenester; direkte publisert tjeneste'),
('3905-H06','https://www.vallobaatforening.no/index.php/vallo-batforening/vallo-sin-historie','spyleplass','Foreningen oppgir bygget spyleplass i 2024.','2024 Ny spyleplass; renseytelse ukjent'),
('4001-H15','https://www.havneweb.no/sandoyabatforening/','endret avfallsordning','Foreningen opplyser at container for farlig avfall er stengt; brukere må selv håndtere avfall.','AVFALLSCONTAINER ER STENGT; ikke en slutning fra fravær av kilde'),
('4001-H16','https://elvoghav.no/prosjekter/kystlotteriet/her-kan-du-levere-hente-sekk/','strandrydding','Kystlotteriet oppgir ryddestasjon ved Langangen motorbåtforening.','Porsgrunn / ved Langangen motorbåtforening; presis stedskobling fortsatt foreløpig'),
('3110-H01','https://www.xn--utgrdskilenbtforening-u2bj.no/nyheter-og-aktuelt-16702s.html','strandrydding','Foreningen omtaler stativ ved miljøstasjonen og rydding.','Nyheter om stativ ved miljøstasjon; kontroller relevans til korrekt Utgårdskilen-gruppe'),
]
# Resolve the cross-municipality Saltholmen group through one actual harbour ID.
for hid,url,topic,claim,loc in entries:
 if hid in groups:hid=groups[hid]['harbour_ids'][0]
 if 'Utgårdskilen' in claim:
  candidates=[g for g in rows if any('Utgårdskilen' in n for n in g['names'])];assert len(candidates)==1;hid=candidates[0]['harbour_ids'][0]
 add(hid,url,topic,claim,loc)
# Historical, explicitly matched Moss waste-plan rows: count once per physical group.
plan='https://www.kambomarina.no/kambo_marina/avfallsplan'
for f in fc['features']:
 p=f['properties']
 if p.get('municipality')!='Moss':continue
 linked=[r for r in p.get('source_register_members',[]) if r.get('link_status')=='bilde_og_kildekontrollert']
 if linked:
  add(p['harbour_id'],plan,'historisk avfallsordning','Felles avfallsplan inneholder en stedskoblet rad for '+', '.join(r['name'] for r in linked)+'. Aktuell drift er ikke kontrollert.', 'Tabellrad '+', '.join(str(r['number']) for r in linked)+'; rundt 2020',level='historisk_kortgrunnlag')
# Fredrikstad: only explicit plan participation and unambiguous group names are counted.
plan='https://www.fredrikstad-seilforening.no/wp-content/uploads/2023/02/Godkjent-30.03.2022-Felles-avfallsplan-for-smabathavner-i-Fredrikstad-kommune-2022-versjon-II.docx.pdf'
for hid,num,name,page in [('3107-H37',29,'Fjeldberg Båthavn',14),('3107-H38',34,'Fredrikstad sentrum gjestehavn',14),('3107-H21',49,'Hubukta Vei og Bryggeforening',15),('3107-H40',51,'Isegran Veteranbåthavn',15),('3107-H33',58,'Langøen Båtforening',15),('3107-H24',61,'Marnet Marina',15),('3107-H48',62,'Nabbetorp Båtforening',15)]:
 add(hid,plan,'historisk avfallsplan',f'{name} er oppført som deltaker i fellesplanen fra 2022. Dette dokumenterer planopplysningen, ikke dagens drift.',f'PDF-side {page}, tabell 2, rad {num}; detaljtabeller kapittel 3',level='historisk_kortgrunnlag')
# Deduplicate same evidence in multipolygon groups.
unique={ (e['group_id'],e['source_id'],e['locator']):e for e in evidence};evidence=list(unique.values())
for n,e in enumerate(evidence,1):e['evidence_id']=f'E{n:03}'
(O/'reviewed-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
(O/'septic-matching-review.json').write_text(json.dumps(spatial,ensure_ascii=False,indent=2)+'\n')
for g in rows:
 es=[e for e in evidence if e['group_id']==g['group_id']]
 g['eligibility']='kortgrunnlag' if any(e['eligibility']=='kortgrunnlag' for e in es) else 'historisk_kortgrunnlag' if es else 'uavklart'
 g['evidence_ids']=[e['evidence_id'] for e in es]
 g['baseline_urls_checked']=[r['id'] for r in ss if urllib.parse.urldefrag(r['url'])[0] in {urllib.parse.urldefrag(u)[0] for u in g['urls']}]
 g['review_scope']='Registergjennomgang og målrettet kildescreening; ingen befaring eller fullstendig separat nettsøk for alle navn.'
 g['environmental_measures_absent']=None
 g['next_step']='Bekreft operatør, fysisk omfang, kildedato og dagens drift før kort publiseres.' if es else 'Avklar navn/operatør og finn lokal miljø-/avfallskilde; ukjent betyr ikke at tiltak mangler.'
counts=collections.Counter(g['eligibility'] for g in rows)
(O/'assessment.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
with (O/'assessment.csv').open('w',encoding='utf-8-sig',newline='') as h:
 keys=list(rows[0]);w=csv.DictWriter(h,fieldnames=keys,delimiter=';');w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in g.items()} for g in rows)
summary=dict(reviewed_date='2026-10-31',denominator=664,polygons=816,eligible_lower_bound=counts['kortgrunnlag']+counts['historisk_kortgrunnlag'],counts=dict(counts),evidence=len(evidence),source_requests=len(ss),source_access_errors=sum('error' in s for s in ss),source_parse_errors=sum(bool(s.get('parse_error')) for s in ss),all_groups_in_inventory=True,all_groups_individually_web_searched=False,full_ecological_assessment=False,baseline_sha256=hashlib.sha256((R/'data/samlet/oslofjorden-bathavner-samlet.geojson').read_bytes()).hexdigest(),method='Minst ett konkret stedskoblet miljøtiltak, tjeneste, rutine eller datert historisk plan. Søkeordtreff eller generelle regler alene teller ikke. Telles per offentlig gid, aldri per polygon eller operatør.',outside_denominator_cards=['MK-06 Bispebrygga: kartkobling til de 664 uavklart'],note='Dette er en dokumentert nedre grense, ikke en endelig øvre grense for hvor mange som kan få kort. Kortgrunnlag betyr ikke bekreftet drift eller positiv miljøprestasjon.')
(O/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(summary)

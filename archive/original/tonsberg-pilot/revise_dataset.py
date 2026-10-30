import sys,json,csv
from pathlib import Path
P=Path(__file__).parent;sys.path.insert(0,str(P/'deps'))
from shapely.geometry import Polygon,shape,mapping
from shapely.ops import transform,unary_union
from shapely.geometry.polygon import orient
from pyproj import Transformer
from PIL import Image
F=Transformer.from_crs(4326,25833,always_xy=True).transform;B=Transformer.from_crs(25833,4326,always_xy=True).transform
boundary=unary_union([transform(F,shape(x['geometry'])) for x in json.loads((P/'kommunegrense.geojson').read_text())['features']])
old=json.loads((P/'revisjon-1/tonsberg-bathavner.geojson').read_text());features={x['properties']['id']:x for x in old['features']};evidence=[]
def outline(key,pts,offset=(0,0)):
 m=json.loads((P/'images'/f'{key}.json').read_text());w,h=Image.open(P/'images'/f'{key}.jpg').size;x0,y0,x1,y1=m['bbox']
 g=Polygon([(x0+(x+offset[0])/w*(x1-x0),y1-(y+offset[1])/h*(y1-y0)) for x,y in pts]);assert g.is_valid,(key,pts)
 evidence.append(dict(image=key,pixels=pts,offset=offset));return g

def update(n,key=None,pts=None,offset=(0,0),name=None,harbour=None,possible=False,basis='minst_10_synlige_plasser_i_felles_anlegg',sources=(),capacity=None,note=None,geometry=None):
 fid=f'3905-H{n:02d}-B01';f=features[fid];p=f['properties'];p.update(classification='mulig_smabathavn' if possible else 'smabathavn',classification_basis=basis,berth_count_published=capacity,berth_count_source=sources[0] if capacity is not None and sources else None,reviewed_date='2026-10-29',revision=2,current_operation_verified=False,source_observation_date=None,estimated_accuracy_m=None,needs_orthophoto_review=False,needs_dated_imagery_review=True,approval_status='til_godkjenning',status='usikker_kandidat' if possible else 'bilde_og_kildeunderbygget',geometry_role='brygger_batplasser_og_mellomliggende_sjo',method='manuell_avgrensning_kontrollert_mot_flybilde_og_topografisk_kart')
 if name:p['name']=name
 if harbour:p['harbour_id']=harbour
 if note is not None:p['note']=note
 if key:
  m=json.loads((P/'images'/f'{key}.json').read_text());p['sources']=list(dict.fromkeys(list(sources)+p['sources']+[m['url']]));p['imagery_source']='Esri World Imagery';p['imagery_retrieved_date']='2026-10-29';p['image_resolution_m_per_pixel']=round((m['bbox'][2]-m['bbox'][0])/m['width'],3)
  if pts is not None:geometry=outline(key,pts,offset)
 else:p['needs_orthophoto_review']=True
 if geometry is not None:
  clipped=not boundary.covers(geometry);geometry=geometry.intersection(boundary);assert geometry.geom_type=='Polygon' and geometry.is_valid and not geometry.is_empty,(fid,geometry.geom_type);p['municipality_clipped']=clipped;f['geometry']=mapping(transform(B,orient(geometry,sign=1)))
 p['name_is_descriptive']=n in [3,9,10,11,15,22,23,98,99]
 p['berth_count_approximate']=capacity==160 if capacity is not None else None
 p['map_attribution']='© Kartverket; imagery © Esri and its imagery suppliers (see source service metadata); OSM © OpenStreetMap contributors, ODbL'
 return f

def add(n,name,key,pts,offset=(0,0),part=1,harbour=None,possible=False,basis='minst_10_synlige_plasser_i_felles_anlegg',sources=(),capacity=None,note=''):
 fid=f'3905-H{n:02d}-B01';newid=f'3905-H{n:02d}-B{part:02d}'
 template=json.loads(json.dumps(old['features'][0]));template['properties'].update(id=fid,harbour_id=harbour or f'3905-H{n:02d}',name=name,sources=[],osm_ids=[],retrieved_date='2026-10-29');features[fid]=template
 f=update(n,key,pts,offset,name=name,harbour=harbour,possible=possible,basis=basis,sources=sources,capacity=capacity,note=note)
 if partid:=part!=1:
  del features[fid];f['properties']['id']=newid;features[newid]=f
 return f

# Old geometries that already follow the visible facilities; all checked against imagery.
update(1,'sentrum-ortho',basis='dokumentert_batforening_med_faste_plasser')
update(2,'sentrum-ortho',name='Kaldnes Båtforening',basis='dokumentert_batforening_med_faste_plasser',sources=['https://kaldnesbatforening.wordpress.com/kontakt/'],note='Navn og lokalisering kontrollert mot foreningens oppgitte besøkskoordinater; tidligere navn Kaldnes marina.')
update(3,'sentrum-ortho',basis='dokumentert_gjestehavn',note='Søndre del ved Brygga. Nordre flytebrygger har samme harbour_id, eget polygon B02. Gjestehavnen er sesongstengt vinteren 2026/27 ifølge kommunen.')
# Kaldnes Brygge: connected water bodies, avoid the residential blocks.
a=outline('sentrum-ortho',[(148,520),(159,516),(211,646),(239,754),(250,770),(234,774),(220,761),(202,651),(177,593)],(200,100))
b=outline('sentrum-ortho',[(177,485),(219,485),(258,500),(292,541),(328,590),(336,607),(283,625),(226,648),(205,621),(190,584),(166,523),(151,521),(146,505),(162,502)],(200,100))
g=unary_union([a,b]);assert g.geom_type=='Polygon'
update(4,'sentrum-ortho',name='Kaldnes Brygge',geometry=g,basis='dokumentert_felles_batplassanlegg_og_synlige_plasser',sources=['https://www.selvaagbolig.no/vestfold/kaldnes-brygge/batplass/dokumenter-batplass/oversikt-batplasser-kaldnes-brygge/'],note='Tidligere indre og ytre kandidater (H04 og H05) er samlet som ett anlegg. Boligblokkene er utelatt.')
update(6,'vallo-ortho',basis='dokumentert_batforening_med_faste_plasser',sources=['https://www.vallobaatforening.no/index.php/vallo-batforening/vallo-sin-historie'])
update(7,'vallo-ortho',basis='dokumentert_marina_med_faste_plasser')
update(8,'bliksekilen-ortho',pts=[(538,440),(549,418),(558,426),(670,467),(641,611),(518,590)],basis='minst_10_synlige_plasser_i_felles_anlegg')
update(9,'husvik-ortho')
update(10,'husvik-ortho',pts=[(39,88),(94,68),(121,135),(87,151),(69,159)],offset=(650,1450),name='Nordre Nes – felles bryggeanlegg',note='To sammenhengende bryggearmer ved boligrekken. Minst ti båtplasser/fortøyde båter kan skilles i flybildet; operatør er ukjent.')
update(11,'husvik-ortho',possible=True,basis='flere_brygger_men_felles_drift_og_antall_plasser_ukjent',note='Bryggegruppen er synlig, men deler kan være separate private brygger. Beholdt som mulig småbåthavn etter ny regel.')
update(12,'husoy-ortho',pts=[(575,442),(677,447),(683,481),(584,524),(575,491)],basis='dokumentert_batforening_og_synlig_felles_brygge',sources=['https://virksomhet.brreg.no/nb/oppslag/enheter/987379383'],note='Registrert båtforening med drift av fellesanlegg; T-formet fellesbrygge med båter synlig i flybildet.')
# Jarlsø west: envelope of the coherent pontoon row, not the buildings.
update(14,'jarlso-ortho',pts=[(1257,1223),(1305,1245),(1290,1305),(1275,1348),(1270,1380),(1257,1402),(1245,1440),(1239,1470),(1254,1510),(1270,1550),(1270,1590),(1284,1630),(1290,1670),(1298,1720),(1309,1766),(1316,1804),(1344,1852),(1337,1868),(1184,1861),(1175,1800),(1204,1667),(1165,1548),(1196,1387),(1197,1293)],basis='dokumentert_bryggesameie_med_faste_plasser',sources=['https://www.havneweb.no/jarlso-brygge/'],capacity=170,note='170 er oppgitt kapasitet for Bryggesameiet Jarlsø Vest, ikke opptelling fra bildet. Nordre gjestebrygger leveres som eget delpolygon under samme havnegruppe; eierskap til gjestebryggene er ikke bekreftet.')
update(15,'jarlso-ortho',harbour='3905-H14',basis='dokumenterte_gjestebrygger_del_av_Jarlso_havnegruppe',note='To dokumenterte gjestebrygger ved broen; delpolygon i Jarlsø-gruppen, ikke telt som en ekstra selvstendig havn. Eier/operatør er ikke bekreftet.')
update(16,'vestfjord-ortho',basis='dokumentert_felles_smabathavn',note='Fellesanlegg dokumentert i Enhetsregisteret og tydelig brygge-/båtplassmønster i flybildet.')
add(20,'Klopp båthavn','klopp-ortho',[(421,942),(450,925),(525,935),(588,1000),(595,1032),(552,1086),(422,1053),(412,1043)],sources=['https://www.kloppbat.com/','https://virksomhet.brreg.no/nb/oppslag/enheter/997688848'],capacity=160,basis='dokumentert_batforening_med_faste_plasser',note='Operatøren oppgir ca. 160 plasser. Manglet i revisjon 1.')
add(21,'Husøy Småbåthavn SA','husoy-ortho',[(1195,1526),(1296,1498),(1306,1520),(1277,1555),(1353,1696),(1317,1730),(1225,1598),(1227,1576),(1234,1567),(1205,1564)],sources=['https://www.hsbhavn.com/om-oss/'],capacity=75,basis='dokumentert_batforening_med_faste_plasser',note='Operatøren oppgir 75 plasser. Avgrenser sjøanlegget på Husøys side av Myrasundet, ikke opplagsplassen på land. Manglet i revisjon 1.')
add(22,'Husøy Havn – vestre båtanlegg','husoy-ortho',[(155,36),(177,25),(244,49),(232,88),(209,109),(150,98)],offset=(1100,240),sources=['https://spir.no/prosjekter/husoy-havn','https://husoyhavn.no/wp-content/uploads/2019/08/HusoyHavn_Prospekt_HUS_3_oppslag.pdf'],basis='dokumentert_boligtilknyttet_anlegg_og_synlige_faste_plasser',note='Vestre av to boligtilknyttede småbåtanlegg. Samme harbour_id som østre del.')
# add() uses a temporary H99 slot to preserve the already constructed H22 B01.
f=add(99,'Husøy Havn – østre båtanlegg','husoy-ortho',[(1610,405),(1676,400),(1662,502),(1608,507),(1610,469),(1630,428)],harbour='3905-H22',sources=['https://spir.no/prosjekter/husoy-havn','https://husoyhavn.no/wp-content/uploads/2019/08/HusoyHavn_Prospekt_HUS_3_oppslag.pdf'],basis='dokumentert_boligtilknyttet_anlegg_og_synlige_faste_plasser',note='Østre av to boligtilknyttede småbåtanlegg. Samme harbour_id som vestre del.')
del features['3905-H99-B01'];f['properties']['id']='3905-H22-B02';features[f['properties']['id']]=f
f=add(98,'Tønsberg gjestehavn – nordre flytebrygger','sentrum-ortho',[(168,62),(227,71),(248,176),(275,221),(331,286),(327,307),(267,294),(225,260),(183,195),(174,139)],offset=(200,100),harbour='3905-H03',sources=['https://www.tonsberg.kommune.no/tjenester/kultur-idrett-og-fritid/turist-i-tonsberg/gjestehavna/','https://www-bib.hive.no/tekster/tunsberg/tbghavn/kap08.html'],basis='dokumentert_gjestehavn',note='Nordre del ved Strandpromenaden. Samme havne-ID som Brygga. Manglet i revisjon 1; historisk lokalisering støtter navnet, nåværende brygger er synlige i flybildet.')
del features['3905-H98-B01'];f['properties']['id']='3905-H03-B02';features[f['properties']['id']]=f
add(23,'Jarlsøsundet – nordre bryggeanlegg','jarlso-ortho',[(1004,1002),(1110,1021),(1228,1010),(1305,997),(1318,1030),(1307,1054),(1162,1072),(1061,1047),(998,1023)],possible=True,basis='sammenhengende_bryggeanlegg_men_drift_og_antall_faste_plasser_ukjent',note='Langt sammenhengende bryggeanlegg nord for Jarlsøsundet; båter synlige, men antall faste plasser og operatør er ikke bekreftet.')
removed={5:('slatt_sammen','Samlet i Kaldnes Brygge (3905-H04-B01).'),13:('utgatt_feil_avgrensning','OSM-området ved Kirkegaten følger land/badeområde i dagens bilde, ikke et synlig havneanlegg. Husøy Småbåthavn SA er tatt inn med korrekt sjøavgrensning som H21.'),17:('utelatt_etter_regel','Moloområde; ikke dokumentert felles havn eller minst ti faste båtplasser.'),18:('utelatt_etter_regel','Lite moloområde ved camping; ikke dokumentert felles havn eller minst ti faste båtplasser.'),19:('utelatt_etter_regel','Moloområde; ikke dokumentert felles havn eller minst ti faste båtplasser. Delvis skydekke i regionalt flybilde.')}
changes=[]
for n,(action,reason) in removed.items():
 fid=f'3905-H{n:02d}-B01';removed_f=features.pop(fid);changes.append(dict(id=fid,name=removed_f['properties']['name'],action=action,reason=reason))
for fid,f in features.items():
 p=f['properties'];g=transform(F,shape(f['geometry']));assert g.is_valid and not g.is_empty and g.geom_type=='Polygon',fid
 assert g.difference(boundary).area<0.02,(fid,'outside municipality')
 p['area_m2']=round(g.area,1);q=shape(f['geometry']).representative_point();p['longitude']=round(q.x,7);p['latitude']=round(q.y,7)
 if fid not in {x['properties']['id'] for x in old['features']}:changes.append(dict(id=fid,name=p['name'],action='lagt_til',reason=p['note']))
 else:changes.append(dict(id=fid,name=p['name'],action='revurdert',reason=p['classification_basis']))
fs=sorted(features.values(),key=lambda x:x['properties']['id'])
for i,a in enumerate(fs):
 for b in fs[i+1:]:
  area=transform(F,shape(a['geometry'])).intersection(transform(F,shape(b['geometry']))).area
  assert area<1,(a['properties']['id'],b['properties']['id'],area)
rule=dict(version='2026-10-29',smabathavn='Felles anlegg med minst 10 båtplasser, eller dokumentert marina/båtforening med faste plasser.',mulig_smabathavn='Flere sammenhengende brygger, men antall plasser eller felles drift er uklart.',utelatt='Spredte private brygger uten tydelig felles organisering; rene service-/fergekaier, moloområder uten båtplassbelegg og badebrygger.',grouping='Delpolygoner i samme havneanlegg har samme harbour_id. Antall polygoner er ikke antall havner.')
fc=dict(type='FeatureCollection',name='Tønsberg – småbåthavner, revisjon 2',revision=2,classification_rule=rule,description='Alle 35 tidligere kartfliser gjennomgått på nytt. Kystanlegg kontrollert mot Esri World Imagery og dokumentkilder. Bildets opptaksdato er ukjent; dagens drift og fullstendighet er ikke garantert.',features=fs)
(P/'tonsberg-bathavner-rev2.geojson').write_text(json.dumps(fc,ensure_ascii=False,indent=2))
fields=list(dict.fromkeys(k for f in fs for k in f['properties']))
with (P/'tonsberg-metadata-rev2.csv').open('w',encoding='utf-8-sig',newline='') as out:
 w=csv.DictWriter(out,fieldnames=fields,delimiter=';');w.writeheader()
 for f in fs:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in f['properties'].items()})
(P/'revision-2-digitization.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2))
(P/'revision-2-changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2))
with (P/'tonsberg-endringer-rev2.csv').open('w',encoding='utf-8-sig',newline='') as out:
 w=csv.DictWriter(out,fieldnames=['id','name','action','reason'],delimiter=';');w.writeheader();w.writerows(changes)
summary=dict(polygons=len(fs),harbours=len({f['properties']['harbour_id'] for f in fs}),confirmed_harbours=len({f['properties']['harbour_id'] for f in fs if f['properties']['classification']=='smabathavn'}),possible_harbours=len({f['properties']['harbour_id'] for f in fs if f['properties']['classification']=='mulig_smabathavn'}),new_polygons=sum(c['action']=='lagt_til' for c in changes),removed_polygons=sum(c['action'].startswith('ut') for c in changes),merged_polygons=sum(c['action']=='slatt_sammen' for c in changes),validation='Valid Polygon geometries, within official boundary, pairwise overlap <1 m2')
(P/'revision-2-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False))

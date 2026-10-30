"""Beslutninger Drammen rev. 1 (metode 1.2). Vurdert på kontrollark qa/r-*.jpg og zoombilder."""
exec(open('decisions_lib.py').read())
ELV = ' Ligger i nedre Drammenselva (tidevannspåvirket elv til Drammensfjorden); tatt med på samme måte som Glomma-anlegg i Fredrikstad.'
exc('A001 A002 A003 A004 A005 A007 A008 A009 A010 A011 A012 A013 A014 A016 A017 A018 A019 A020 A022 A024 A025 A028 A031 A034 A042 A043')
exc('A036', 'Lekter/flytende konstruksjon ved bru; ikke båtplassanlegg.')
inc('A006', 'm', name='Drammenselva ved Åserud – tre brygger', note='Tre brygger uten synlige båter i bildet.' + ELV)
man('A015', [[228012, 6633504], [228075, 6633500], [228117, 6633483], [228154, 6633442], [228167, 6633412], [228133, 6633396], [228108, 6633425], [228075, 6633471], [228025, 6633482], [228012, 6633487]],
    cls='s', name='Muusøya båthavn', descr=False, note='Lukket basseng med mange båter. OSM-pirene lå langs elvebredden utenfor bassenget; omrisset er tegnet manuelt på zoombilde z-muusoya.' + ELV)
inc('A021', 's', True, name='Union brygge', descr=False, note='Lang brygge med mange utriggerplasser langs boligområdet. OSM-pirens posisjon avviker noe fra bildet; avgrensningen er usikker. Union brygge servicesameie er registrert.' + ELV)
inc('A023', 's', name='Holmen motorbåtforening', descr=False, note='Lange brygger langs elva på begge sider av brua.' + ELV)
inc('A026', 's', name='Åsetomta båthavn', descr=False, note='Rekke brygger med båter langs kaia.')
inc('A027', 's', name='Nøsted brygge småbåthavn / Glassverket', descr=False, note='To bassenger med brygger ved boligutbyggingen; Glassverket båtforening er registrert.')
man('A029', [[233958, 6628825], [233979, 6628829], [234075, 6628717], [234088, 6628667], [234067, 6628658], [234033, 6628683], [233992, 6628758], [233963, 6628800]],
    cls='s', name='Solumstrand båthavn', descr=False, note='Langt basseng med mange båter bak molo. OSM-pirene lå på moloens utside; omrisset er tegnet manuelt på zoombilde z-solumstrand.')
inc('A030', 's', name='Sande-/Svelviksiden – marina ved Almeløkka', note='Marina med tre lange brygger og mange båter; operatør ikke dokumentert.')
inc('A032', 'm', name='Baskomti – brygger', note='To–tre brygger med få båter; Baskomtibryggen DA er nevnt i OSM.')
inc('A033', 's', True, name='Kjeller/Sandbakken – marina bak molo', note='To brygger med utriggere i lukket molobasseng.')
inc('A035', 's', True, name='Berger brygge / Berger båtforening', descr=False, sources=['https://www.statsforvalteren.no/siteassets/fm-oslo-og-viken/horinger-og-kunngjoringer/klima-og-miljovern/berger-batforening/2021.0238.t.pdf'], note='Lang brygge i smal kanal i Bergerbukta. Berger båtforening driver båthavn i Bergerbukta ifølge Statsforvalterens mudringstillatelse.')
inc('A037', 's', name='Svelvik Marina', descr=False, note='Flere lange brygger med mange båter.')
inc('A038', 's', True, name='Svelvik gjestebrygge', descr=False, basis='dokumentert_gjestehavn', note='Gjestebrygge langs kaia i sentrum (OSM).')
inc('A039', 's', True, name='Svelvik motorbåtforening', descr=False, note='Lang brygge langs kanalen med mange båter. Båter langs vestsiden av kanalen ligger delvis utenfor polygonet.')
man('A040', [[240992, 6614975], [240996, 6615017], [241067, 6615054], [241100, 6615054], [241183, 6614992], [241217, 6614962], [241200, 6614933], [241158, 6614921], [241058, 6614933], [240996, 6614950]],
    cls='s', name='Bokerøya båthavn', descr=False, note='Fire lange brygger bak molo. Bare en liten del var dekket av OSM-pirer; omrisset er tegnet manuelt på zoombilde z-bokeroya. Vårbilde med få båter.')
inc('A041', 's', name='Krok småbåthavn', descr=False, action='clip', box=[240300, 6612440, 240560, 6612650], note='Brygge med fire–fem utriggerarmer. Spredte private brygger lenger sør er klippet bort etter overleggskontroll.')
inc('A044', 's', name='Baskomti – marina', descr=False, note='T-brygge med mange utriggerplasser; OSM Baskomtibryggen DA.')

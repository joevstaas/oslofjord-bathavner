"""Beslutninger Lier rev. 1 (metode 1.2). Vurdert på kontrollark qa/r-00.jpg og g-*.jpg."""
exec(open('decisions_lib.py').read())
exc('A002', 'Tømmerterminalens kai med lekter; næringskai, ikke småbåthavn.')
exc('A003', 'Molo/fylling ved Gullaugodden uten synlige båtplasser.')
exc('A005', 'Lang brygge i Holsfjorden/Tyrifjorden (innsjø) uten synlige båter; ikke del av Oslofjorden og ikke dokumentert båtplassanlegg.')
inc('A001', 's', name='Lierstranda – båthavn ved Tømmerterminalen', note='Fire brygger med båter og en lang molo/bølgebryter. Lier båtforening er registrert i kommunen; koblingen er ikke fastslått.')
inc('A004', 's', name='Engersand havn – marina', descr=False, note='Basseng med flere brygger og mange båter ved boligområdet Engersand havn. Fellessameiet Engersand havn nord (Lier) og syd (Drammen) er registrert; kommunegrensen kan gå nær anlegget.')

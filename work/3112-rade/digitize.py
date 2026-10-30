"""Manuell digitalisering for Råde rev. 1.
Pikselkoordinater er lest av visningsbilder laget med view.py: bildet `image` beskåret til `frame`
(EPSG:25833) og skalert til bredde `size`. Omregning skjer i build.py."""

RBF = 'https://www.rbf.no/index.php/batplasser'
SBF = 'https://saltnesbf.no/?page_id=19'
KDP = 'https://www.rade.kommune.no/_f/p1/i1db1d7e1-c08e-4118-a0e8-f70e09a26638/kommunedelplan_for_saltnesomraadet-vedtatt_210607.pdf'
BRREG = 'https://virksomhet.brreg.no/nb/oppslag/enheter/'
TASKEN = 'https://www.finn.no/385649027'

rows = []


def add(cid, name, group, image, frame, size, pixels, *, basis, possible=False, uncertain=False, descriptive=True,
        sources=(), osm=(), capacity=None, cap_source=None, cap_period=None, note='', water_body='saltvann',
        cross_group=None, members=()):
    rows.append(dict(candidate_id=cid, name=name, group=group, image=image, frame=frame, size=size, pixels=pixels,
                     basis=basis, possible=possible, geometry_uncertain=uncertain, name_is_descriptive=descriptive,
                     sources=list(sources), osm_ids=list(osm), capacity=capacity, capacity_source=cap_source,
                     capacity_period=cap_period, note=note, water_body=water_body, cross_group=cross_group,
                     source_register_members=list(members),
                     tracing_method='manuell_digitalisering_georeferert_flybilde'))


add('SRC-RBF', 'Makrellrød båthavn / Råde båtforening', 'makrellrod', 'z-makrellrod', [259300, 6581900, 260100, 6582700], 900,
    [(347, 488), (370, 508), (440, 533), (520, 573), (578, 613), (572, 640), (528, 682), (450, 725), (428, 725), (312, 628), (306, 560), (322, 515)],
    basis='operator_dokumenterer_faste_batplasser', descriptive=False,
    sources=[RBF, BRREG + '993953253', KDP], osm=['node/5106918395'], capacity=402, cap_source=RBF,
    cap_period='ukjent_referanseperiode_nettside_lest_2026-10-29',
    note='Operatøren oppgir 402 båtplasser og 4 gjesteplasser langs ytre molo. Kommunedelplanen fra 2007 oppga 280 plasser; tallene er ikke summert. '
         'Polygonet dekker bassenget innenfor moloen. Ytre molo med gjesteplasser, separat nordre servicebrygge, opplag og parkering er utelatt.')

add('SRC-SBF', 'Saltholmen båthavn / Saltnes båtforening – Råde-del', 'saltholmen', 'z-saltholmen', [257300, 6579200, 258100, 6580000], 900,
    [(498, 272), (545, 280), (585, 300), (605, 322), (600, 345), (575, 385), (545, 400), (510, 420), (480, 440), (440, 440), (420, 430), (460, 370), (482, 318)],
    basis='operator_dokumenterer_faste_batplasser', descriptive=False, uncertain=True,
    sources=[SBF, BRREG + '993955779', KDP], capacity=220, cap_source=SBF, cap_period='foreningen_oppgir_tall_med_medlemstall_pr_2021-01-01',
    cross_group='X-SALTHOLMEN-3112-3107',
    note='Foreningen oppgir 220 bryggeplasser for hele havna. Offisiell kommunegrense krysser bryggeanlegget; bare Råde-delen er levert. '
         'Søndre del ligger i Fredrikstad (3107) og er registrert i ventelogg for egen behandling. Kapasiteten gjelder hele anlegget, ikke Råde-delen.')

add('OSM-node/5106950299', 'Åven – vestre båthavn', 'aven-vest', 'z-aven', [256780, 6582560, 257100, 6582880], 900,
    [(30, 528), (182, 422), (205, 437), (258, 503), (264, 612), (185, 690), (200, 730), (178, 742), (30, 545)],
    basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', osm=['node/5106950299'],
    note='Hovedbrygge med tre utriggerbrygger og mer enn ti synlige båtplasser. OSM-punkt «Småbåtshavn». Operatør og faste plasser er ikke dokumentert.')

add('VIS-aven-indre', 'Åven – indre båtbasseng', 'aven-indre', 'z-aven', [256780, 6582560, 257100, 6582880], 900,
    [(520, 372), (705, 165), (745, 175), (790, 235), (838, 322), (735, 368), (640, 362), (590, 390), (540, 395)],
    basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', uncertain=True,
    note='To brygger i et avgrenset indre basseng med mer enn ti synlige båter. Nærhet til vestre båthavn dokumenterer ikke felles drift; derfor egen havne-ID. '
         'Strandsoner og grunne partier er delvis inkludert ved inngangen.')

add('OSM-node/5106953733', 'Fuglevik (Råde) – søndre bryggeanlegg', 'fuglevik-sor', 'z-fuglevik', [258250, 6582420, 258500, 6582670], 900,
    [(392, 320), (495, 232), (530, 238), (610, 300), (645, 350), (625, 410), (575, 455), (500, 615), (478, 620), (445, 575), (470, 520), (425, 450), (400, 340)],
    basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', osm=['node/5106953733'],
    note='Tre brygger med utriggere og mer enn ti synlige båter, ved Katteskjærveien. OSM-punkt «Småbåtshavn». '
         'Ikke samme anlegg som Fuglevik marina/Rygge båtforening i Moss. Operatør er ikke dokumentert.')

add('VIS-fuglevik-kanal', 'Fuglevik (Råde) – båtplasser langs kanalen', 'fuglevik-kanal', 'z-fuglevik', [258050, 6582700, 258400, 6583050], 900,
    [(538, 90), (600, 88), (635, 170), (670, 330), (700, 400), (675, 490), (640, 590), (605, 665), (575, 690), (562, 670), (600, 590), (630, 500), (640, 420), (600, 380), (578, 300), (555, 200)],
    basis='minst_10_synlige_plasser_i_sammenhengende_anlegg', uncertain=True,
    note='Flere korte brygger og utriggere langs kanalen og vestsiden av fyllingen, samlet mer enn ti synlige båter. '
         'Felles drift og operatør er ikke dokumentert; avgrensningen mot fyllingen er usikker.')

add('VIS-fuglevik-vest', 'Fuglevik (Råde) – vestre felles brygge', 'fuglevik-vest', 'z-fuglevik', [258050, 6582700, 258400, 6583050], 900,
    [(228, 700), (245, 690), (300, 740), (352, 790), (330, 820), (310, 815), (255, 760), (225, 715)],
    basis='en_lang_brygge_med_rundt_10_synlige_batplasser', possible=True, uncertain=True,
    note='Én lang brygge med båter på begge sider, rundt ti synlige båtplasser. Felles drift og faste plasser er ikke dokumentert.')

add('SRC-KROGSTAD-BF', 'Krokstadfjorden – østre bryggeanlegg (Krogstad båtforening)', 'krokstad-ost', 'z-krokstad-inner', [261040, 6583540, 261520, 6583820], 900,
    [(512, 245), (540, 232), (580, 225), (620, 215), (665, 192), (700, 180), (740, 160), (790, 148), (830, 150), (845, 165), (835, 200), (800, 215), (760, 235), (705, 268), (650, 290), (600, 305), (570, 320), (545, 312)],
    basis='minst_10_synlige_plasser_i_sammenhengende_anlegg',
    sources=[BRREG + '992113030'],
    note='Fem–seks brygger med utriggere og mer enn ti synlige båter innerst i Krokstadfjorden. Krogstad båtforening (stiftet 1984) har adresse Krogstadveien 3 like ved; '
         'koblingen er geografisk og ikke en dokumentert operatørgrense. Kapasitet er ikke funnet.')

add('SRC-KROGSTAD-MARINA', 'Krokstadfjorden – kai og bryggerekke ved båtverkstedet', 'krokstad-vest', 'z-krokstad-inner', [261040, 6583540, 261520, 6583820], 900,
    [(15, 490), (110, 450), (185, 415), (300, 375), (385, 345), (395, 360), (398, 395), (300, 422), (200, 452), (130, 482), (60, 515), (22, 525)],
    basis='flere_brygger_men_felles_drift_eller_kapasitet_uklar', possible=True, uncertain=True,
    sources=[BRREG + '937345348'],
    note='Bryggerekke med utriggere og mange båter langs kaien ved båtverksted/forhandler (Krogstadfjorden Marina AS, Krogstadveien 5). '
         'Det er uklart om plassene er faste småbåtplasser eller verksted-/salgsplasser. Ikke gruppert med østre anlegg fordi felles drift ikke er dokumentert.')

add('SRC-TASKEN', 'Nordre Tasken – felles brygge i Kurefjorden', 'tasken', 'z-kure-s', [258220, 6584010, 258380, 6584150], 500,
    [(195, 225), (215, 222), (260, 245), (310, 262), (358, 300), (350, 312), (300, 310), (240, 290), (198, 262)],
    basis='eiendomsannonse_omtaler_felles_bryggeanlegg_rundt_10_synlige_plasser', possible=True, uncertain=True,
    sources=[TASKEN],
    note='Eiendomsannonse for Nordre Tasken omtaler felles bryggeanlegg ved Kurefjorden med egne båtplasser. Bildet viser én brygge med utriggere og rundt ti båter. '
         'Annonsen er en svak kilde; kobling og antall faste plasser er ikke bekreftet. Grunt område med vegetasjon.')

add('SRC-GRIMSTADBUKTA', 'Grimstadstøa – felles brygge i Vansjø', 'grimstad', 'z-grimstad', [262240, 6588820, 262380, 6588960], 500,
    [(168, 335), (195, 262), (258, 170), (290, 178), (302, 192), (262, 262), (230, 300), (190, 338)],
    basis='forening_registrert_og_brygge_med_utriggere_men_faste_plasser_ikke_dokumentert', possible=True, uncertain=True,
    sources=[BRREG + '916901321'], water_body='ferskvann',
    note='Brygge med utriggere ved stedsnavnet Grimstadstøa. Grimstadbukta bryggeforening (stiftet 1984) har adresse i Grimstad; koblingen er geografisk og foreløpig. '
         'Bildet viser få båter; antall plasser og felles drift er ikke dokumentert.')

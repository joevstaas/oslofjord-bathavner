# Small-boat harbours in the Oslofjord

Polygons with traceable metadata for small-boat harbours (marinas, boat club harbours and other shared berthing facilities) in the municipalities bordering the inner and outer Oslofjord, Norway.

Approved status: **456 polygons from 14 municipalities** (Holmestrand, Horten, Tønsberg, Færder, Sandefjord, Larvik, Moss, Råde, Fredrikstad, Bærum, Asker, Lier, Drammen, Oslo). Remaining: Nordre Follo, Nesodden, Frogn, Vestby, Hvaler, Sarpsborg, Halden, Porsgrunn, Bamble (Ås not yet confirmed as coastal). See `status.json`.

The dataset is an imagery- and source-based mapping. It does not show official harbour or property boundaries. Approval does not remove uncertainty about classification or geometry.

## Analysis method

The full methodology and the per-municipality logs are in [`docs/METODIKK.md`](docs/METODIKK.md) (Norwegian). Summary of method version 1.2, used from Fredrikstad onwards:

### What counts as a small-boat harbour?

| Class | Rule |
|---|---|
| `smabathavn` (harbour) | Shared facility with at least 10 berths, or a documented marina or boat club with permanent berths |
| `mulig_smabathavn` (possible harbour) | Several connected piers, but the number of berths or the shared operation is unclear |
| Excluded | Scattered private piers, bathing piers, ferry quays, slipways, plain breakwaters, planned facilities |

The ten-berth threshold is a project rule, not a legal definition. A club's postal address does not prove where its harbour is, and a zoning plan area is not an existing harbour.

### Workflow per municipality

1. **Boundary and coverage.** The municipal boundary comes from the Norwegian Mapping Authority (Kartverket). The shoreline is divided into tiles. For each tile, aerial imagery (Esri World Imagery, about 0.67 m/pixel) and a topographic map (Kartverket WMS) are stored with georeferencing in EPSG:25833.
2. **Candidate search from two independent sources.**
   - *Map:* OpenStreetMap piers, marinas and moorings from Overpass.
   - *Sources:* the Central Coordinating Register for Legal Entities (boat clubs, marinas), Kartverket place names, municipal harbour pages and other public documents.
3. **Automatic draft.** OSM piers within 60 m of each other are clustered. Each cluster is buffered by 12 m and closed by 20 m. The result is clipped to the water area of the topographic map and to the municipal boundary. This is only a draft geometry.
4. **Visual review of every candidate.** The draft is drawn on top of the aerial image. Each candidate gets one decision: include, clip, split, add a manual area, draw manually, or exclude. Every decision has a stated reason and is recorded in `decisions.py` and the candidate ledger.
5. **Systematic imagery sweep.** All detail tiles near the fjord are reviewed in contact sheets with the candidates overlaid, to find harbours missing from OSM. These are drawn manually.
6. **Polygon rule.** A polygon covers the piers, the berths and the water between them. It does not cover the whole bay, land areas or the club's property. Separate parts become separate polygons that share a `harbour_id`. Harbours that cross a municipal boundary are clipped, flagged with `municipality_clipped` and linked through `cross_municipality_group_id`.
7. **Quality control.** Every exported polygon is checked as an overlay on the aerial image after the last edit. The delivery is also validated for:
   - valid geometry
   - unique IDs
   - fit to the municipal boundary
   - no overlap with other polygons or with the combined file
   - CSV matching the GeoJSON
8. **Approval.** The user approves each municipality, or an agreed batch, by inspecting the GeoJSON file. Only after approval is the delivery copied to `data/kommuner/<code>-<name>/rev-NN/` and merged into the combined file. Uncertain boundaries and open candidates are kept. New findings in already approved municipalities go to a separate pending log (`neighbour-pending.json`).

Each polygon row records, among other things:
- the classification and its basis
- the method field (OSM-based or drawn manually)
- sources and OSM IDs
- the imagery source and its resolution
- a flag for uncertain boundaries (`needs_orthophoto_review`)

Wall-clock time is recorded per municipality in `timing.json`. Field names and values are in Norwegian.

### Known limitations

- Image acquisition dates are unknown. A structure is shown to exist, but not that it is in use today.
- OSM piers can be offset from the imagery. Boats moored along quays without an OSM pier can fall outside the polygon.
- Visual analysis can miss small facilities. No field survey or land surveying has been done.
- Holmestrand and Horten are earlier map-based pilots and have not been re-checked with the current method.

## Getting started

```bash
git clone https://github.com/joevstaas/oslofjord-bathavner.git
cd oslofjord-bathavner
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/validate_project.py   # expects 456 polygons / 14 municipalities
claude
```

Requires Python 3.11 or newer. Claude Code is installed separately.

Aerial images, raw downloads and QA sheets for approved municipalities are not in git (see `.gitignore`). They are only needed to revise an approved municipality and can be fetched again. After cloning, the validation script therefore reports 0 municipalities with original imagery.

## Contents

- `data/samlet/`: the approved combined file (GeoJSON, WGS84) and its manifest.
- `data/kommuner/<code>-<name>/rev-NN/`: approved municipal deliveries with metadata CSV, candidate ledger, decisions, open candidates, coverage and timing.
- `status.json`: current status with relative paths.
- `docs/METODIKK.md`: the authoritative methodology and municipal logs. `docs/OVERLEVERING.md`: file map and handover notes.
- `CLAUDE.md`: project instructions for Claude Code.
- `work/`: analysis scripts per municipality. The most recent one (`0301-oslo`) is the template for the next.
- `archive/original/`: historical deliveries, notes and scripts for the first municipalities.
- `scripts/validate_project.py`: local check that needs no network.

Sources: © Kartverket; Esri, Vantor, Earthstar Geographics and the GIS User Community; © OpenStreetMap contributors (ODbL); Brønnøysund Register Centre (Enhetsregisteret).

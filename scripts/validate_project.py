from pathlib import Path
import json, csv, collections
from shapely.geometry import shape
ROOT = Path(__file__).resolve().parents[1]
def read(path): return json.loads(path.read_text())
fc = read(ROOT / "data/samlet/oslofjorden-bathavner-samlet.geojson")
features = fc["features"]
assert len(features) == 817, "Forventet 817 godkjente polygoner"
assert len({f["properties"]["id"] for f in features}) == len(features), "Dupliserte ID-er"
assert all(shape(f["geometry"]).is_valid and not shape(f["geometry"]).is_empty for f in features)
by_name = collections.Counter(f["properties"]["municipality"] for f in features)
assert len(by_name) == 23
master = {f["properties"]["id"]: f for f in features}
status = read(ROOT / "status.json")
approved = [m for m in status["municipalities"] if m["status"] != "til_godkjenning"]
pending = [m["name"] for m in status["municipalities"] if m["status"] == "til_godkjenning"]
assert not set(pending) & set(by_name), "Kommune til godkjenning finnes i samlefilen"
for municipality in approved:
    deliveries = [municipality] + municipality.get("supplements", [])
    municipality_features = []
    for delivery in deliveries:
        local = read(ROOT / delivery["result"])["features"]
        municipality_features.extend(local)
        assert all(master[f["properties"]["id"]] == f for f in local)
        with (ROOT / delivery["metadata"]).open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter=";"))
        assert len(rows) == len(local)
        for row, f in zip(rows, local):
            for key, value in f["properties"].items():
                expected = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else ("" if value is None else str(value))
                assert row[key] == expected, (row.get("id"), key)
    ids = [f["properties"]["id"] for f in municipality_features]
    assert len(ids) == len(set(ids)), "Dupliserte ID-er mellom kommuneleveranse og supplement"
    assert len(municipality_features) == by_name[municipality["name"]]
manifest = read(ROOT / "data/samlet/samlet-manifest.json")
assert manifest["features"] == 817 and sum(x["features"] for x in manifest["municipalities"]) == 817
print("OK: 817 polygoner / 23 kommuner, unike ID-er, gyldige geometrier og samsvar mellom samlefil, kommuneleveranser og CSV.")
if pending:
    print("Til godkjenning, utenfor samlefilen:", ", ".join(pending))
image_dirs = [ROOT / "archive/original" / (name + "-pilot") / "images" for name in ["holmestrand", "horten", "tonsberg", "faerder", "sandefjord", "larvik", "moss"]] + [ROOT / "work/3112-rade/images", ROOT / "work/3107-fredrikstad/images"] + [ROOT / "work" / d / "images" for d in ["3201-baerum", "3203-asker", "3312-lier", "3301-drammen", "0301-oslo"]]
print("Originalbilder tilgjengelige for", sum(d.is_dir() for d in image_dirs), "av", len(image_dirs), "kommuner.")

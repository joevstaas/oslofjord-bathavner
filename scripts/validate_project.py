from pathlib import Path
import json, csv, collections
from shapely.geometry import shape
ROOT = Path(__file__).resolve().parents[1]
def read(path): return json.loads(path.read_text())
fc = read(ROOT / "data/samlet/oslofjorden-bathavner-samlet.geojson")
features = fc["features"]
assert len(features) == 469, "Forventet 469 godkjente polygoner"
assert len({f["properties"]["id"] for f in features}) == len(features), "Dupliserte ID-er"
assert all(shape(f["geometry"]).is_valid and not shape(f["geometry"]).is_empty for f in features)
by_name = collections.Counter(f["properties"]["municipality"] for f in features)
assert len(by_name) == 16
master = {f["properties"]["id"]: f for f in features}
status = read(ROOT / "status.json")
approved = [m for m in status["municipalities"] if m["status"] != "til_godkjenning"]
pending = [m["name"] for m in status["municipalities"] if m["status"] == "til_godkjenning"]
assert not set(pending) & set(by_name), "Kommune til godkjenning finnes i samlefilen"
for municipality in approved:
    path = ROOT / municipality["result"]
    local = read(path)["features"]
    assert len(local) == by_name[municipality["name"]]
    assert all(master[f["properties"]["id"]] == f for f in local)
    with (ROOT / municipality["metadata"]).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter=";"))
    assert len(rows) == len(local)
    for row, f in zip(rows, local):
        for key, value in f["properties"].items():
            expected = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else ("" if value is None else str(value))
            assert row[key] == expected, (row.get("id"), key)
manifest = read(ROOT / "data/samlet/samlet-manifest.json")
assert manifest["features"] == 469 and sum(x["features"] for x in manifest["municipalities"]) == 469
print("OK: 469 polygoner / 16 kommuner, unike ID-er, gyldige geometrier og samsvar mellom samlefil, kommuneleveranser og CSV.")
if pending:
    print("Til godkjenning, utenfor samlefilen:", ", ".join(pending))
image_dirs = [ROOT / "archive/original" / (name + "-pilot") / "images" for name in ["holmestrand", "horten", "tonsberg", "faerder", "sandefjord", "larvik", "moss"]] + [ROOT / "work/3112-rade/images", ROOT / "work/3107-fredrikstad/images"] + [ROOT / "work" / d / "images" for d in ["3201-baerum", "3203-asker", "3312-lier", "3301-drammen", "0301-oslo"]]
print("Originalbilder tilgjengelige for", sum(d.is_dir() for d in image_dirs), "av", len(image_dirs), "kommuner.")

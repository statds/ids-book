"""Create a compact teaching map from NYC Open Data ZCTA boundaries."""

import argparse
import json
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "nyc_zcta_boundaries.geojson"
CONTEXT = ROOT / "data" / "zcta_context.csv"
SOURCE = "https://data.cityofnewyork.us/resource/35j5-n34v.geojson"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source", type=Path,
        help="Use a downloaded source GeoJSON instead of requesting the API.",
    )
    args = parser.parse_args()

    if args.source:
        source = json.loads(args.source.read_text(encoding="utf-8"))
    else:
        response = requests.get(SOURCE, params={"$limit": 500}, timeout=120)
        response.raise_for_status()
        source = response.json()

    zctas = gpd.GeoDataFrame.from_features(source["features"], crs="EPSG:4326")
    codes = set(pd.read_csv(CONTEXT, dtype={"zcta": "string"})["zcta"])
    if (
        len(zctas) != len(codes)
        or not zctas["zcta5"].is_unique
        or set(zctas["zcta5"]) != codes
    ):
        raise ValueError("ZCTA geometry does not match the context table.")

    zctas = zctas[["zcta5", "geometry"]].to_crs("EPSG:2263")
    zctas["geometry"] = zctas.geometry.simplify(
        tolerance=50, preserve_topology=True
    )
    zctas = zctas.to_crs("EPSG:4326").sort_values("zcta5")
    zctas = zctas.rename(columns={"zcta5": "zcta"})
    OUTPUT.write_text(zctas.to_json(drop_id=True), encoding="utf-8")
    print(f"Wrote {len(zctas)} ZCTAs to {OUTPUT}")


if __name__ == "__main__":
    main()

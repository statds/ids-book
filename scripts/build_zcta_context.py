"""Build the NYC ZCTA context table from official public data files."""

import csv
import io
import re
from pathlib import Path
from zipfile import ZipFile

import requests


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "zcta_context.csv"
NYC_ZCTAS = "https://data.cityofnewyork.us/resource/35j5-n34v.csv"
ZCTA_GAZETTEER = (
    "https://www2.census.gov/geo/docs/maps-data/data/gazetteer/"
    "2024_Gazetteer/2024_Gaz_zcta_national.zip"
)
ACS_BASE = (
    "https://www2.census.gov/programs-surveys/acs/summary_file/2024/"
    "table-based-SF/data/5YRData"
)
GEO_PREFIX = "860Z200US"


def city_zctas(session):
    response = session.get(
        NYC_ZCTAS,
        params={"$select": "zcta5", "$limit": 5000},
        timeout=60,
    )
    response.raise_for_status()
    codes = {
        row["zcta5"].strip()
        for row in csv.DictReader(io.StringIO(response.text))
    }
    if not codes or any(not re.fullmatch(r"\d{5}", code) for code in codes):
        raise ValueError("The NYC ZCTA list is empty or contains invalid codes.")
    return codes


def acs_values(session, table, codes, fields):
    url = f"{ACS_BASE}/acsdt5y2024-{table.lower()}.dat"
    values = {}
    with session.get(url, stream=True, timeout=120) as response:
        response.raise_for_status()
        lines = (
            line.decode("utf-8-sig")
            for line in response.iter_lines()
            if line
        )
        for row in csv.DictReader(lines, delimiter="|"):
            geo_id = row["GEO_ID"]
            if not geo_id.startswith(GEO_PREFIX):
                continue
            code = geo_id.removeprefix(GEO_PREFIX)
            if code not in codes:
                continue
            if code in values:
                raise ValueError(f"Duplicate ACS row for ZCTA {code}.")
            values[code] = {
                name: nonnegative_integer(row[estimate_column])
                for name, estimate_column, _ in fields
            }
            values[code].update({
                f"{name}_moe": nonnegative_integer(row[moe_column])
                for name, _, moe_column in fields
            })
    return values


def zcta_land_areas(session, codes):
    response = session.get(ZCTA_GAZETTEER, timeout=60)
    response.raise_for_status()
    areas = {}
    with ZipFile(io.BytesIO(response.content)) as archive:
        text_files = [name for name in archive.namelist() if name.endswith(".txt")]
        if len(text_files) != 1:
            raise ValueError("The ZCTA Gazetteer archive has an unexpected layout.")
        with archive.open(text_files[0]) as source:
            reader = csv.DictReader(
                io.TextIOWrapper(source, encoding="utf-8-sig"), delimiter="\t"
            )
            for row in reader:
                code = row["GEOID"]
                if code not in codes:
                    continue
                if code in areas:
                    raise ValueError(f"Duplicate Gazetteer row for ZCTA {code}.")
                area = float(row["ALAND_SQMI"])
                if area <= 0:
                    raise ValueError(f"Nonpositive land area for ZCTA {code}.")
                areas[code] = area
    return areas


def nonnegative_integer(value):
    """Represent Census negative missing-value codes as blank CSV cells."""
    if not value:
        return None
    number = int(value)
    return number if number >= 0 else None


def main():
    with requests.Session() as session:
        codes = city_zctas(session)
        population = acs_values(
            session, "B01003", codes,
            [("population", "B01003_E001", "B01003_M001")],
        )
        income = acs_values(
            session, "B19013", codes,
            [("median_household_income", "B19013_E001", "B19013_M001")],
        )
        vehicles = acs_values(
            session, "B08201", codes,
            [
                ("households_total", "B08201_E001", "B08201_M001"),
                ("households_no_vehicle", "B08201_E002", "B08201_M002"),
            ],
        )
        land_area = zcta_land_areas(session, codes)

    missing = (
        (codes - population.keys())
        | (codes - income.keys())
        | (codes - vehicles.keys())
    )
    if missing:
        raise ValueError(f"ACS tables omit NYC ZCTAs: {sorted(missing)}")

    with OUTPUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow([
            "zcta",
            "acs_year",
            "population",
            "population_moe",
            "land_area_sqmi",
            "population_density_per_sqmi",
            "median_household_income",
            "median_household_income_moe",
            "median_household_income_top_coded",
            "households_total",
            "households_total_moe",
            "households_no_vehicle",
            "households_no_vehicle_moe",
            "share_households_with_vehicle",
        ])
        for code in sorted(codes):
            income_estimate = income[code]["median_household_income"]
            top_coded = income_estimate == 250001
            household_count = vehicles[code]["households_total"]
            no_vehicle_count = vehicles[code]["households_no_vehicle"]
            if household_count and no_vehicle_count is not None:
                if no_vehicle_count > household_count:
                    raise ValueError(f"Invalid vehicle counts for ZCTA {code}.")
                vehicle_share = 1 - no_vehicle_count / household_count
            else:
                vehicle_share = None
            population_count = population[code]["population"]
            area = land_area.get(code)
            population_density = (
                population_count / area
                if population_count is not None and area is not None
                else None
            )
            writer.writerow([
                code,
                2024,
                population_count,
                population[code]["population_moe"],
                area,
                population_density,
                None if top_coded else income_estimate,
                income[code]["median_household_income_moe"],
                top_coded,
                household_count,
                vehicles[code]["households_total_moe"],
                no_vehicle_count,
                vehicles[code]["households_no_vehicle_moe"],
                vehicle_share,
            ])

    print(f"Wrote {len(codes)} NYC ZCTAs to {OUTPUT}")
    missing_area = sorted(codes - land_area.keys())
    if missing_area:
        print(
            "No 2024 Gazetteer land area for "
            f"{len(missing_area)} listed ZCTAs: {', '.join(missing_area)}. "
            "Their land area and population density are blank."
        )


if __name__ == "__main__":
    main()

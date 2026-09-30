"""Build the NYC ZCTA context table from official public data files."""

import csv
import io
import re
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "zcta_context.csv"
NYC_ZCTAS = "https://data.cityofnewyork.us/resource/35j5-n34v.csv"
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


def acs_values(session, table, codes):
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
            values[code] = (
                nonnegative_integer(row[f"{table}_E001"]),
                nonnegative_integer(row[f"{table}_M001"]),
            )
    return values


def nonnegative_integer(value):
    """Represent Census negative missing-value codes as blank CSV cells."""
    if not value:
        return None
    number = int(value)
    return number if number >= 0 else None


def main():
    with requests.Session() as session:
        codes = city_zctas(session)
        population = acs_values(session, "B01003", codes)
        income = acs_values(session, "B19013", codes)

    missing = (codes - population.keys()) | (codes - income.keys())
    if missing:
        raise ValueError(f"ACS tables omit NYC ZCTAs: {sorted(missing)}")

    with OUTPUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "zcta",
            "acs_year",
            "population",
            "population_moe",
            "median_household_income",
            "median_household_income_moe",
            "median_household_income_top_coded",
        ])
        for code in sorted(codes):
            income_estimate, income_moe = income[code]
            top_coded = income_estimate == 250001
            writer.writerow([
                code,
                2024,
                *population[code],
                None if top_coded else income_estimate,
                income_moe,
                top_coded,
            ])

    print(f"Wrote {len(codes)} NYC ZCTAs to {OUTPUT}")


if __name__ == "__main__":
    main()

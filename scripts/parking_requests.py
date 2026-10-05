"""Prepare the shared illegal-parking request table for book examples."""

from pathlib import Path

import pandas as pd


DATA = Path(__file__).resolve().parents[1] / "data"


def load_parking_requests() -> pd.DataFrame:
    """Return NYPD illegal-parking requests created September 6–12, 2026."""
    source = DATA / "311_nypd_lbdwk_2026.csv.zip"
    requests = pd.read_csv(
        source,
        compression="zip",
        dtype={"Unique Key": "string", "Incident Zip": "string"},
        low_memory=False,
    )
    date_format = "%m/%d/%Y %I:%M:%S %p"
    for column in ["Created Date", "Closed Date"]:
        requests[column] = pd.to_datetime(
            requests[column], format=date_format, errors="coerce"
        )

    start = pd.Timestamp("2026-09-06")
    end = pd.Timestamp("2026-09-13")
    parking = requests.loc[
        requests["Created Date"].between(start, end, inclusive="left")
        & requests["Problem (formerly Complaint Type)"].eq("Illegal Parking"),
        [
            "Unique Key", "Created Date", "Closed Date",
            "Problem Detail (formerly Descriptor)", "Borough", "Incident Zip",
            "Latitude", "Longitude",
        ],
    ].copy()
    parking = parking.rename(columns={
        "Unique Key": "request_id",
        "Created Date": "created_at",
        "Closed Date": "closed_at",
        "Problem Detail (formerly Descriptor)": "problem_detail",
        "Borough": "borough",
        "Incident Zip": "incident_zip",
        "Latitude": "latitude",
        "Longitude": "longitude",
    })
    parking["closure_hours"] = (
        parking["closed_at"] - parking["created_at"]
    ).dt.total_seconds() / 3600
    return parking


def load_zcta_context() -> pd.DataFrame:
    """Load and validate the saved NYC ZCTA context lookup."""
    context = pd.read_csv(DATA / "zcta_context.csv", dtype={"zcta": "string"})
    context["zcta"] = context["zcta"].str.strip()
    if context["zcta"].isna().any():
        raise ValueError("The ZCTA lookup contains missing keys.")
    if not context["zcta"].str.fullmatch(r"\d{5}").all():
        raise ValueError("ZCTA keys must be five-digit strings.")
    if context["zcta"].duplicated().any():
        raise ValueError("The ZCTA lookup must contain one row per key.")
    if not context["acs_year"].eq(2024).all():
        raise ValueError("The ZCTA lookup contains an unexpected ACS year.")
    return context


def attach_zcta_context(parking: pd.DataFrame) -> pd.DataFrame:
    """Preserve requests in a checked many-to-one ZIP-label lookup."""
    zip_text = parking["incident_zip"].str.strip()
    with_key = parking.assign(
        zcta_match=zip_text.where(zip_text.str.fullmatch(r"\d{5}", na=False))
    )
    matched = with_key.merge(
        load_zcta_context(),
        left_on="zcta_match", right_on="zcta",
        how="left", validate="many_to_one", indicator=True,
    )
    if len(matched) != len(parking) or not matched["request_id"].is_unique:
        raise ValueError("The ZCTA lookup changed the request unit.")
    return matched

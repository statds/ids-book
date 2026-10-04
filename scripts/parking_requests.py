"""Prepare the shared illegal-parking request table for book examples."""

from pathlib import Path

import pandas as pd


def load_parking_requests() -> pd.DataFrame:
    """Return NYPD illegal-parking requests created September 6–12, 2026."""
    source = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "311_nypd_lbdwk_2026.csv.zip"
    )
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

"""Write the request-ZCTA table used in the modeling exercises."""

from pathlib import Path

from parking_requests import attach_zcta_context, load_parking_requests


OUTPUT = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "parking_requests_with_zcta.parquet"
)


def main():
    parking = load_parking_requests()
    merged = attach_zcta_context(parking)
    merged.to_parquet(OUTPUT, index=False)
    print(f"Wrote {len(merged):,} requests to {OUTPUT}")


if __name__ == "__main__":
    main()

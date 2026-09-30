# NYC ZCTA context data

The file `zcta_context.csv` combines two official public sources. NYC Open
Data's [ZIP Code Tabulation Areas](https://data.cityofnewyork.us/City-Government/ZIP-Code-Tabulation-Areas/35j5-n34v)
dataset supplies the `zcta5` codes for ZCTAs that fall within New York City.
The [2024 American Community Survey five-year summary file](https://www.census.gov/programs-surveys/acs/data/summary-file/2024.html)
supplies population and median household income estimates for those ZCTAs.
Both sources were accessed on September 30, 2026. The city list contains 221
distinct ZCTAs; a listed ZCTA may also extend outside the city boundary.

The source tables are the Census Bureau's [B01003 total population](https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-b01003.dat)
and [B19013 median household income](https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-b19013.dat)
files. The estimates cover the 2020–2024 ACS period, use 2020 ZCTA
geography, and precede the September 2026 service requests. The income
estimate is expressed in 2024 inflation-adjusted dollars. Census ZIP Code
Tabulation Areas and postal ZIP Codes are related but distinct geographic
concepts.

| Column | Definition |
|---|---|
| `zcta` | Five-character ZCTA code from NYC Open Data. |
| `acs_year` | End year of the five-year ACS estimate period, 2024. |
| `population` | B01003 total population estimate. |
| `population_moe` | Published margin of error for the population estimate. |
| `median_household_income` | B19013 median household income estimate in 2024 dollars. |
| `median_household_income_moe` | Published margin of error for the income estimate. |
| `median_household_income_top_coded` | `True` when the source reports the median in the open-ended upper interval rather than as an exact estimate. |

The extraction replaces negative Census missing-value codes with blank cells.
It also leaves the numeric income field blank for four top-coded values that
appear as `250001` in the source file, while retaining a `True` indicator for
those rows. The resulting table has 221 rows, no missing population estimates,
and 34 missing numeric income estimates, including the four top-coded values.
Missing values should remain missing in subsequent calculations unless an
analysis gives an explicit and documented reason to handle them differently.

The [build script](../scripts/build_zcta_context.py) downloads the NYC code
list and the two ACS tables, checks their keys, and writes this CSV. Run it
from the repository root with the project's Python environment:

```bash
python scripts/build_zcta_context.py
```

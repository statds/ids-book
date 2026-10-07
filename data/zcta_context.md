# NYC ZCTA context data

The file `zcta_context.csv` combines data from NYC Open Data and the U.S.
Census Bureau. NYC Open Data's [ZIP Code Tabulation Areas](https://data.cityofnewyork.us/City-Government/ZIP-Code-Tabulation-Areas/35j5-n34v)
dataset supplies the `zcta5` codes for ZCTAs that fall within New York City.
The [2024 American Community Survey five-year summary file](https://www.census.gov/programs-surveys/acs/data/summary-file/2024.html)
supplies population, median household income, and household vehicle
availability estimates for those ZCTAs. The Census Bureau's [2024 ZCTA
Gazetteer file](https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2024_Gazetteer/2024_Gaz_zcta_national.zip)
supplies land area. These sources were accessed on October 7, 2026. The
city list contains 221 distinct ZCTAs; a listed ZCTA may also extend outside
the city boundary. The 2024 Gazetteer matches the geographic vintage of the
2020–2024 ACS estimates used here.

The source tables are the Census Bureau's [B01003 total population](https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-b01003.dat),
[B19013 median household income](https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-b19013.dat),
and [B08201 household size by vehicles available](https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-b08201.dat)
files. The ACS estimates cover the 2020–2024 period and use 2020 ZCTA
geography, so they predate the September 2026 service requests. The income
estimate is expressed in 2024 inflation-adjusted dollars. Census ZIP Code
Tabulation Areas and postal ZIP Codes are related but distinct geographic
concepts.

| Column | Definition |
|---|---|
| `zcta` | Five-character ZCTA code from NYC Open Data. |
| `acs_year` | End year of the five-year ACS estimate period, 2024. |
| `population` | B01003 total population estimate. |
| `population_moe` | Published margin of error for the population estimate. |
| `land_area_sqmi` | 2024 Gazetteer land area in square miles. |
| `population_density_per_sqmi` | Population estimate divided by Gazetteer land area. |
| `median_household_income` | B19013 median household income estimate in 2024 dollars. |
| `median_household_income_moe` | Published margin of error for the income estimate. |
| `median_household_income_top_coded` | `True` when the source reports the median in the open-ended upper interval rather than as an exact estimate. |
| `households_total` | B08201 total household estimate. |
| `households_total_moe` | Published margin of error for the total household estimate. |
| `households_no_vehicle` | B08201 estimate of households with no vehicle available. |
| `households_no_vehicle_moe` | Published margin of error for households with no vehicle available. |
| `share_households_with_vehicle` | One minus households with no vehicle available divided by total households; missing when the total is zero. |

The vehicle measure describes vehicles available for household use, not
vehicle ownership, registration, parking location, or illegal-parking
behavior. Population density combines an ACS estimate with 2024 Gazetteer
land area, and it describes residents per square mile rather than curb or parking
space density. The derived vehicle share's sampling uncertainty is not
computed from the two published margins of error. These are area-level
estimates, not attributes of individual requesters; differences among ZCTAs
cannot establish individual behavior or a causal effect on closure time.
They may help describe neighborhood context, but direct measures of curb
regulations, parking supply, vehicle activity, and precinct workload would
be more informative for those mechanisms.

The extraction replaces negative Census missing-value codes with blank cells.
It also leaves the numeric income field blank for four top-coded values that
appear as `250001` in the source file, while retaining a `True` indicator for
those rows. The resulting table has 221 rows and no missing population
estimates. It has 34 missing numeric income estimates, including the four
top-coded values, and 29 missing vehicle shares because the ACS household
estimate is zero for those codes. All 221 listed ZCTAs have land-area records
in the 2024 Gazetteer. Missing values should remain missing in subsequent
calculations unless an analysis gives an explicit and documented reason to
handle them differently.

The [build script](../scripts/build_zcta_context.py) downloads the NYC code
list, the Gazetteer file, and the three ACS tables, checks their keys, and
writes this CSV. Run it from the repository root with the project's Python
environment:

```bash
python scripts/build_zcta_context.py
```

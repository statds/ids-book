# NYC ZCTA boundaries

The file `nyc_zcta_boundaries.geojson` contains polygons from NYC Open Data's
[ZIP Code Tabulation Areas](https://data.cityofnewyork.us/City-Government/ZIP-Code-Tabulation-Areas/35j5-n34v)
dataset. The source was downloaded on October 3, 2026. It has 221 distinct
ZCTAs that fall within or extend into New York City. The geometry is supplied
in longitude and latitude coordinates (EPSG:4326), and its codes match the
221 entries in `zcta_context.csv`.

The [build script](../scripts/build_zcta_boundaries.py) selects each ZCTA code
and geometry, projects the polygons to New York State Plane coordinates
(EPSG:2263), simplifies them with a 50-foot tolerance while preserving
topology, and returns the result to EPSG:4326. The compact file supports
maps in the book without a network request at render time. Simplification
removes some boundary detail, so a point near a border should be checked
against the original geometry before assigning it to an area. Run the script
from the repository root with the book's Python environment to rebuild the
file from the official API:

```bash
.ids/bin/python scripts/build_zcta_boundaries.py
```

ZCTAs are Census statistical areas, while `Incident Zip` in a 311 record is
a postal ZIP Code. Equality of their five-digit labels is a useful but
imperfect analytical approximation, as explained in the book's ZCTA
matching discussion. Neither geometry nor a count of requests supplies a
denominator for the risk of illegal parking.

# Scottish Census

## Data Sources

This section lists the sources of data used for the Scottish Census analysis:

-   [Scottish Census Data 2022](https://www.scotlandscensus.gov.uk/documents/2022-output-area-data/) - Detailed census data for Scotland's output areas.
-   [Scottish Buildings](https://download.geofabrik.de/europe/united-kingdom/scotland.html) - Building data from Geofabrik, specific to Scotland.
-   [Scottish Output Areas](https://www.nrscotland.gov.uk/statistics-and-data/geography/our-products/census-datasets/2022-census/2022-census-digital-boundaries) - Digital boundaries for the 2022 census, clipped to the coastline.

### Setup Instructions

To prepare the data conversion script for execution, follow these steps:

1. Make the script executable:

```bash
chmod +x convert_to_pmtiles.sh
```

2. Run the script from your terminal:

```bash
./convert_to_pmtiles.sh
```

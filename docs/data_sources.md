# Data Sources

## 1. Our World in Data (OWID)
- **Dataset:** CO2 and Greenhouse Gas Emissions
- **Source:** https://github.com/owid/co2-data
- **File:** `data/raw/owid-co2-data.csv`
- **Format:** CSV
- **Purpose:** Provides country-level carbon emissions data, including CO2 emissions per capita.

## 2. United Nations Development Programme (UNDP)
- **Dataset:** Human Development Reports 2025, Composite Indices Complete Time Series
- **Source:** https://hdr.undp.org/data-center/documentation-and-downloads
- **File:** `data/raw/HDR25_Composite_indices_complete_time_series.csv`
- **Format:** CSV
- **Purpose:** Provides annual Human Development Index (HDI) values for countries from 1990 through 2023, allowing comparisons of human development across countries and over time.
- **Acquisition method:** Download the Composite Indices Complete Time Series CSV from the official UNDP Human Development Reports Data Center. Save the file in `data/raw/` using the filename above.
- **Processing:** The cleaning script extracts HDI values for 1990–2023 and standardizes the country identifiers for integration with the other datasets.
- **Integrity verification:** The downloaded file can be checked against its recorded SHA-256 checksum using `scripts/verify_raw_data.py`.

## 3. World Bank
- **Dataset:** World Development Indicators
- **Source:** https://data.worldbank.org/
- **Format:** CSV
- **Purpose:** Provides GDP per capita and additional indicators for examining differences in carbon emissions.

### Selected Indicators

| Indicator | World Bank Code | Raw File |
|---|---|---|
| GDP per capita (current US$) | NY.GDP.PCAP.CD | `gdp_per_capita.csv` |
| Urban population (% of total) | SP.URB.TOTL.IN.ZS | `urban_population.csv` |
| Industry, including construction (% of GDP) | NV.IND.TOTL.ZS | `industry_including_construction.csv` |
| Renewable energy consumption (% of total final energy consumption) | EG.FEC.RNEW.ZS | `renewable_energy_consumptino.csv` |

## Data Management
Original downloaded datasets are stored in `data/raw/` to preserve their contents. Cleaned datasets will be stored in `data/cleaned/` and the merged country-year dataset will be stored in `data/integrated/`.

## Provenance Information to Complete
- Download date for each source: November 15, 2026
- Source licenses and redistribution permissions: Pending review
- SHA-256 checksums: Pending calculation 
- Dataset versions and temporal coverage: Pending verification

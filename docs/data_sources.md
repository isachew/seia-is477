# Data Sources

## 1. Our World in Data (OWID)
- **Dataset:** CO2 and Greenhouse Gas Emissions
- **Source:** https://github.com/owid/co2-data
- **File:** `data/raw/owid-co2-data.csv`
- **Format:** CSV
- **Purpose:** Provides country-level carbon emissions data, including CO2 emissions per capita.

## 2. United Nations Development Programme (UNDP)
- **Dataset:** Human Development Reports 2025 Statistical Annex, HDI Table
- **Source:** https://hdr.undp.org/data-center/documentation-and-downloads
- **File:** `data/raw/HDR25_Statistical_Annex_HDI_Table.xlsx`
- **Format:** Excel
- **Purpose:** Provides Human Development Index (HDI) data for comparing human development across countries.
- **Verification needed:** Confirm that the file contains annual HDI observations for 1990–2023.

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

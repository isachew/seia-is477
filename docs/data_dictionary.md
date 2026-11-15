# Data Dictionary

## Dataset Overview

The integrated dataset, `data/integrated/country_year_integrated.csv`, combines indicators from Our World in Data (OWID), the United Nations Development Programme (UNDP) and the World Bank.

The dataset contains 6,630 country-year records representing 195 countries from 1990 to 2023. Each row represents one country in one year.

## Variable Definitions

| Variable | Description | Unit / Format | Source |
|---|---|---|---|
| `iso3` | Three-letter country identifier used to match records across sources | ISO-3 country code | Standardized across sources |
| `year` | Calendar year of observation | Integer, 1990–2023 | All sources |
| `hdi` | Human Development Index, a composite measure of health, education and standard of living | Index, 0–1 | UNDP |
| `co2_per_capita` | Annual territorial CO₂ emissions divided by population | Metric tonnes of CO₂ per person | OWID |
| `gdp_per_capita` | Gross domestic product divided by population | Current US dollars per person | World Bank |
| `urban_population_pct` | Percentage of the population living in urban areas | Percentage, 0–100 | World Bank |
| `industry_share_pct` | Industry, including construction, value added as a share of GDP | Percentage of GDP | World Bank |
| `renewable_energy_pct` | Renewable energy consumption as a share of total final energy consumption | Percentage, 0–100 | World Bank |

## Dataset Structure

- **Primary key:** `iso3` and `year` together uniquely identify each observation.
- **Geographic coverage:** 195 countries selected using the country codes available in the UNDP dataset.
- **Temporal coverage:** 1990–2023.
- **Total records:** 6,630.
- **Missing values:** Missing indicator values are represented as blank cells in the CSV and are interpreted as `NaN` when loaded with pandas.
- **Duplicate records:** The post-integration quality assessment found no duplicate country-year keys.

## Important Data Limitations

The availability of indicator values differs across countries and years. Although the integrated dataset includes a row for every country-year combination, not every row contains values for all six indicators.

The renewable energy consumption dataset has no available observations for 2023. Therefore, analyses involving renewable energy must account for this limitation.

GDP per capita is measured in current US dollars rather than inflation-adjusted or purchasing-power-parity dollars. This distinction should be considered when comparing income levels across countries and years.

The dataset also contains one unusually high CO₂ emissions observation flagged during the post-integration quality assessment. This observation requires verification against the original source before deciding whether it should be included in specific analyses.

## Data Processing

The integrated dataset was produced through the following scripts:

1. `scripts/assess_data_quality.py`
2. `scripts/clean_data.py`
3. `scripts/integrate_data.py`
4. `scripts/assess_post_integration.py`

Raw dataset integrity is checked using `scripts/verify_raw_data.py`. The workflow is coordinated through `scripts/run_all.py`.

Original data files are preserved in `data/raw/`, cleaned datasets are stored in `data/cleaned/` and the integrated dataset is stored in `data/integrated/`.

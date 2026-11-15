# Data Licensing and Attribution

## Overview

This project, *Income, Human Development, and Carbon Emissions*, integrates publicly available datasets from Our World in Data (OWID), the United Nations Development Programme (UNDP) and the World Bank. The original datasets are preserved in `data/raw/`, and their sources are documented in `docs/data_sources.md`.

## 1. Our World in Data (OWID)

- **Dataset:** CO₂ and Greenhouse Gas Emissions
- **Source:** https://github.com/owid/co2-data
- **License:** To be verified against the dataset's published license and attribution requirements.
- **Use in project:** Annual CO₂ emissions per capita.

OWID combines information from multiple underlying sources. Any relevant attribution or reuse conditions for the emissions data should be reviewed before the final dataset is redistributed.

## 2. United Nations Development Programme (UNDP)

- **Dataset:** Human Development Report 2025, Composite Indices Complete Time Series
- **Source:** https://hdr.undp.org/data-center/documentation-and-downloads
- **License:** To be verified against UNDP's published data usage terms.
- **Use in project:** Annual Human Development Index values.

The project uses HDI observations from 1990 through 2023. The UNDP dataset should be cited as the original source of these values.

## 3. World Bank

- **Dataset:** World Development Indicators
- **Source:** https://data.worldbank.org/
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0), subject to any third-party exceptions identified by the World Bank.
- **Use in project:** GDP per capita, urban population percentage, industry share of GDP and renewable energy consumption percentage.

World Bank indicators are used for academic analysis. Appropriate attribution should be included in the final report and dataset documentation.

## 4. Integrated Dataset

The integrated dataset combines information from the three providers. The project does not claim ownership of the original source data.

Before assigning a license to the integrated dataset, the group will review the reuse conditions of all source datasets to determine which licensing terms are compatible with redistribution.

## 5. Code Licensing

The Python scripts in this repository were developed for the course project. The group will select an appropriate open-source software license before final submission.

## 6. Attribution

The final project report will acknowledge all three data providers and link to the original datasets. Dataset-specific citations and licensing information will be updated as the relevant terms are confirmed.

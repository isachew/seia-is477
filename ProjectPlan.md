# Project Plan: Income, Human Development and Carbon Emissions
## Overview
The goal of this project is to build a clean, documented, and reproducible country-by-year dataset that links carbon emissions to income and Hyman development, and use it to research how emissions can change as countries develop. We will integrate three sources: the Our World in Data C02 Emissions dataset, the UN Human Development Reports composite indices, and World Bank Open Data indicators. 

Our planned approach to achieve this involves four main phases:
1. **Data Acquisition & Ingestion:** Pulling raw data from three authoritative global sources (World Bank, UNDP, and Our World in Data) while enforcing strict provenance tracking using checksums and download logs.
2. **Data Wrangling & Integration:** Merging the datasets using standardized ISO country codes and calendar years as composite keys.
3. **Exploratory Data Analysis (EDA):** Investigating statistical relationships, tracking trajectories of high-development nations, and identifying environmental Kuznets curve patterns.
4. **Reproducible Reporting:** Compiling our code, cleaning scripts, and final insights into a fully reproducible GitHub repository and final report.

## Team
| Member | Role | Planned responsibilities |
|---|---|---|
| Isa | Acquisition and repository lead | Repository structure, one download script per source, checksums, GitHub tags and releases |
| Sarah | Data quality and cleaning lead | Pre- and post-integration quality assessments, cleaning scripts |
| Ean | Integration and workflow lead | Integration script, workflow orchestration, reproducibility testing |
| Abigail | Documentation and ethics lead | License and terms-of-use review, metadata and data dictionary, report coordination |

All four members will contribute to the analysis, review each other's pull requests, and co-write the status report.
## Research Questions
1. How are per-capita CO2 emissions related to GDP per capita and the Human Development Index across countries from 1990 to 2023?
2. Among countries with very high human development, have per-capita emissions fallen while development continued to rise?
3. Do urbanization, industry share of GDP, and renewable energy share help explain why countries at similar income levels have different per-capita emissions?
## Datasets
None of our datasets come from Kaggle.

**1. Our World in Data: CO2 and Greenhouse Gas Emissions**
- Source: https://ourworldindata.org/grapher/co-emissions-per-capita?tab=chart&country=USA~GBR~CHN~ZAF~PAN
- Content: annual CO2 and greenhouse gas emissions (total, per capita, by fuel), energy use, plus population and GDP columns
- Role: the outcome we are studying (emissions)

**2. UN Human Development Reports: composite indices time series**
- Source: https://hdr.undp.org/data-center/human-development-index#/indicies/HDI
- Content: Human Development Index and components (life expectancy, schooling, income per person), 1990 to 2023
- Role: the human development measure

**3. UN Human Development Reports: composite indices time series**
- Source: https://data.worldbank.org
- Content: GDP per capita, urban population share, industry value added, renewable energy share, and population
- Role: income and the explanatory factors for question 3

**Why integration is feasible:**
**Storage and organization:**
## Timeline
## Constraints
- **Uneven coverage:** the UN data begins in 1990 and some indicators, such as renewable energy share, have gaps for smaller countries and recent years, which limits the complete-case sample.
- **Changing sources:** all three are updated in place, so results can shift between runs. We will record download dates and checksums, and keep copies of raw files where the license allows.
## Gaps
- We still need to read and document the exact terms of use for the UN Human Development Reports and World Bank data, and confirm whether raw copies may be redistributed in our repository.
- We need guidance on the expected depth of the metadata and on which metadata standard to follow.
- We have not yet decided how to treat missing values (drop, interpolate, or flag), which depends on what the quality assessment shows.

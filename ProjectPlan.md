# Project Plan: Income, Human Development and Carbon Emissions
## Overview
The goal of this project is to build a clean, documented, and reproducible country-by-year dataset that links carbon emissions to income and Human development, and use it to research how emissions can change as countries develop. We will integrate three sources: the Our World in Data C02 Emissions dataset, the UN Human Development Reports composite indices, and World Bank Open Data indicators.

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
- Content: Annual CO2 and greenhouse gas emissions (total, per capita, by fuel), energy use, plus population and GDP columns
- Role: The outcome we are studying (emissions)

**2. UN Human Development Reports: Composite Indices Time Series**
- Source: https://hdr.undp.org/data-center/human-development-index#/indicies/HDI
- Content: Human Development Index and components (life expectancy, schooling, income per person), 1990 to 2023
- Role: The human development measure

**3. World Bank Open Data: World Development Indicators**
- Source: https://data.worldbank.org/indicator/NY.GDP.PCAP.CD?end=2025&start=1960&view=chart)
- Content: Annual GDP per capital (USD $)from 1960-2025, as reported by country and geographic region.
- Role: Income and the explanatory factors for question 3

**Why integration is feasible:**
Integration is structurally straightforward because all three datasets share two universal identifiers: **standardized country identifiers** (such as ISO Alpha-3 country codes or matching country names) and **calendar years** (annual frequency). Because all three sources operate at the exact same observational unit—the **country-year** level—we can perform reliable relational merges (using Python/pandas or SQL) on the composite key. Additionally, their temporal coverages heavily overlap (particularly from 1990 onward), ensuring we have a robust multi-decade window for panel data analysis without structural mismatches in time frames.

**Storage and organization:**
We will organize our project files in a structured GitHub repository to support reproducibility and clear documentation of each stage of the data curation process. The datasets will primarily consist of structured, tabular data stored in CSV files, with country-level observations recorded across multiple years. We plan to separate raw, cleaned, and integrated datasets into different folders to preserve the original data and document all transformations. A scripts/ folder will contain Python scripts for data acquisition, cleaning, integration, and analysis, while an outputs/ folder will store our final results and visualizations. We will use consistent file naming conventions and relative file paths to ensure that the workflow can be reproduced across different computers. Additionally, we will maintain a data dictionary describing the variables, data types, units of measurement, and sources. This organizational structure will help track data provenance, prevent accidental modifications to raw data, and allow each team member to work on different stages of the project.

## Timeline
| Dates | Task | Description | Responsible Member(s) |
|---|---|---|---|
| Oct 12 | Project plan release | Commit `ProjectPlan.md`, tag and release `project-plan` | All members; Isa coordinates |
| Oct 13 to 19 | Acquisition and organization | Repository structure; one download script per source; checksums; record access dates and licenses | Isa, Abigail |
| Oct 20 to 26 | Pre-integration quality assessment | Profile each dataset for accuracy, completeness, timeliness, and consistency; document results | Sarah |
| Oct 27 to Nov 2 | Data cleaning | Reshape the UN file to long format; remove regional aggregates; standardize country codes; handle missing values and outliers | Sarah |
| Nov 3 to 9 | Integration | Join the three cleaned tables on country code and year; log unmatched keys | Ean, Sarah |
| Nov 10 to 15 | Post-integration quality assessment | Re-assess the four dimensions on the integrated table; compare GDP and population across sources as an accuracy check | Ean, Sarah |
| Nov 16 to 19 | Status report | Write and release the interim status report; update this plan from feedback | All members |
| Nov 20 to 29 | Analysis and automation | Descriptive statistics and plots for the three questions | All members |
| Nov 30 to Dec 4 | Reproducibility and metadata | Run the workflow from a fresh clone; pin package versions; write the data dictionary and metadata | Ean, Abigail, Isa |
| Dec 5 to 7 | Final submission | Final report and `final-project` GitHub release | All members |

## Constraints
- **Uneven Coverage:** The UN data begins in 1990 and some indicators, such as renewable energy share, have gaps for smaller countries and recent years, which limits the complete-case sample.
- **Changing Sources:** All three are updated in place, so results can shift between runs. We will record download dates and checksums, and keep copies of raw files where the license allows.
- **Data Integration:** Although the datasets share country identifiers and calendar years, differences in country naming conventions, country codes, and reporting periods may complicate integration. Some datasets may also include regional aggregates that do not correspond to individual countries. We will standardize country identifiers, exclude non-country aggregates, and document unmatched records.
- **Data Consistency:** The three sources may use different definitions, measurement units, or calculation methods for similar indicators. For example, GDP per capita and population estimates may differ across sources. We will assess consistency before and after integration to identify discrepancies and determine appropriate cleaning procedures. 
## Gaps
- We still need to read and document the exact terms of use for the UN Human Development Reports and World Bank data, and confirm whether raw copies may be redistributed in our repository.
- We need guidance on the expected depth of the metadata and on which metadata standard to follow.
- We have not yet decided how to treat missing values (drop, interpolate, or flag), which depends on what the quality assessment shows.
- We would need to decide how to assess and determine accuracy when GDP and population values that may appear in the OWID and World Bank slightly differ.

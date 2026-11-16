# Status Report 
**Income, Human Development, and Carbon Emissions**

## 1. Project Overview & Current Status 
Our project builds a clean, documented, and reproducible country-by-year dataset that examines the relationship between carbon emissions, income, and human development from 1990 to 2023. We use it to study how emissions change as countries develop. We are integrating three sources: the **Our World in Data (OWID) CO2 and Greenhouse Gas Emissions** dataset, the **UN Human Development Reports (HDR) Composite Indices Time Series**, and the **World Bank World Development Indicators (WDI)**. Our research questions are:
1. How are per-capita CO2 emissions related to GDP per capita and the Human Development Index (HDI) across countries from 1990 to 2023?
2. Among countries with very high human development, have per-capita emissions fallen while development continued to rise?
3. Do urbanization, industry share of GDP, and renewable energy share help explain why countries at similar income levels have different per-capita emissions?

## 2. Progress on Planned Tasks

### 2.1 Data Acquisition & Organization
Our group acquired data from three sources: Our World in Data (OWID), the United Nations Development Programme (UNDP) and the World Bank. These datasets provide information on CO₂ emissions per capita, Human Development Index (HDI), GDP per capita, urban population, industry share of GDP and renewable energy consumption. During acquisition, we discovered that the original UNDP statistical annex didn't contain the complete annual HDI observations needed for analysis. To address this issue, we obtained the UNDP composite indices time-series dataset, which includes HDI values from 1990 to 2023. All original datasets have been preserved in the [`data/raw/`](data/raw/) folder, and their sources are documented in [`docs/data_sources.md`](docs/data_sources.md). We also developed and tested [`scripts/acquire_data.py`](scripts/acquire_data.py), which retrieves the OWID emissions dataset and four World Bank indicators from their published sources without modifying the original raw datasets.

### 2.2 Data Quality Assessment & Cleaning
We developed a Python script in [`scripts/`](scripts/) to evaluate the raw datasets across four data quality dimensions: completeness, accuracy, consistency and timeliness. The assessment identified missing values across all six indicators, with industry share of GDP having the highest missing-value percentage at 13.54%. We also identified 1,217 OWID records without country codes and found that the renewable energy dataset only contained available observations through 2022. No duplicate country-year records or invalid values were flagged by the implemented checks.

Based on these findings, we created a cleaning script to standardize country identifiers, reshape datasets into a consistent country-year format and convert relevant variables into numeric values. We restricted the data to 195 countries and the 1990–2023 study period, resulting in six cleaned datasets containing 6,630 country-year records each. Missing observations were preserved rather than replaced with estimated values. The assessment results and cleaning summaries are documented in the repository. We also implemented SHA-256 integrity verification to confirm that the six raw datasets match their recorded checksums before processing.

### 2.3 Data Integration & Workflow
After data cleaning, we developed a Python integration script to combine all six indicators using ISO-3 country codes and years as matching identifiers. The resulting integrated dataset contains 6,630 records representing 195 countries across 34 years, from 1990 to 2023. The integration process preserved missing values and did not result in the loss of country-year records. We saved the master dataset in [`data/integrated/`](data/integrated/) and documented the integration results in [`results/integration/`](results/integration/).

To support reproducibility, we developed an automated workflow, [`scripts/run_all.py`](scripts/run_all.py), which runs raw data integrity verification, pre-integration quality assessment, cleaning, integration and post-integration quality assessment in sequence. We tested the complete workflow, with all six raw datasets passing SHA-256 verification and all processing steps completing without errors. The post-integration assessment confirmed that the integrated dataset contains no duplicate country-year records and evaluated indicator completeness and coverage for each research question. These results are documented in [`results/post_integration_quality/`](results/post_integration_quality/). Although the processing workflow is automated, the acquisition of updated source data remains partially manual.

### 2.4 Documentation & Ethics
We have documented the origin of each dataset, including source URLs and dataset descriptions, in [`docs/data_sources.md`](docs/data_sources.md), and our checksums record the exact versions of the raw files we used. OWID data is published under a Creative Commons Attribution (CC BY 4.0) license, and World Bank WDI data is also available under CC BY 4.0, so both may be shared with proper attribution. We still need to confirm the UNDP Human Development Reports terms of use, including whether we may redistribute the raw time-series file in our repository. If redistribution is not allowed, we will remove the raw file and provide download instructions instead.

Remaining documentation includes a data dictionary describing each variable in the integrated dataset (name, definition, units, source, and years covered), project-level metadata, and a README explaining how to run the workflow from a fresh clone.


## 3. Updated Project Timeline 
We are on track with our original plan. Acquisition, quality assessment, cleaning, integration, and post-integration assessment are complete, and the automated workflow runs end to end. The remaining tasks are analysis, documentation, the reproducibility test, and the final report, all of which fit within the original schedule and finish by December 7.

| Task | Original dates | Status | Expected completion | Responsible |
|---|---|---|---|---|
| Project plan release | Oct 12 | Completed | Oct 12 | All; Isa coordinates |
| Acquisition and organization | Oct 13–19 | Completed | — | Isa, Abigail |
| Pre-integration quality assessment | Oct 20–26 | Completed | — | Sarah |
| Data cleaning | Oct 27–Nov 2 | Completed | — | Sarah |
| Integration | Nov 3–9 | Completed | — | Ean, Sarah |
| Post-integration quality assessment | Nov 10–15 | Completed | — | Ean, Sarah |
| Workflow automation (`run_all.py`) | Nov 20–29 | Completed (ahead of schedule) | — | Ean |
| Status report | Nov 16–19 | In progress | Nov 19 | All |
| UNDP terms-of-use review | Oct 13–19 | In progress | Nov 22 | Abigail |
| Analysis and visualizations | Nov 20–29 | Not started | Nov 29 | All |
| Reproducibility test and package pinning | Nov 30–Dec 4 | Not started | Dec 4 | Ean, Isa |
| Data dictionary and metadata | Nov 30–Dec 4 | Not started | Dec 4 | Abigail |
| Final report and `final-project` release | Dec 5–7 | Not started | Dec 7 | All |


## 4. Changes to Original Project Plan (~150 words)
- Have we made any changes to our original approach, datasets, or research questions?
- Did we receive any feedback on Milestone 2 that we need to address?
- Explain any changes we've made to our timeline or responsibilities.
- If the overall plan hasn't changed, just explain that we're keeping the same approach and adjusting our timeline as needed.

Draft, please revise:

Our group has maintained the original project objectives and research questions, but we have made several adjustments based on instructor feedback and challenges encountered during data acquisition and processing.

One change involved our UNDP dataset. We initially downloaded the 2025 Human Development Report statistical annex, but discovered that it did not provide the complete annual HDI observations needed for our 1990–2023 analysis. To address this issue, we obtained the UNDP composite indices time-series dataset, which provides the historical HDI values required for our research. This adjustment allows us to examine changes in human development over time rather than relying on a limited number of years.

We also clarified our approach to Research Question 3 based on instructor feedback. Rather than broadly examining factors that might explain differences in emissions, we will specifically focus on urban population percentage, industry share of GDP and renewable energy consumption percentage. Our analysis will remain primarily descriptive, using comparisons and visualizations to explore how these indicators relate to emissions among countries with similar income levels. We do not plan to make causal claims based on these relationships.

Finally, our initial data quality assessment revealed differences in data availability across sources. In particular, renewable energy consumption observations were available only through 2022, despite our overall study period extending through 2023. We will preserve missing observations and clearly document these limitations rather than substitute values from other years. These adjustments do not change our overall research goals but help ensure that our analysis remains accurate, transparent and consistent with the available data.

## 5. Challenges & Proposed Solutions (~200 words)
- What problems have we run into so far?
- Potential issues to discuss if we've encountered them:
  - Differences in country names or country codes across datasets.
  - Missing data for certain countries or years.
  - Differences in how sources measure GDP, emissions, or development.
  - Falling behind our original project timeline.
- Explain what we've done to address each issue or what we plan to do about it.

## 6. Individual Contributions (~150–200 words total)
- Each person writes a short paragraph (around 40–50 words) about what they've worked on so far.
- Mention specific tasks completed, files created, or contributions to the report.
- Each person should add and commit their own paragraph to GitHub so their contribution shows up in the commit history.

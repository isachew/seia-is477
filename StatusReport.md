# Status Report 
**Income, Human Development, and Carbon Emissions**

## 1. Project Overview & Current Status 
Our project builds a clean, documented, and reproducible country-by-year dataset that examines the relationship between carbon emissions, income, and human development from 1990 to 2023. We are integrating three sources: **Our World in Data (OWID) CO2 and Greenhouse Gas Emissions** dataset, **UN Human Development Reports (HDR) Composite Indices Time Series**, and **World Bank World Development Indicators (WDI)**. Research questions:

1. How are per-capita CO2 emissions related to GDP per capita and the Human Development Index (HDI) across countries from 1990 to 2023?
2. Among countries with very high human development, have per-capita emissions fallen while development continued to rise?
3. Do urbanization, industry share of GDP, and renewable energy share help explain why countries at similar income levels have different per-capita emissions?

## 2. Progress on Planned Tasks

### 2.1 Data Acquisition & Organization
Our data is acquired from: Our World in Data (OWID), the United Nations Development Programme (UNDP) and the World Bank. These datasets provide information on CO₂ emissions per capita, Human Development Index (HDI), GDP per capita, urban population, industry share of GDP and renewable energy consumption. During acquisition, we discovered that the original UNDP statistical annex didn't contain the complete annual HDI observations needed for analysis. To address this issue, we obtained the UNDP composite indices time-series dataset, which includes HDI values from 1990 to 2023. All original datasets have been preserved in the [`data/raw/`](data/raw/) folder, and their sources are documented in [`docs/data_sources.md`](docs/data_sources.md). We also developed and tested [`scripts/acquire_data.py`](scripts/acquire_data.py), which retrieves the OWID emissions dataset and four World Bank indicators from their published sources without modifying the original raw datasets.

### 2.2 Data Quality Assessment & Cleaning
We developed a Python script in [`scripts/`](scripts/) to evaluate the raw datasets across four data quality dimensions: completeness, accuracy, consistency and timeliness. The assessment identified missing values across all six indicators, with industry share of GDP having the highest missing-value percentage at 13.54%. We also identified 1,217 OWID records without country codes and found that the renewable energy dataset only contained available observations through 2022. No duplicate country-year records or invalid values were flagged by the implemented checks.

Based on these findings, we created a cleaning script to standardize country identifiers, reshape datasets into a consistent country-year format and convert relevant variables into numeric values. We restricted the data to 195 countries and the 1990–2023 study period, resulting in six cleaned datasets containing 6,630 country-year records each. Missing observations were preserved rather than replaced with estimated values. The assessment results and cleaning summaries are documented in the repository. We also implemented SHA-256 integrity verification to confirm that the six raw datasets match their recorded checksums before processing.

### 2.3 Data Integration & Workflow
After data cleaning, we developed a Python integration script to combine all six indicators using ISO-3 country codes and years as matching identifiers. The resulting integrated dataset contains 6,630 records representing 195 countries across 34 years, from 1990 to 2023. The integration process preserved missing values and didn't result in the loss of country-year records. We saved the master dataset in [`data/integrated/`](data/integrated/) and documented the integration results in [`results/integration/`](results/integration/).

To support reproducibility, we developed an automated workflow, [`scripts/run_all.py`](scripts/run_all.py), which runs raw data integrity verification, pre-integration quality assessment, cleaning, integration and post-integration quality assessment in sequence. We tested the complete workflow, with all six raw datasets passing SHA-256 verification and all processing steps completing without errors. The post-integration assessment confirmed that the integrated dataset contains no duplicate country-year records and evaluated indicator completeness and coverage for each research question. These results are documented in [`results/post_integration_quality/`](results/post_integration_quality/). Although the processing workflow is automated, the acquisition of updated source data remains partially manual.

### 2.4 Documentation & Ethics
We documented the origin of each dataset in [`docs/data_sources.md`](docs/data_sources.md) and recorded licensing and attribution information in [`docs/data_licenses.md`](docs/data_licenses.md). The World Bank WDI data is available under CC BY 4.0. The OWID and UNDP terms are still being verified, including whether the raw UNDP time-series file may be redistributed in our repository; if it cannot, we will remove it and provide download instructions instead. We have drafted a data dictionary for the integrated dataset in [`docs/data_dictionary.md`](docs/data_dictionary.md), covering each variable's definition, units, and source, and schema.org dataset metadata in [`docs/metadata.jsonld`](docs/metadata.jsonld). Remaining work includes confirming the outstanding licenses, choosing a license for our code and integrated dataset, and writing a README that explains how to run the workflow from a fresh clone.


## 3. Updated Project Timeline 

Some tasks were completed later than planned, and we have updated our timeline to ensure completion of remaining work.

| Task | Original dates | Status | Expected completion | Responsible |
|---|---|---|---|---|
| Project plan release | Oct 12 | Completed | Oct 12 | All; Isa coordinates |
| Acquisition and organization | Oct 13–19 | Completed | Nov 15 | Sarah |
| Pre-integration quality assessment | Oct 20–26 | Completed | Nov 15 | Sarah |
| Data cleaning | Oct 27–Nov 2 | Completed | Nov 15 | Sarah |
| Integration | Nov 3–9 | Completed | Nov 15 | Sarah |
| Post-integration quality assessment | Nov 10–15 | Completed | Nov 15 | Sarah |
| Workflow automation and integrity checks | Nov 20–29 | Completed (ahead of schedule) | Nov 15 | Sarah |
| Status report | Nov 16–19 | In progress | Nov 16 | All |
| License and terms-of-use review | Oct 13–19 | In progress | Nov 22 | Abigail |
| Exploratory data analysis | New task | Not started | Nov 24 | Ean, Isa |
| Create Graphs and Visualizations | New task | Not started | Nov 27 | Isa, Abigail |
| Dataset validation | New task | Drafted | Dec 4 | All |
| Interpretation of findings | Nov 20–29 | Not started | Nov 29 | All |
| Reproducibility test and package pinning | Nov 30–Dec 4 | Not started | Dec 4 | Ean, Isa |
| Final report and `final-project` release | Dec 5–7 | Not started | Dec 5–7 | All |


## 4. Changes to Original Project Plan 
Our project goals and research questions are unchanged. We made the following changes in response to Milestone 2 feedback and issues found during processing.

**Feedback: clearly identify the explanatory variables for RQ3.** We now specify four World Bank Indicators: GDP per capita in current US dollars (`NY.GDP.PCAP.CD`), urban population share (`SP.URB.TOTL.IN.ZS`), industry share of GDP including construction (`NV.IND.TOTL.ZS`), and renewable energy share of final energy consumption (`EG.FEC.RNEW.ZS`). These are retrieved by [`scripts/acquire_data.py`](scripts/acquire_data.py) and defined in [`docs/data_dictionary.md`](docs/data_dictionary.md).

**Feedback: keep the analysis simple and descriptive.** We will answer all three research questions with summary statistics, comparisons across income and HDI groups, and visualizations. We will not fit models or make causal claims, keeping the focus on data curation.

**UNDP dataset.** The 2025 HDR statistical annex lacked complete annual HDI values, so we replaced it with the UNDP composite indices time series, which covers 1990–2023.

**Timeline and responsibilities.** Acquisition through integration finished later than planned but was complete by November 15. Remaining tasks have been reassigned as shown in Section 3.

**Missing values.** Our project plan left open whether to drop, interpolate, or flag missing values. We chose to preserve them and document gaps, such as renewable energy data ending in 2022, rather than estimate values. 

## 5. Challenges & Proposed Solutions 

A challenge was acquiring the UNDP dataset, since our research is related to the HDI and the original didn't include all annual HDI values. We obtained the UNDP composite indices time-series dataset to get coverage from 1990-2023 by downloading and verifying it with the SHA-256 checksums since it couldn't be fetched directly via our acquisition script. 

To resolve missing data, we kept missing values instead of estimating and assuming values that could be inaccurate. Although this causes limitations in the data availability, it avoids adding inaccurate placeholders.

Our sources used inconsistent structures and country identifiers, including 1,217 OWID records that lacked country codes (such as regional aggregates). To resolve this, our cleaning script reshaped all datasets into a uniform country-year panel and standardized them to 195 countries using ISO-3 codes. 

Remaining challenges include review and reproducibility testing. We need clear setup instructions in our README and conduct an end-to-end reproducibility test with pinned package versions from a fresh repository clone to ensure anyone can reproduce our results without errors. We need to verify permissions, and provide alternative download instructions if needed.


## 6. Individual Contributions 
- **Ean Kim:** I drafted and revisted `ProjectPlan.md`, including research questions, dataset descriptions, and timeline. For this milestone, I reviewed our repository against the plan and wrote and edited the documentation, timeline and changes. Next, I will lead the reproducibility test and contribute to the analysis.

- **Isa Chew:** I helped outline the status report organization and interpret the challenges faced so far and potential challenges we expect to face in the remainder of the project. I updated the project timeline to consider our future responsibilities and tasks.
  
- **Abigail Matern:** I helped with license and terms-of-use review for our datasets, drafted the data entry and schema.org metadata with docs/data_dictionary.md and docs/metadata.jsonld. I co-wrote the challenges section of this status report and next will finish verifying the OWID and UNDP redistribution terms, finalize  dataset documentation and validation, and create visualizations.

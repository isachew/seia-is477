# Pre-Integration Data Quality Assessment

## 1. Purpose

This assessment evaluates the quality of the raw datasets collected for our project, *Income, Human Development, and Carbon Emissions*. Before cleaning and integrating the data, we examined completeness, accuracy, consistency and timeliness to identify potential issues that could affect our analysis of relationships among GDP per capita, human development and CO₂ emissions from 1990 to 2023.

The assessment was conducted using a Python script (`scripts/assess_data_quality.py`). The generated results are available in `results/pre_integration_quality/`.

## 2. Completeness

We evaluated completeness by measuring the percentage of missing indicator values across the study period.

| Dataset | Missing Values |
|---|---:|
| OWID CO₂ emissions per capita | 9.00% |
| UNDP Human Development Index | 9.85% |
| World Bank GDP per capita | 4.39% |
| World Bank urban population | 0.38% |
| World Bank industry share of GDP | 13.54% |
| World Bank renewable energy consumption | 8.96% |

Industry share of GDP had the highest percentage of missing values at 13.54%, while urban population had the lowest at 0.38%. Missing observations may limit comparisons across countries and years, particularly when multiple indicators are required for the same observation.

These percentages describe the raw datasets before restricting them to a common set of countries and years.

## 3. Accuracy

The assessment checked for negative values and values exceeding expected bounds for indicators with defined ranges. No negative values or out-of-range values were flagged by these checks.

However, these results do not guarantee that all observations are accurate. Additional validation will be necessary to ensure that the indicators are interpreted correctly, especially because the datasets contain different measurements, including emissions per capita, monetary values and percentages.

## 4. Consistency

The assessment identified no duplicate country-year records in the datasets.

However, the OWID dataset contained 1,217 records without country codes. These records require further investigation because country identifiers are essential for accurately joining datasets.

The sources also use different structures. OWID contains country-year observations, UNDP provides HDI values across year-specific columns and World Bank indicator files contain metadata rows and separate year columns. These differences will need to be standardized before integration.

## 5. Timeliness

The project focuses on 1990–2023. Most selected indicators contain observations through 2023, although completeness varies across countries and years.

The World Bank renewable energy consumption indicator only contains available observations through 2022 in the downloaded dataset. As a result, renewable energy cannot be used as an observed explanatory variable for 2023 without obtaining additional data.

We will document this limitation rather than assume that 2022 renewable energy values represent 2023.

## 6. Planned Cleaning and Integration

Based on the assessment, our next steps are to:

1. Standardize country identifiers using ISO-3 country codes.
2. Investigate records with missing country codes and distinguish countries from regional aggregates.
3. Reshape UNDP and World Bank data into a consistent country-year format.
4. Convert indicator columns into appropriate numeric types.
5. Preserve missing values where reliable observations are unavailable rather than automatically replacing them with estimates.
6. Align datasets using country and year while documenting observations lost during integration.
7. Address the renewable energy coverage limitation when analyzing the 2023 observations.

The original datasets will remain unchanged in `data/raw/`. Cleaned datasets will be stored in `data/cleaned/`, followed by integrated outputs in `data/integrated/`.

## 7. Reproducibility

The assessment was conducted using Python and pandas. The script and generated outputs are stored in the project repository:

- `scripts/assess_data_quality.py`
- `results/pre_integration_quality/assessment_summary.md`
- `results/pre_integration_quality/quality_summary.csv`
- `results/pre_integration_quality/quality_issues.csv`
- `results/pre_integration_quality/yearly_coverage.csv`
- `results/pre_integration_quality/observed_sha256.csv`

These artifacts document the initial data quality findings and provide a baseline for evaluating whether subsequent cleaning and integration improve the usability of the datasets.

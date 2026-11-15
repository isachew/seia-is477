# Post-Integration Data Quality Assessment

- Total records: 6,630
- Country codes: 195
- Years: 34
- Duplicate country-year keys: 0

## Missing Values

| Indicator | Missing | Missing % |
|---|---:|---:|
| hdi | 690 | 10.41% |
| co2_per_capita | 81 | 1.22% |
| gdp_per_capita | 130 | 1.96% |
| urban_population_pct | 0 | 0.00% |
| industry_share_pct | 717 | 10.81% |
| renewable_energy_pct | 473 | 7.13% |

## Research Question Coverage

| Analysis | Complete Rows | Complete % |
|---|---:|---:|
| RQ1_CO2_GDP_HDI | 5862 | 88.42% |
| RQ2_CO2_HDI | 5915 | 89.22% |
| RQ3_CO2_GDP_urban_industry_renewable | 5548 | 83.68% |
| All_six_indicators | 5189 | 78.27% |

## Limitations

- Range checks cannot verify every value's accuracy.
- High CO2 values require verification against OWID.
- ISO-3 codes have not been checked against an official registry.
- Source-to-integrated value reconciliation remains necessary.
- Missing values were preserved rather than estimated.
- RQ2 still requires a defined very-high-HDI country selection.

## Generated Files

- indicator_completeness.csv
- yearly_coverage.csv
- quality_flags.csv
- research_question_coverage.csv

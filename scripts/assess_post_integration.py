
"""Post-integration data quality assessment for IS 477."""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/integrated/country_year_integrated.csv"
OUT = ROOT / "results/post_integration_quality"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT, dtype={"iso3": "string"})

required = [
    "iso3", "year", "hdi", "co2_per_capita", "gdp_per_capita",
    "urban_population_pct", "industry_share_pct",
    "renewable_energy_pct"
]

missing_columns = set(required) - set(df.columns)
if missing_columns:
    raise ValueError(f"Missing columns: {sorted(missing_columns)}")

variables = required[2:]

for col in ["year"] + variables:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 1. Completeness
summary = pd.DataFrame([
    {
        "indicator": col,
        "total_rows": len(df),
        "non_missing": int(df[col].notna().sum()),
        "missing": int(df[col].isna().sum()),
        "missing_pct": round(df[col].isna().mean() * 100, 2),
        "min_observed": df[col].min(),
        "max_observed": df[col].max()
    }
    for col in variables
])
summary.to_csv(OUT / "indicator_completeness.csv", index=False)

# 2. Timeliness and yearly coverage
coverage = df.groupby("year", dropna=False)[variables].count()
coverage.reset_index().to_csv(OUT / "yearly_coverage.csv", index=False)

# 3. Consistency and accuracy checks
rules = {
    "hdi": (0, 1),
    "co2_per_capita": (0, None),
    "gdp_per_capita": (0, None),
    "urban_population_pct": (0, 100),
    "industry_share_pct": (0, 100),
    "renewable_energy_pct": (0, 100)
}

issues = []

def record(issue, mask, detail):
    rows = df.loc[mask.fillna(False), ["iso3", "year"]]
    for _, row in rows.iterrows():
        issues.append({
            "issue": issue,
            "iso3": row["iso3"],
            "year": row["year"],
            "detail": detail
        })

record(
    "missing_country_code",
    df["iso3"].isna() |
    ~df["iso3"].str.fullmatch(r"[A-Z]{3}", na=False),
    "Expected three-letter ISO code"
)

record(
    "invalid_year",
    df["year"].isna() | ~df["year"].between(1990, 2023),
    "Expected year between 1990 and 2023"
)

record(
    "duplicate_country_year",
    df.duplicated(["iso3", "year"], keep=False),
    "Duplicate integration key"
)

for col, (lower, upper) in rules.items():
    invalid = df[col].notna() & (df[col] < lower)
    if upper is not None:
        invalid |= df[col].notna() & (df[col] > upper)
    record(
        f"out_of_range_{col}",
        invalid,
        f"Expected range: {lower} to {upper}"
    )

# Flag extreme CO2 values for review, not automatic removal
record(
    "review_high_co2_per_capita",
    df["co2_per_capita"] > 100,
    "Verify value against original OWID dataset"
)

pd.DataFrame(
    issues,
    columns=["issue", "iso3", "year", "detail"]
).to_csv(OUT / "quality_flags.csv", index=False)

# 4. Research question completeness
research_sets = {
    "RQ1_CO2_GDP_HDI": [
        "co2_per_capita", "gdp_per_capita", "hdi"
    ],
    "RQ2_CO2_HDI": [
        "co2_per_capita", "hdi"
    ],
    "RQ3_CO2_GDP_urban_industry_renewable": [
        "co2_per_capita", "gdp_per_capita",
        "urban_population_pct", "industry_share_pct",
        "renewable_energy_pct"
    ],
    "All_six_indicators": variables
}

rq_results = []

for name, cols in research_sets.items():
    complete = df[cols].notna().all(axis=1)
    rq_results.append({
        "analysis": name,
        "required_indicators": ", ".join(cols),
        "complete_rows": int(complete.sum()),
        "complete_pct": round(complete.mean() * 100, 2),
        "countries_with_complete_rows": int(
            df.loc[complete, "iso3"].nunique()
        )
    })

rq = pd.DataFrame(rq_results)
rq.to_csv(OUT / "research_question_coverage.csv", index=False)

# 5. Markdown summary
countries = df["iso3"].nunique()
years = df["year"].nunique()
duplicates = df.duplicated(["iso3", "year"]).sum()

lines = [
    "# Post-Integration Data Quality Assessment",
    "",
    f"- Total records: {len(df):,}",
    f"- Country codes: {countries}",
    f"- Years: {years}",
    f"- Duplicate country-year keys: {duplicates}",
    "",
    "## Missing Values",
    "",
    "| Indicator | Missing | Missing % |",
    "|---|---:|---:|"
]

for _, row in summary.iterrows():
    lines.append(
        f"| {row['indicator']} | {int(row['missing'])} "
        f"| {row['missing_pct']:.2f}% |"
    )

lines += [
    "",
    "## Research Question Coverage",
    "",
    "| Analysis | Complete Rows | Complete % |",
    "|---|---:|---:|"
]

for _, row in rq.iterrows():
    lines.append(
        f"| {row['analysis']} | {int(row['complete_rows'])} "
        f"| {row['complete_pct']:.2f}% |"
    )

lines += [
    "",
    "## Limitations",
    "",
    "- Range checks cannot verify every value's accuracy.",
    "- High CO2 values require verification against OWID.",
    "- ISO-3 codes have not been checked against an official registry.",
    "- Source-to-integrated value reconciliation remains necessary.",
    "- Missing values were preserved rather than estimated.",
    "- RQ2 still requires a defined very-high-HDI country selection.",
    "",
    "## Generated Files",
    "",
    "- indicator_completeness.csv",
    "- yearly_coverage.csv",
    "- quality_flags.csv",
    "- research_question_coverage.csv"
]

(OUT / "assessment_summary.md").write_text(
    "\n".join(lines) + "\n",
    encoding="utf-8"
)

print(
    f"Post-integration assessment complete: "
    f"{len(df):,} rows, {countries} countries, {years} years."
)
print(f"Duplicate country-year keys: {duplicates}")
print(f"Quality flags: {len(issues)}")
print(rq[["analysis", "complete_rows"]].to_string(index=False))
print(f"Saved five files in: {OUT.relative_to(ROOT)}")

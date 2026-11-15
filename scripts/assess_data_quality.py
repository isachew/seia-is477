"""IS 477: reproducible pre-integration assessment of raw project datasets.
Run from the repository root: python scripts/assess_data_quality.py
Requires pandas and openpyxl (openpyxl is not needed for the time-series CSV).
"""
from pathlib import Path
import hashlib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
OUT = ROOT / 'results' / 'pre_integration_quality'
OUT.mkdir(parents=True, exist_ok=True)
YEARS = list(range(1990, 2024))
FILES = {
    'owid': 'owid-co2-data.csv',
    'undp': 'HDR25_Composite_indices_complete_time_series.csv',
    'gdp_per_capita': 'gdp_per_capita.csv',
    'urban_population': 'urban_population.csv',
    'industry': 'industry_including_construction.csv',
    'renewable_energy': 'renewable_energy_consumption.csv',
}
INDICATORS = {
    'gdp_per_capita': 'NY.GDP.PCAP.CD',
    'urban_population': 'SP.URB.TOTL.IN.ZS',
    'industry': 'NV.IND.TOTL.ZS',
    'renewable_energy': 'EG.FEC.RNEW.ZS',
}

summary = []
coverage = []
issues = []
checksums = []


def issue(source, check, count, explanation):
    issues.append({'source': source, 'check': check, 'count': int(count), 'explanation': explanation})


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def evaluate(source, frame, country_col, year_col, value_col, code_col):
    frame = frame.copy()
    frame[year_col] = pd.to_numeric(frame[year_col], errors='coerce')
    frame[value_col] = pd.to_numeric(frame[value_col], errors='coerce')
    frame = frame[frame[year_col].isin(YEARS)].copy()
    duplicates = int(frame.duplicated([country_col, year_col]).sum())
    missing_codes = int(frame[code_col].isna().sum())
    missing_values = int(frame[value_col].isna().sum())
    nonmissing = frame[value_col].dropna()
    negative = int((nonmissing < 0).sum())
    bounded = source in ('undp', 'urban_population', 'industry', 'renewable_energy')
    upper = 1 if source == 'undp' else 100
    above_bound = int((nonmissing > upper).sum()) if bounded else 0
    available_years = sorted(frame.loc[frame[value_col].notna(), year_col].dropna().astype(int).unique().tolist())
    summary.append({
        'source': source, 'rows_1990_2023': len(frame),
        'unique_country_identifiers': frame[code_col].nunique(dropna=True),
        'duplicate_country_year_rows': duplicates, 'missing_country_codes': missing_codes,
        'missing_indicator_values': missing_values,
        'missing_indicator_pct': round(100 * missing_values / len(frame), 2) if len(frame) else None,
        'nonmissing_indicator_values': int(nonmissing.size),
        'earliest_available_year': min(available_years) if available_years else None,
        'latest_available_year': max(available_years) if available_years else None,
        'years_with_values': len(available_years),
        'negative_values': negative, 'values_above_expected_bound': above_bound,
    })
    issue(source, 'duplicate country-year keys', duplicates, 'Review keys before joining')
    issue(source, 'missing indicator values', missing_values, 'Check coverage before deciding how to handle missingness')
    issue(source, 'missing country codes', missing_codes, 'Check whether these are aggregates or unmapped entities')
    issue(source, 'negative values', negative, 'Review negative values against source definitions')
    if bounded:
        issue(source, 'above expected upper bound', above_bound, f'Expected upper bound is {upper}; inspect source definitions')
    for year in YEARS:
        yr = frame[frame[year_col] == year]
        coverage.append({'source': source, 'year': year, 'rows': len(yr),
                         'nonmissing_values': int(yr[value_col].notna().sum()),
                         'missing_values': int(yr[value_col].isna().sum())})


for source, filename in FILES.items():
    path = RAW / filename
    if not path.exists():
        raise FileNotFoundError(f'Missing {path}. Confirm the exact filename in data/raw/.')
    checksums.append({'source': source, 'file': filename, 'sha256_observed': sha256(path)})

    if source == 'owid':
        df = pd.read_csv(path, low_memory=False)
        required = ['country', 'iso_code', 'year', 'co2_per_capita']
        missing = set(required) - set(df.columns)
        if missing:
            raise ValueError(f'OWID missing columns: {missing}')
        # Keep raw data untouched; 3-letter codes are a candidate country filter, not proof of sovereignty.
        issue(source, 'non-ISO3 or missing ISO codes in raw file',
              int((~df['iso_code'].fillna('').astype(str).str.fullmatch(r'[A-Z]{3}')).sum()),
              'Some OWID rows represent world/regions or lack standard country codes')
        evaluate(source, df, 'country', 'year', 'co2_per_capita', 'iso_code')

    elif source == 'undp':
        # UNDP file contains some non-UTF-8 text; latin1 preserves all bytes for assessment.
        df = pd.read_csv(path, encoding='latin1', low_memory=False)
        required = ['iso3', 'country'] + [f'hdi_{y}' for y in YEARS]
        missing = set(required) - set(df.columns)
        if missing:
            raise ValueError(f'UNDP missing columns: {sorted(missing)[:10]}')
        long = df[['iso3', 'country'] + [f'hdi_{y}' for y in YEARS]].melt(
            id_vars=['iso3', 'country'], var_name='year', value_name='hdi')
        long['year'] = long['year'].str.replace('hdi_', '', regex=False).astype(int)
        evaluate(source, long, 'country', 'year', 'hdi', 'iso3')

    else:
        # World Bank CSV: two metadata lines and blank lines before the header.
        df = pd.read_csv(path, skiprows=4, encoding='utf-8-sig', low_memory=False)
        required = ['Country Name', 'Country Code', 'Indicator Code'] + [str(y) for y in YEARS]
        missing = set(required) - set(df.columns)
        if missing:
            raise ValueError(f'{filename} missing columns: {sorted(missing)[:10]}')
        codes = df['Indicator Code'].dropna().unique().tolist()
        if codes != [INDICATORS[source]]:
            issue(source, 'unexpected indicator code rows', int((df['Indicator Code'] != INDICATORS[source]).sum()),
                  f'Expected {INDICATORS[source]}; found {codes}')
        long = df[['Country Name', 'Country Code'] + [str(y) for y in YEARS]].melt(
            id_vars=['Country Name', 'Country Code'], var_name='year', value_name='value')
        evaluate(source, long, 'Country Name', 'year', 'value', 'Country Code')
        issue(source, 'country/region aggregate filtering needed', 0,
              'World Bank files include regional/income aggregates; identify using World Bank metadata before joining')

pd.DataFrame(summary).to_csv(OUT / 'quality_summary.csv', index=False)
pd.DataFrame(coverage).to_csv(OUT / 'yearly_coverage.csv', index=False)
pd.DataFrame(issues).to_csv(OUT / 'quality_issues.csv', index=False)
pd.DataFrame(checksums).to_csv(OUT / 'observed_sha256.csv', index=False)

lines = ['# Pre-integration data quality assessment', '',
         'Generated by `scripts/assess_data_quality.py` from unmodified files in `data/raw/`.',
         'Scope: 1990–2023. World Bank aggregates have NOT yet been excluded.', '',
         '## Summary', '', '```text', pd.DataFrame(summary).to_string(index=False), '```', '',
         '## Interpretation notes', '',
         '- **Completeness:** Missing indicator values and yearly coverage are quantified in the CSV outputs.',
         '- **Accuracy:** Negative and out-of-range values are screening flags, not proof of error; verify against source definitions.',
         '- **Consistency:** Duplicate keys and missing country codes are counted. Cross-source ISO3 alignment must be checked before integration.',
         '- **Timeliness:** Available years are measured for each indicator; source update dates and download dates must be documented separately.',
         '- **Important:** World Bank data includes regional/income aggregates. A future cleaning step must identify and exclude them using authoritative metadata.',
         '- **Integrity:** `observed_sha256.csv` records observed checksums, but independent verification requires trusted expected checksums or a frozen source snapshot.',
         '- **Limitations:** These automated checks do not establish source-level accuracy or verify every country name; manually review anomalies and provenance.', '']
(OUT / 'assessment_summary.md').write_text('\n'.join(lines), encoding='utf-8')
print('Assessment complete. Outputs saved to:', OUT)
print(pd.DataFrame(summary).to_string(index=False))

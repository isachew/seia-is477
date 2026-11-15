"""Integrate six cleaned IS 477 indicators on ISO-3 country code and year.

Run from anywhere: python3 scripts/integrate_data.py
Inputs: data/cleaned/*.csv
Outputs: data/integrated/country_year_integrated.csv
         results/integration/integration_summary.csv
Requires: pandas
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / 'data' / 'cleaned'
INTEGRATED = ROOT / 'data' / 'integrated'
RESULTS = ROOT / 'results' / 'integration'
INTEGRATED.mkdir(parents=True, exist_ok=True)
RESULTS.mkdir(parents=True, exist_ok=True)

INDICATORS = [
    'hdi', 'co2_per_capita', 'gdp_per_capita',
    'urban_population_pct', 'industry_share_pct', 'renewable_energy_pct'
]
KEYS = ['iso3', 'year']
EXPECTED_YEARS = set(range(1990, 2024))
EXPECTED_COUNTRIES = 195  # The UNDP country universe selected during cleaning.

frames = {}
summary = []
for name in INDICATORS:
    path = CLEAN / f'{name}.csv'
    if not path.is_file():
        raise FileNotFoundError(f'Missing cleaned dataset: {path}')
    df = pd.read_csv(path, dtype={'iso3': 'string'})
    required = set(KEYS + [name])
    if not required.issubset(df.columns):
        raise ValueError(f'{path.name} is missing columns: {sorted(required - set(df.columns))}')
    if df[KEYS].isna().any().any():
        raise ValueError(f'{path.name} has missing country/year keys')
    df['iso3'] = df['iso3'].str.strip()
    df['year'] = pd.to_numeric(df['year'], errors='raise').astype(int)
    if df.duplicated(KEYS).any():
        raise ValueError(f'{path.name} has duplicate country-year keys')
    if not set(df['year']).issubset(EXPECTED_YEARS):
        raise ValueError(f'{path.name} has years outside 1990–2023')
    df[name] = pd.to_numeric(df[name], errors='raise')
    frames[name] = df[KEYS + [name]].copy()
    summary.append({
        'indicator': name,
        'input_rows': len(df),
        'input_countries': df['iso3'].nunique(),
        'missing_values_before_join': int(df[name].isna().sum()),
    })

# HDI is the reference country-year grid; fail if another indicator lacks a key.
master = frames['hdi'].copy()
reference_keys = pd.MultiIndex.from_frame(master[KEYS])
for name in INDICATORS[1:]:
    other_keys = pd.MultiIndex.from_frame(frames[name][KEYS])
    missing_keys = reference_keys.difference(other_keys)
    extra_keys = other_keys.difference(reference_keys)
    if len(missing_keys) or len(extra_keys):
        raise ValueError(
            f'{name} keys do not match HDI: {len(missing_keys)} missing, '
            f'{len(extra_keys)} extra. Review cleaning before integration.'
        )
    master = master.merge(frames[name], on=KEYS, how='left', validate='one_to_one')

master = master.sort_values(KEYS).reset_index(drop=True)
if master.duplicated(KEYS).any() or master[KEYS].isna().any().any():
    raise ValueError('Integrated dataset has invalid or duplicated keys')
if master['iso3'].nunique() != EXPECTED_COUNTRIES or set(master['year']) != EXPECTED_YEARS:
    raise ValueError('Integrated country or year coverage differs from the expected 195 countries and 1990–2023')
if len(master) != EXPECTED_COUNTRIES * len(EXPECTED_YEARS):
    raise ValueError('Integrated dataset is missing country-year combinations')

for row in summary:
    name = row['indicator']
    row['integrated_rows'] = len(master)
    row['missing_values_after_join'] = int(master[name].isna().sum())
    row['join_introduced_missing_values'] = row['missing_values_after_join'] - row['missing_values_before_join']

output = INTEGRATED / 'country_year_integrated.csv'
master.to_csv(output, index=False)
pd.DataFrame(summary).to_csv(RESULTS / 'integration_summary.csv', index=False)
print(f'Integration complete: {len(master):,} rows, {master.iso3.nunique()} countries, '
      f'{master.year.min()}–{master.year.max()}.')
print(f'Saved: {output.relative_to(ROOT)}')
print(f'Saved: {(RESULTS / "integration_summary.csv").relative_to(ROOT)}')
print('Missing values remain missing; no imputation was performed.')

"""IS 477: Clean six indicators without modifying raw files.
Run from repository root: python3 scripts/clean_data.py
Requires: pandas. Outputs CSVs in data/cleaned/ and an audit in results/cleaning/.
Country selection uses the intersection with UNDP's three-letter country codes;
this is a practical project scope rule, not a complete sovereignty classifier.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
CLEAN = ROOT / 'data' / 'cleaned'
AUDIT = ROOT / 'results' / 'cleaning'
CLEAN.mkdir(parents=True, exist_ok=True)
AUDIT.mkdir(parents=True, exist_ok=True)
YEARS = list(range(1990, 2024))
WB = {
    'gdp_per_capita': ('gdp_per_capita.csv', 'NY.GDP.PCAP.CD'),
    'urban_population_pct': ('urban_population.csv', 'SP.URB.TOTL.IN.ZS'),
    'industry_share_pct': ('industry_including_construction.csv', 'NV.IND.TOTL.ZS'),
    'renewable_energy_pct': ('renewable_energy_consumptino.csv', 'EG.FEC.RNEW.ZS'),
}
report = []


def save(name, df, raw_count, excluded, invalid):
    df = df.sort_values(['iso3', 'year']).reset_index(drop=True)
    if df.duplicated(['iso3', 'year']).any():
        raise ValueError(f'Duplicate country-year keys in {name}')
    df.to_csv(CLEAN / f'{name}.csv', index=False)
    report.append({'dataset': name, 'input_rows_after_reshaping': raw_count,
                   'excluded_non_country_or_unmatched_rows': excluded,
                   'invalid_values_set_missing': invalid,
                   'output_rows': len(df), 'missing_indicator_values': int(df[name].isna().sum()),
                   'unique_countries': df.iso3.nunique(),
                   'first_year': int(df.year.min()), 'last_year': int(df.year.max())})
    print(f'{name}: {len(df):,} rows, {df.iso3.nunique()} country codes, {df[name].isna().sum():,} missing values')

# UNDP provides the project country universe. Exclude its regional/development aggregates.
u = pd.read_csv(RAW / 'HDR25_Composite_indices_complete_time_series.csv', encoding='latin1', low_memory=False)
required = ['iso3', 'country'] + [f'hdi_{y}' for y in YEARS]
if not set(required).issubset(u.columns):
    raise ValueError('UNDP HDI columns are missing')
u['iso3'] = u['iso3'].astype('string').str.strip()
u = u[u.iso3.str.fullmatch(r'[A-Z]{3}', na=False)].copy()
if u.iso3.duplicated().any():
    raise ValueError('UNDP contains repeated ISO3 country codes')
COUNTRIES = set(u.iso3)
h = u[required].melt(id_vars=['iso3', 'country'], value_vars=[f'hdi_{y}' for y in YEARS], var_name='year', value_name='hdi')
h['year'] = h.year.str.removeprefix('hdi_').astype(int)
h['hdi'] = pd.to_numeric(h.hdi, errors='coerce')
invalid = int(((h.hdi < 0) | (h.hdi > 1)).sum())
h.loc[(h.hdi < 0) | (h.hdi > 1), 'hdi'] = float('nan')
save('hdi', h[['iso3', 'country', 'year', 'hdi']], len(h), 0, invalid)

# OWID has some aggregate or missing identifiers. Restrict to the UNDP country set.
o = pd.read_csv(RAW / 'owid-co2-data.csv', usecols=['country', 'iso_code', 'year', 'co2_per_capita'], low_memory=False)
o['iso3'] = o.iso_code.astype('string').str.strip()
o['year'] = pd.to_numeric(o.year, errors='coerce')
o = o[o.year.isin(YEARS)].copy()
before = len(o)
o = o[o.iso3.isin(COUNTRIES)].copy()
o['year'] = o.year.astype(int)
o['co2_per_capita'] = pd.to_numeric(o.co2_per_capita, errors='coerce')
invalid = int((o.co2_per_capita < 0).sum())
o.loc[o.co2_per_capita < 0, 'co2_per_capita'] = float('nan')
save('co2_per_capita', o[['iso3', 'country', 'year', 'co2_per_capita']], before, before-len(o), invalid)

# WDI downloads contain four introductory metadata lines and wide year columns.
for name, (filename, indicator) in WB.items():
    w = pd.read_csv(RAW / filename, skiprows=4, encoding='utf-8-sig', low_memory=False)
    required = ['Country Name', 'Country Code', 'Indicator Code'] + [str(y) for y in YEARS]
    if not set(required).issubset(w.columns):
        raise ValueError(f'Missing World Bank columns in {filename}')
    if not w['Indicator Code'].dropna().eq(indicator).all():
        raise ValueError(f'Unexpected indicator code in {filename}')
    w = w.rename(columns={'Country Code': 'iso3', 'Country Name': 'country'})
    long = w[['iso3', 'country'] + [str(y) for y in YEARS]].melt(
        id_vars=['iso3', 'country'], value_vars=[str(y) for y in YEARS],
        var_name='year', value_name=name)
    before = len(long)
    long['iso3'] = long.iso3.astype('string').str.strip()
    long = long[long.iso3.isin(COUNTRIES)].copy()
    long['year'] = long.year.astype(int)
    long[name] = pd.to_numeric(long[name], errors='coerce')
    bad = long[name] < 0
    if name.endswith('_pct'):
        bad = bad | (long[name] > 100)
    invalid = int(bad.sum())
    long.loc[bad, name] = float('nan')
    save(name, long[['iso3', 'country', 'year', name]], before, before-len(long), invalid)

pd.DataFrame(report).to_csv(AUDIT / 'cleaning_summary.csv', index=False)
print('\nCleaning complete. Review data/cleaned/ and results/cleaning/cleaning_summary.csv')
print('Missing observations remain missing; no interpolation or year substitution was performed.')

"""Explore story candidates for DE 4-2 without choosing the student's stories.

Uses only Python's standard library and the course-provided CSV/TSV files.
Run from this directory with the p314 interpreter as documented in README.md.
"""
from collections import defaultdict
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_csv(path, delimiter=',', encoding='utf-8-sig'):
    with path.open(newline='', encoding=encoding) as handle:
        return list(csv.DictReader(handle, delimiter=delimiter))


def num(value):
    try:
        value = float(value)
        return value if math.isfinite(value) else None
    except (TypeError, ValueError):
        return None


def median(values):
    xs = sorted(v for v in values if v is not None)
    n = len(xs)
    if not n:
        return None
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def fmt(x, digits=2):
    return 'NA' if x is None else f'{x:.{digits}f}'


def lifespan_candidates():
    rows = load_csv(ROOT / 'data/life-expectancy-owid/life-expectancy-owid.csv')
    series = defaultdict(dict)
    names = {}
    for row in rows:
        code = row['Code']
        year = int(row['Year'])
        value = num(row['Period life expectancy at birth'])
        if code and not code.startswith('OWID_') and value is not None:
            series[code][year] = value
            names[code] = row['Entity']

    drops = []
    for code, vals in series.items():
        for year in sorted(vals):
            if year - 1 in vals:
                d = vals[year] - vals[year - 1]
                if year >= 1950:
                    drops.append((d, names[code], year, vals[year - 1], vals[year]))
    drops.sort()

    pandemic = []
    for code, vals in series.items():
        if 2019 in vals and 2021 in vals:
            pandemic.append((vals[2021] - vals[2019], names[code], vals.get(2022)))
    pandemic.sort()

    disruptions = []
    for code, vals in series.items():
        for year in sorted(y for y in vals if y >= 1950):
            if year - 1 not in vals or year + 1 not in vals:
                continue
            drop = vals[year] - vals[year - 1]
            if drop <= -3:
                prior = vals[year - 1]
                recovery = next((y for y in range(year + 1, min(year + 11, max(vals) + 1))
                                 if y in vals and vals[y] >= prior), None)
                disruptions.append((drop, names[code], year, recovery))
    disruptions.sort()
    return drops[:12], pandemic[:12], disruptions[:15]


def census_candidates():
    rows = load_csv(ROOT / 'data/full_census_dataset.csv', encoding='cp1252')
    # These columns are rates (per 1,000 residents), so county size does not dominate.
    groups = defaultdict(lambda: defaultdict(list))
    county_data = []
    for row in rows:
        code = num(row.get('Rural Urban Continuum Code 2023'))
        domestic_mig = num(row.get('Domestic Migration Rate 2023'))
        net_mig = num(row.get('Net Migration Rate 2023'))
        nat = num(row.get('Natural Change Rate 2023'))
        death = num(row.get('Death Rate 2023'))
        unemp = num(row.get('Unemployment rate 2023'))
        pop = num(row.get('Population Estimate 2023'))
        # County-level RUCC values are 1-9. Exclude state/national aggregate rows.
        if code is None or not 1 <= code <= 9:
            continue
        bucket = 'Metro (RUCC 1–3)' if code <= 3 else 'Nonmetro (RUCC 4–9)'
        for key, value in [('domestic_migration', domestic_mig), ('net_migration', net_mig),
                           ('natural_change', nat), ('death', death), ('unemployment', unemp)]:
            if value is not None:
                groups[bucket][key].append(value)
        if net_mig is not None and nat is not None:
            county_data.append((row.get('Area name'), row.get('State'), int(code), net_mig, nat, pop))

    medians = {g: {k: median(v) for k, v in metrics.items()} for g, metrics in groups.items()}
    top_movers = sorted((r for r in county_data if r[3] is not None), key=lambda r: r[3], reverse=True)[:8]
    high_nat_low_mig = sorted((r for r in county_data if r[4] is not None and r[3] is not None), key=lambda r: (r[4] - r[3]), reverse=True)[:8]
    quadrants = defaultdict(int)
    for row in county_data:
        mig, nat = row[3], row[4]
        quadrants[('positive' if nat > 0 else 'negative' if nat < 0 else 'zero',
                   'positive' if mig > 0 else 'negative' if mig < 0 else 'zero')] += 1
    return len(county_data), medians, top_movers, high_nat_low_mig, quadrants


def main():
    top_drops, pandemic, disruptions = lifespan_candidates()
    n_counties, census, movers, natural_vs_migration, quadrants = census_candidates()
    lines = [
        '# Exploratory findings for Mike to choose from',
        '',
        'These are candidate patterns, not selected stories or submission text. Values were computed from course-provided files only.',
        '',
        '## Life expectancy (OWID series)',
        '',
        'Largest one-year declines since 1950 (all available country/territory series):',
        '',
        '| Change | Entity | Year of decline | Before | After |',
        '|---:|---|---:|---:|---:|',
    ]
    for d, name, year, before, after in top_drops:
        lines.append(f'| {d:.2f} | {name} | {year} | {before:.2f} | {after:.2f} |')
    lines += ['', 'Largest 2019–2021 changes (2022 shown as context):', '',
              '| 2019–21 change | Entity | 2022 value |', '|---:|---|---:|']
    for change, name, value22 in pandemic:
        lines.append(f'| {change:.2f} | {name} | {fmt(value22)} |')
    lines += ['', 'Large drops (at least 3 years in one year) and time to regain the prior year level (within 10 years):', '',
              '| Change | Entity | Drop year | Regained prior level |', '|---:|---|---:|---:|']
    for d, name, year, recovery in disruptions:
        lines.append(f'| {d:.2f} | {name} | {year} | {recovery if recovery is not None else "not observed within 10y"} |')

    lines += ['', '## Census county patterns (2023)', '',
              f'Analyzed {n_counties:,} county rows with valid 2023 rural–urban continuum codes. RUCC 1–3 is treated as metro; 4–9 as nonmetro.', '',
              '| Group | Median net migration rate | Median domestic migration rate | Median natural change rate | Median death rate | Median unemployment rate |',
              '|---|---:|---:|---:|---:|---:|']
    for group in ['Metro (RUCC 1–3)', 'Nonmetro (RUCC 4–9)']:
        m = census.get(group, {})
        lines.append(f'| {group} | {fmt(m.get("net_migration"))} | {fmt(m.get("domestic_migration"))} | {fmt(m.get("natural_change"))} | {fmt(m.get("death"))} | {fmt(m.get("unemployment"))} |')
    lines += ['', '2023 county counts by sign of natural change and net migration rate (rows are natural change; columns are net migration):', '',
              '| Natural change | Net migration positive | Net migration negative | Net migration zero |',
              '|---|---:|---:|---:|']
    for natural in ['positive', 'negative', 'zero']:
        lines.append(f'| {natural.title()} | {quadrants[(natural, "positive")]} | {quadrants[(natural, "negative")]} | {quadrants[(natural, "zero")]} |')
    lines += ['', 'Highest net migration rates (inspect population size and verify outliers before using):', '',
              '| County | State | RUCC | Net migration rate | Natural change rate | 2023 population |',
              '|---|---|---:|---:|---:|---:|']
    for name, state, code, mig, nat, pop in movers:
        lines.append(f'| {name} | {state} | {code} | {mig:.2f} | {fmt(nat)} | {fmt(pop, 0)} |')
    lines += ['', 'Largest natural-change-minus-net-migration gaps (a candidate for inspecting places whose growth balance comes from births/deaths versus moves):', '',
              '| County | State | RUCC | Net migration rate | Natural change rate | 2023 population |',
              '|---|---|---:|---:|---:|---:|']
    for name, state, code, mig, nat, pop in natural_vs_migration:
        lines.append(f'| {name} | {state} | {code} | {mig:.2f} | {nat:.2f} | {fmt(pop, 0)} |')

    lines += ['', '## Design possibilities to consider', '',
              '- Life expectancy: a selected-country line chart with directly labeled disruption/recovery intervals; a heatmap of annual changes can show whether declines cluster across regions. These answer related questions with different tradeoffs (trajectory context vs. breadth).',
              '- Census: a county scatterplot of natural-change rate vs. net-migration rate, colored by metro/nonmetro and annotated around zero, makes the two components of population change legible. A paired distribution plot can compare metro/nonmetro spread but loses the county-level pairing.',
              '- Candidate design choices and stories remain Mike’s decision; these summaries do not establish causes.']
    out = ROOT / 'work/exploration.md'
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(out)


if __name__ == '__main__':
    main()

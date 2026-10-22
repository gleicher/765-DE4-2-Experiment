# Exploratory findings for Mike to choose from

These are candidate patterns, not selected stories or submission text. Values were computed from course-provided files only.

## Life expectancy (OWID series)

Largest one-year declines since 1950 (all available country/territory series):

| Change | Entity | Year of decline | Before | After |
|---:|---|---:|---:|---:|
| -35.21 | Central African Republic | 2009 | 49.87 | 14.67 |
| -30.78 | Rwanda | 1994 | 42.94 | 12.16 |
| -26.51 | Cambodia | 1975 | 39.30 | 12.78 |
| -21.48 | Somalia | 1991 | 46.90 | 25.42 |
| -21.46 | Central African Republic | 2022 | 40.28 | 18.82 |
| -21.31 | Lebanon | 1976 | 57.74 | 36.44 |
| -20.77 | Central African Republic | 2019 | 52.30 | 31.53 |
| -19.85 | Bosnia and Herzegovina | 1992 | 71.81 | 51.97 |
| -17.40 | Burundi | 1972 | 43.17 | 25.78 |
| -16.45 | Somalia | 2011 | 48.90 | 32.45 |
| -16.15 | Bangladesh | 1971 | 42.67 | 26.52 |
| -16.12 | Haiti | 2010 | 61.69 | 45.58 |

Largest 2019–2021 changes (2022 shown as context):

| 2019–21 change | Entity | 2022 value |
|---:|---|---:|
| -6.39 | Bolivia | 67.43 |
| -5.56 | Paraguay | 72.32 |
| -4.78 | Mexico | 73.97 |
| -4.74 | Guyana | 69.89 |
| -4.68 | Peru | 76.83 |
| -4.56 | Lebanon | 78.00 |
| -4.54 | Ecuador | 76.58 |
| -4.33 | Martinique | 80.84 |
| -4.21 | Cuba | 77.63 |
| -4.09 | Colombia | 76.51 |
| -4.06 | South Africa | 65.45 |
| -3.98 | Oman | 77.91 |

Large drops (at least 3 years in one year) and time to regain the prior year level (within 10 years):

| Change | Entity | Drop year | Regained prior level |
|---:|---|---:|---:|
| -35.21 | Central African Republic | 2009 | 2011 |
| -30.78 | Rwanda | 1994 | 1998 |
| -26.51 | Cambodia | 1975 | 1979 |
| -21.48 | Somalia | 1991 | 1993 |
| -21.46 | Central African Republic | 2022 | 2023 |
| -21.31 | Lebanon | 1976 | 1977 |
| -20.77 | Central African Republic | 2019 | 2023 |
| -19.85 | Bosnia and Herzegovina | 1992 | 1996 |
| -17.40 | Burundi | 1972 | 1974 |
| -16.45 | Somalia | 2011 | 2012 |
| -16.15 | Bangladesh | 1971 | 1972 |
| -16.12 | Haiti | 2010 | 2012 |
| -14.86 | Armenia | 1988 | 1989 |
| -14.45 | Cyprus | 1974 | 1975 |
| -14.02 | South Sudan | 1998 | 1999 |

## Census county patterns (2023)

Analyzed 3,106 county rows with valid 2023 rural–urban continuum codes. RUCC 1–3 is treated as metro; 4–9 as nonmetro.

| Group | Median net migration rate | Median domestic migration rate | Median natural change rate | Median death rate | Median unemployment rate |
|---|---:|---:|---:|---:|---:|
| Metro (RUCC 1–3) | 5.20 | 3.60 | -0.20 | 10.70 | 3.40 |
| Nonmetro (RUCC 4–9) | 3.20 | 2.40 | -3.40 | 14.00 | 3.50 |

2023 county counts by sign of natural change and net migration rate (rows are natural change; columns are net migration):

| Natural change | Net migration positive | Net migration negative | Net migration zero |
|---|---:|---:|---:|
| Positive | 568 | 358 | 5 |
| Negative | 1555 | 585 | 10 |
| Zero | 17 | 7 | 1 |

Highest net migration rates (inspect population size and verify outliers before using):

| County | State | RUCC | Net migration rate | Natural change rate | 2023 population |
|---|---|---:|---:|---:|---:|
| Kaufman County | TX | 1 | 67.00 | 6.30 | 185690 |
| Sumter County | FL | 3 | 59.30 | -13.40 | 151565 |
| Rockwall County | TX | 1 | 58.30 | 4.60 | 131307 |
| Petroleum County | MT | 9 | 57.70 | 5.60 | 554 |
| Long County | GA | 3 | 56.20 | 7.00 | 19594 |
| Blanco County | TX | 8 | 55.50 | -5.30 | 13048 |
| Liberty County | TX | 1 | 51.70 | 3.80 | 108272 |
| Jackson County | GA | 4 | 50.20 | 3.30 | 88615 |

Largest natural-change-minus-net-migration gaps (a candidate for inspecting places whose growth balance comes from births/deaths versus moves):

| County | State | RUCC | Net migration rate | Natural change rate | 2023 population |
|---|---|---:|---:|---:|---:|
| DeKalb County | MO | 3 | -130.90 | -3.50 | 9899 |
| Telfair County | GA | 9 | -122.20 | -4.40 | 10920 |
| King County | TX | 9 | -84.30 | 8.90 | 217 |
| Kusilvak Census Area | AK | 9 | -43.80 | 17.80 | 8001 |
| Grant County | NE | 9 | -43.50 | 10.40 | 565 |
| Logan County | NE | 9 | -49.30 | 3.00 | 655 |
| Geary County | KS | 3 | -32.50 | 19.10 | 35047 |
| Sherman County | TX | 9 | -41.80 | 5.10 | 2678 |

## Design possibilities to consider

- Life expectancy: a selected-country line chart with directly labeled disruption/recovery intervals; a heatmap of annual changes can show whether declines cluster across regions. These answer related questions with different tradeoffs (trajectory context vs. breadth).
- Census: a county scatterplot of natural-change rate vs. net-migration rate, colored by metro/nonmetro and annotated around zero, makes the two components of population change legible. A paired distribution plot can compare metro/nonmetro spread but loses the county-level pairing.
- Candidate design choices and stories remain Mike’s decision; these summaries do not establish causes.

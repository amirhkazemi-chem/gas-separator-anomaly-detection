# Gas Separator Anomaly Detection & Mass Balance Analysis

A Python-based data analysis project for detecting anomalies, trends, and mass balance
inconsistencies in chemical process sensor data, combining statistical analysis with
chemical engineering process knowledge.

## Overview

This project analyzes 250 minutes of sensor data from a chemical gas separator unit,
covering temperature, pressure, and inlet/outlet flow rates. It demonstrates an
end-to-end data analysis workflow: from raw CSV data to a fully documented engineering
report with actionable recommendations.

**Goal**: identify process anomalies (sudden spikes/drops, gradual drift, missing sensor
readings) and distinguish which ones require immediate action versus routine monitoring.

## What This Project Demonstrates

- Outlier detection using the Interquartile Range (IQR) method
- Time-trend detection using correlation analysis (full range vs. sub-windows)
- Noise reduction and trend visualization with rolling averages
- Mass balance calculation (`inlet flow = sum of outlet flows`) to detect
  process-level inconsistencies (e.g. leaks)
- Cross-variable analysis to determine whether anomalies are related or independent
- Engineering interpretation of statistical findings (not just numbers, but what they
  mean for the process)

## Project Structure

```
gas-separator-project/
├── data/
│   └── final_project_unknown.csv       # Raw sensor data
├── src/
│   └── gas_separator_analysis.py       # Analysis script
├── images/
│   └── chart_of_final_project.png      # Generated visualization
├── reports/
│   └── gas_separator_report.md         # Full engineering analysis report
├── requirements.txt
└── README.md
```

## How to Run

```bash
pip install -r requirements.txt
cd src
python gas_separator_analysis.py
```

This will print the analysis results to the console and regenerate the chart in
`images/chart_of_final_project.png`.

## Key Findings (Summary)

- A severe temperature spike (112°C, ~23°C above baseline) was detected at row 95,
  flagged as requiring immediate investigation.
- A gradual upward drift in mass balance error was detected starting at row 166,
  independent of temperature/pressure anomalies — suggesting a flow-side issue
  (e.g. a leak or pump behavior change) rather than a thermal one.
- Two milder temperature spikes and two pressure spikes were identified as likely
  sensor noise rather than critical events, based on their magnitude relative to
  the severe outlier.

See [`reports/gas_separator_report.md`](reports/gas_separator_report.md) for the full
analysis, including engineering interpretation and recommendations.

## Tech Stack

- Python 3
- pandas
- matplotlib

## Author

Amirhossein Kazemi — Chemical Engineering student building Python-based data analysis
tools for the process industry.

[GitHub](https://github.com/amirhkazemi-chem)

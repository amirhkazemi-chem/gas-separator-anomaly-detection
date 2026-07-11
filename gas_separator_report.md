# Anomaly Detection and Mass Balance Analysis in Chemical Separator Data

## 1. Title

Investigation of anomalies and time-based trends in chemical separator process data: mass balance, temperature, and pressure analysis.

## 2. Data and Methodology

### Data

The dataset contains 250 rows of process data from a chemical gas separator, collected over a 0–249 minute window. Main columns:

- `time_min`: time in minutes
- `separator_temp_C`: separator temperature (°C)
- `flow_in_L_min`: inlet flow rate (L/min)
- `flow_out1_L_min`, `flow_out2_L_min`: outlet flow rates (L/min)
- `pressure_bar`: separator pressure (bar)

### Methods

1. **Mass balance calculation**: `mass_balance_error = flow_in - (flow_out1 + flow_out2)` was used to detect flow imbalance.
2. **Outlier detection**: The Interquartile Range (IQR) method (Q1 - 1.5×IQR, Q3 + 1.5×IQR) was applied to each variable.
3. **Time correlation analysis**: Pearson correlation between `time_min` and each variable was computed across the full dataset and separately for the first half (rows 0–124) and second half (rows 125–249).
4. **Noise smoothing**: A rolling average (window=10) was used to reduce noise and reveal underlying trends.
5. **Visualization**: Line plots with rolling averages and annotations for outliers and drift periods were created for each variable.

## 3. Findings

### Mass Balance Error

- No missing values.
- 10 outliers detected (including rows 12, 228, 241).
- Time correlation: full data ≈ 0.01 (not significant), first half ≈ 0.05, second half ≈ 0.02.
- **Drift**: a sustained upward trend from row 166 to 250, rising from approximately 0 to 4–5 L/min.

### Separator Temperature

- No missing values.
- 4 outliers detected (rows 74, 95, 179, 209):
  - Row 74: 85.38°C (drop)
  - Row 95: 112.0°C (severe spike)
  - Row 179: 90.72°C (mild spike)
  - Row 209: 91.85°C (mild spike)
- Time correlation: full ≈ 0.01, first half ≈ 0.02, second half ≈ 0.01 (no meaningful trend).

### Separator Pressure

- 2 missing values (rows 40 and 201).
- 6 outliers detected (including rows 61 and 101):
  - Row 61: 7.93 bar (spike)
  - Row 101: 7.921 bar (spike)
- Time correlation: full ≈ -0.02, first half ≈ -0.01, second half ≈ -0.03 (no meaningful trend).

## 4. Chart

![chart of final project](chart_of_final_project.png)

The figure contains three subplots:

1. **Separator temperature**: raw data with rolling average; annotated spikes (rows 95, 179, 209) and a drop (row 74).
2. **Separator pressure**: raw data with rolling average; annotated spikes (rows 61, 101) and missing data points (rows 40, 201).
3. **Mass balance error**: raw data with rolling average; annotated drift (rows 166–250), a drop (row 12), and spikes (rows 228, 241).

## 5. Analysis and Discussion

### a) Severity Differentiation Among Temperature Outliers

The four temperature outliers (rows 74, 95, 179, 209) differ substantially in severity:

- **Row 95 (112.0°C)**: the most severe outlier, approximately 23°C above the average separator temperature (~89°C). A spike of this magnitude could indicate a sensor failure, an ingress of high-temperature material, or a sudden process shift (e.g. an exothermic reaction onset). This level of deviation is far more serious than normal fluctuation and warrants immediate investigation.
- **Rows 179 (90.72°C) and 209 (91.85°C)**: only 1.5–2.8°C above average, consistent with sensor noise or normal process variation. The sharp contrast with row 95 suggests row 95 is a genuine, critical anomaly, while rows 179 and 209 are likely just noise.
- **Row 74 (85.38°C)**: a drop of about 3.6°C below average, possibly indicating a sudden cooling event or a heat source issue.

**Why this distinction matters**: differentiating severity is essential for prioritizing corrective action. A 23°C outlier (row 95) may require an immediate process stop, whereas the milder outliers (rows 179, 209) can be handled through continued monitoring.

### b) Timing Relationship Between Mass Balance Drift and Other Anomalies

- The mass balance drift begins at row 166 and continues through row 250.
- Nearest outliers to row 166:
  - Temperature: row 179 (13 rows later), 90.72°C.
  - Pressure: row 101 (65 rows earlier), 7.921 bar.

**Timing analysis**:

- **Row 166 (drift onset)**: no simultaneous outlier in temperature or pressure. Values at row 166: temperature 88.82°C (normal range), pressure 8.777 bar (normal range), mass balance error 1.55 L/min (start of gradual increase).
- **Row 179 (nearest temperature outlier)**: temperature reaches 90.72°C (a mild outlier), but the mass balance error at row 179 is -1.15 L/min — within the normal range, showing no relationship to the drift.

**Conclusion**: the mass balance drift (starting row 166) is independent of the temperature and pressure outliers. This suggests the drift is more likely related to changes in the inlet/outlet flow streams themselves (e.g. a system leak, pump behavior change, or flow sensor deviation) rather than to the temperature or pressure anomalies. This indicates the mass balance is governed by different underlying factors and warrants separate investigation.

## 6. Recommendations

1. **Immediate investigation of the row 95 outlier (112°C)**:
   - Verify the temperature sensor's health.
   - Investigate the process for any sudden changes (e.g. hot material ingress, onset of an exothermic reaction).

2. **Investigate the mass balance drift (rows 166–250)**:
   - Inspect the flow system for leaks or pump behavior changes.
   - Check calibration of the flow sensors (`flow_in`, `flow_out1`, `flow_out2`).
   - Consider statistical process control (e.g. control charts) for ongoing mass balance monitoring.

3. **Handle missing pressure values (rows 40, 201)**:
   - Use interpolation or a rolling average to fill gaps.
   - Investigate the cause of the missing readings (e.g. sensor downtime).

4. **Improve code and analysis workflow**:
   - Modularize repeated logic into reusable functions to reduce duplication.
   - Consider regression analysis to test whether pressure or temperature can predict the mass balance error.

5. **Continuous monitoring**:
   - Implement an alert system for severe outliers (e.g. temperature above 100°C or mass balance error outside ±3 L/min).
   - Consider a real-time dashboard for simultaneous monitoring of temperature, pressure, and mass balance.

## 7. Final Conclusion

The data reveals that the separator system faces several distinct challenges:

- The row 95 temperature outlier represents a critical, urgent issue.
- The mass balance drift is a systemic and independent issue requiring investigation of the flow streams and their sensors.
- The milder outliers (temperature rows 179/209, pressure rows 61/101) can be managed through ongoing monitoring and calibration.

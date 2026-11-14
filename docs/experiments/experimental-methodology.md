# Experimental Methodology

## 1. Objective

The experiments investigated the vacuum-generation response of the prototype pump under different PWM duty-cycle settings. Pressure measurements were obtained using a BMP280 pressure sensor and recorded as gauge pressure relative to the atmospheric reference.

The experiments were preliminary hardware characterisation tests. They were not medical performance or safety validation tests.

## 2. Measurement setup

The experimental system included:

- Raspberry Pi Pico 2W running MicroPython
- BMP280 pressure sensor
- KMDP vacuum pump
- L298N motor driver
- PWM-based motor actuation
- XL6009 DC-DC converter

The archived firmware logs identify a PWM frequency of 1 kHz. The archived experiments used nominal sampling intervals of approximately 0.1 seconds.

## 3. Archived experiments

### Experiment 01

- PWM settings: 80% and 100%
- Sampling interval: 0.1 seconds
- Settling time recorded in the log: 3 seconds
- Measurements: 189 per PWM segment
- Date: Not recorded in the available log

### Experiment 02

- PWM setting: 100%
- Date: 14 July 2026
- Measurements: 9
- The log records intermittent actuation and pressure recovery observations.
- This was a short observation rather than a complete response-characterisation run.

### Experiment 03

- PWM settings: 80% and 100%
- Date: 14 July 2026
- Sampling interval: approximately 0.1 seconds
- Settling time recorded in the log: 3 seconds
- Measurements: 189 per PWM segment
- Atmospheric calibration samples were recorded before the test.

The 100% PWM segment in Experiment 03 followed the 80% segment without a documented return to atmospheric pressure. It therefore began under residual vacuum conditions and should not be interpreted as an independent test starting from the same initial pressure.

## 4. Final lab-session dataset

A separate dataset was transcribed from the original plotting scripts used during the final lab session.

- PWM settings: 80%, 90%, and 100%
- Sampling interval: 1 second
- Measurements: 16 per PWM setting
- Duration represented: 0–15 seconds per setting

The original raw serial logs for this session were not available in the archived data. The dataset is therefore retained separately as supplementary experimental data.

## 5. Data processing

The archived serial logs were parsed to extract:

- PWM duty cycle
- Absolute pressure
- Gauge vacuum pressure
- Sample index
- Original source line number

For each PWM segment, the analysis calculated:

- Sample count
- Mean gauge pressure
- Standard deviation
- Most negative recorded gauge pressure
- Least negative recorded gauge pressure
- Final recorded pressure

The reported summary statistics in the original logs were compared against independently recalculated values.

The final-session dataset was analysed separately. A descriptive plateau-detection heuristic was used with a pressure tolerance of 0.02 mmHg and a minimum of three samples. This is a numerical characterisation method, not proof of physical steady state.

## 6. Data interpretation and limitations

- Archived measurement records do not contain individual timestamps. Their plots therefore use sample index rather than reconstructed elapsed time.
- The nominal sampling interval should not be treated as an individually verified timestamp for every measurement.
- Experiment 02 contains only nine observations.
- The final-session dataset was transcribed from plotting scripts rather than recovered from original serial logs.
- The experimental vacuum levels were substantially below the intended design range.
- The prototype was not validated as a medical device.

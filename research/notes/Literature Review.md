# Literature Notes
## Project: Biomimetic Closed-Loop Electric Breast Pump

---

## Research Objective

Develop a proof-of-concept biomimetic breast pump platform that combines:
- Embedded control systems,
- Pneumatic vacuum generation,
- Pressure feedback,
- Future integration with a breast milk analyser.

---

## Key Papers Reviewed

### 1. SmartLact8: A Bio-Inspired Robotic Breast Pump
- Natural infant suckling consists of rhythmic vacuum cycles.
- Breastfeeding involves both suction and compression.
- Biomimetic pumping should reproduce the temporal vacuum waveform rather than only the average vacuum.

**Key Takeaway:**
> The controller should generate stimulation and expression modes with different vacuum amplitudes and frequencies.

---

### 2. Breastfeeding Biomechanics (Springer, 2021)
- Breast pumping is a dynamic biomechanical process.
- Tissue compliance and leakage introduce disturbances.
- Feedback control is preferable to fixed open-loop control.

**Key Takeaway:**
> The pump-chamber system can be modeled as a dynamic plant requiring closed-loop regulation.

---

### 3. WF Sensors - Multi-stage Suction Adjustment
- Modern breast pumps employ pressure sensors.
- Pressure feedback enables user-adjustable suction levels.
- Typical operating range: -50 mmHg to -200 mmHg.

**Key Takeaway:**
> Pressure sensing is essential for intelligent and biomimetic breast pump operation.

---

## Overall Design Insights

- Target vacuum range: -50 mmHg to -200 mmHg.
- Two operating modes:
  - Stimulation (high frequency, low vacuum).
  - Expression (lower frequency, higher vacuum).
- Closed-loop pressure control can compensate for leakage and varying breast seal conditions.
Project Status and Future Work
1. Completed Work
Hardware and Prototyping
- Developed a vacuum-pump prototype using a KMDP-U1-24V pump.
- Interfaced a BMP280 pressure sensor during development.
- Used a Raspberry Pi Pico 2W as the later controller.
- Developed motor actuation using an L298N module.
- Identified and measured the CKS5001/04 solenoid valve.
- Performed mechanical measurements for CAD modelling.
Embedded Development
- Developed MicroPython sensor and motor-control code.
- Implemented PWM-based motor speed control.
- Developed pressure acquisition and monitoring routines.
- Created a preliminary PI controller implementation.
- Developed preliminary operating-mode and state-machine structures.
Experimental Analysis
- Conducted PWM-based vacuum characterisation.
- Preserved archived experimental measurements.
- Transcribed a supplementary final-session dataset from
- original plotting scripts.
- Developed Python scripts for processing and plotting data.
- Documented the experimental methodology and results.
Mechanical and Electrical Design
- Developed FreeCAD models for the pump motor sleeve and valve.
- Created an earlier ESP32-based KiCad schematic reference.
2. Experimental Performance
The intended pressure range was approximately -50 to -200 mmHg.
The documented measurements were approximately -3 to -11 mmHg.
The prototype did not achieve its intended pressure range
during the recorded experiments.
The experiments provide preliminary information about the
pressure response to PWM duty-cycle changes. They do not
establish clinical or medical-device performance.
3. Incomplete Work
- Integration and validation of the solenoid valve.
- Reconciliation of the BMP280 driver interfaces.
- Integration of firmware into one consistent application.
- PI controller tuning and physical closed-loop validation.
- Completion of stimulation and expression modes.
- Verification of the complete electrical and pneumatic design.
- Fabrication and validation of mechanical CAD components.
4. Recommended Future Work
1. Consolidate the BMP280 driver and sensor interface.
2. Establish a verified wiring and power-distribution diagram.
3. Validate sensor calibration and measurement accuracy.
4. Characterise pump performance under controlled conditions.
5. Investigate the difference between target and measured vacuum.
6. Complete valve-driver and pneumatic integration.
7. Tune the PI controller using measured system response.
8. Validate closed-loop operation with independent pressure
9. monitoring and appropriate hardware safety measures.
10. Fabricate and fit-test the mechanical components.
11. Conduct repeatability and reliability testing.
5. Scope and Disclaimer
This repository documents an engineering prototype and its
development process. It is not a validated medical device and
must not be used to make medical or clinical claims.

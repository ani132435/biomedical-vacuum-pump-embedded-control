import matplotlib.pyplot as plt
import numpy as np


t80 = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

v80 = np.array([
0,
-3.9,
-5.2,
-5.5,
-5.56,
-5.58,
-5.58,
-5.58,
-5.58,
-5.58,
-5.58,
-5.58,
-5.58,
-5.58,
-5.58,
-5.58
])


t90 = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

v90 = np.array([
0,
-5.5,
-7.0,
-7.65,
-7.90,
-8.00,
-8.08,
-8.12,
-8.16,
-8.18,
-8.20,
-8.21,
-8.22,
-8.22,
-8.22,
-8.22
])


t100 = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

v100 = np.array([
0,
-3.20,
-5.06,
-5.95,
-6.83,
-7.30,
-7.81,
-8.21,
-8.49,
-9.00,
-9.25,
-9.61,
-9.91,
-10.16,
-10.37,
-10.71
])



plt.figure(figsize=(8,5))

plt.plot(t80, v80,
         marker='o',
         linewidth=2,
         markersize=5,
         label='80% PWM')

plt.plot(t90, v90,
         marker='s',
         linewidth=2,
         markersize=5,
         label='90% PWM')

plt.plot(t100, v100,
         marker='^',
         linewidth=2,
         markersize=5,
         label='100% PWM')

plt.grid(True, linestyle='--', alpha=0.6)

plt.xlabel('Time (s)', fontsize=12)
plt.ylabel('Vacuum Pressure (mmHg)', fontsize=12)

plt.title('Vacuum Pressure Response at Different PWM Duty Cycles',
          fontsize=13)

plt.xlim(0,15)
plt.ylim(-11.5,0.5)



plt.legend()

plt.tight_layout()

plt.savefig("Vacuum_Response_PWM.png", dpi=300)

plt.show()
import matplotlib.pyplot as plt

pwm = [80, 90, 100]
vacuum = [-5.58, -8.22, -10.71]

plt.figure(figsize=(6,4))

plt.plot(
    pwm,
    vacuum,
    marker='o',
    linewidth=2,
    markersize=8
)

plt.grid(True, linestyle='--', alpha=0.6)

plt.xlabel("PWM Duty Cycle (%)", fontsize=12)
plt.ylabel("Steady-State Vacuum (mmHg)", fontsize=12)

plt.title("Steady-State Vacuum vs PWM Duty Cycle", fontsize=13)

plt.xticks([80,90,100])

plt.tight_layout()

plt.savefig("PWM_vs_Vacuum.png", dpi=300)

plt.show()
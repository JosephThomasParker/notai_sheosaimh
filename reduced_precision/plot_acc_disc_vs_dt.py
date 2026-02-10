import numpy as np
import matplotlib.pyplot as plt

# Parameters
alpha = 1.0
beta = 1.0
gamma = 1.0

# Three (eps_a, eps_b) pairs
eps32 = 6e-8
eps64 = 1e-16
eps_pairs = [
    (eps32, eps32),
    (eps64, eps64),
    (eps32, eps64)
]

# dt range
dt = np.logspace(-11, 0, 200)  # from 1e-3 to 10

plt.figure(figsize=(6,4))

for i, (eps_a, eps_b) in enumerate(eps_pairs, 1):
    y = np.maximum.reduce([
        alpha * dt,
        beta * eps_a * np.ones_like(dt),
        gamma * eps_b / dt
    ])
    plt.loglog(dt, y, label=f"eps_a={eps_a}, eps_b={eps_b}")

plt.xlabel("dt")
plt.ylabel("max(alpha*dt, beta*eps_a, gamma*eps_b/dt)")
plt.title("Piecewise max function vs dt")
plt.legend()
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.savefig("acc_disc_vs_dt.png")


import numpy as np
import matplotlib.pyplot as plt

time_delay = 30*1e-9 # 30ns

freq = np.linspace(3e9,3.1e9,100)
delay_correction_factor = np.exp(1j * 2 * np.pi * freq * time_delay)

plt.plot(freq, delay_correction_factor.real)
plt.plot(freq, delay_correction_factor.imag)
plt.show()
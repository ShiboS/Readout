import Fitter as Fit
import numpy as np
import matplotlib.pyplot as plt


a = 2
alpha = np.pi/2.
tau = 0
phi0 = 0
f0 = 1e9
Qi = 5e10
Qc = 1e5
Qr = 1./(1/Qc + 1/Qi)

freq = np.linspace(f0*0.9995, f0*1.0005, 1001)
curve = Fit.Fit_7para_Model(a, alpha, tau, phi0, f0, Qr, Qc, freq)

plt.subplot(2,2,1)
plt.plot(curve.real, curve.imag)
plt.axis('equal')

plt.subplot(2,2,2)
plt.plot(freq/f0, np.arctan2(curve.imag, curve.real), 'r.')
plt.xlim([0.9995,1.0005])
ax = plt.gca()
ax.ticklabel_format(useOffset=False)
plt.subplot(2,2,3)
plt.plot(freq/f0, curve.real, 'r.')

plt.xlim([0.9995,1.0005])
ax = plt.gca()
ax.ticklabel_format(useOffset=False)
plt.subplot(2,2,4)
plt.plot(freq/f0, curve.imag, 'r.')

plt.xlim([0.9995,1.0005])
ax = plt.gca()
ax.ticklabel_format(useOffset=False)
plt.show()

curve = Fit.Fit_7para_Model(a, 0, tau, 0, f0, Qr, Qc, freq)
plt.plot(curve.real, curve.imag, 'r')

curve = Fit.Fit_7para_Model(a, 0.1, tau, 0, f0, Qr, Qc, freq)
plt.plot(curve.real, curve.imag)
curve = Fit.Fit_7para_Model(a, 0.1, tau, -0.1, f0, Qr, Qc, freq)
plt.plot(curve.real, curve.imag)
#curve = Fit.Fit_7para_Model(a, 0.3, tau, -0.3, f0, Qr, Qc, freq)
#plt.plot(curve.real, curve.imag, 'r.')
plt.show()

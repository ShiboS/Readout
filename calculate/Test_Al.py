import MB_Original as MB
import SurfImp
import matplotlib.pyplot as plt
import numpy as np

delta_0_eV_Al = 177e-6 # Al eV
Tc_Al = 1.25
sigma_n = 0.0565e8 # Nb 25nm
thickness = 25e-9
BCS_ratio = 1.76

a = [0]*150
c = [0]*150
sigma = [0]*150
Z_s = [0]*150
R_s = [0]*150
X_s = [0]*150
Thin = [0]*150
Thick = [0]*150
for fr in range(1,151):
    T = 0.1 +(fr-1)*0.02
    a[fr-1] = MB.MB_sigma1(MB.delta_eV_func(BCS_ratio, Tc_Al, T), 7e9, T)
    c[fr-1] = MB.MB_sigma2(MB.delta_eV_func(BCS_ratio, Tc_Al, T), 7e9, T)
    sigma[fr-1] = (a[fr-1] - c[fr-1]*1j)*sigma_n
    Z_s[fr-1] = SurfImp.SurfImp(sigma[fr-1], 7e9, thickness)
    R_s[fr-1] = Z_s[fr-1].real
    X_s[fr-1] = Z_s[fr-1].imag
    Thin[fr-1] = SurfImp.SurfImp_thin(1./sigma_n, Tc_Al, thickness, MB.delta_eV_func(BCS_ratio, Tc_Al, T), T, 7e9)
    Thick[fr-1] = SurfImp.SurfImp_thick_local(1./sigma_n, Tc_AL, MB.delta_eV_func(BCS_ratio, Tc_Al, T), T, 7e9)

import csv
f = open('MB.csv', 'w')
fwrite = csv.writer(f)
for fr in range(1,151):
    T = 0.1 +(fr-1)*0.02
    fwrite.writerow([T, R_s[fr-1], X_s[fr-1], Thin[fr-1].real, Thin[fr-1].imag, Thick[fr-1].real, Thick[fr-1].imag])
f.close()

fr = np.linspace(1,150,150)
plt.plot(fr, a)
plt.plot(fr, c)
#plt.xscale("log")
plt.yscale("log")
plt.show()
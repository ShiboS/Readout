import MB_Original as MB
import SurfImp
import matplotlib.pyplot as plt
import numpy as np
import CPW as CPW
from scipy.constants import  pi

delta_0_eV_Al = 177e-6 # Al eV
Tc_Nb25nm = 9
sigma_n = 1./(2e-8)
sigma_n_nb25 = 0.0565e8 # Nb 25nm
thickness = 150e-9
BCS_ratio = 1.76

CPW_C = 6e-6
CPW_G = 2e-6

n = 160
a = [0]*n
c = [0]*n
sigma = [0]*n
Z_s = [0]*n
R_s = [0]*n
X_s = [0]*n
Thin = [0]*n
Thick = [0]*n
CPW_imp = [0]*n
CPW_alpha = [0]*n
CPW_imp2 = [0]*n
CPW_alpha2 = [0]*n
Zssigma = [0]*n
CPW_alphasigma = [0]*n
for fr in range(1,n+1):
    T = 0.1
    freq = fr*1e9
    a[fr-1] = MB.MB_sigma1(MB.delta_eV_func(BCS_ratio, Tc_Nb25nm, T), freq, T)
    c[fr-1] = MB.MB_sigma2(MB.delta_eV_func(BCS_ratio, Tc_Nb25nm, T), freq, T)
    sigma[fr-1] = (a[fr-1] - c[fr-1]*1j)*sigma_n
    Z_s[fr-1] = SurfImp.SurfImp(sigma[fr-1], freq, thickness)
    R_s[fr-1] = Z_s[fr-1].real
    X_s[fr-1] = Z_s[fr-1].imag
    Thin[fr-1] = SurfImp.SurfImp_thin(1./sigma_n, Tc_Nb25nm, thickness, MB.delta_eV_func(BCS_ratio, Tc_Nb25nm, T), T, freq)
    Thick[fr-1] = SurfImp.SurfImp_thick_local(1./sigma_n, Tc_Nb25nm, MB.delta_eV_func(BCS_ratio, Tc_Nb25nm, T), T, freq)
    CPW_imp2[fr-1] = CPW.Imp_Simple(CPW_C, CPW_G, 11.7, thickness, R_s[fr-1], X_s[fr-1]/freq/2./pi)[0]
    CPW_alpha2[fr-1] = CPW.Imp_Simple(CPW_C, CPW_G, 11.7, thickness, R_s[fr-1], X_s[fr-1]/freq/2./pi)[1]
    CPW_imp[fr-1] = CPW.Imp_Simple(CPW_C, CPW_G, 11.7, thickness, Thin[fr-1].real, Thin[fr-1].imag/freq/2./pi)[0]
    CPW_alpha[fr-1] = CPW.Imp_Simple(CPW_C, CPW_G, 11.7, thickness, Thin[fr-1].real, Thin[fr-1].imag/freq/2./pi)[1]
    Zssigma[fr-1] = SurfImp.SurfImp_sigma(sigma[fr-1], thickness)
    CPW_alphasigma[fr-1] = CPW.Imp_Simple(CPW_C, CPW_G, 11.7, thickness, Zssigma[fr-1].real, Zssigma[fr-1].imag/freq/2./pi)[1]

import csv
f = open('MB.csv', 'w')
fwrite = csv.writer(f)
fwrite.writerow(['Temp K', 'Rs Visser', 'Xs visser', 'Rs Review Thin', 'Xs Review Thin', 'Rs Review Thick', 'Xs Review Thick', 'CPW Imp Visser', 'alpha Visser', 'CPW Imp Review Thin', 'alpha Review Thin', 'sigma2 thickness alpha'])
for fr in range(1,n+1):
    T = 0.1 +(fr-1)*0.02
    freq = fr*1e9
    fwrite.writerow([freq/1e9, R_s[fr-1], X_s[fr-1], Thin[fr-1].real, Thin[fr-1].imag, Thick[fr-1].real, Thick[fr-1].imag, CPW_imp2[fr-1], CPW_alpha2[fr-1], CPW_imp[fr-1], CPW_alpha[fr-1], CPW_alphasigma[fr-1]])
f.close()
"""
fr = np.linspace(1,150,150)
plt.plot(fr, a)
plt.plot(fr, c)
#plt.xscale("log")
plt.yscale("log")
plt.show()
"""
# CPW.Imp_Hybrid(CPW_C, CPW_G, epsilon, C_thickness, G_thickness, C_R_s, C_L_s, G_R_s, G_L_s)
print CPW_alphasigma[0]
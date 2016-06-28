import MB_Original as MB
import SurfImp
import matplotlib.pyplot as plt
import numpy as np
import CPW as CPW
from scipy.constants import  pi
from DataReader import ReadSingle
import FitResult as fit

def inductance(CPW_C, CPW_G, thickness, BCS_ratio, T_c, Temp, freq, sigma_n):
    ## Driessen PRL2012 supp
    delta_0 = MB.delta_eV_func(BCS_ratio, T_c, Temp)
    L_s = SurfImp.SurfL(delta_0, freq, Temp, thickness, sigma_n)
    
    Die_thickness = 380e-6
    k, k_prime, k_1, k_1_prime, K_k, K_k_prime, K_k_1, K_k_1_prime, q = CPW.kparameter(CPW_C, CPW_G, Die_thickness)
    g_c, g_g = CPW.GeoFactor(CPW_C, CPW_G, thickness, k, K_k)
    gamma = g_c + g_g

    L_g = CPW.GeoInductance(K_k_prime, K_k)
    L_k = gamma*L_s
    return L_k, L_g

def f_0(A, CPW_C, CPW_G, thickness, BCS_ratio, T_c, Temp, freq, sigma_n):
    L_k, L_g = inductance(CPW_C, CPW_G, thickness, BCS_ratio, T_c, Temp, freq, sigma_n)
    f_0 = A/np.sqrt(L_g+L_k)
    return f_0

def initialA(CPW_C, CPW_G, thickness, BCS_ratio, T_c, Temp, freq, sigma_n):
    L_k, L_g = inductance(CPW_C, CPW_G, thickness, BCS_ratio, T_c, Temp, freq, sigma_n)
    A = np.sqrt(L_g+L_k) * freq
    return A

### Coumou 2013 IEEE
def beta(thickness, penedepth):
    return 1 + (2*thickness/penedepth/np.sinh(2*thickness/penedepth))

def Qical(CPW_C, CPW_G, thickness, BCS_ratio, T_c, Temp, freq, sigma_n):
    delta_0 = MB.delta_eV_func(BCS_ratio, T_c, Temp)
    L_k, L_g = inductance(CPW_C, CPW_G, thickness, BCS_ratio, T_c, Temp, freq, sigma_n)
    penedepth = SurfImp.SurfL_PeneDepth(delta_0, freq, Temp, sigma_n)
    alpha = L_k/(L_k+L_g)
    betta = beta(thickness,penedepth)
    sigma1 = MB.MB_sigma1(delta_0, freq, Temp)
    sigma2 = MB.MB_sigma2(delta_0, freq, Temp)
    return (2/alpha/betta)*(sigma2/sigma1)
    
### What do I really want to fit?
folder = "../../../MeasurementResult/Milano/"
filename = "20160412_Nb140nm_3.8615855_-25dBm.csv"
power, tempdata, frmin, frfit, frfit_err, Qr, Qr_err, Qc, Qc_err, Qifit, Qi_err = ReadSingle(folder, filename)

CPW_C = 4e-6
CPW_G = 1.5e-6
thickness = 140e-9
BCS_ratio = 1.76
T_c = 8.7
sigma_n = 1.0/16.5e-8

temp = tempdata/1000
freq = frfit*1e9
f0 = freq[0]
temp0 = temp[0]
"""
A0 = initialA(CPW_C, CPW_G, thickness, BCS_ratio, T_c, temp0, f0, sigma_n)
f0 = f_0(A0, CPW_C, CPW_G, thickness, BCS_ratio, T_c, temp0, f0, sigma_n)

fitpara = [CPW_C, CPW_G, thickness, BCS_ratio, T_c, f0, sigma_n, A0]
a = fit.Fit_frvsT(temp[10:], freq[10:], fitpara)
fitresult = np.asarray([f_0(a[2], CPW_C, CPW_G, thickness, BCS_ratio, a[0], temperature, f0, sigma_n) for temperature in temp])

tempplot = np.linspace(temp0, temp[len(temp)-1], num=10)
freqsweep = np.asarray([f_0(A0, CPW_C, CPW_G, thickness, BCS_ratio, T_c, temperature, f0, sigma_n) for temperature in tempplot])

plt.figure(1)
plt.plot(temp, fitresult/1e9, 'o')
plt.plot(temp, frfit,'.')
#plt.plot(tempplot, freqsweep/1e9,'.r')
#plt.xlim([0.1,0.4])
#plt.ylim([2.176e9,2.223e9])
plt.show()
"""
plt.figure(2)
Qi = np.asarray([Qical(CPW_C, CPW_G, thickness, BCS_ratio, T_c, temp[i], f0, sigma_n) for i in range(0, len(temp))])
Qi8 = np.asarray([Qical(CPW_C, CPW_G, thickness, BCS_ratio, 8.0, temp[i], f0, sigma_n) for i in range(0, len(temp))])
Qfitpara = [CPW_C, CPW_G, thickness, BCS_ratio, T_c, f0, sigma_n]
Qfitresult = fit.Fit_QvsT(temp[15:], freq[15:], Qfitpara)
Qical = np.asarray([Qfitresult[2]*Qical(CPW_C, CPW_G, thickness, BCS_ratio, Qfitresult[0], temperature, f0, sigma_n) for temperature in temp])
plt.plot(temp/T_c, Qical)
plt.plot(tempdata/1000/T_c, Qifit, '.')
#plt.plot(temp/T_c, Qi)
#plt.plot(temp/T_c, Qi8)
#plt.ylim([1e4,1e6])
plt.yscale('log')
plt.show()
import MB_Original as MB
import SurfImp
import matplotlib.pyplot as plt
import numpy as np
import CPW as CPW
from scipy.constants import  pi
from dataReader import ReadSingle


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


folder = "../../../MeasurementResult/20160516_Nb154nmCry3/"
filename = "20160516_Nb154nmCry3_3.8675664_-50dBm.csv"
power, temp, frmin, frfit, frfit_err, Qr, Qr_err, Qc, Qc_err, Qi, Qi_err = ReadSingle(folder, filename)

CPW_C = 3e-6
CPW_G = 2e-6
thickness = 6e-9
BCS_ratio = 1.76
T_c = 1.5
Temp = 0.1*T_c
freq = 2.222e9
sigma_n = 380e-8
A0 = initialA(CPW_C, CPW_G, thickness, BCS_ratio, T_c, Temp, freq, sigma_n)
f0 = f_0(A0, CPW_C, CPW_G, thickness, BCS_ratio, T_c, Temp, freq, sigma_n)

temp = np.linspace(0.1*T_c, 0.5*T_c, num=90)
freq = 2.222e9
freqsweep = np.asarray([f_0(A0, CPW_C, CPW_G, thickness, BCS_ratio, T_c, temp[i], freq, sigma_n) for i in range(0, len(temp))])


fig, ax = plt.subplots()
ax.plot(temp/T_c, freqsweep,'.r')
ax.ticklabel_format(useOffset=False)
plt.xlim([0.1,0.4])
plt.ylim([2.176e9,2.223e9])
plt.show()



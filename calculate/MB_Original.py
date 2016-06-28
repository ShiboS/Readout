import numpy as np
import scipy.integrate as integrate
from scipy.constants import e, hbar, pi, k as k_B


def kBT_eV_func(Temperature):
    return k_B * Temperature / e
    
def hbaromega_eV_func(freq):
    return 2 * pi * freq * hbar /e
    
def delta_eV_func(BCS_ratio, Tc, Temperature):
    delta_0_eV = BCS_ratio * Tc * k_B / e
    t = Temperature/Tc
    return delta_0_eV*np.sqrt(np.cos(pi/2.*t*t))

def f(E,kBT_eV):
    if kBT_eV == 0:
        return 0
    elif (E/kBT_eV) > 709:
        return 0
    else:
        return 1.0/(np.exp(E/kBT_eV) + 1.0)

def g1_1(E, delta_0_eV, hbaromega_eV):
    return (E**2 + delta_0_eV**2 + hbaromega_eV*E) / ((E**2-delta_0_eV**2)**0.5*((E+hbaromega_eV)**2-delta_0_eV**2)**0.5)
    
def g1_2(E, delta_0_eV, hbaromega_eV):
    if hbaromega_eV > 2*delta_0_eV:
        return (E**2 + delta_0_eV**2 + hbaromega_eV*E) / ((E**2-delta_0_eV**2)**0.5*((E+hbaromega_eV)**2-delta_0_eV**2)**0.5)
    else:
        return 0
        
def g2(E, delta_0_eV, hbaromega_eV):
    return (E**2 + delta_0_eV**2 + hbaromega_eV*E) / ((delta_0_eV**2-E**2)**0.5*((E+hbaromega_eV)**2-delta_0_eV**2)**0.5)
    
def MB_sigma1_1_integration(delta_0_eV, hbaromega_eV, kBT_eV):
    sigma_1_1 = lambda E: (2.0/hbaromega_eV) * (f(E, kBT_eV)-f(E+hbaromega_eV, kBT_eV)) * g1_1(E, delta_0_eV, hbaromega_eV)
    return integrate.quad(sigma_1_1, delta_0_eV, np.Inf, epsabs = 0)
    # There will be warning for this integration, because of the epsabs=0 cannot be achieved.
    # Check the result and error. Need to be improved.
    
def MB_sigma1_2_integration(delta_0_eV, hbaromega_eV, kBT_eV):
    sigma_1_2 = lambda E: (1.0/hbaromega_eV) * (1.0-2.0*f(E+hbaromega_eV, kBT_eV)) * g1_2(E, delta_0_eV, hbaromega_eV)
    return integrate.quad(sigma_1_2, min(delta_0_eV-hbaromega_eV, -delta_0_eV), -delta_0_eV)

def MB_sigma2_integration(delta_0_eV, hbaromega_eV, kBT_eV):
    sigma_2 = lambda E: (1.0/hbaromega_eV) * (1.0-2.0*f(E+hbaromega_eV, kBT_eV)) * g2(E, delta_0_eV, hbaromega_eV)
    return integrate.quad(sigma_2, max(delta_0_eV-hbaromega_eV, -delta_0_eV), delta_0_eV)
    
def MB_sigma1(delta_0_eV, freq, T):
    hbaromega_eV = hbaromega_eV_func(freq)
    kBT_eV = kBT_eV_func(T)
    sigma_1_1 = MB_sigma1_1_integration(delta_0_eV, hbaromega_eV, kBT_eV)
    sigma_1_2 = MB_sigma1_2_integration(delta_0_eV, hbaromega_eV, kBT_eV)
    print sigma_1_1, sigma_1_2
    return sigma_1_1[0] - sigma_1_2[0]

def MB_sigma2(delta_0_eV,  freq, T):
    hbaromega_eV = hbaromega_eV_func(freq)
    kBT_eV = kBT_eV_func(T)
    sigma_2 = MB_sigma2_integration(delta_0_eV, hbaromega_eV, kBT_eV)
    return sigma_2[0]
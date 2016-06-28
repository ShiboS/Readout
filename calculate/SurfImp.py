import numpy as np
from scipy.constants import mu_0, pi
import MB_Original as MB

### Visser p96 accurate in our case
def SurfImp(sigma, freq, thickness):
    omega = 2 * pi * freq
    return np.sqrt(mu_0*omega*1j/sigma)*1.0/np.tanh(thickness * np.sqrt(1j*mu_0*omega*sigma))
 
### Jonas Review Eqn 6 ~ 12   
def PeneDepth_local(Rho_n, T_c):
    return 105e-9*np.sqrt(Rho_n*10e8/T_c)
    
def PeneDepth_thin(Rho_n, T_c, Thickness):
    return PeneDepth_local(Rho_n, T_c)**2/Thickness
    
def DeltaSigma(delta_0, freq, Temp):
    return MB.MB_sigma1(delta_0, freq, Temp) - 1j*(MB.MB_sigma2(delta_0, freq, Temp)-MB.MB_sigma2(delta_0, freq, 0))

def SurfImp_T0(PeneDepth, omega):
    return 1j*mu_0*omega*PeneDepth

def SurfImp_thick_local(Rho_n, T_c, delta_0, Temp, freq):
    omega = 2*pi*freq
    return SurfImp_T0(PeneDepth_local(Rho_n, T_c), omega)/np.sqrt(1 + 1j*DeltaSigma(delta_0, freq, Temp)/MB.MB_sigma2(delta_0, freq, 0))

def SurfImp_thin(Rho_n, T_c, Thickness, delta_0, Temp, freq):
    omega = 2*pi*freq
    return 1j*mu_0*omega*PeneDepth_thin(Rho_n, T_c, Thickness)/(1 + 1j*DeltaSigma(delta_0, freq, Temp)/MB.MB_sigma2(delta_0, freq, 0))

### Gao p34 Eqn 2.79
def SurfImp_sigma(sigma, thickness):
    return 1./sigma/thickness
    
### Driessen PRL2012 supp
def SurfL_PeneDepth(delta_0, freq, Temp, sigma_n):
    omega = 2*pi*freq
    return 1.0/np.sqrt(mu_0*omega*MB.MB_sigma2(delta_0, freq, Temp)*sigma_n)
    
def SurfL(delta_0, freq, Temp, Thickness, sigma_n):
    PeneDepth = SurfL_PeneDepth(delta_0, freq, Temp, sigma_n)
    return mu_0*PeneDepth/np.tanh(Thickness/PeneDepth)
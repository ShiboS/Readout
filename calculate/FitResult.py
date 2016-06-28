import numpy as np
from matplotlib import pyplot as plt, cm, colors
from lmfit import minimize, Parameters, fit_report
import MB_Original as MB
import SurfImp
import CPW as CPW
from scipy.constants import  pi

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

def Fit_frvsT_Func(params, temp, freq):
        """ PhaseFit test"""
        CPWC = params['CPWC'].value
        CPWG = params['CPWG'].value
        thick = params['thick'].value
        BCS = params['BCS'].value
        Tc = params['Tc'].value
        f0 = params['f0'].value
        sigman = params['sigman'].value
        A = params['A'].value
        fr = [f_0(A, CPWC, CPWG, thick, BCS, Tc, temperature, f0, sigman) for temperature in temp]
        return fr-freq

def Fit_frvsT(temp, freq, fitpara):
    # create a set of Parameters
    params = Parameters()
    print fitpara
    params.add_many(('CPWC',  fitpara[0], False, None, None,  None),
                    ('CPWG',  fitpara[1], False, None, None,  None),
                    ('thick', fitpara[2], False, None, None,  None),
                    ('BCS',   fitpara[3], False, None, None,  None),
                    ('Tc',    fitpara[4],  True, None, None,  None),
                    ('f0',    fitpara[5], False, None, None,  None),
                    ('sigman',fitpara[6], False, None, None,  None),
                    ('A',     fitpara[7],  True, fitpara[7]*0.9, fitpara[7]*1.1,  None))

    # do fit, here with leastsq model
    result = minimize(Fit_frvsT_Func, params, args=(temp, freq))
    
    # calculate final result
    residual = result.residual
    
    Tc = result.params['Tc'].value
    Tc_err = np.abs(result.params['Tc'].stderr/Tc)
    A = result.params['A'].value
    A_err = np.abs(result.params['A'].stderr/A)
    print fit_report(result)
    return Tc, Tc_err, A, A_err, fit_report(result)

### Coumou 2013 IEEE
def beta(thickness, penedepth):
    return 1 + (2*thickness/penedepth/np.sinh(2*thickness/penedepth))

def Qical(CPW_C, CPW_G, thickness, BCS_ratio, T_c, Temp, freq, sigma_n, A):
    delta_0 = MB.delta_eV_func(BCS_ratio, T_c, Temp)
    L_k, L_g = inductance(CPW_C, CPW_G, thickness, BCS_ratio, T_c, Temp, freq, sigma_n)
    penedepth = SurfImp.SurfL_PeneDepth(delta_0, freq, Temp, sigma_n)
    alpha = L_k/(L_k+L_g)
    betta = beta(thickness,penedepth)
    sigma1 = MB.MB_sigma1(delta_0, freq, Temp)
    sigma2 = MB.MB_sigma2(delta_0, freq, Temp)
    return A*(2./alpha/betta)*(sigma2/sigma1)

def Fit_QvsT_Func(params, temp, Q):
        """ PhaseFit test"""
        CPWC = params['CPWC'].value
        CPWG = params['CPWG'].value
        thick = params['thick'].value
        BCS = params['BCS'].value
        Tc = params['Tc'].value
        f0 = params['f0'].value
        sigman = params['sigman'].value
        A = params['A'].value
        Qcal = [Qical(CPWC, CPWG, thick, BCS, Tc, temperature, f0, sigman, A) for temperature in temp]
        return Q-Qcal

def Fit_QvsT(temp, freq, fitpara):
    # create a set of Parameters
    params = Parameters()
    params.add_many(('CPWC',  fitpara[0], False, None, None,  None),
                    ('CPWG',  fitpara[1], False, None, None,  None),
                    ('thick', fitpara[2], False, None, None,  None),
                    ('BCS',   fitpara[3], False, None, None,  None),
                    ('Tc',    fitpara[4],  True, 0.1, 10,  None),
                    ('f0',    fitpara[5], False, None, None,  None),
                    ('sigman',fitpara[6], False, None, None,  None),
                    ('A',           1e-5,  True, 1e-30, 1,  None))

    # do fit, here with leastsq model
    result = minimize(Fit_QvsT_Func, params, args=(temp, freq))
    
    # calculate final result
    residual = result.residual
    
    Tc = result.params['Tc'].value
    Tc_err = np.abs(result.params['Tc'].stderr/Tc)
    A = result.params['A'].value
    A_err = np.abs(result.params['A'].stderr/A)
    print fit_report(result)
    return Tc, Tc_err, A, A_err, fit_report(result)
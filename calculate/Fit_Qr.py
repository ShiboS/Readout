from lmfit import minimize, Parameters, fit_report
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as sc
from scipy.special import iv # Modified Bessel function of the first kind of real order I_0
from scipy.special import kn # Modified Bessel function of the second kind of integer order n K_0

def readout(folder, filename):
    data = []
    ###   Read parameter file
    with open(folder + filename,'r') as n:
        for line in n:
            data.append(map(str,line.rstrip('\r\n').split(',')))
        
    data = np.asarray(data)

    temperature = []
    Qr = []
    fr = []
    for i in range(1,len(data)):
        temperature.append(float(data[i][1]))
        Qr.append(float(data[i][5]))
        fr.append(float(data[i][12]))
    return np.asarray(temperature)/1000, np.asarray(Qr), np.asarray(fr)
    

def sigma1mbf(temperature, delta1, delta2, freq):
    omega = 2*sc.pi*freq
    sigma1mb = 4*delta1/sc.hbar/omega*np.exp(-delta1/sc.k/temperature)*np.sinh(sc.hbar*omega/2/sc.k/temperature)*kn(0,sc.hbar*omega/2/sc.k/temperature)
    return sigma1mb
  
def sigma1gbf(temperature, delta1, delta2, freq):
    omega = 2*sc.pi*freq
    sigma1gb = sc.pi*delta2/sc.hbar/omega*(1+2*delta1/sc.k/temperature*np.exp(-delta1/sc.k/temperature)*np.exp(-sc.hbar*omega/2/sc.k/temperature)*iv(0,sc.hbar*omega/2/sc.k/temperature))
    return sigma1gb

def sigma1f(temperature, delta1, delta2, freq):
    sigma1 = sigma1mbf(temperature, delta1, delta2, freq)+sigma1gbf(temperature, delta1, delta2, freq)
    return sigma1
    
def sigma2f(temperature, delta1, delta2, freq):
    omega = 2*sc.pi*freq
    sigma2 = sc.pi*delta1/sc.hbar/omega*(1-2*np.exp(-delta1/sc.k/temperature)*np.exp(-sc.hbar*omega/2/sc.k/temperature)*iv(0,sc.hbar*omega/2/sc.k/temperature))
    return sigma2  

def Qr_calc(temp, sdelta, Tc, alpha):
    delta1 = 1.764*sc.k*Tc
    delta2 = sdelta*delta1
    frequency = 4.479828125e9
    
    sigma1result = sigma1f(temp, delta1, delta2, frequency)
    sigma2result = sigma2f(temp, delta1, delta2, frequency)
    Qs = sigma2result/sigma1result
    Qr_calculated = 1/alpha * Qs
    
    return Qr_calculated

def Fit_Func(params, x, y):
    sdelta = params['sdelta'].value
    Tc = params['Tc'].value
    alpha = params['alpha'].value
    
    Qr_calculated = Qr_calc(x, sdelta, Tc, alpha)
    model = Qr_calculated - y
    return model

def Fit_Qr(x, y):
    # create a set of Parameters
    params = Parameters()
    params.add('sdelta', value= 1e-4, min = 1e-10, max = 1e-2)
    params.add('Tc', value= 1.2, min = 0.1, max = 1.8)
    params.add('alpha', value= 1, min = 1e-10, max = 1)
    
    # do fit, here with leastsq model
    result = minimize(Fit_Func, params, args=(x, y))
    
    # calculate final result
    residual = result.residual
    
    # Calculate Qc and Qi
    sdelta = result.params['sdelta'].value
    sdelta_err = np.abs(result.params['sdelta'].stderr/sdelta)
    Tc = result.params['Tc'].value
    Tc_err = np.abs(result.params['Tc'].stderr/Tc)
    alpha = result.params['alpha'].value
    alpha_err = np.abs(result.params['alpha'].stderr/Tc)
    print fit_report(result)
    
    return sdelta, sdelta_err, Tc, Tc_err, alpha, alpha_err, fit_report(result), residual
    
    

folder = ""
name0 = "20160814_Al_Noguchi_4.479828125_-25dBm.csv"
temp, Qr, freq = readout(folder, name0)
temp = temp[:-4]
Qr = Qr[:-4]
freq = freq[:-4]

# fit
sdelta, sdelta_err, Tc, Tc_err, alpha, alpha_err, fit_report, residual = Fit_Qr(temp, Qr)
Qr_fit = Qr_calc(temp, sdelta, Tc, alpha)

# plot
plt.subplot(2, 1, 1)
plt.plot(temp, Qr, 'b.', label="Qr measured")
plt.plot(temp, Qr_fit, 'r.', label="Qr fitted")
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(temp, residual, 'r.', label="residual")
plt.legend()
plt.show()


"""
plt.plot(temp, Qr, '.', label="Qr measured")
Qr_fit = Qr_calc(temp, sdelta, Tc, alpha)
plt.semilogy(temp, Qr_fit, '.', label = "Qr 1")
Qr_fit = Qr_calc(temp, sdelta, Tc, alpha/2)
plt.semilogy(temp, Qr_fit, '.', label = "Qr /2")
Qr_fit = Qr_calc(temp, sdelta, Tc, alpha*2)
plt.semilogy(temp, Qr_fit, '.', label = "Qr *2")
plt.legend()
plt.show()
"""
                                    
"""
temperature = np.linspace(0.01, 0.2, 101)
#temperature = 300 # K
frequency = 4.479828125e9
delta1 = 1.764*sc.k*1.26
delta2 = 0.00001*delta1
resistivity = 0.48*1e-8
normal_conductivity = 1/resistivity

sigma1mbresult = sigma1mbf(temperature, delta1, delta2, frequency)
sigma1gbresult = sigma1gbf(temperature, delta1, delta2, frequency)
sigma1result = sigma1f(temperature, delta1, delta2, frequency)
sigma2fresult = sigma2f(temperature, delta1, delta2, frequency)
Qs = sigma2fresult/sigma1result
#Qr_calculated = inverse_alpha * Qs
complex_conductivity = (sigma1result - 1j*sigma2fresult)*normal_conductivity
#plt.plot(temperature, sigma1mbresult)
#plt.plot(temperature, sigma1gbresult)
#plt.semilogy(temperature, sigma1result)
#plt.semilogy(temperature, sigma2fresult)
plt.semilogy(temperature, Qs, 'b.')
plt.semilogy(np.asarray(temp)/1000, Qr, 'r.')
plt.ylim([1e4, 1e7])
plt.show()

"""
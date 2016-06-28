import matplotlib.pyplot as plt
import numpy as np
import Fitter # For circle fitting
from lmfit import minimize, Parameters, Parameter, report_fit

### Read data from file
result = []
filename = '20160227_-15dBm_3.629962158_0.0025_81.08mK.csv'
with open('20160227_OMT/' + filename,'r') as f:
    for line in f:
        result.append(map(str,line.split(',')))
        #print line

### print test for reading data successfully
print result[1][0], result[1][1], result[1][2]
print float(result[2][0]), float(result[2][1]), float(result[2][2])

### http://stackoverflow.com/questions/27227399/python-split-a-string-at-an-underscore
### Split file name to get center frequency
def split_str(s, c, n):
    words = s.split(c)
    return c.join(words[:n]), c.join(words[n:])

### Get temperature and center freq with float format
### from single long filename like: "20160104_-30dBm_5.373811875_0.0025_99.96mK"
def centerFreqTemp(longfilename):
    FirstSplit = split_str(str(longfilename).replace("[", "").replace("]", "").replace("'", "").replace("\\r", ""), "_", 2)
    SecondSplit = split_str(FirstSplit[1], "_", 1)
    Temp = split_str(SecondSplit[1], "_", 1)
    T_float = float(Temp[1].replace("mK", ""))
    return T_float, float(SecondSplit[0])

### Initial fit frequency
MeasState = centerFreqTemp(filename.replace(".csv",""))
frInitial = MeasState[1]*1e9

freq = [0] * (len(result)-2)
linear = [0] * (len(result)-2)
phase = [0] * (len(result)-2)
real = [0] * (len(result)-2)
imag = [0] * (len(result)-2)

for i in range(0,len(result)-2):
    freq[i] = float(result[i+2][0])
    linear[i] = float(result[i+2][1])
    phase[i] = float(result[i+2][2])
    real[i] = linear[i] * np.cos(np.deg2rad(phase[i]))
    imag[i] = linear[i] * np.sin(np.deg2rad(phase[i]))

### Fit Circle
fitpara=np.array(Fitter.leastsq_circle(real,imag))
Fitter.plot_data_circle(real, imag, fitpara[0], fitpara[1], fitpara[2])
plt.show()
print fitpara

# Move origin dot to the fitted center of measured data
# Rotating and translating to the origin

x_c = fitpara[0]
y_c = fitpara[1]
radius = fitpara[2]
Z_i = [0]*(len(result)-2)
for i in range(0,len(result)-2):
    Z_i[i] = real[i] + 1j*imag[i]
Z_ii = (x_c + 1j*y_c - Z_i)*np.exp(-1j * np.arctan(y_c/x_c))
plt.plot(Z_ii.real, Z_ii.imag, 'r.', mew=0.1)
Fitter.plot_data_circle(Z_ii.real, Z_ii.imag, fitpara[0], fitpara[1], fitpara[2])
plt.show()

### Fit Phase
data_phase = np.arctan2(Z_ii.imag, Z_ii.real)

plt.plot(freq, data_phase)

plt.plot(Z_ii.real, Z_ii.imag)
plt.show()
print np.arctan2(y_c, x_c), np.arctan(y_c/x_c)
print len(Z_ii), len(freq)
"""
delete_number = 400
index = np.linspace(0, delete_number, delete_number+1)
Z_ii = np.delete(Z_ii, index)
freq = np.delete(freq, index)
index = np.linspace(len(Z_ii), len(Z_ii)-delete_number, delete_number+1)
Z_ii = np.delete(Z_ii, index)
freq = np.delete(freq, index)
print len(Z_ii), len(freq)
"""
### Get average of start and end point position
Z_real = 0
Z_imag = 0
for i in (0,1):
    Z_real = Z_ii.real[i] + Z_ii.real[len(Z_ii)-1-i] + Z_real
    Z_imag = Z_ii.imag[i] + Z_ii.imag[len(Z_ii)-1-i] + Z_imag

### Change phase here
Z_iic = Z_ii*np.exp(1j * (np.pi/2+np.arctan2(Z_real, Z_imag)))
phase_c = np.arctan2(Z_iic.imag, Z_iic.real)
#plt.plot(freq, phase_c)

plt.plot(Z_ii.real, Z_ii.imag)
plt.plot(Z_iic.real, Z_iic.imag)
plt.show()

### Fit phase
from lmfit import minimize, Parameters, Parameter, fit_report


# define objective function: returns the array to be minimized
def PhaseFit(params, freq, phase_c):
    """ PhaseFit test"""
    theta0 = params['theta0'].value
    Q_r = params['Q_r'].value
    f_r = params['f_r'].value
    model = -theta0 + 2*np.arctan(2 * Q_r * (1 - freq/f_r))
    return model - phase_c

# create a set of Parameters
params = Parameters()
params.add('theta0',   value= 0)
params.add('Q_r', value= 1e5, min = 1e3, max = 1e6)
params.add('f_r', value= frInitial, min = 3e9, max= 8e9)


# do fit, here with leastsq model
result = minimize(PhaseFit, params, args=(freq, phase_c))

# calculate final result
final = phase_c + result.residual

# Calculate Qc and Qi
Qr = result.params['Q_r'].value
Qc = (np.absolute(x_c + 1j*y_c) + radius)/2/radius*Qr # Ref: Gao Thesis
Qi = Qr*Qc/(Qc-Qr)

# write error report
print(fit_report(result))

#print "theta0", params['theta0'].value
print "fr", result.params['f_r'].value
print "Qr", Qr
print "Qi", Qi
print "Qc", Qc

#### Check the phase fitting
###  !!!!!!!!!
try:
    import pylab
    pylab.plot(freq, phase_c, 'k+')
    pylab.plot(freq, final, 'r')
    #pylab.plot(freq, result.residual, 'b')
    pylab.show()
except:
    pass

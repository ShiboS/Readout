import matplotlib.pyplot as plt
import numpy as np
import Fitter # For circle fitting
from lmfit import minimize, Parameters, Parameter, report_fit

### Read filename list
data_name = []
with open('20160104_Nb25nm/20160104_list1.csv','r') as n:
    for line in n:
        data_name.append(map(str,line.rstrip('\n').split(','))) # Remove '\n'

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

### Get all temperature and center freq with float format
### from data filename list
def centerFreqList(dataNameList):
    FreqList = []
    for i in dataNameList:
        FreqList.append(centerFreqTemp(i))
    return FreqList

### In the filename list, the filename are recorded from low temperature to high temperature
### and several KIDs are measured at each single temperature
### Here we can get all information for single KID with number "n", which means nth KID
def centerFreqForNth(freqlist, n):
    return freqlist[n-1::5]

FirstKID = centerFreqForNth(centerFreqList(data_name),1)
SecondKID = centerFreqForNth(centerFreqList(data_name),2)
ThirdKID = centerFreqForNth(centerFreqList(data_name),3)
FourthKID = centerFreqForNth(centerFreqList(data_name),4)
FifthKID = centerFreqForNth(centerFreqList(data_name),5)

### plot with 
def plotFreqTemp(NthKID):
    x_val = [x[0] for x in NthKID]
    y_val = [y[1] for y in NthKID]
    x_valnew = [x for x in x_val]
    y_valnew = [(y - y_val[0])/y_val[0] for y in y_val]
    plt.plot(x_valnew, y_valnew, label=y_val[0])
    
plotFreqTemp(FirstKID)
plotFreqTemp(SecondKID)
plotFreqTemp(ThirdKID)
plotFreqTemp(FourthKID)
plotFreqTemp(FifthKID)
plt.xlabel('Temperature (mK)')
plt.ylabel('Frequency Shift (MHz)')
plt.legend()
plt.show()

###
###
###
### Read data from file
result = []
with open('20160104/' + str(data_name[0]).replace("[", "").replace("]", "").replace("'", "").replace("\\r", "") + '.csv','r') as f:
    for line in f:
        result.append(map(str,line.split(',')))
        #print line

### print test for reading data successfully
print result[1][0], result[1][1], result[1][2], result[1][3]
print float(result[2][0]), float(result[2][1]), float(result[2][2]), float(result[2][3])

"""
result = []
with open('20151119_0dBm_6.796012358_0.0025_580.25mK.csv','r') as f:
    for line in f:
        result.append(map(str,line.split(',')))
        #print line
print result[1][0], result[1][1], result[1][2], len(result)
print float(result[2][0]), float(result[2][1]), float(result[2][2])
"""

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

"""
plt.plot(freq, linear)
plt.plot(freq, phase)
plt.plot(freq, real)
#plt.plot(real, imag)
plt.show()
"""
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

delete_number = 400
index = np.linspace(0, delete_number, delete_number+1)
Z_ii = np.delete(Z_ii, index)
freq = np.delete(freq, index)
index = np.linspace(len(Z_ii), len(Z_ii)-delete_number, delete_number+1)
Z_ii = np.delete(Z_ii, index)
freq = np.delete(freq, index)
print len(Z_ii), len(freq)

### Get average of start and end point position
Z_real = 0
Z_imag = 0
for i in (0,1):
    Z_real = Z_ii.real[i] + Z_ii.real[len(Z_ii)-1-i] + Z_real
    Z_imag = Z_ii.imag[i] + Z_ii.imag[len(Z_ii)-1-i] + Z_imag

Z_iic = Z_ii*np.exp(1j * (np.pi-np.arctan2(Z_real, Z_imag)))
phase_c = np.arctan2(Z_iic.imag, Z_iic.real)
#plt.plot(freq, phase_c)

plt.plot(Z_ii.real, Z_ii.imag)
plt.plot(Z_iic.real, Z_iic.imag)
plt.show()

### Fit phase
from lmfit import minimize, Parameters, Parameter, fit_report

# create data to be fitted
#x = np.linspace(0, 15, 301)
#data = (5. * np.sin(2 * x - 0.1) * np.exp(-x*x*0.025) +
#        np.random.normal(size=len(x), scale=0.2) )

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
params.add('f_r', value= 5e9, min = 3e9, max= 7e9)


# do fit, here with leastsq model
result = minimize(PhaseFit, params, args=(freq, phase_c))

# calculate final result
final = phase_c + result.residual

# write error report
report_fit(params)

# Calculate Qc and Qi
Qr = params['Q_r'].value
Qc = (np.absolute(x_c + 1j*y_c) + radius)/2/radius*Qr # Ref: Gao Thesis
Qi = Qr*Qc/(Qc-Qr)

print "theta0", params['theta0'].value
print "Qr", params['Q_r'].value
print "fr", params['f_r'].value


print(fit_report(result))

# try to plot results
try:
    import pylab
    pylab.plot(freq, phase_c, 'k+')
    pylab.plot(freq, final, 'r')
    #pylab.plot(freq, result.residual, 'b')
    pylab.show()
except:
    pass

#<end of examples/doc_basic.py>
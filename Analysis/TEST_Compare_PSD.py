from scipy import signal
import numpy as np
from matplotlib import mlab
import matplotlib.pyplot as plt

folder = '../../../MeasurementResult/'
name_of_file = 'Noise_19dBm_3868MHz_50K_1S'
result = []
with open(folder + name_of_file + '.csv','r') as f:
    for line in f:
        result.append(map(str,line.split(',')))
I = []
Q = []
for i in range(22,len(result)):
    ### read paras
    I.append(float(result[i][1]))
    Q.append(float(result[i][2].replace("\n", "")))
    

fs = 1e5
n = len(I)
#fwelch,Pwelch = signal.welch(I, fs, nperseg=len(I))
Pmlab,fmlab = mlab.psd(I, NFFT=n/10, Fs = fs, window=mlab.window_hanning,)
Pmlab1,fmlab1 = mlab.psd(I, NFFT=n/10, Fs = fs, window=mlab.window_hanning, noverlap=(n/200))
Pmlab2,fmlab2 = mlab.psd(I, NFFT=n/2, Fs = fs, window=mlab.window_hanning, noverlap=n/4)
print n, n//2, n/2
#Pmlab,fmlab = mlab.psd(I, NFFT=n, Fs = fs, window=mlab.window_hanning, noverlap=(n//2))
### welch and mlab are same except lowest frequency point
#plt.loglog(fwelch,Pwelch,label='welch')
plt.loglog(fmlab,Pmlab,label='mlab')
plt.loglog(fmlab1,Pmlab1,label='mlab1')
#plt.loglog(fmlab2,Pmlab2,label='mlab2')
plt.legend()

#plt.plot(0,0,'*')
#plt.plot(I,Q)
plt.show()
### test data correction is OK or not
### For example, use the correction parameters to correct the original calibration data
### to see the calibration data could be circled or not
import numpy as np
import matplotlib.pyplot as plt
import IQMixer.IQCalib as IQ    

folder ='IQMixer_Calib/Cryostat2/-5dBm/'

filename = 'EllipseFit_-5dBm_3000MHz_8000MHz'
RF_Power = '-5dBm'
RF_Freq_Start = 3000# MHz
RF_Freq_Interval = 10 # MHz, RF measurement sample every 10 MHz
Frequency = 3000
paras = IQ.IQ_GetPara(folder,filename,(Frequency-RF_Freq_Start)/RF_Freq_Interval)

### Get IQ measurement data
data_file = RF_Power + '_' + str(Frequency) + 'MHz.csv'
data = []
with open(folder + data_file,'r') as f:
    for line in f:
        data.append(map(str,line.split(',')))

I = [float(data[i][1]) for i in range(0,len(data))]
Q = [float(data[i][2].replace("\n", "")) for i in range(0,len(data))]

IcalG, QcalG = IQ.IQ_CorrtGao(paras,I,Q)
plt.plot(I,Q,'g')
plt.plot(IcalG,QcalG)
plt.show()

IcalB, QcalB = IQ.IQ_CorrtBarends(paras,I,Q)
plt.plot(I,Q,'g')
plt.plot(IcalB,QcalB,'r')

"""
from scipy import signal
fs = 5e4

fwelch,Pwelch = signal.welch(Icrr, fs, nperseg=len(Icrr))
plt.loglog(fwelch,Pwelch,label='Icrr')

fwelch,Pwelch = signal.welch(I, fs, nperseg=len(Icrr))
plt.loglog(fwelch,Pwelch,label='I')
plt.show()
"""
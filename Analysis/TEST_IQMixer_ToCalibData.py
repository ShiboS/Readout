import numpy as np
import csv
import matplotlib.pyplot as plt
import IQMixer.IQCalib as IQ


folder =''
filename = 'EllipseFit_-19dBm_3000MHz_3000MHz'
RF_Power = '-19dBm'
RF_Freq_Start = 3000  # MHz
RF_Freq_Interval = 10 # MHz, RF measurement sample every 10 MHz
Frequency = 3000
paras = IQ.IQ_GetPara(folder,filename,(Frequency-RF_Freq_Start)/RF_Freq_Interval)

### Get IQ measurement data
data_file = 'Noise_17dBm_3000MHz_100K_1S_1'
data = []
with open(data_file + '.csv','r') as f:
    for line in f:
        data.append(map(str,line.split(',')))
        
freq = [float(data[i][0]) for i in range(0,len(data))]
I = [float(data[i][1]) for i in range(0,len(data))]
Q = [float(data[i][2].replace("\n", "")) for i in range(0,len(data))]

Icrr, Qcrr = IQ.IQ_CorrtBarends(paras,I,Q)

plt.plot(0,0,'.')
plt.plot(I,Q,'.')
plt.plot(Icrr,Qcrr,'.')
#plt.show()

delay_time = 50e-9
for i in range(0,len(Icrr)):
    Icrr[i] = ((Icrr[i]+1j*Qcrr[i]) * IQ.cable_delay_calib(delay_time,3e9)).real
    Qcrr[i] = ((Icrr[i]+1j*Qcrr[i]) * IQ.cable_delay_calib(delay_time,3e9)).imag

### save calibrated result
folder2= ''
crrfile = open(folder2 + data_file + '_IQDelaycalibrated.csv', 'w')
fwrite = csv.writer(crrfile)

for i in range(0, len(Icrr)):
    fwrite.writerow([Icrr[i], Qcrr[i]])
crrfile.close()

plt.plot(0,0,'.')
plt.plot(Icrr,Qcrr)
plt.show()


### rotate data and save
theta = np.arctan2(np.mean(Qcrr), np.mean(Icrr))-0.17

Ishift = []
Qshift = []
for i in range(0,len(Icrr)):
    Ishift.append(((Icrr[i]+1j*Qcrr[i])*np.exp(-1j*(theta))).real)
    Qshift.append(((Icrr[i]+1j*Qcrr[i])*np.exp(-1j*(theta))).imag)


rotfile = open(folder2 + data_file + '_IQDelaycalibrated_rotated.csv', 'w')
fwrite = csv.writer(rotfile)

for i in range(0, len(Ishift)):
    fwrite.writerow([Ishift[i], Qshift[i]])
rotfile.close()

plt.plot(Ishift,Qshift)
plt.show()
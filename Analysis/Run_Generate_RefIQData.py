### Generate IQ reference data from sweep measurement data
import numpy as np
import IQMixer.IQCalib as IQ
import csv

"""
Input data folder and file created by LabVIEW (SweepMeasurement)
with center freq 5000MHz and span 6000 MHz and 6001 points
"""
folder ="../../../MeasurementResult/"
filename = 'Sweep_5000MHz'

### Get IQ measurement data
data = []
with open(folder + filename + '.csv','r') as f:
    for line in f:
        data.append(map(str,line.split(',')))

frequency = np.asarray([int(float(data[i][0])/1e6) for i in range(0,len(data))])
I = np.asarray([float(data[i][1]) for i in range(0,len(data))])
Q = np.asarray([float(data[i][2].replace("\n", "")) for i in range(0,len(data))])
print frequency[0]

### IQMixer calibration file to correct data measured with IQMixer
#   If the BOX is changed, please calibrate IQMixer again
IQCorrectionfile ='IQMixer_Calib/20160803_1M_BOX/EllipseFit_0dBm_2000MHz_8000MHz.csv'
Icrr= []
Qcrr= []
for i in range(0, len(frequency)):
    paras = IQ.IQ_GetPara(IQCorrectionfile,frequency[i])
    Itemp, Qtemp = IQ.IQ_CorrtBarendsSingle(paras, I[i], Q[i])
    Icrr.append(Itemp)
    Qcrr.append(Qtemp)


### save calibrated result
crrfile = open(folder + filename + '_IQMixerCalibrated.csv', 'w')
fwrite = csv.writer(crrfile)

for i in range(0, len(Icrr)):
    fwrite.writerow([frequency[i], Icrr[i], Qcrr[i]])
crrfile.close()
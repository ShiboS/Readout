import numpy as np
import matplotlib.pyplot as plt
import IQMixer.IQCalib as IQ
import csv
from scipy import interpolate
import FileReader as reader

folder ="../../../MeasurementResult/"
filename = 'Sweep_5000MHz_IQMixerCalibrated'
### Get IQ measurement data
data = []
with open(folder + filename + '.csv','r') as f:
    for line in f:
        data.append(map(str,line.split(',')))

frequency = np.asarray([int(data[i][0]) for i in range(0,len(data))])
I = np.asarray([float(data[i][1]) for i in range(0,len(data))])
Q = np.asarray([float(data[i][2].replace("\n", "")) for i in range(0,len(data))])

folder_sweep ="../../../MeasurementResult/"
filename_sweep = 'Sweep_3868MHz'
freq, Iraw, Qraw = reader.ReadSweep(folder_sweep, filename_sweep)

interpolate_start =  int(freq[0]/1e6)-2000-5
interpolate_end=  int(freq[len(freq)-1]/1e6)-2000+5

fI = interpolate.interp1d(frequency[interpolate_start:interpolate_end], I[interpolate_start:interpolate_end], kind='cubic')
fQ = interpolate.interp1d(frequency[interpolate_start:interpolate_end], Q[interpolate_start:interpolate_end], kind='cubic')

IQnormalized = (Iraw + 1j*Qraw)/(fI(freq/1e6)+1j*fQ(freq/1e6))

#plt.plot(frequency[interpolate_start:interpolate_end], I[interpolate_start:interpolate_end], '.')
#plt.plot(freq/1e6, fI(freq/1e6), '.')
#plt.plot(freq/1e6, Iraw, '.')
plt.plot(Iraw, Qraw)
plt.plot(IQnormalized.real, IQnormalized.imag)
plt.show()

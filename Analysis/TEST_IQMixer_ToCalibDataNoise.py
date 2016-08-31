import numpy as np
import matplotlib.pyplot as plt
import IQMixer.IQCalib as IQ
import Analyse_PSD as PSD
import FileReader as reader

IQCorrectionfile ='IQMixer_Calib/20160803_1M_BOX/EllipseFit_0dBm_2000MHz_8000MHz.csv'
folder ='../../../MeasurementResult/'
filename = 'Noise_19dBm_4000MHz_2000K_1S_2'
freq = 4000

fs, num, I, Q = reader.ReadNoise(folder, filename)
paras = IQ.IQ_GetPara(IQCorrectionfile,freq)
Icrr, Qcrr = IQ.IQ_CorrtBarends(paras,I,Q)
IQ = (Icrr+1j*Qcrr)/np.sqrt(np.mean(Qcrr)**2 + np.mean(Icrr)**2)

revisetheta = -np.arctan2(np.mean(IQ.imag), np.mean(IQ.real))
noisecompfinalrevised = IQ * np.exp(1j*revisetheta)

fx, Pxx, fy, Pyy, fxy, Pxy = PSD.Full_Spectrum(IQ.real, IQ.imag, fs)
fxr, Pxxr, fyr, Pyyr, fxyr, Pxyr = PSD.Full_Spectrum(noisecompfinalrevised.real, noisecompfinalrevised.imag, fs)

plt.plot(fx, 10*np.log10(Pxx), label='ONres  Amplitude ')
plt.plot(fy, 10*np.log10(Pyy), label='ONres  Phase')
plt.plot(fxr, 10*np.log10(Pxxr), label='Ir')
plt.plot(fyr, 10*np.log10(Pyyr), label='Qr')
plt.xscale('log')
plt.legend()
plt.show()

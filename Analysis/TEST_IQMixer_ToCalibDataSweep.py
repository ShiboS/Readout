import numpy as np
import csv
import matplotlib.pyplot as plt
import IQMixer.IQCalib as IQ
import Analyse_Fit_SingleKID as FitSingle
import Analyse_PSD as PSD
import FileReader as reader

IQCorrectionfile ='IQMixer_Calib/20160803_1M_BOX/EllipseFit_0dBm_2000MHz_8000MHz.csv'
sweepdata_folder = "../../../MeasurementResult/20160814_Al_Noguchi/"
sweepdata_file = 'Sweep_4579MHz'
freq, I, Q = reader.ReadSweep(sweepdata_folder, sweepdata_file)
paras = IQ.IQ_GetPara(IQCorrectionfile, int(round(freq[len(freq)/2]/1e6)))
I_mixercalibrated, Q_mixercalibrated = IQ.IQ_CorrtBarends(paras,I,Q)

####   CUT   ####
bandwidth = 1e6
freq, real, imag = reader.CutSweep(bandwidth, freq, I_mixercalibrated, Q_mixercalibrated)
comp = np.asarray([real[i]+imag[i]*1j for i in range(0, len(real))])

### Fit ###
tau = 45e-9
a, a_err, alpha, alpha_err, tau, tau_err, phi0, phi0_err, fr, fr_err, Qr, Qr_err, Qc, Qc_err, Qi = FitSingle.Fit_7parameterIQ1(freq, comp, tau)
fitIQ1 = a * np.exp(1j*alpha) * np.exp(-2*np.pi*1j*freq*tau) * (1 - (Qr/Qc*np.exp(1j*phi0))/(1 + 2*1j*Qr*(freq-fr)/fr))
comptilt = comp * np.exp(2*np.pi*1j*freq*tau)
plt.axis('equal')
plt.plot(I_mixercalibrated,Q_mixercalibrated,'b')
plt.plot(fitIQ1.real, fitIQ1.imag, '.r')
plt.show()
print fr

para_guess = a,alpha,0,phi0,fr,Qr,Qc
a, a_err, alpha, alpha_err, tau0, tau0_err, phi0, phi0_err, fr, fr_err, Qr, Qr_err, Qc, Qc_err, x_c, x_c_err, y_c, y_c_err, radius, radius_err = FitSingle.Fit_7parameterIQ2(freq, comptilt, para_guess)
fitIQ2 = a * np.exp(1j*alpha) * np.exp(-2*np.pi*1j*freq*tau0) * (1 - (Qr/Qc*np.exp(1j*phi0))/(1 + 2*1j*Qr*(freq-fr)/fr))
plt.axis('equal')
plt.plot(fitIQ2.real, fitIQ2.imag, '.r')
plt.plot(comptilt.real, comptilt.imag)
plt.show()
print fr

comptiltmove = comptilt-(x_c+1j*y_c)
idx = FitSingle.find_nearest(freq, fr)
print freq[idx]
theta = np.arctan2(comptiltmove[idx].imag, comptiltmove[idx].real)
compfinal = comptiltmove * np.exp(-1j*theta) /radius

"""
rotfile = open(data_folder + data_file + '_IQDelaycalibrated_rotated.csv', 'w')
fwrite = csv.writer(rotfile)

for i in range(0, len(compfinal)):
    fwrite.writerow([compfinal[i].real, compfinal[i].imag])
rotfile.close()
"""

##### Noise #####
### On resonance noise
noise_folder = "../../../MeasurementResult/20160613_NbRRR48_Noise/"
noise_file = 'Noise_19dBm_4993MHz_2000K_1S'
noisefr = fr
fs, num, noiseI, noiseQ = reader.ReadNoise(noise_folder, noise_file)

noiseIcrr, noiseQcrr = IQ.IQ_CorrtBarends(paras,noiseI,noiseQ)
noisecomp = np.asarray([noiseIcrr[i]+noiseQcrr[i]*1j for i in range(0, len(noiseIcrr))])
noisecomptilt = noisecomp * np.exp(2*np.pi*1j*noisefr*tau)
noisecomptiltmove = noisecomptilt-(x_c+1j*y_c)
noisecompfinal = noisecomptiltmove * np.exp(-1j*theta) /radius

#revisetheta = np.arctan2(np.max(noisecompfinal.real)-np.mean(noisecompfinal.real), np.max(noisecompfinal.imag)-np.mean(noisecompfinal.imag))
revisetheta = -np.arctan2(np.mean(noisecompfinal.imag), np.mean(noisecompfinal.real))
noisecompfinalrevised = noisecompfinal * np.exp(1j*revisetheta)

### Off resonance noise
offnoise_file = 'Noise_19dBm_4995MHz_2000K_1S'
offFreq = 4995
offparas = IQ.IQ_GetPara(IQCorrectionfile,offFreq)
offnoisefr = offFreq*1e6
offfs, offnum, offnoiseI, offnoiseQ = reader.ReadNoise(noise_folder, offnoise_file)

offnoiseIcrr, offnoiseQcrr = IQ.IQ_CorrtBarends(offparas,offnoiseI,offnoiseQ)
offnoisecomp = np.asarray([offnoiseIcrr[i]+offnoiseQcrr[i]*1j for i in range(0, len(offnoiseIcrr))])
offnoisecomptilt = offnoisecomp * np.exp(2*np.pi*1j*offnoisefr*tau)
offnoisecomptiltmove = offnoisecomptilt-(x_c+1j*y_c)
offnoisecompfinal = offnoisecomptiltmove * np.exp(-1j*theta) /radius

### PLOT sweep and noise
plt.figure(1)
plt.axis('equal')
plt.plot(I, Q) # raw data
#plt.plot(comp.real, comp.imag, '.') # mixer calibrated
#plt.plot(comptilt.real, comptilt.imag, 'r') # remove cable delay
#plt.plot(comptiltmove.real, comptiltmove.imag, 'r') # move to center (0,0)
#plt.plot(compfinal.real, compfinal.imag, '-r') # shift frequency point to x-axis
plt.plot(noiseI, noiseQ, '.') # raw data
#plt.plot(noisecomp.real, noisecomp.imag,'.') # mixer calibrated
#plt.plot(noisecomptilt.real, noisecomptilt.imag, 'r.') # remove cable delay
#plt.plot(noisecomptiltmove.real, noisecomptiltmove.imag, 'r.') # move to center (0,0)
#plt.plot(noisecompfinal.real, noisecompfinal.imag, '.r') # shift frequency point to x-axis
#plt.plot(noisecompfinalrevised.real, noisecompfinalrevised.imag, '.b') # make noise prependicular to axis
plt.plot(offnoiseI, offnoiseQ, '.') # raw data
#plt.plot(offnoisecomp.real, offnoisecomp.imag,'.') # mixer calibrated
#plt.plot(offnoisecomptilt.real, offnoisecomptilt.imag, 'r.') # remove cable delay
#plt.plot(offnoisecomptiltmove.real, offnoisecomptiltmove.imag, 'r.') # move to center (0,0)
#plt.plot(offnoisecompfinal.real, offnoisecompfinal.imag, '.r') # shift frequency point to x-axis

plt.show()

### PSD
fx, Pxx, fy, Pyy, fxy, Pxy = PSD.Full_Spectrum(noisecompfinal.real, noisecompfinal.imag, fs)
fxr, Pxxr, fyr, Pyyr, fxyr, Pxyr = PSD.Full_Spectrum(noisecompfinalrevised.real, noisecompfinalrevised.imag, fs)
fxp, Pxxp, fyp, Pyyp = PSD.Full_SpectrumPwelch(noisecompfinal.real, noisecompfinal.imag, fs)
fxf, Pxxf, fyf, Pyyf = PSD.Full_SpectrumPwelch(offnoisecompfinal.real, offnoisecompfinal.imag, fs)
plt.figure(2)
plt.plot(fx, 10*np.log10(Pxx), label='ONres  Amplitude ')
plt.plot(fy, 10*np.log10(Pyy), label='ONres  Phase')
plt.plot(fxf, 10*np.log10(Pxxf), label='OFFres Amplitude')
plt.plot(fyf, 10*np.log10(Pyyf), label='OFFres Phase')
#plt.plot(fxr, 10*np.log10(Pxxr), label='Ir')
#plt.plot(fyr, 10*np.log10(Pyyr), label='Qr')
#plt.plot(fxy,10*np.log10(Pxy), label='IQ')
plt.xscale('log')
plt.xlim([2*len(num)/fs,fs/2])
plt.ylim([-120,-50])

plt.xlabel('Frequency (Hz)')
plt.ylabel('Noise Spectral Density (dBc/Hz)')
plt.legend()
leg = plt.gca().get_legend()
ltext  = leg.get_texts() 
plt.setp(ltext, fontsize='small')
plt.show()
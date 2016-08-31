import numpy as np
import Analyse_Fit_SingleKID as FitSingle
import FileReader as reader
import IQMixer.IQCalib as IQ
import matplotlib.pyplot as plt
import Analyse_PSD as PSD

### IQ Mixer calibration file
IQCalibrationfile ='IQMixer_Calib/20160803_1M_BOX/EllipseFit_0dBm_2000MHz_8000MHz.csv'
### IQ Reference data (already IQ Mixer calibrated) folder and filename
### IQ Reference data is measured with T>Tc/2
IQReffolder ="../../../MeasurementResult/"
IQReffilename = 'Sweep_5000MHz_IQMixerCalibrated'

### IQ Sweep data from LabVIEW folder and filename
###
###
data_folder = "../../../MeasurementResult/20160814_Al_Noguchi/"
###
###
###
sweeplist_file = 'sweeplist'
sweeplist = []
with open(data_folder + sweeplist_file + '.txt','r') as f:
    for line in f:
        sweeplist.append(line.replace("\n", ""))

resfreqlist_file = 'resfreqlist'
resfreqlist = []
with open(data_folder + resfreqlist_file + '.txt','r') as f:
    for line in f:
        resfreqlist.append(line.replace("\n", ""))

noiselist_file = 'noiselist'
noiselist = []
with open(data_folder + noiselist_file + '.txt','r') as f:
    for line in f:
        noiselist.append(line.replace("\n", ""))

num = len(sweeplist)
plt.figure(figsize=(18.5, 10.5))
for n in range(0, num):
    ### Get file name and resonance frequency
    sweepdata_file = sweeplist[n]
    noisedata_file = noiselist[n]
    resfreq = float(resfreqlist[n])
    
    #   Read data
    sweepfreq, sweepI, sweepQ = reader.ReadSweep(data_folder, sweepdata_file)
    fsample, number, noiseI, noiseQ = reader.ReadNoise(data_folder, noisedata_file)
    meastime = len(number)/float(fsample)
    
    #   Get IQ Mixer calibration parameter
    resfreqinMHz = int(round(sweepfreq[len(sweepfreq)/2]/1e6))
    paras = IQ.IQ_GetPara(IQCalibrationfile, resfreqinMHz)
    
    #   Calibrate IQ data
    I_mixercalibrated, Q_mixercalibrated = IQ.IQ_CorrtBarends(paras, sweepI, sweepQ)
    noiseI_mixercalibrated, noiseQ_mixercalibrated = IQ.IQ_CorrtBarends(paras, noiseI, noiseQ)
    
    #   Normalize calibrated IQ Sweep data to IQ reference data
    #   Get complex IQ
    sweepIQ_normalized = IQ.IQ_Normalize_Sweep(sweepfreq, I_mixercalibrated, Q_mixercalibrated, IQReffolder, IQReffilename)
    noiseIQ_normalized = IQ.IQ_Normalize_Noise(resfreq, noiseI_mixercalibrated, noiseQ_mixercalibrated, IQReffolder, IQReffilename)
    
    #   Fit circle and phase
    x_c, x_c_err, y_c, y_c_err, radius, radius_err, circle_fit_report, theta0, theta0_err, fr, fr_err, Qr, Qr_err, Qc, Qc_err, Qi, Qi_err, fit_report_phase = FitSingle.Fit_IQ_Sweep(sweepfreq, sweepIQ_normalized)
    
    #   Move sweep center to origin
    sweepIQcenter = sweepIQ_normalized - (x_c + 1j*y_c)
    noiseIQcenter = noiseIQ_normalized - (x_c + 1j*y_c)
    
    #   Find cloest data point to fitted resonance frequency and calculate angle
    idx = FitSingle.find_nearest(sweepfreq, fr)
    theta = np.arctan2(sweepIQcenter[idx].imag, sweepIQcenter[idx].real)
    
    #   Tilt sweep circle to make sure resonance frequency point is (1, 0)
    #   and also scale radius to one
    sweepIQfinal = sweepIQcenter * np.exp(-1j*theta) /radius    
    noiseIQfinal = noiseIQcenter * np.exp(-1j*theta) /radius
    
    plt.subplot(2, num, n+1)
    plt.plot(sweepIQfinal.real, sweepIQfinal.imag)
    plt.plot(noiseIQfinal[::100].real, noiseIQfinal[::100].imag, '.')
    plt.xlim([-1,2])
    plt.ylim([-1,1])
    plt.xlabel('I')
    plt.ylabel('Q')
    plt.title('KID:' + str(resfreqinMHz) + 'MHz   ' + str(fsample/1e6) + 'MHz   ' + str(meastime) + 's')
    
    plt.subplot(2, num, n+1+num)
    fx, Pxx, fy, Pyy, fxy, Pxy = PSD.Full_Spectrum(noiseIQfinal.real, noiseIQfinal.imag, fsample)
    plt.plot(fx, 10*np.log10(Pxx), label='ONres  Amplitude ')
    plt.plot(fy, 10*np.log10(Pyy), label='ONres  Phase')
    plt.xscale('log')
    plt.xlim([1/meastime, fsample/2])
    plt.ylim([-100,-0])
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('PSD (dBc)')
    plt.title(str(1.0/meastime) + '-100Hz: ' + str(1.0/meastime) + 'Hz    100-1kHz: ' + str(10.0/meastime) + 'Hz    1k-' + str(fsample/1e6) + 'MHz: ' + str(100.0/meastime) + 'Hz')
plt.show()
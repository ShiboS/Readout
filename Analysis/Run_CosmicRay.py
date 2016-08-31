import Fitter
import matplotlib.pyplot as plt
import IQMixer.IQCalib as IQ
import numpy as np
import FileReader as reader
from matplotlib.backends.backend_pdf import PdfPages

IQCorrectionfile ='IQMixer_Calib/20160803_1M_BOX/EllipseFit_0dBm_2000MHz_8000MHz.csv'

"""
Edit folder and file name and measurement frequency in nnnn MHz
"""
cosraydata_folder = "../../../MeasurementResult/20160814_Al_Noguchi/CosmicRay/4579/"
freq = 4579
cosraydata_file = '2000K_0.5S_9624'

###   Calibrate IQ data and calculate amplitude of IQ (IQ)
fs, num, I, Q = reader.ReadCosmicRay(cosraydata_folder, cosraydata_file)
paras = IQ.IQ_GetPara(IQCorrectionfile, freq)
I_mixercalibrated, Q_mixercalibrated = IQ.IQ_CorrtBarends(paras,I,Q)
IQ = np.sqrt((I_mixercalibrated-np.mean(I_mixercalibrated))**2 + (Q_mixercalibrated-np.mean(Q_mixercalibrated))**2)

###   Get index of maximum point and 
###   cut measurement data 500 points left from the peak and
###   2500 points right from the peak
numleft = 500
numright = 2500
index = IQ.argmax()
Ievent = I_mixercalibrated[index-numleft:index+numright]
Qevent = Q_mixercalibrated[index-numleft:index+numright]
amplitude = np.asarray(IQ[index-numleft:index+numright])
phase = np.arctan2(Qevent, Ievent)

###   Transfer number to time with microsecond unit 
t = num[index-numleft:index+numright] / fs * 1e6
a, a_err, A, A_err, t0, t0_err, tau, tau_err, taur, taur_err, fit_report, residual = Fitter.Fit_CosmicRay(t, amplitude)
fitresult = Fitter.Fit_CosmicRay_model(t, t0, a, A, tau, taur)

###   Plot data and fitting result and residual
font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 10,
        }

with PdfPages(cosraydata_folder + cosraydata_file + '.pdf') as pdf:
    plt.figure(figsize=(18.5, 10.5))

    plt.subplot(2, 1, 1)
    plt.plot(t, fitresult,'.r')
    plt.plot(t, amplitude,',')
    plt.xlabel('time (us)')
    plt.ylabel('Amplitude')
    #plt.text(t[len(t)*3/4], np.amin(fitresult), r'$A(e^{-\frac{t-t_0}{\tau}} - e^{-\frac{t-t_0}{\tau_r}})+a$', fontdict=font)
    #plt.text(322000, 0.01, 'a' + str(a) +'err' + str(a_err*100) + '%', fontdict=font)
    plt.text(t[len(t)/2], np.amin(fitresult)*2, fit_report, fontdict=font)
    
    plt.subplot(2, 1, 2)
    plt.plot(t, residual,'.')
    plt.xlabel('time (us)')
    plt.ylabel('Residual')
    plt.show()
            
    #plt.title('Page One')
    pdf.savefig()  # saves the current figure into a pdf page
    plt.close()
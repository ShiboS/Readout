from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab


def DifResPwelch(data, fs):
    f1, P1 = signal.welch(data, fs, nperseg=len(data))
    f2, P2 = signal.welch(data, fs, nperseg=len(data)/10)
    f3, P3 = signal.welch(data, fs, nperseg=len(data)/100)
    return f1, P1, f2, P2, f3, P3
    
def DifResMlabPsd(data, fs):
    P1, f1 = mlab.psd(data, len(data), Fs=fs, window=mlab.window_hanning, noverlap=(len(data) // 2))
    P2, f2 = mlab.psd(data, len(data)/10, Fs=fs, window=mlab.window_hanning, noverlap=(len(data)/10 // 2))
    P3, f3 = mlab.psd(data, len(data)/100, Fs=fs, window=mlab.window_hanning, noverlap=(len(data)/100 // 2))
    return f1, P1, f2, P2, f3, P3

def DifResMlabCsd(data1, data2, fs):
    P1, f1 = mlab.csd(data1, data2, len(data1), Fs=fs, window=mlab.window_hanning)
    P2, f2 = mlab.csd(data1, data2, len(data1)/10, Fs=fs, window=mlab.window_hanning)
    P3, f3 = mlab.csd(data1, data2, len(data1)/100, Fs=fs, window=mlab.window_hanning)
    return f1, P1, f2, P2, f3, P3

def Combine_psd(f1, P1, f2, P2, f3, P3, fs):
    f = []
    P = []
    
    index = np.where(np.logical_and(f1>=0,f1<100))
    farray = f1[index]
    Parray = P1[index]
    for i in range(0, len(farray)):
        f.append(farray[i])
        P.append(Parray[i])

    index = np.where(np.logical_and(f2>=100,f2<1000))
    farray = f2[index]
    Parray = P2[index]
    for i in range(0, len(farray)):
        f.append(farray[i])
        P.append(Parray[i])
    
    index = np.where(np.logical_and(f3>=1000,f3<=fs))
    farray = f3[index]
    Parray = P3[index]
    for i in range(0, len(farray)):
        f.append(farray[i])
        P.append(Parray[i])
        
    return f,P

def Full_Spectrum(I, Q, fs):
    f1, P1, f2, P2, f3, P3 = DifResMlabPsd(I, fs)
    fx,Pxx=Combine_psd(f1, P1, f2, P2, f3, P3, fs)
    f1, P1, f2, P2, f3, P3 = DifResMlabPsd(Q, fs)
    fy,Pyy=Combine_psd(f1, P1, f2, P2, f3, P3, fs)
    f1, P1, f2, P2, f3, P3 = DifResMlabCsd(I, Q, fs)
    fxy,Pxy=Combine_psd(f1, P1, f2, P2, f3, P3, fs)
    
    return fx, Pxx, fy, Pyy, fxy, Pxy
    
def Full_SpectrumPwelch(I, Q, fs):
    f1, P1, f2, P2, f3, P3 = DifResPwelch(I, fs)
    fx,Pxx=Combine_psd(f1, P1, f2, P2, f3, P3, fs)
    f1, P1, f2, P2, f3, P3 = DifResPwelch(Q, fs)
    fy,Pyy=Combine_psd(f1, P1, f2, P2, f3, P3, fs)
    
    return fx, Pxx, fy, Pyy
    
def test_fullspec():
    folder = ''
    name_of_file = 'Noise_17dBm_3000MHz_100K_1S_BEFORE_IQDelaycalibrated_rotated'
    result = []
    with open(folder + name_of_file + '.csv','r') as f:
        for line in f:
            result.append(map(str,line.split(',')))
    I = []
    Q = []
    for i in range(0,len(result)):
        ### read paras
        I.append(float(result[i][0]))
        Q.append(float(result[i][1].replace("\n", "")))


    name_of_file2 = 'Noise_17dBm_3000MHz_100K_1S_1_IQDelaycalibrated_rotated'
    result2 = []
    with open(folder + name_of_file2 + '.csv','r') as f:
        for line in f:
            result2.append(map(str,line.split(',')))
    I2 = []
    Q2 = []
    for i in range(0,len(result2)):
        ### read paras
        I2.append(float(result2[i][0]))
        Q2.append(float(result2[i][1].replace("\n", "")))

    fs = 1e5
    fx, Pxx, fy, Pyy, fxy, Pxy = Full_Spectrum(I, Q, fs)

    plt.loglog(fx, Pxx, label='I')
    plt.loglog(fy, Pyy, label='Q')
    #plt.loglog(fxy,Pxy, label='IQ')

    plt.legend()
    leg = plt.gca().get_legend()
    ltext  = leg.get_texts() 
    plt.setp(ltext, fontsize='small')
    plt.show()

    #P1, f1 = mlab.csd(I,Q, NFFT=len(I), Fs = fs)
    #plt.loglog(f1,P1,'.')
    plt.show()
    
#test_fullspec()
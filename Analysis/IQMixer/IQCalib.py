import numpy as np
from scipy import interpolate

def IQ_GetPara(path_to_file, frequency):
    ### Read IQ mixer calibration parameters from ellipse fitting
    result = []
    with open(path_to_file,'r') as f:
        for line in f:
            result.append(map(str,line.split(',')))

    f_list = [int(result[i][0]) for i in range(1,len(result))]
    x_c = [float(result[i][1]) for i in range(1,len(result))]
    y_c = [float(result[i][3]) for i in range(1,len(result))]
    A_I = [float(result[i][11]) for i in range(1,len(result))]
    A_Q = [float(result[i][12]) for i in range(1,len(result))]
    gamma = [float(result[i][15].replace("\n", "")) for i in range(1,len(result))]
    freq = (frequency-f_list[0])/(f_list[1]-f_list[0])

    return x_c[freq], y_c[freq], A_I[freq], A_Q[freq], gamma[freq]

def IQ_CorrtGao(paras,I,Q):
    ### Calibrate IQ measurement data
    ### read parameters
    x_c = paras[0]
    y_c = paras[1]
    A_I = paras[2]
    A_Q = paras[3]
    gamma = paras[4]
    g = []
    theta = []
    r = []
    datalength = len(I)
    ### move IQ data center to center (0,0)
    Imoved = [I[i]-x_c for i in range(0,datalength)]
    Qmoved = [Q[i]-y_c for i in range(0,datalength)]
    for i in range(0,datalength):
        g.append((A_I*Qmoved[i])/(A_Q*Imoved[i]))
        if I>0:
            theta.append(np.arctan2((np.cos(gamma)-g[i]),np.sin(gamma)))
        else:
            theta.append(np.arctan2((np.cos(gamma)-g[i]),np.sin(gamma)) + np.pi)
        
        if np.cos(theta[i])!=0:
            r.append(Imoved[i]/(A_I*np.cos(theta[i])))
        else:
            r.append(Qmoved[i]/(A_Q*np.cos(theta[i]+gamma)))
            
    Ical = [r[i]*np.cos(theta[i]) for i in range(0,datalength)]
    Qcal = [r[i]*np.sin(theta[i]) for i in range(0,datalength)]
    return Ical, Qcal

def IQ_CorrtBarends(paras,I,Q):
    ### Calibrate IQ measurement data
    ### read parameters
    x_c = paras[0]
    y_c = paras[1]
    A_I = paras[2]
    A_Q = paras[3]
    gamma = paras[4]+np.pi/2.
    datalength = len(I)
    
    ### move IQ data center to center (0,0)
    Imoved = [I[i]-x_c for i in range(0,datalength)]
    Qmoved = [Q[i]-y_c for i in range(0,datalength)]
    QA = [Qmoved[i]*A_I/A_Q for i in range(0,datalength)]
    theta = [np.arctan2(QA[i]-Imoved[i]*np.sin(gamma), Imoved[i]*np.cos(gamma))  for i in range(0,datalength)]
    rroot = [np.sqrt((Imoved[i]**2 + QA[i]**2)/(np.cos(theta[i])**2 + np.sin(theta[i]+gamma)**2)) for i in range(0,datalength)]
    Ical = np.asarray([rroot[i]*np.cos(theta[i]) for i in range(0,datalength)])
    Qcal = np.asarray([rroot[i]*np.sin(theta[i]) for i in range(0,datalength)])
    return Ical, Qcal
    
def IQ_CorrtBarendsSingle(paras,I,Q):
    ### Calibrate IQ measurement data
    ### read parameters
    x_c = paras[0]
    y_c = paras[1]
    A_I = paras[2]
    A_Q = paras[3]
    gamma = paras[4]+np.pi/2.
    
    ### move IQ data center to center (0,0)
    Imoved = I-x_c
    Qmoved = Q-y_c
    QA = Qmoved*A_I/A_Q
    theta = np.arctan2(QA-Imoved*np.sin(gamma), Imoved*np.cos(gamma))
    rroot = np.sqrt((Imoved**2 + QA**2)/(np.cos(theta)**2 + np.sin(theta+gamma)**2))
    Ical = rroot*np.cos(theta)
    Qcal = rroot*np.sin(theta)
    return Ical, Qcal
    
def IQ_Normalize_Sweep(Sweepfreq, Iraw, Qraw, IQReffolder, IQReffilename):
    """
    Normalize IQ sweep data to T>Tc/2 IQ data (IQRef data)
    """
    ### Read IQRef data
    data = []
    with open(IQReffolder + IQReffilename + '.csv','r') as f:
        for line in f:
            data.append(map(str,line.split(',')))

    frequency = np.asarray([int(data[i][0]) for i in range(0, len(data))])
    IRef = np.asarray([float(data[i][1]) for i in range(0, len(data))])
    QRef = np.asarray([float(data[i][2].replace("\n", "")) for i in range(0, len(data))])
    ### select interpolate data range
    ### +/- 5 points (5 MHz) of sweep frequency
    interpolate_start =  int(Sweepfreq[0]/1e6)-2000-5
    interpolate_end=  int(Sweepfreq[len(Sweepfreq)-1]/1e6)-2000+5
    ### interpolate function ('cubic')
    fI = interpolate.interp1d(frequency[interpolate_start:interpolate_end], IRef[interpolate_start:interpolate_end], kind='cubic')
    fQ = interpolate.interp1d(frequency[interpolate_start:interpolate_end], QRef[interpolate_start:interpolate_end], kind='cubic')
    ### normalize IQ sweep data to IQRef data
    IQnormalized = (Iraw + 1j*Qraw)/(fI(Sweepfreq/1e6)+1j*fQ(Sweepfreq/1e6))
    return IQnormalized
    
def IQ_Normalize_Noise(Noisefreq, Iraw, Qraw, IQReffolder, IQReffilename):
    """
    Normalize IQ sweep data to T>Tc/2 IQ data (IQRef data)
    """
    ### Read IQRef data
    data = []
    with open(IQReffolder + IQReffilename + '.csv','r') as f:
        for line in f:
            data.append(map(str,line.split(',')))

    frequency = np.asarray([int(data[i][0]) for i in range(0, len(data))])
    IRef = np.asarray([float(data[i][1]) for i in range(0, len(data))])
    QRef = np.asarray([float(data[i][2].replace("\n", "")) for i in range(0, len(data))])
    ### select interpolate data range
    ### +/- 5 points (5 MHz) of sweep frequency
    interpolate_start =  int(Noisefreq)-2000-5
    interpolate_end=  int(Noisefreq)-2000+5
    ### interpolate function ('cubic')
    fI = interpolate.interp1d(frequency[interpolate_start:interpolate_end], IRef[interpolate_start:interpolate_end], kind='cubic')
    fQ = interpolate.interp1d(frequency[interpolate_start:interpolate_end], QRef[interpolate_start:interpolate_end], kind='cubic')
    ### normalize IQ sweep data to IQRef data
    IQnormalized = (Iraw + 1j*Qraw)/(fI(Noisefreq) + 1j*fQ(Noisefreq))
    return IQnormalized

def cable_delay_calib(time_delay, frequency):
    ### Gao Thesis Appendix E Eqn E.1
    return np.exp(2*np.pi*1j*time_delay*frequency)
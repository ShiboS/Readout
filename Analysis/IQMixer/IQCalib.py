import numpy as np

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
    Ical = [rroot[i]*np.cos(theta[i]) for i in range(0,datalength)]
    Qcal = [rroot[i]*np.sin(theta[i]) for i in range(0,datalength)]
    return Ical, Qcal
    
def cable_delay_calib(time_delay, frequency):
    ### Gao Thesis Appendix E Eqn E.1
    return np.exp(2*np.pi*1j*time_delay*frequency)
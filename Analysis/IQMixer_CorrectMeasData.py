import numpy as np
import matplotlib.pyplot as plt

def IQ_GetPara(folder, filename, freq):
    ### Read IQ mixer calibration parameters from ellipse fitting
    name_of_file = filename + '.csv'
    result = []
    with open(folder + name_of_file,'r') as f:
        for line in f:
            result.append(map(str,line.split(',')))
    f_list = []
    x_c = []
    y_c = []
    A_I = []
    A_Q = []
    gamma = []
    for i in range(1,len(result)):
        ### read paras
        f_list.append(float(result[i][0]))
        x_c.append(float(result[i][1]))
        y_c.append(float(result[i][3]))
        A_I.append(float(result[i][11]))
        A_Q.append(float(result[i][12]))
        gamma.append(float(result[i][15].replace("\n", "")))
    return x_c[freq], y_c[freq], A_I[freq], A_Q[freq], gamma[freq]

def IQ_Corrt(paras,I,Q):
    ### Calibrate IQ measurement data
    A_I = paras[2]
    A_Q = paras[3]
    gamma = paras[4]
    g = []
    theta = []
    r = []
    for i in range(0,len(I)):
        g.append((A_I*Q[i])/(A_Q*I[i]))
        if I>0:
            theta.append(np.arctan2((np.cos(gamma)-g[i]),np.sin(gamma)))
        else:
            theta.append(np.arctan2((np.cos(gamma)-g[i]),np.sin(gamma)) + np.pi)
        
        if np.cos(theta[i])!=0:
            r.append(I[i]/(A_I*np.cos(theta[i])))
        else:
            r.append(Q[i]/(A_Q*np.cos(theta[i]+gamma)))
    return g,theta,r
    

folder ='IQMixer_Calib/Cryostat2/-5dBm/'

filename = 'EllipseFit_-5dBm_3000MHz_8000MHz'
RF_Power = '-5dBm'
RF_Freq_Start = 3000# MHz
RF_Freq_Interval = 10 # MHz, RF measurement sample every 10 MHz
Frequency = 5000
paras = IQ_GetPara(folder,filename,(Frequency-RF_Freq_Start)/RF_Freq_Interval)
x_c = paras[0]
y_c = paras[1]

### Get IQ measurement data
data_file = 'IQMixer_Calib/sss.csv'
data = []
with open(data_file,'r') as f:
    for line in f:
        data.append(map(str,line.split(',')))
I = []
Q = []
Icrr = []
Qcrr = []
for i in range(0,len(data)):
    ### move IQ data to center (0,0)
    I.append(float(data[i][1])-x_c)
    Q.append(float(data[i][2].replace("\n", ""))-y_c)

### get calibration parameters
g,theta,r = IQ_Corrt(paras,I,Q)

for i in range(0,len(I)):
    ### get calibrated IQ data
    Icrr.append((r[i])*np.cos(theta[i]))
    Qcrr.append((r[i])*np.sin(theta[i]))

plt.plot(Icrr,Qcrr)
plt.show()
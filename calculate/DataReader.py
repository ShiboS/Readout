import numpy as np

def ReadSingle(folder, filename):
    data = []
    with open(folder + filename,'r') as f:
        for line in f:
            data.append(map(str,line.split(',')))
    n = len(data)
    power = np.asarray([float(data[i][0]) for i in range(1,n)])
    temp = np.asarray([float(data[i][1]) for i in range(1,n)])
    frmin = np.asarray([float(data[i][2]) for i in range(1,n)])
    frfit = np.asarray([float(data[i][3]) for i in range(1,n)])
    frfit_err = np.asarray([float(data[i][4]) for i in range(1,n)])
    Qr = np.asarray([float(data[i][5]) for i in range(1,n)])
    Qr_err = np.asarray([float(data[i][6]) for i in range(1,n)])
    Qc = np.asarray([float(data[i][7]) for i in range(1,n)])
    Qc_err = np.asarray([float(data[i][8]) for i in range(1,n)])
    Qi = np.asarray([float(data[i][9]) for i in range(1,n)])
    Qi_err = np.asarray([float(data[i][10]) for i in range(1,n)])
    
    return power, temp, frmin, frfit, frfit_err, Qr, Qr_err, Qc, Qc_err, Qi, Qi_err
    
#folder = "../../../MeasurementResult/20160516_Nb154nmCry3/"
#filename = "20160516_Nb154nmCry3_3.8675664_-50dBm.csv"
#data = ReadSingle(folder, filename)


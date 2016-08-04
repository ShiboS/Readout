import numpy as np

def ReadSweep(folder, filename):
    data = []
    with open(folder + filename + '.csv','r') as f:
        for line in f:
            data.append(map(str,line.split(',')))
        
    freq = np.asarray([float(data[i][0]) for i in range(0,len(data))])
    I = np.asarray([float(data[i][1]) for i in range(0,len(data))])
    Q = np.asarray([float(data[i][2].replace("\n", "")) for i in range(0,len(data))])
    
    return freq, I, Q
    
def ReadNoise(folder, filename):
    noisedata = []
    with open(folder + filename + '.csv','r') as f:
        for line in f:
            noisedata.append(map(str,line.split(',')))
    noiselength = len(noisedata)
    fs = int(noisedata[14][1])
    num = np.asarray([float(noisedata[i][0]) for i in range(22,noiselength)])
    noiseI = np.asarray([float(noisedata[i][1]) for i in range(22,noiselength)])
    noiseQ = np.asarray([float(noisedata[i][2].replace("\n", "")) for i in range(22, noiselength)])
    
    return fs, num, noiseI, noiseQ
    
def CutSweep(bandwidth, freq, I, Q):
    n = len(freq)
    span = freq[n-1]-freq[0]
    interval = span/(n-1)
    cut_num = n-1-int(bandwidth/interval) # 1.4MHz span
    if cut_num<0: cut_num = 0
    print "cut_num", cut_num, "n", n
    freq = np.asarray([freq[i] for i in range(cut_num/2, n-cut_num/2)])
    Icut = np.asarray([I[i] for i in range(cut_num/2, n-cut_num/2)])
    Qcut = np.asarray([Q[i] for i in range(cut_num/2, n-cut_num/2)])
    return freq, Icut, Qcut
import Analyse_Fit_SingleKID
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

def Get_S21mag_SingleKID(folder, filename):
    ### Read data from file
    result = []

    with open(folder + filename,'r') as f:
        for line in f:
            result.append(map(str,line.split(',')))

    ### print test for reading data successfully
    ### print result[1][0], result[1][1], result[1][2]
    ### print float(result[2][0]), float(result[2][1]), float(result[2][2])

    ### Initial fit frequency
    MeasState = Analyse_Fit_SingleKID.centerFreqTempPower(filename.replace(".csv",""))

    freq = []
    linear = []
    phase = []
    real = []
    imag = []
    mag = []

    for i in range(0,len(result)-2):
        freq.append(float(result[i+2][0]))
        linear.append(float(result[i+2][1]))
        phase.append(float(result[i+2][2]))
        real.append(linear[i] * np.cos(np.deg2rad(phase[i])))
        imag.append(linear[i] * np.sin(np.deg2rad(phase[i])))
        mag.append(float(result[i+2][3]))
    return freq, mag, MeasState[0], MeasState[1]

### Read filename list
data_name = []
folder = "../../../MeasurementResult/20160606_Nb152nmCryA2low/"
readpower = '-30dBm'
name_of_list = '20160606_' + readpower + '_list.csv'
#name_of_list = '20160322' + '_list.csv'
global Num_of_KID
Num_of_KID = 4

with open(folder + name_of_list,'r') as n:
    for line in n:
        data_name.append(map(str,line.rstrip('\n').split(','))) # Remove '\n'

magS21all = []
for filename in data_name:
    #print filename
    filename = str(filename).replace("[", "").replace("]", "").replace("'", "").replace("\\r", "")+".csv"
    magS21all.append(Get_S21mag_SingleKID(folder, filename))


def slicing(freqlist, n):
    return freqlist[n-1::Num_of_KID]
    

a = slicing(magS21all,1)
b = slicing(magS21all,2)
c = slicing(magS21all,3)
d = slicing(magS21all,4)
"""
e = slicing(magS21all,5)
f = slicing(magS21all,6)

g = slicing(magS21all,7)
h = slicing(magS21all,8)

i = slicing(magS21all,9)
j = slicing(magS21all,10)

k = slicing(magS21all,11)
l = slicing(magS21all,12)
"""
def Plot_TempDepS21(data, folder, power):
    name_of_file = folder.replace("/", "") + "_" + str(data[0][3]) + "_" + power
    with PdfPages(folder + name_of_file + '.pdf') as pdf:
        plt.figure(figsize=(10, 10))
        for i in range(0,len(data)):
            plt.plot(data[i][0], data[i][1])
            #plt.legend(str(data[i][2]))
        
        #plt.title('Page One')
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()


Plot_TempDepS21(a, folder, readpower)
Plot_TempDepS21(b, folder, readpower)
Plot_TempDepS21(c, folder, readpower)
Plot_TempDepS21(d, folder, readpower)
"""
Plot_TempDepS21(e, folder, readpower)
Plot_TempDepS21(f, folder, readpower)

Plot_TempDepS21(g, folder, readpower)
Plot_TempDepS21(h, folder, readpower)
Plot_TempDepS21(i, folder, readpower)
Plot_TempDepS21(j, folder, readpower)

Plot_TempDepS21(k, folder, readpower)
Plot_TempDepS21(l, folder, readpower)
"""

"""
f = open(folder + name_of_file + '.csv', 'w')
result = []
"""
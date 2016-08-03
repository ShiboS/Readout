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

def slicing(freqlist, n, Num_of_KIDs):
    return freqlist[n-1::Num_of_KIDs]

def Plot_TempDepS21(data, folder, power):
    name_of_file = folder.replace("../../../MeasurementResult/","").replace("/", "") + "_" + str(data[0][3]) + "_" + power
    with PdfPages(folder + name_of_file + '.pdf') as pdf:
        plt.figure(figsize=(10, 10))
        for i in range(0,len(data)):
            plt.plot(data[i][0], data[i][1])
            #plt.legend(str(data[i][2]))
        
        #plt.title('Page One')
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()

def Plot_Temperature(folder, date):
    name_of_list = date + "_list.csv"
    name_of_para = date + "_parameter.csv"
    ###   Read parameter file
    parameter = []
    with open(folder + name_of_para,'r') as n:
        for line in n:
            parameter.append(map(str,line.rstrip('\r\n').split(',')))
    StartPower = int(parameter[3][0])
    EndPower = int(parameter[3][1])
    PowerStep = int(parameter[3][2])
    Num_of_Power = int(parameter[2][3])
    Num_of_KIDs = int(parameter[4][1])

    for numpower in range(Num_of_Power):
        # Loop for power
        power = str(numpower*PowerStep + StartPower) + "dBm"
        name_of_list = date + '_' + power  + '_list.csv'
        data_name = []
        with open(folder + name_of_list,'r') as n:
            for line in n:
                data_name.append(map(str,line.rstrip('\n').split(','))) # Remove '\n'
        magS21all = []
        for filename in data_name:
            filename = str(filename).replace("[", "").replace("]", "").replace("'", "").replace("\\r", "")+".csv"
            magS21all.append(Get_S21mag_SingleKID(folder, filename))
        for numKID in range(Num_of_KIDs):
            # Loop for KID
            Plot_TempDepS21(slicing(magS21all,numKID+1,Num_of_KIDs), folder, power)

"""
# for test
folder = "../../../MeasurementResult/20160729_OMTdelta/"
date = "20160729"
Plot_Temperature(folder, date)
"""
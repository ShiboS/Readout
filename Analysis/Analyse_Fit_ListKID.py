import Analyse_Fit_SingleKID
import csv

def slicing(freqlist, n, Num_of_KIDs):
    return freqlist[n-1::Num_of_KIDs]
    
def save_fit(data, folder, power):
    name_of_file = folder.replace("../../../MeasurementResult/","").replace("/", "") + "_" + str(data[0][2]) + "_" + power
    f = open(folder + name_of_file + '.csv', 'w')
    fwrite = csv.writer(f)

    # Write first and second rows with variable names and measurement parameters
    fwrite.writerow( ('Power(dBm)', 'Temperature(mK)', 'fr from mag(S21)', 'fr from phase fitting', 'standard 1 sigma err of fr', 'Qr from phase fitting', 'standard 1 sigma err of Qr', 'Qc from phase fitting', 'standard 1 sigma err of Qc', 'Qi from phase fitting', 'standard 1 sigma err of Qi', 'name of data file', "deltaf/fo from mag(S21)", "deltaf/fo from phase fitting"))
    
    # Write number-of-points rows
    for i in range(0, len(data)):
        fwrite.writerow([data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6], data[i][7], data[i][8], data[i][9], data[i][10], data[i][11], (data[i][2]-data[0][2])/data[0][2], (data[i][3]-data[0][3])/data[0][3]])

def Fit_List_KIDs(folder, date, span):
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
        Fit_result = []
        for filename in data_name:
            filename = str(filename).replace("[", "").replace("]", "").replace("'", "").replace("\\r", "")+".csv"
            Fit_result.append(Analyse_Fit_SingleKID.Fit_SingleKID(folder, filename, span))
        for numKID in range(Num_of_KIDs):
            # Loop for KID
            save_fit(slicing(Fit_result, numKID+1, Num_of_KIDs), folder, power)

"""
# for test
folder = "../../../MeasurementResult/20160729_OMTdelta/"
date = "20160729"
span = 1e6
Fit_List_KIDs(folder, date, span)
"""
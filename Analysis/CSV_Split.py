# split csv file to several files
import csv

def CSV_Split(folder, date):
    name_of_list = date + "_list.csv"
    name_of_para = date + "_parameter.csv"
    data_name = []
    parameter = []
    
    ###   Read parameter file
    with open(folder + name_of_para,'r') as n:
        for line in n:
            parameter.append(map(str,line.rstrip('\r\n').split(',')))
    
    StartPower = int(parameter[3][0])
    EndPower = int(parameter[3][1])
    PowerStep = int(parameter[3][2])
    Num_of_Power = int(parameter[2][3])
    Num_of_KIDs = int(parameter[4][1])
    
    ###   Read data set name list
    with open(folder + name_of_list,'r') as n:
        for line in n:
            data_name.append(str(line).replace("\r\n", ""))#map(str,line.rstrip('\n').split(','))) # Remove '\n'
    
    def slicing(freqlist, n, Num):
        return freqlist[n:n+Num:1]
    
    ###   Slicing data name list and save it with different readout power.
    for i in range(0, len(data_name), Num_of_KIDs*Num_of_Power):
        for numpower in range(Num_of_Power):
            """
            This program will not overwrite existing file.
            Be careful when the files have already existed.
            """
            slicing_data = slicing(data_name, i+Num_of_KIDs*numpower, Num_of_KIDs)
            power = numpower*PowerStep + StartPower
            f = open(folder + date + '_' + str(power) + 'dBm_list' + '.csv', 'a')
            fwrite = csv.writer(f)
            for s in range(0, len(slicing_data)):
                fwrite.writerow([slicing_data[s]])
            f.close()
            
"""
###   Edit these two
#     Be care of the date if the measurement was done overnight.
folder = "../../../MeasurementResult/20160729_OMTdelta/"
date = "20160729"
CSV_Split(folder, date)
"""
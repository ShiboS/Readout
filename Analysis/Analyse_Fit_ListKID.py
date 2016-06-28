import Analyse_Fit_SingleKID
import csv

### Read filename list
data_name = []
folder = "../../../MeasurementResult/20160616_Nb154nmCry48/"
readpower = '10dBm'

name_of_list = '20160616_' + readpower + '_list.csv'
#name_of_list = '20160227' + '_list.csv'
global Num_of_KID
Num_of_KID = 10
BW=1e6

with open(folder + name_of_list,'r') as n:
    for line in n:
        data_name.append(map(str,line.rstrip('\n').split(','))) # Remove '\n'

Fit_result = []
for filename in data_name:
    #print filename
    filename = str(filename).replace("[", "").replace("]", "").replace("'", "").replace("\\r", "")+".csv"
    Fit_result.append(Analyse_Fit_SingleKID.Fit_SingleKID(folder, filename, BW))


def slicing(freqlist, n):
    return freqlist[n-1::Num_of_KID]
    
a = slicing(Fit_result,1)
b = slicing(Fit_result,2)
c = slicing(Fit_result,3)
d = slicing(Fit_result,4)

e = slicing(Fit_result,5)
f = slicing(Fit_result,6)

g = slicing(Fit_result,7)
h = slicing(Fit_result,8)

ii = slicing(Fit_result,9)
j = slicing(Fit_result,10)
"""
"""
def save_fit(data, folder, power):
    name_of_file = folder.replace("../../../MeasurementResult/","").replace("/", "") + "_" + str(data[0][2]) + "_" + power
    f = open(folder + name_of_file + '.csv', 'w')
    fwrite = csv.writer(f)

    # Write first and second rows with variable names and measurement parameters
    fwrite.writerow( ('Power(dBm)', 'Temperature(mK)', 'fr from mag(S21)', 'fr from phase fitting', 'standard 1 sigma err of fr', 'Qr from phase fitting', 'standard 1 sigma err of Qr', 'Qc from phase fitting', 'standard 1 sigma err of Qc', 'Qi from phase fitting', 'standard 1 sigma err of Qi', 'name of data file', "deltaf/fo from mag(S21)", "deltaf/fo from phase fitting"))
    
    # Write number-of-points rows
    for i in range(0, len(data)):
        fwrite.writerow([data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6], data[i][7], data[i][8], data[i][9], data[i][10], data[i][11], (data[i][2]-data[0][2])/data[0][2], (data[i][3]-data[0][3])/data[0][3]])
        
save_fit(a, folder, readpower)
save_fit(b, folder, readpower)
save_fit(c, folder, readpower)
save_fit(d, folder, readpower)

save_fit(e, folder, readpower)
save_fit(f, folder, readpower)

save_fit(g, folder, readpower)
save_fit(h, folder, readpower)

save_fit(ii, folder, readpower)
save_fit(j, folder, readpower)
"""
save_fit(k, folder, readpower)
save_fit(l, folder, readpower)
"""
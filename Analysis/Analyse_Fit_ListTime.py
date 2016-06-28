import Analyse_Fit_SingleKID
import csv

### Read filename list
data_name = []
folder = "../../../MeasurementResult/20160612_NbRRR46time/"

name_of_list = '20160612_list.csv'

with open(folder + name_of_list,'r') as n:
    for line in n:
        data_name.append(map(str,line.rstrip('\n').split(','))) # Remove '\n'

Fit_result = []
for filename in data_name:
    #print filename
    filename = str(filename).replace("[", "").replace("]", "").replace("'", "").replace("\\r", "")+".csv"
    Fit_result.append(Analyse_Fit_SingleKID.Fit_SingleKID(folder, filename))
    

def save_fit(data, folder, power):
    name_of_file = folder.replace("/", "") + "_" + str(data[0][2]) + "_" + power
    f = open(folder + name_of_file + '.csv', 'w')
    fwrite = csv.writer(f)

    # Write first and second rows with variable names and measurement parameters
    fwrite.writerow( ('Power(dBm)', 'Temperature(mK)', 'fr from mag(S21)', 'fr from phase fitting', 'standard 1 sigma err of fr', 'Qr from phase fitting', 'standard 1 sigma err of Qr', 'Qc from phase fitting', 'standard 1 sigma err of Qc', 'Qi from phase fitting', 'standard 1 sigma err of Qi', 'name of data file', "deltaf/fo from mag(S21)", "deltaf/fo from phase fitting"))
    
    # Write number-of-points rows
    for i in range(0, len(data)):
        fwrite.writerow([data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6], data[i][7], data[i][8], data[i][9], data[i][10], data[i][11], (data[i][2]-data[0][2])/data[0][2], (data[i][3]-data[0][3])/data[0][3]])
        
save_fit(Fit_result, folder, "-25dBm")
# split csv file to several files
import csv

data_name = []
folder = "../../../MeasurementResult/20160616_Nb154nmCry48/"
name_of_list = "20160616_list.csv"
global Num_of_Split
Num_of_Power = 9
Num_of_KIDs = 10

with open(folder + name_of_list,'r') as n:
    for line in n:
        data_name.append(str(line).replace("\r\n", ""))#map(str,line.rstrip('\n').split(','))) # Remove '\n'
"""
file_name_list = []
for filename in data_name:
    #print filename
    filename = str(filename).replace("[", "").replace("]", "").replace("'", "").replace("\\r", "")+".csv"
    file_name_list.append()
"""

def slicing(freqlist, n, Num1):
    return freqlist[n:n+Num1:1]
#a = slicing(data_name, 0, Num_of_KIDs)
#print a

file1 = []
file2 = []
file3 = []

file4 = []

file5 = []

file6 = []
file7 = []
file8 = []
file9 = []
"""
"""
for i in range(0, len(data_name), Num_of_KIDs*Num_of_Power):
    a = slicing(data_name, i, Num_of_KIDs)
    #print a
    b = slicing(data_name, i+Num_of_KIDs, Num_of_KIDs)
    c = slicing(data_name, i+2*Num_of_KIDs, Num_of_KIDs)
    d = slicing(data_name, i+3*Num_of_KIDs, Num_of_KIDs)
    e = slicing(data_name, i+4*Num_of_KIDs, Num_of_KIDs)
    f = slicing(data_name, i+5*Num_of_KIDs, Num_of_KIDs)
    g = slicing(data_name, i+6*Num_of_KIDs, Num_of_KIDs)
    h = slicing(data_name, i+7*Num_of_KIDs, Num_of_KIDs)
    ii = slicing(data_name, i+8*Num_of_KIDs, Num_of_KIDs)
    print a
    for k in range(0, len(a)):
        file1.append(a[k])
        file2.append(b[k])
        file3.append(c[k])
        
        file4.append(d[k])
        
        file5.append(e[k])
        
        file6.append(f[k])
        file7.append(g[k])
        file8.append(h[k])
        file9.append(ii[k])
        """
        """

data = '20160616'
print folder + data
f = open(folder + data + '_-30dBm_list' + '.csv', 'w')
fwrite = csv.writer(f)
for i in range(0, len(file1)):
        fwrite.writerow([file1[i]])
f.close()

f = open(folder + data + '_-25dBm_list' + '.csv', 'w')
fwrite = csv.writer(f)
for i in range(0, len(file2)):
        fwrite.writerow([file2[i]])
f.close()

f = open(folder + data + '_-20dBm_list' + '.csv', 'w')
fwrite = csv.writer(f)
for i in range(0, len(file3)):
        fwrite.writerow([file3[i]])
f.close()

f = open(folder + data + '_-15dBm_list' + '.csv', 'w')
fwrite = csv.writer(f)
for i in range(0, len(file4)):
        fwrite.writerow([file4[i]])
f.close()

f = open(folder + data + '_-10dBm_list' + '.csv', 'w')
fwrite = csv.writer(f)
for i in range(0, len(file5)):
        fwrite.writerow([file5[i]])
f.close()

f = open(folder + data + '_-5dBm_list' + '.csv', 'w')
fwrite = csv.writer(f)
for i in range(0, len(file6)):
        fwrite.writerow([file6[i]])
f.close()

f = open(folder + data + '_0dBm_list' + '.csv', 'w')
fwrite = csv.writer(f)
for i in range(0, len(file7)):
        fwrite.writerow([file7[i]])
f.close()

f = open(folder + data + '_5dBm_list' + '.csv', 'w')
fwrite = csv.writer(f)
for i in range(0, len(file8)):
        fwrite.writerow([file8[i]])
f.close()

f = open(folder + data + '_10dBm_list' + '.csv', 'w')
fwrite = csv.writer(f)
for i in range(0, len(file9)):
        fwrite.writerow([file9[i]])
f.close()
"""
"""
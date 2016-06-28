from DataReader import ReadSingle
import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import  pi
import itertools

### Nb
folder = "../../../MeasurementResult/20160516_Nb154nmCry3/"
filename = "20160516_Nb154nmCry3_3.856849225_-50dBm.csv"
input_attn = 60
power, tempdata, frmin, frfit, frfit_err, Qr, Qr_err, Qc, Qc_err, Qi, Qi_err = ReadSingle(folder, filename)
line_1 = plt.errorbar(tempdata/1000, Qi, yerr=Qi_err*Qi, fmt='o-', color='#0066FF', linewidth=3, markersize=8, label = str(int(power[0])-input_attn)+"dBm")

#intP = 10*np.log10(2.0/pi*Qr*Qr/Qc)+power

filename = "20160516_Nb154nmCry3_3.856849225_-40dBm.csv"
power, tempdata, frmin, frfit, frfit_err, Qr, Qr_err, Qc, Qc_err, Qi, Qi_err = ReadSingle(folder, filename)
line_2 = plt.errorbar(tempdata/1000, Qi, yerr=Qi_err*Qi, fmt='o-', color='#00FF00', linewidth=3, markersize=8, label = str(int(power[0])-input_attn)+"dBm")

filename = "20160516_Nb154nmCry3_3.856849225_-30dBm.csv"
power, tempdata, frmin, frfit, frfit_err, Qr, Qr_err, Qc, Qc_err, Qi, Qi_err = ReadSingle(folder, filename)
line_3 = plt.errorbar(tempdata/1000, Qi, yerr=Qi_err*Qi, fmt='o-', color='#FFFF00', linewidth=3, markersize=8, label = str(int(power[0])-input_attn)+"dBm")

filename = "20160516_Nb154nmCry3_3.856849225_-20dBm.csv"
power, tempdata, frmin, frfit, frfit_err, Qr, Qr_err, Qc, Qc_err, Qi, Qi_err = ReadSingle(folder, filename)
line_4 = plt.errorbar(tempdata/1000, Qi, yerr=Qi_err*Qi, fmt='o-', color='#FF9900', linewidth=3, markersize=8, label = str(int(power[0])-input_attn)+"dBm")

filename = "20160516_Nb154nmCry3_3.85685235_-10dBm.csv"
power, tempdata, frmin, frfit, frfit_err, Qr, Qr_err, Qc, Qc_err, Qi, Qi_err = ReadSingle(folder, filename)
line_5 = plt.errorbar(tempdata/1000, Qi, yerr=Qi_err*Qi, fmt='o-', color='#FF0000', linewidth=3, markersize=8, label = str(int(power[0])-input_attn)+"dBm")
legend1 = plt.legend(handles=[line_5, line_4, line_3, line_2, line_1], loc=1)

### Nb
folder = "../../../MeasurementResult/20160412_Nb140nm/"
filename = "20160412_Nb140nm_3.8615855_-45dBm.csv"
input_attn = 60
power, tempdata, frmin, frfit, frfit_err, Qr, Qr_err, Qc, Qc_err, Qi, Qi_err = ReadSingle(folder, filename)
line_1 = plt.errorbar(tempdata/1000, Qi, yerr=Qi_err*Qi, fmt='^-', color='#0066FF', linewidth=3, markersize=8, label = str(int(power[0])-input_attn)+"dBm")

filename = "20160412_Nb140nm_3.8615855_-35dBm.csv"
power, tempdata, frmin, frfit, frfit_err, Qr, Qr_err, Qc, Qc_err, Qi, Qi_err = ReadSingle(folder, filename)
line_2 = plt.errorbar(tempdata/1000, Qi, yerr=Qi_err*Qi, fmt='^-', color='#00FF00', linewidth=3, markersize=8, label = str(int(power[0])-input_attn)+"dBm")

filename = "20160412_Nb140nm_3.8615855_-25dBm.csv"
power, tempdata, frmin, frfit, frfit_err, Qr, Qr_err, Qc, Qc_err, Qi, Qi_err = ReadSingle(folder, filename)
line_3 = plt.errorbar(tempdata/1000, Qi, yerr=Qi_err*Qi, fmt='^-', color='#FFFF00', linewidth=3, markersize=8, label = str(int(power[0])-input_attn)+"dBm")

filename = "20160412_Nb140nm_3.861589666_-15dBm.csv"
power, tempdata, frmin, frfit, frfit_err, Qr, Qr_err, Qc, Qc_err, Qi, Qi_err = ReadSingle(folder, filename)
line_4 = plt.errorbar(tempdata/1000, Qi, yerr=Qi_err*Qi, fmt='^-', color='#FF9900', linewidth=3, markersize=8, label = str(int(power[0])-input_attn)+"dBm")

filename = "20160412_Nb140nm_3.861589666_-5dBm.csv"
power, tempdata, frmin, frfit, frfit_err, Qr, Qr_err, Qc, Qc_err, Qi, Qi_err = ReadSingle(folder, filename)
line_5 = plt.errorbar(tempdata/1000, Qi, yerr=Qi_err*Qi, fmt='^-', color='#FF0000', linewidth=3, markersize=8, label = str(int(power[0])-input_attn)+"dBm")


plt.gca().add_artist(legend1)
plt.legend(handles=[line_5, line_4, line_3, line_2, line_1], loc=3)
plt.yscale('log')
#plt.title('Temperature dependance of internal qualifty factor Qi')
plt.xlabel('Temperature (K)')
plt.ylabel('Internal quality factor Qi')

plt.show()

"""
parameters = ["20160412_Nb140nm_3.8615855_-45dBm.csv",
              "20160412_Nb140nm_3.8615855_-35dBm.csv",
              "20160412_Nb140nm_3.8615855_-25dBm.csv",
              "20160412_Nb140nm_3.861589666_-15dBm.csv",
              "20160412_Nb140nm_3.861589666_-5dBm.csv"]
colors = ['#0066FF', '#00FF00', '#FFFF00', '#FF9900', '#FF0000']
cc = itertools.cycle(colors)
plot_lines = []
for p in parameters:
    power, tempdata, frmin, frfit, frfit_err, Qr, Qr_err, Qc, Qc_err, Qi, Qi_err = ReadSingle(folder, filename)
    plt.hold(True)
    c = next(cc)
    ll = plt.errorbar(tempdata/1000, Qi, yerr=Qi_err*Qi, fmt='o', color=c)
    plot_lines.append([ll])

#legend1 = plt.legend(plot_lines[0], ["algo1", "algo2", "algo3", "algo2", "algo3"], loc=1)
plt.legend([l[0] for l in plot_lines], parameters, loc=4)
#plt.gca().add_artist(legend1)
plt.show()
"""
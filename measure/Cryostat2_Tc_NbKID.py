# Calibrate VNA first
# With Ecal N4691-60001
import Instrument.E5071C as inst0
import Instrument.LS350 as inst1
import time
import csv
import numpy as np

### Check connection with instruments
VNA = inst0.E5071()
LS350 = inst1.LS350()
VNA.whoareyou()
LS350.whoareyou()

### Initialize VNA
# You can increase the number of points and decrease the IF Bandwidth,
# but be care of the averaging waiting time
VNA.SetOutP("ON")
VNA.SetMeasurement("S21")

# Change measurement format
# "POL"  Polar Real/Imag
# "PLIN" Polar Linear/Phase
# "PLOG" Polar Log/Phase
VNA.SetFormat("MLOG")
VNA.SetSmoothing("OFF")
VNA.SetPower("-30")
VNA.SetAutoScale()
VNA.SetAveraging("OFF")
VNA.SetAutoScale()
VNA.SetFormat("MLOG")
VNA.SetAutoScale()
LS350.SetHeaterRange(5)
LS350.SetPoint(0.07)
VNA.SetStartFreq("1E9")
VNA.SetStopFreq("8E9")
VNA.SetNumPoint("101")

# f = open('20164101_TempSweep_NbMKID_GoUp.csv', 'w')
f = open('20160618_TempSweep_NbCry152nmA2_GoUp1.csv', 'w')
fwrite = csv.writer(f)

for k in range(0, 14400): 

    y_data = VNA.GetTraceData()
    y_array = np.array(y_data)
    y_array_log = y_array[0::2]

    Stage_TempA = float(LS350.GetTemp("A"))
    Stage_TempB = float(LS350.GetTemp("B"))
    Stage_TempC = float(LS350.GetTemp("C"))
    Stage_TempD = float(LS350.GetTemp("D"))
    fwrite.writerow([k, Stage_TempA, Stage_TempB, Stage_TempC, Stage_TempD]+y_array_log.tolist())

    T = k * 0.002
    print Stage_TempD, T
    LS350.SetPoint(T)
    time.sleep(1)
    if (Stage_TempD > 12)&( T>12):
        break

    print k, Stage_TempD
f.close()
LS350.SetHeaterRange(3)
LS350.SetPoint(0.1)
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

VNA.SetOutP("ON")
VNA.SetMeasurement("S21")
VNA.SetFormat("MLOG")
VNA.SetSmoothing("OFF")
VNA.SetPower("-30")
VNA.SetAutoScale()
VNA.SetAveraging("OFF")
VNA.SetAutoScale()
VNA.SetStartFreq("1E9")
VNA.SetStopFreq("8E9")
VNA.SetNumPoint("101")

LS350.SetHeaterRange(5)

f = open('20151225_TempSweep_ALMKID_GoUp1.csv', 'w')
fwrite = csv.writer(f)

for k in range(1, 14400): 
    y_array = np.array(VNA.GetTraceData())
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
    if (Stage_TempD > 3)&( T>3):
        break
    print k, Stage_TempD
f.close()
LS350.SetHeaterRange(3)
LS350.SetPoint(0.1)
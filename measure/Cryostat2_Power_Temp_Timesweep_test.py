# Calibrate VNA first
# With Ecal N4691-60001
import Instrument.E5071C as inst0
import Instrument.LS350 as inst1
import time
import csv
import numpy as np
from matplotlib import pyplot as plt, cm, colors

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
VNA.SetPower("-50")
VNA.SetNumPoint("4801")
VNA.SetIFBdw("1E4")       # 10kHz

# Measure Electrical Delay (About ~51ns for Cryostat 2)
# Reference: Gao Thesis Appendix E.
# Select a no resonance frequency and set Marker.
VNA.SetCenterFreq("4E9")
VNA.SetSpanFreq("1E8")
VNA.Marker("4E9")
VNA.SetAutoScale()
#VNA.SetSmoothing("ON")
VNA.SetAverageFactor("16")
VNA.SetAveraging("ON")
VNA.SetAutoScale()

# Wait 5 seconds for averaging.
# This time depends on how long the averaging finishs
time.sleep(5)

# Use Marker function to set Electrical Delay
# After setting marker function, a MarkerSearchExecute command must be run
VNA.MarkerFunc("DEL")
VNA.MarkerSearchExecute()
VNA.GetElectricalDelay()

VNA.SetSmoothing("OFF")

VNA.SetCenterFreq("6.7E9")
VNA.SetSpanFreq("0.1E9")
VNA.SetPower("0")
VNA.SetAutoScale()
time.sleep(1)

VNA.SetAveraging("OFF")
VNA.SetAutoScale()

VNA.SetFormat("MLOG")
VNA.SetAutoScale()

LS350.SetHeaterRange(5)
LS350.SetPoint(0.07)
f = open('20151119_TempSweep_Sample2_finial_GoUp.csv', 'w')
fwrite = csv.writer(f)

for k in range(1, 14400): 
    VNA.SetCenterFreq("6.7E9")
    VNA.SetSpanFreq("0.1E9")
    y_data = VNA.GetTraceData()
    y_array = np.array(y_data)
    y_array_log = y_array[0::2]
    y_log_average = np.average(y_array_log)
    time.sleep(1)
    VNA.SetCenterFreq("4.1E9")
    VNA.SetSpanFreq("0.1E9")
    y_data = VNA.GetTraceData()
    y_array = np.array(y_data)
    y_array_log = y_array[0::2]
    y_log_average1 = np.average(y_array_log)
    Stage_TempA = float(LS350.GetTemp("A"))
    Stage_TempB = float(LS350.GetTemp("B"))
    Stage_TempC = float(LS350.GetTemp("C"))
    Stage_TempD = float(LS350.GetTemp("D"))
    fwrite.writerow([Stage_TempA, Stage_TempB, Stage_TempC, Stage_TempD, y_log_average, y_log_average1])
    print Stage_TempD, y_log_average, y_log_average1
    time.sleep(1)

    T = k * 0.001
    LS350.SetPoint(T)
    if Stage_TempD > 10:
        break
    """
    if Stage_TempD < 0.2:
        break
    """
    print k
f.close()
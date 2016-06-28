import Instrument.E5071C as inst0
import Instrument.LS350 as inst1
import time
import csv
import numpy as np

VNA = inst0.E5071()
LS350 = inst1.LS350()
VNA.whoareyou()
LS350.whoareyou()

VNA.SetOutP("ON")
VNA.SetMeasurement("S21")

VNA.SetFormat("MLOG")
VNA.SetPower("-25")
VNA.SetAutoScale()
VNA.SetAveraging("ON")
VNA.SetAutoScale()

VNA.SetNumPoint("4801")
VNA.SetIFBdw("1E4")       # 10kHz

VNA.SetCenterFreq("5E9")
VNA.SetSpanFreq("2.5E9")
VNA.Marker("5E9")
VNA.SetAutoScale()

VNA.SetAverageFactor("16")
VNA.SetAveraging("ON")
VNA.SetAutoScale()
time.sleep(5)
VNA.MarkerFunc("DEL")
VNA.MarkerSearchExecute()
VNA.GetElectricalDelay()
VNA.SetSmoothing("OFF")

file_name_list = []
def Measure_KID(KID_freq, Power):
    VNA.SetCenterFreq(KID_freq)
    # Set a big span around kid and then search the minimum point
    # Set it as center frequency
    VNA.SetSpanFreq("2E6")
    VNA.SetPower(Power)
    #VNA.SetSmoothing("ON")
    VNA.SetAutoScale()
    
    # Use Marker Search to search the minimum point
    # Set minimum point to center frequency
    VNA.MarkerSearch("MIN")
    VNA.MarkerSearchExecute()
    VNA.MarkerFunc("CENT")
    VNA.SetSpanFreq("2E6")
    VNA.SetAutoScale()

    
def Save_KID(folder,num):
    ### Get frequency data
    x_data = VNA.GetFreqData()
    x_array = np.array(x_data)
    
    ### PLOG data - MLOG and Phase SLIN/Linear,phase
    VNA.SetFormat("SLIN")
    VNA.SetAutoScale()
    # Get trace data
    y_data = VNA.GetTraceData()
    y_array = np.array(y_data)
    #y_array_mlog = y_array[0::2]
    #y_array_phase = y_array[1::2]
    y_array_lin = y_array[0::2]
    y_array_phase = y_array[1::2]
    # LOG data
    VNA.SetFormat("MLOG")
    VNA.SetAutoScale()
    # Get trace data
    y_data = VNA.GetTraceData()
    y_array = np.array(y_data)
    y_array_mlog = y_array[0::2]
    
    ### Save data
    # yyyymmdd string date format
    time_yyyymmdd = time.strftime('%Y%m%d')
    POWER = str(int(float(VNA.GetPower()))) + 'dBm'
    FCENTER = str(int(float(VNA.GetCenterFreq()))/1E9)
    FSPAN = str(int(float(VNA.GetSpanFreq()))/1E9)
    
    # Query the stage temperature from LS370 Chaneel: D
    Stage_Temp = str(1000*float(LS350.GetTemp("D"))) + 'mK'
    
    # Name of file
    name_of_file = time_yyyymmdd + '_' + POWER + '_' +  FCENTER + '_' + FSPAN + '_' + Stage_Temp + '_' + num
    file_name_list.append(name_of_file)
    # Make a new csv format document with name_of_file and write it
    f = open(folder + name_of_file + '.csv', 'w')
    fwrite = csv.writer(f)

    # Write first and second rows with variable names and measurement parameters
    fwrite.writerow( ('Frequency', 'S21'))
    fwrite.writerow( ('Hz', 'linear', 'Phase', 'Log'))

    # Write number-of-points rows
    for i in range(0, int(VNA.GetNumPoint())):
        fwrite.writerow([x_array[i], y_array_lin[i], y_array_phase[i], y_array_mlog[i]])
VNA.SetAveraging("OFF")
folder = '../../../MeasurementResult/20160612_NbRRR46time/'
pixel1 = 4.97213E9
for i in range(0,1800):
    print i
    Measure_KID(pixel1, -20)
    Save_KID(folder,str(i))
    time.sleep(10)
    
f = open(folder + time.strftime('%Y%m%d') + '_list' + '.csv', 'w')
fwrite = csv.writer(f)

# Write number-of-points rows
for i in range(0, len(file_name_list)):
        fwrite.writerow([file_name_list[i]])
f.close()
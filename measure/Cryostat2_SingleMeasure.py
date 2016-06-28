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
        
# Save kid automatically: linear, phase and dB
def Save_KID(folder):
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

    # Ask VNA what the output power is and we get string format of float value.
    # Change this string format to float format, then change it to integar format
    # and then change it back to string format
    # u'-4.00000000000E+001\n' ---> -40.0 ---> -40 ---> '-40'
    POWER = str(int(float(VNA.GetPower()))) + 'dBm'

    # Four frequencies are the same with power
    FSTART = str(int(float(VNA.GetStartFreq()))/1E9)
    FSTOP = str(int(float(VNA.GetStopFreq()))/1E9)
    FCENTER = str(int(float(VNA.GetCenterFreq()))/1E9)
    FSPAN = str(int(float(VNA.GetSpanFreq()))/1E9)
    
    # Query the stage temperature from LS370 Chaneel: D
    Stage_Temp = str(1000*float(LS350.GetTemp("D"))) + 'mK'
    
    # Name of file
    name_of_file = time_yyyymmdd + '_' + POWER + '_' +  FCENTER + '_' + FSPAN + '_' + Stage_Temp

    # Make a new csv format document with name_of_file and write it
    f = open(folder + name_of_file + '.csv', 'w')
    fwrite = csv.writer(f)

    # Write first and second rows with variable names and measurement parameters
    fwrite.writerow( ('Frequency', 'S21'))
    fwrite.writerow( ('Hz', 'linear', 'Phase', 'Log'))

    # Write number-of-points rows
    for i in range(0, int(VNA.GetNumPoint())):
        fwrite.writerow([x_array[i], y_array_lin[i], y_array_phase[i], y_array_mlog[i]])

folder = "20160227_OMT/"
Save_KID(folder)
import Instrument.E5071C as inst0
import Instrument.LS370 as inst1
import Instrument.LS350 as inst2
import time
import csv
import numpy as np

VNA = inst0.E5071()

def VNA_Initialize_Delay(DelayFreq):
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

    # Measure Electrical Delay (About ~31ns for Cryostat 2)
    # Reference: Gao Thesis Appendix E.
    # Select a no resonance frequency and set Marker.
    VNA.SetCenterFreq(DelayFreq)
    VNA.SetSpanFreq("1E8")
    VNA.Marker(DelayFreq)
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

# (Give the frequency which is close to the center frequency of KID,
# search the minimum frequency point automatically 
# and set it as center frequency)
# Do measurement setting for saving KID data
def Measure_KID(KID_freq, KID_span, Power):
    VNA.SetCenterFreq(KID_freq)
    # Set a big span around kid and then search the minimum point
    # Set it as center frequency
    VNA.SetSpanFreq("15E6")
    VNA.SetPower(Power)
    #VNA.SetSmoothing("ON")
    VNA.SetAutoScale()
    VNA.SetAveraging("OFF")
    # Wait one second
    time.sleep(3)
    
    # Use Marker Search to search the minimum point
    # Set minimum point to center frequency
    VNA.MarkerSearch("MIN")
    VNA.MarkerSearchExecute()
    VNA.MarkerFunc("CENT")
    VNA.SetSpanFreq(KID_span)
    
    # Averaging ON and 16 times average
    VNA.SetAverageFactor("16")
    VNA.SetAveraging("ON")
    VNA.SetAutoScale()
    
    # Wait 8 seconds for averaging.
    # This time depends on how long the averaging finishs
    # This could be changed to longer time
    time.sleep(8)
        
# Save kid automatically: linear, phase and dB
def Save_KID_Cryostat1(folder):
    LS370 = inst1.LS370()
    ### Get frequency data
    x_array = np.array(VNA.GetFreqData())
    
    ### PLOG data - MLOG and Phase SLIN/Linear,phase
    VNA.SetFormat("SLIN")
    VNA.SetAutoScale()
    # Get trace data
    y_array = np.array(VNA.GetTraceData())
    #y_array_mlog = y_array[0::2]
    #y_array_phase = y_array[1::2]
    y_array_lin = y_array[0::2]
    y_array_phase = y_array[1::2]
    # LOG data
    VNA.SetFormat("MLOG")
    VNA.SetAutoScale()
    # Get trace data
    y_array = np.array(VNA.GetTraceData())
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
    Stage_Temp = str(1000*float(LS370.GetTemp("4"))) + 'mK'
    
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
    return name_of_file
        
def Save_KID_Cryostat2(folder):
    LS350 = inst2.LS350()
    ### Get frequency data
    x_array = np.array(VNA.GetFreqData())
    
    ### PLOG data - MLOG and Phase SLIN/Linear,phase
    VNA.SetFormat("SLIN")
    VNA.SetAutoScale()
    # Get trace data
    y_array = np.array(VNA.GetTraceData())
    #y_array_mlog = y_array[0::2]
    #y_array_phase = y_array[1::2]
    y_array_lin = y_array[0::2]
    y_array_phase = y_array[1::2]
    # LOG data
    VNA.SetFormat("MLOG")
    VNA.SetAutoScale()
    # Get trace data
    y_array = np.array(VNA.GetTraceData())
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
    #Stage_Temp = '90mK'
    
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
    return name_of_file

def Save_dB():
    x_data = VNA.GetFreqData()
    x_array = np.array(x_data)
    VNA.SetFormat("MLOG")
    VNA.SetAutoScale()
    # Get trace data
    y_data = VNA.GetTraceData()
    y_array = np.array(y_data)
    y_array_log = y_array[0::2]
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

    
    # Name of file
    name_of_file = time_yyyymmdd + '_' + POWER + '_' +  FCENTER + '_' + FSPAN

    # Make a new csv format document with name_of_file and write it
    f = open(name_of_file + '.csv', 'w')
    fwrite = csv.writer(f)

    # Write first and second rows with variable names and measurement parameters
    fwrite.writerow( ('Frequency', 'S21'))
    fwrite.writerow( ('Hz', 'dB'))

    # Write number-of-points rows
    for i in range(0, int(VNA.GetNumPoint())):
        fwrite.writerow([x_array[i], y_array_log[i]])
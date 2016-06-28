# Calibrate VNA first
# With Ecal N4691-60001
import E5071C as inst0
import LS350 as inst1
import time
import csv
import numpy as np
from matplotlib import pyplot as plt, cm, colors
from scipy.optimize import curve_fit
import Fitter # For circle fitting
import fitting # For phase fitting

VNA = inst0.E5071()
LS350 = inst1.LS350()

VNA.whoareyou()
LS350.whoareyou()

# Initialize VNA
# You can increase the number of points and decrease the IF Bandwidth,
# but be care of the averaging waiting time
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
VNA.SetSmoothing("ON")
VNA.SetAverageFactor("8")
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

# (Give the frequency which is close to the center frequency of KID,
# search the minimum frequency point automatically 
# and set it as center frequency)
# Do measurement setting for saving KID data
def Measure_KID(KID_freq, Power):
    VNA.SetCenterFreq(KID_freq)
    VNA.SetSpanFreq("2E6")
    VNA.SetPower(Power)
    #VNA.SetSmoothing("ON")
    VNA.SetAutoScale()
    
    # Wait one second
    time.sleep(1)
    '''
    # Use Marker Search to search the minimum point
    # Set minimum point to center frequency
    VNA.MarkerSearch("MIN")
    VNA.MarkerSearchExecute()
    VNA.MarkerFunc("CENT")
    '''
    # Averaging ON and 8 times average
    VNA.SetAverageFactor("8")
    VNA.SetAveraging("ON")
    VNA.SetAutoScale()
    
    # Wait 5 seconds for averaging.
    # This time depends on how long the averaging finishs
    time.sleep(5)

# Read out data
def Save_KID():
    ### Get frequency data
    x_data = VNA.GetFreqData()
    x_array = np.array(x_data)
    
    ### MLOG data
    VNA.SetFormat("MLOG")
    VNA.SetAutoScale()
    # Get trace data
    y_data = VNA.GetTraceData()
    y_array = np.array(y_data)
    y_array_mlog = y_array[0::2]
    
    ### POL Real/Imag data
    VNA.SetFormat("POL")
    VNA.SetAutoScale()
    # Get trace data
    y_data = VNA.GetTraceData()
    y_array = np.array(y_data)
    y_array_real = y_array[0::2]
    y_array_imag = y_array[1::2]
    
    ### Phase data
    VNA.SetFormat("PPH")
    VNA.SetAutoScale()
    # Get trace data
    y_data = VNA.GetTraceData()
    y_array = np.array(y_data)
    y_array_phase = y_array[0::2]
    
    

    
    
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
    
    # Query the stage temperature from LS350 Chaneel: D
    Stage_Temp = str(1000*float(LS350.GetTemp("D"))) + 'mK'
    
    # Name of file
    name_of_file = time_yyyymmdd + '_' + POWER + '_' +  FSTART + '-' + FSTOP + '_' + Stage_Temp

    # Make a new csv format document with name_of_file and write it
    f = open(name_of_file + '.csv', 'w')
    fwrite = csv.writer(f)

    # Write first and second rows with variable names and measurement parameters
    fwrite.writerow( ('Frequency', 'S21'))
    fwrite.writerow( ('Hz', 'dB', 'Real', 'Imag', 'Phase'))

    # Write number-of-points rows
    for i in range(0, int(VNA.GetNumPoint())):
        fwrite.writerow([x_array[i], y_array_mlog[i], y_array_real[i], y_array_imag[i], y_array_phase[i]])
    
Measure_KID(4.8361742E9, -50)
Save_KID()
Measure_KID(4.8361742E9, -40)
Save_KID()
Measure_KID(4.8361742E9, -30)
Save_KID()
Measure_KID(4.8361742E9, -20)
Save_KID()

# Temperature control
LS350.SetHeaterRange(2)
#LS350.SetPID("6000", "12", "0")
StartTemp = 100  # mK
EndTemp = 300 # mK
Step = 20

for Temp in range(StartTemp, EndTemp+20, Step):
    LS350.SetPoint(str(Temp/1000.))

    for i in range(1,1800):
        time.sleep(1)
        print i, LS350.GetTemp("D")
        if ((float(LS350.GetTemp("D"))<=Temp/1000.*1.005) and (float(LS350.GetTemp("D"))>=Temp/1000.*0.995)):
            time.sleep(10)
            if ((float(LS350.GetTemp("D"))<=Temp/1000.*1.005) and (float(LS350.GetTemp("D"))>=Temp/1000.*0.995)):
                time.sleep(5)
                if ((float(LS350.GetTemp("D"))<=Temp/1000.*1.005)and (float(LS350.GetTemp("D"))>=Temp/1000.*0.995)):
                    Measure_KID(4.8361742E9, -50)
                    Save_KID()
                    #Measure_KID(4.8361742E9, -40)
                    #Save_KID()
                    #Measure_KID(4.8361742E9, -30)
                    #Save_KID()
                    break
    print Temp
    
# Heater OFF
LS350.SetHeaterRange(0)
        
# Plot both two parts
'''
plt.plot(x_array, y_array_real)
plt.plot(x_array, y_array_imag)
plt.show()
'''

'''
x = np.r_[y_array_real]
y = np.r_[y_array_imag]

fitpara=np.array(Fitter.leastsq_circle(x,y))
Fitter.plot_data_circle(x,y, fitpara[0], fitpara[1], fitpara[2])
plt.show()

# Move origin dot to the fitted center of measured data
# Rotating and translating to the origin
print fitpara
x_c = fitpara[0]
y_c = fitpara[1]
radius = fitpara[2]

Z_i = x + 1j*y
Z_ii = (x_c + 1j*y_c - Z_i)*np.exp(-1j * np.arctan(y_c/x_c))
plt.plot(Z_ii.real, Z_ii.imag, 'r.', mew=0.1)
Fitter.plot_data_circle(Z_ii.real, Z_ii.imag, fitpara[0], fitpara[1], fitpara[2])



# Fit Phase
data_phase = np.arctan2(Z_ii.imag, Z_ii.real)
data_phase[ data_phase<-2.7 ] += 2*np.pi # To make a smooth line, not robust

def Phase_func(f, Theta_0, Q_r, f_r):
    return -Theta_0 + 2 * np.arctan(2*Q_r*(1-f/f_r))
    
popt, pcov = curve_fit(Phase_func, x_array, data_phase)
plt.plot(x_array, Phase_func(x_array, popt[0], popt[1], popt[2]))
plt.plot(x_array, data_phase)


###
para = [1.0, 1e5, 4e9]
para = fitting.theta_to_f(x_array, data_phase, para)

print para
'''

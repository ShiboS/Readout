# Calibrate VNA first
# With Ecal N4691-60001
import Instrument.E5071C as inst0
import Instrument.LS350 as inst1
import time
import csv
import Measurement_Function as meas
VNA = inst0.E5071()
LS350 = inst1.LS350()

### Check connection with instruments
VNA.whoareyou()
LS350.whoareyou()

DelayFrequency = 3E9
meas.VNA_Initialize_Delay(DelayFrequency)

###   Power dBm   ###
StartPower = -55
EndPower = -35
PowerStep = 5

###   Resonance   ###
KID_span = 2E6
resonances = [2.1508E9, 3.6770E9, 3.7348E9, 3.7555E9, 3.8292E9, 3.9319E9, 5.3263E9, 6.9558E9]

###   Folder path need to create this folder manually   ###
folder = '../../../MeasurementResult/20160729_OMTdelta/'

###   File name list
file_name_list = []

for Power in range(StartPower, EndPower+PowerStep, PowerStep):
    for ResFreq in resonances:
        meas.Measure_KID(ResFreq, KID_span, Power)
        name_of_file = meas.Save_KID(folder)
        file_name_list.append(name_of_file)

f = open(folder + time.strftime('%Y%m%d') + '_list' + '.csv', 'w')
fwrite = csv.writer(f)

# Write number-of-points rows
for i in range(0, len(file_name_list)):
        fwrite.writerow([file_name_list[i]])
f.close()
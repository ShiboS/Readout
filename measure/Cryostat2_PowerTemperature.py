# Calibrate VNA first if possible
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

"""
EDIT THIS PART ->
"""
DelayFrequency = 3E9
meas.VNA_Initialize_Delay(DelayFrequency)

###   Temperature control   ###
LS350.SetHeaterRange(3)
#LS350.SetPID("6000", "12", "1")

###   Temperature mK   ###
StartTemp = 80
EndTemp = 400
TempStep = 10
TempStableUp = 1.01
TempStableDn = 0.99

###   Power dBm   ###
StartPower = -55
EndPower = 0
PowerStep = 5
numPower = (EndPower - StartPower)/PowerStep +1

###   Resonance   ###
KID_span = 2E6
resonances = [3.4764E9, 3.4884E9, 3.5247E9, 3.5355E9, 3.6169E9, 3.9431E9, 4.4798E9, 4.5044E9, 4.5262E9, 4.5481E9, 4.579E9, 4.5908E9, 4.7746E9]

###   Folder path need to create this folder manually   ###
folder = '../../../MeasurementResult/20160814_Al_Noguchi/'

"""
<- EDIT THIS PART
"""

###   File name list
file_name_list = []

for Temp in range(StartTemp, EndTemp+TempStep, TempStep):
    SetTemp = Temp/1000.
    LS350.SetPoint(str(SetTemp))
    for i in range(1,3600):
        time.sleep(10)
        print i, LS350.GetTemp("D")
        if ((float(LS350.GetTemp("D"))<=SetTemp*TempStableUp) and (float(LS350.GetTemp("D"))>=SetTemp*TempStableDn)):
            time.sleep(20)
            if ((float(LS350.GetTemp("D"))<=SetTemp*TempStableUp) and (float(LS350.GetTemp("D"))>=SetTemp*TempStableDn)):
                time.sleep(15)
                if ((float(LS350.GetTemp("D"))<=SetTemp*TempStableUp)and (float(LS350.GetTemp("D"))>=SetTemp*TempStableDn)):
                    ###   Power dependance    ###
                    for power in range(StartPower, EndPower+PowerStep, PowerStep):
                        for ResFreq in resonances:
                            meas.Measure_KID(ResFreq, KID_span, power)
                            name_of_file = meas.Save_KID_Cryostat2(folder)
                            file_name_list.append(name_of_file)
                    break # begin next temperature
    print Temp
    
###   Heater OFF: 0
LS350.SetPoint(str(0.01))
LS350.SetHeaterRange(1)

f = open(folder + time.strftime('%Y%m%d') + '_list' + '.csv', 'w')
fwrite = csv.writer(f)

###   Write number-of-points rows
for i in range(0, len(file_name_list)):
        fwrite.writerow([file_name_list[i]])
f.close()

###   Save measurement parameters
f = open(folder + time.strftime('%Y%m%d') + '_parameter' + '.csv', 'w')
fwrite = csv.writer(f)
fwrite.writerow(('Start temperature','End temperature', 'Step'))
fwrite.writerow([StartTemp, EndTemp, TempStep])
fwrite.writerow(('Start power','End power', 'Step', numPower))
fwrite.writerow([StartPower, EndPower, PowerStep])
fwrite.writerow(['Resonance frequencies',len(resonances)])
fwrite.writerow([ResFreq for ResFreq in resonances])
f.close()
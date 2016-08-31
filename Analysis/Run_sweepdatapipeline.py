import Analyse_Fit_SingleKID as FitSingle






### IQ Mixer calibration file
IQCalibrationfile ='IQMixer_Calib/20160803_1M_BOX/EllipseFit_0dBm_2000MHz_8000MHz.csv'
### IQ Reference data (already IQ Mixer calibrated) folder and filename
### IQ Reference data is measured with T>Tc/2
IQReffolder ="../../../MeasurementResult/"
IQReffilename = 'Sweep_5000MHz_IQMixerCalibrated'

### IQ Sweep data from LabVIEW folder and filename
###
###
sweepdata_folder = "../../../MeasurementResult/20160814_Al_Noguchi/"
###
###
###
sweeplist_file = 'sweeplist'
sweeplist = []
with open(sweepdata_folder + sweeplist_file + '.txt','r') as f:
    for line in f:
        sweeplist.append(line.replace("\n", ""))
        
 
f = open(sweepdata_folder + 'resfreqlist' + '.txt', 'w')
for sweepdata_filename in sweeplist:
    fr = FitSingle.GetFr(sweepdata_folder, sweepdata_filename, IQCalibrationfile, IQReffolder, IQReffilename)
    print fr
    f.write(str(fr/1e6) + '\n')
f.close()

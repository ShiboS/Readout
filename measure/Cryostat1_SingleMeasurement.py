# Calibrate VNA first
# With Ecal N4691-60001
import Instrument.E5071C as inst0
import Instrument.LS370 as inst1
import Measurement_Function as meas
VNA = inst0.E5071()
LS370 = inst1.LS370()

### Check connection with instruments
VNA.whoareyou()
LS370.whoareyou()

folder = "20160227_OMT/"   
meas.Save_KID_Cryostat1(folder)
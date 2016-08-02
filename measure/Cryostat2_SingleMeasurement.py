# Calibrate VNA first
# With Ecal N4691-60001
import Instrument.E5071C as inst0
import Instrument.LS350 as inst1
import Measurement_Function as meas
VNA = inst0.E5071()
LS350 = inst1.LS350()

### Check connection with instruments
VNA.whoareyou()
LS350.whoareyou()

folder = "20160227_OMT/"   
meas.Save_KID_Cryostat2(folder)
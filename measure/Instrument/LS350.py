# For Lake Shore 350
import visa
import numpy as np
rm = visa.ResourceManager()

class LS350():
    def __init__(self, address=12):
        self.ctrl = rm.open_resource("GPIB0::%s::INSTR" %address)

    def whoareyou(self):
        print self.ctrl.query("*IDN?")
        
    def SetPoint(self, Temp):
        self.ctrl.write("SETP 2, %s" %Temp)

    def SetHeaterRange(self, Range):
        self.ctrl.write("RANGE 2, %s" %Range)

    def SetPID(self, P, I, D):
        self.ctrl.write("PID 2, %s, %s, %s" %P %I %D)

# Query
    def GetTemp(self, Channel):
        return self.ctrl.query("KRDG? %s" %Channel)

    def GetPID(self):
        return self.ctrl.query('PID?')

    def GetSetPoint(self, Channel):
        return self.ctrl.query("SETP? %s" %Channel)
    
    def GetHeaterRange(self, Channel):
        self.ctrl.query("RANGE? %s" %Channel)
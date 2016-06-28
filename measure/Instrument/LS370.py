# For Lake Shore 370
import visa
import numpy as np
rm = visa.ResourceManager()

class LS370():
    def __init__(self, address=12):
        self.ctrl = rm.open_resource("GPIB0::%s::INSTR" %address)

    def whoareyou(self):
        print self.ctrl.query("*IDN?")
        
    def SetTempControl(self, Channel):
        self.ctrl.write("CSET %s, 0, 1, 3, 2, 8, 100" %Channel)
    
    def SetPoint(self, Temp):
        self.ctrl.write("SETP %sK" %Temp)

    def SetHeaterRange(self, Range):
        self.ctrl.write("HTRRNG %s" %Range)

    def SetPID(self, P, I, D):
        self.ctrl.write("PID %s, %s, %s" %P %I %D)

# Query
    def GetTemp(self, Channel):
        return self.ctrl.query("RDGK? %s" %Channel)

    def GetPID(self):
        return self.ctrl.query('PID?')

    def GetSetPoint(self, Channel):
        return self.ctrl.query("SETP? %s" %Channel)
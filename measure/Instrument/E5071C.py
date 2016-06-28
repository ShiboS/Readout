# For Agilent ENA E5071C GPIB
import visa
rm = visa.ResourceManager()

class E5071():
    def __init__(self, address=17):
        self.ctrl = rm.open_resource("GPIB0::%s::INSTR" %address)

    def whoareyou(self):
        print self.ctrl.query("*IDN?")

    def SetMeasurement(self, Para):
        self.ctrl.write(":CALC1:PAR1:DEF %s" %Para)

    def SetOutP(self, Para):
        self.ctrl.write(":OUTP %s" %Para)

    def SetPower(self, power):
        self.ctrl.write(":SOUR1:POW %s" %power)

    def SetNumPoint(self, NumPoint):
        self.ctrl.write(":SENS1:SWE:POIN %s" %NumPoint)

    def SetIFBdw(self, IFBdw):
        self.ctrl.write(":SENS1:BAND %s" %IFBdw)

    def SetStartFreq(self, StartFreq):
        self.ctrl.write(":SENS1:FREQ:STAR %s" %StartFreq)

    def SetStopFreq(self, StopFreq):
        self.ctrl.write(":SENS1:FREQ:STOP %s" %StopFreq)

    def SetCenterFreq(self, CenterFreq):
        self.ctrl.write(":SENS1:FREQ:CENT %s" %CenterFreq)

    def SetSpanFreq(self, SpanFreq):
        self.ctrl.write(":SENS1:FREQ:SPAN %s" %SpanFreq)

    def SetAverageFactor(self, AverageFactor):
        self.ctrl.write(":SENS1:AVER:COUN %s" %AverageFactor)

    def SetAveraging(self, Status):
        self.ctrl.write(":SENS1:AVER %s" %Status)

    def SetSmoothing(self, Status):
        self.ctrl.write(":CALC1:SMO:STAT %s" %Status)

    def SetFormat(self, Format):
        self.ctrl.write(":CALC1:FORM %s" %Format)
        
    def SetElectricalDelay(self, Delay):
        self.ctrl.write(":CALC1:CORR:EDEL:TIME %s" %Delay)
        
    def SetAutoScale(self):
        self.ctrl.write(":DISP:WIND1:TRAC1:Y:AUTO")
# Query
    def GetPower(self):
        return self.ctrl.query(":SOUR1:POW?")

    def GetNumPoint(self):
        return self.ctrl.query(":SENS1:SWE:POIN?")

    def GetIFBdw(self):
        return self.ctrl.query(":SENS1:BAND?")

    def GetStartFreq(self):
        return self.ctrl.query(":SENS1:FREQ:STAR?")

    def GetStopFreq(self):
        return self.ctrl.query(":SENS1:FREQ:STOP?")

    def GetCenterFreq(self):
        return self.ctrl.query(":SENS1:FREQ:CENT?")

    def GetSpanFreq(self):
        return self.ctrl.query(":SENS1:FREQ:SPAN?")

    def GetElectricalDelay(self):
        return self.ctrl.query(":CALC1:CORR:EDEL:TIME?")
        
    def GetFreqData(self):
        self.ctrl.write(":FORM:DATA REAL")
        return self.ctrl.query_binary_values(":SENS1:FREQ:DATA?", "d", True)

    def GetTraceData(self):
        self.ctrl.write(":FORM:DATA REAL")
        return self.ctrl.query_binary_values(":CALC1:DATA:FDAT?", "d", True)
        
# Marker
    def Marker(self, Freq):
        self.ctrl.write(":CALC1:MARK1:X %s" %Freq)

    def MarkerSearch(self, Type):
        self.ctrl.write(":CALC1:MARK1:FUNC:TYPE %s" %Type)

    def MarkerFunc(self, Func):
        self.ctrl.write(":CALC1:MARK1:SET %s" %Func)
        
    def MarkerSearchExecute(self):
        self.ctrl.write(":CALC1:MARK1:FUNC:EXEC")
import CSV_split
import Analyse_Fit_ListKID as FitList
import Analyse_Plot_ListKID_Temperature as PlotTemperature

###   Edit these two
#     Be care of the date if the measurement was done overnight.
folder = "../../../MeasurementResult/20160729_OMTdelta/"
date = "20160729"

###   KID span for during analysis
span = 1e6

CSV_split.CSV_Split(folder, date)
FitList.Fit_List_KIDs(folder, date, span)
PlotTemperature.Plot_Temperature(folder, date)
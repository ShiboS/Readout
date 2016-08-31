import CSV_Split as CSV_Split
import Analyse_Fit_ListKID as FitList
import Analyse_Plot_ListKID_Temperature as PlotTemperature

###   Edit these two
#     "list" and "parameter" files will be read automaticaly
#      with the input folder and date.
#     Be care of the date in the files if the measurement was done overnight.

folder = "../../../MeasurementResult/20160812_nakamura_Al/"
date = "20160813"

###   KID span during analysis
#     Usually measurement span is 2e6
#     and here it is cutted to smaller span, for example 1e6.
#     Smaller span could give higher accuracy during fitting.
#     For high frequency (~7 Ghz), 1e6 may be small.

span = 1e6

CSV_Split.CSV_Split(folder, date)
FitList.Fit_List_KIDs(folder, date, span)
PlotTemperature.Plot_Temperature(folder, date)
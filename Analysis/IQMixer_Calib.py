import csv
import Fitter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle
 
folder ='../../Device Data/IQMixer/Calibration Data/20160726_BOX_FirstCalibration/'
RF_Power = '0dBm'
RF_Freq_Start = 2000# MHz
RF_Freq_End = 8000 # MHz
RF_Freq_Interval = 10 # MHz, RF measurement sample every 10 MHz
ellipse_array = []
mixer_para_array = []

### Name of file, to be saved
fit_file_name = 'EllipseFit_' + str(RF_Power) + '_' + str(RF_Freq_Start) + 'MHz' + '_' + str(RF_Freq_End) + 'MHz'

### PDF figure 
with PdfPages(folder + fit_file_name + '.pdf') as pdf:
    ### analyze every frequency file in this loop and save df figure
    for freq in range(RF_Freq_Start/RF_Freq_Interval, RF_Freq_End/RF_Freq_Interval+1):
        ### read this file
        name_of_file = RF_Power + '_' + str(freq*10) + 'MHz.csv'
        result = []
        with open(folder + name_of_file,'r') as f:
            for line in f:
                result.append(map(str,line.split(',')))

        I = [float(result[i][1]) for i in range(0,len(result))]
        Q = [float(result[i][2].replace("\n", "")) for i in range(0,len(result))]
        ### fit I, Q with lmfit and get five values and their 1-sigma standard error
        x_c, x_c_err, y_c, y_c_err, x_dim, x_dim_err, y_dim, y_dim_err, angle, angle_err = Fitter.Fit_Ellipse(I,Q)
        ellipse_array.append([x_c, x_c_err, y_c, y_c_err, x_dim, x_dim_err, y_dim, y_dim_err, angle, angle_err])
        
        ###
        A_I = np.sqrt(x_dim**2 * np.cos(angle)**2 + y_dim**2 * np.sin(angle)**2)
        A_Q = np.sqrt(x_dim**2 * np.sin(angle)**2 + y_dim**2 * np.cos(angle)**2)
        alpha_1 = np.arctan2(y_dim*np.sin(angle), x_dim*np.cos(angle))
        alpha_2 = np.pi - np.arctan2(y_dim*np.cos(angle), x_dim*np.sin(angle))
        gamma = alpha_1 - alpha_2
        mixer_para_array.append([A_I, A_Q, alpha_1, alpha_2, gamma])
        
        ### fit result and plot data
        Fitter.plot_data_ellipse(I,Q, x_c, y_c, x_dim, y_dim, angle)
        plt.gca().add_patch(Rectangle((x_c-A_I, y_c-A_Q), 2*A_I, 2*A_Q, fill=None, alpha=1))
        plt.plot([x_c+x_dim*np.cos(angle), x_c-x_dim*np.cos(angle)], [y_c-x_dim*np.sin(angle), y_c+x_dim*np.sin(angle)], 'b-', lw=2)
        plt.plot([x_c+y_dim*np.sin(angle), x_c-y_dim*np.sin(angle)], [y_c+y_dim*np.cos(angle), y_c-y_dim*np.cos(angle)], 'b-', lw=2)
        plt.plot()
        ### title for each figure with RF frequency
        plt.title(str(freq*10) + 'MHz')
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()
        #plt.show()

### save fitting result
fitfile = open(folder + fit_file_name + '.csv', 'w')
fwrite = csv.writer(fitfile)
fwrite.writerow(('freq MHz', 'x_c', 'x_c_err', 'y_c', 'y_c_err', 'x_r', 'x_r_err', 'y_r', 'y_r_err', 'angle', 'angle_err', 'A_I', 'A_Q', 'alpha_1', 'alpha_2', 'gamma'))
for i in range(0, len(ellipse_array)):
    fwrite.writerow([str(RF_Freq_Start+RF_Freq_Interval*i), ellipse_array[i][0], ellipse_array[i][1], ellipse_array[i][2], ellipse_array[i][3], ellipse_array[i][4], ellipse_array[i][5], ellipse_array[i][6], ellipse_array[i][7], ellipse_array[i][8], ellipse_array[i][9], mixer_para_array[i][0], mixer_para_array[i][1], mixer_para_array[i][2], mixer_para_array[i][3], mixer_para_array[i][4]])
fitfile.close()
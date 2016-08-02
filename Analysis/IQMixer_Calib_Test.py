import Fitter
import numpy as np
import matplotlib.pyplot as plt
from lmfit import minimize, Parameters, fit_report

### Read file
name_of_file = '../../Device Data/IQMixer/Calibration Data/20160726_BOX_FirstCalibration/0dBm_2300MHz.csv'

result = []

with open(name_of_file,'r') as f:
    for line in f:
        result.append(map(str,line.split(',')))

I = [float(result[i][1]) for i in range(0,len(result))]
Q = [float(result[i][2].replace("\n", "")) for i in range(0,len(result))]
def EllipseFit(params, I, Q):
    x_c = params['x_c'].value
    y_c = params['y_c'].value
    x_dim = params['x_dim'].value
    y_dim = params['y_dim'].value
    angle = params['angle'].value

    DataDis = np.sqrt((I-x_c)**2 + (Q-y_c)**2)
    DataAngle = np.arctan2(Q-y_c, I-x_c)
    Angle = DataAngle+angle
    r = np.sqrt((x_dim**2*y_dim**2)/((x_dim*np.sin(Angle))**2 + (y_dim*np.cos(Angle))**2))
    residual = DataDis-r
    return residual
    
# create a set of Parameters
params = Parameters()
params.add('x_c', value= 0, min = -0.2, max = 0.2)
params.add('y_c', value= 0, min = -0.2, max = 0.2)
params.add('x_dim', value= 0.1, min = 0.01, max = 0.3)
params.add('y_dim', value= 0.1, min = 0.01, max = 0.3)
params.add('angle', value= -0.2, min = -np.pi, max = np.pi)

# do fit, here with leastsq model
result = minimize(EllipseFit, params, args=(I, Q))
print(fit_report(result))

Fitter.plot_data_ellipse(I,Q, result.params['x_c'].value, result.params['y_c'].value, result.params['x_dim'].value, result.params['y_dim'].value, result.params['angle'].value)
plt.show()
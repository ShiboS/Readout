import numpy as np
from matplotlib import pyplot as plt, cm, colors
from lmfit import minimize, Parameters, fit_report

def Fit_Circle_Func(params, x, y):
    xc = params['xc'].value
    yc = params['yc'].value
    R = params['R'].value
    model = np.sqrt((x-xc)**2 + (y-yc)**2)-R
    return model

def Fit_Circle(x, y):
    # create a set of Parameters
    params = Parameters()
    params.add('xc', value= np.mean(x))
    params.add('yc', value= np.mean(y))
    params.add('R', value= np.max(x) - np.mean(x))
    
    # do fit, here with leastsq model
    result = minimize(Fit_Circle_Func, params, args=(x, y))
    
    # calculate final result
    residual = result.residual
    
    # Calculate Qc and Qi
    xc = result.params['xc'].value
    xc_err = np.abs(result.params['xc'].stderr/xc)
    yc = result.params['yc'].value
    yc_err = np.abs(result.params['yc'].stderr/yc)
    R = result.params['R'].value
    R_err = result.params['R'].stderr/R
    
    return xc, xc_err, yc, yc_err, R, R_err, fit_report(result)

def plot_data_circle(x,y, xc, yc, R):
    f = plt.figure( facecolor='white')  #figsize=(7, 5.4), dpi=72,
    plt.axis('equal')

    theta_fit = np.linspace(-np.pi, np.pi, 180)

    x_fit = xc + R*np.cos(theta_fit)
    y_fit = yc + R*np.sin(theta_fit)
    plt.plot(x_fit, y_fit, 'b-' , label="fitted circle", lw=2)
    plt.plot([xc], [yc], 'bD', mec='y', mew=1)
    plt.xlabel('x')
    plt.ylabel('y')   
    # plot data
    plt.plot(x, y, 'r-.', label='data', mew=1)

    plt.legend(loc='best',labelspacing=0.1 )
    plt.grid()
    plt.title('Least Squares Circle')

def Fit_Ellipse_Func(params, I, Q):
    ### Ref: www.nlreg.com/ellipse.htm
    x_c = params['x_c'].value
    y_c = params['y_c'].value
    x_dim = params['x_dim'].value
    y_dim = params['y_dim'].value
    angle = params['angle'].value
    # distance from data point to ellipse center
    DataDis = np.sqrt((I-x_c)**2 + (Q-y_c)**2)
    # data angle to the center of ellipse
    DataAngle = np.arctan2(Q-y_c, I-x_c)
    # data angle plus tilt angle
    Angle = DataAngle+angle
    # distance of model data point to the center of ellipse
    r = np.sqrt((x_dim**2*y_dim**2)/((x_dim*np.sin(Angle))**2 + (y_dim*np.cos(Angle))**2))
    # return the residual
    residual = DataDis-r
    return residual
    
def Fit_Ellipse(I,Q):
    # from data to find the initial value
    I_average = sum(I) / float(len(I))
    Q_average = sum(Q) / float(len(Q))
    I_pktopk = (max(I) - min(I))/2.
    Q_pktopk = (max(Q) - min(Q))/2.
    # create a set of Parameters
    params = Parameters()
    # range for fitting for each parameter, please edit the range or delete them
    # x_c, y_c: center of ellipse
    # x_dim, y_dim: half long axis and half short axis
    # angle: tilt angle of ellipse
    # CAUTION: angle is determined by the relation of x_dim and y_dim. When x_dim and y_dim are very close, the angle value may be changed by -1.
    #          The result is always correct but the angle may be timed with -1
    params.add('x_c', value= I_average, min = -0.2, max = 0.2)
    params.add('y_c', value= Q_average, min = -0.2, max = 0.2)
    params.add('x_dim', value= I_pktopk, min = 0.001, max = 0.2)
    params.add('y_dim', value= Q_pktopk, min = 0.001, max = 0.2)
    params.add('angle', value= 0, min = -1, max = 1)

    # do fit, here with leastsq model
    result = minimize(Fit_Ellipse_Func, params, args=(I, Q))
    # print the fitting result
    print(fit_report(result))
    # get fitted value and 1 sigma error value
    x_c = result.params['x_c'].value
    x_c_err = result.params['x_c'].stderr
    y_c = result.params['y_c'].value
    y_c_err = result.params['y_c'].stderr
    x_dim = result.params['x_dim'].value
    x_dim_err = result.params['x_dim'].stderr
    y_dim = result.params['y_dim'].value
    y_dim_err = result.params['y_dim'].stderr
    angle = result.params['angle'].value
    angle_err = result.params['angle'].stderr
    return x_c, x_c_err, y_c, y_c_err, x_dim, x_dim_err, y_dim, y_dim_err, angle, angle_err

def plot_data_ellipse(x,y, x_c, y_c, x_dim, y_dim, angle):
    # plot ellipse data to compare with fitting result
    # x, y: initial data
    # x_c, y_c, x_dim, y_dim, angle: fitting result
    f = plt.figure( facecolor='white')
    plt.axis('equal')

    theta_fit = np.linspace(-np.pi, np.pi, 180)

    x_fit = x_c + x_dim*np.cos(theta_fit)*np.cos(angle) + y_dim*np.sin(theta_fit)*np.sin(angle)
    y_fit = y_c + y_dim*np.sin(theta_fit)*np.cos(angle) - x_dim*np.cos(theta_fit)*np.sin(angle)
    plt.plot(x_fit, y_fit, 'b-' , label="fitted circle", lw=2)
    plt.plot([x_c], [y_c], 'bD', mec='y', mew=1)
    plt.xlabel('x')
    plt.ylabel('y')   
    # plot data
    plt.plot(x, y, 'r-.', label='data', mew=1)

    plt.legend(loc='best',labelspacing=0.1 )
    plt.grid()
    plt.title('Least Squares Ellipse')

def Fit_Phase_Func(params, freq, phase_c):
    """ PhaseFit test"""
    theta0 = params['theta0'].value
    Q_r = params['Q_r'].value
    f_r = params['f_r'].value
    model = -theta0 + 2*np.arctan(2 * Q_r * (1-freq/f_r))
    return model - phase_c

def Fit_Phase(freq, phase, para_guess):
    # create a set of Parameters
    params = Parameters()
    params.add('theta0', value= para_guess[0], min = -np.pi, max = np.pi)
    params.add('f_r', value= para_guess[1], min = 1e9, max= 8e9)
    params.add('Q_r', value= para_guess[2], min = 1e3, max = 5e7)
    
    # do fit, here with leastsq model
    result = minimize(Fit_Phase_Func, params, args=(freq, phase))
    
    # calculate final result
    final = phase + result.residual
    
    # Calculate Qc and Qi
    theta0 = result.params['theta0'].value
    theta0_err = np.abs(result.params['theta0'].stderr/theta0)
    fr = result.params['f_r'].value
    fr_err = result.params['f_r'].stderr/fr
    Qr = result.params['Q_r'].value
    Qr_err = result.params['Q_r'].stderr/Qr
    
    return theta0, theta0_err, fr, fr_err, Qr, Qr_err, fit_report(result)
    
def Fit_Million_Func(params, freq, t):
    a =    params['a'].value
    phi0 = params['phi0'].value
    Qi =   params['Qi'].value
    Qc_scaled = params['Qc_scaled'].value
    fr =   params['fr'].value
    aphi0 = params['aphi0'].value

    func = a * (1 + Qi/Qc_scaled * np.exp(1j*phi0) * 1/(1 + 1j*2*Qi*(freq/fr-1)))* np.exp(1j*aphi0)
    residual = np.abs(func - t)
    return residual
    
def Fit_Million(freq, t, para_guess):
    # Planar superconducting resonators with internal quality factors above one million
    params = Parameters()
    params.add('a', value= para_guess[0], min = -100, max = 3000)
    params.add('phi0', value= para_guess[1], min = -np.pi, max = np.pi)
    params.add('Qi', value= para_guess[2], min = 1e3, max = 1e8)
    params.add('Qc_scaled', value= para_guess[3], min = 1e2, max = 1e8)
    params.add('fr', value= para_guess[4], min = freq[0], max = freq[len(freq)-1])
    params.add('aphi0', value= para_guess[5], min = -np.pi, max = np.pi)

    # do fit, here with leastsq model
    result = minimize(Fit_Million_Func, params, args=(freq, t))
    
    a = result.params['a'].value
    a_err = result.params['a'].stderr
    phi0 = result.params['phi0'].value
    phi0_err = result.params['phi0'].stderr
    Qi = result.params['Qi'].value
    Qi_err = result.params['Qi'].stderr
    Qc_scaled = result.params['Qc_scaled'].value
    Qc_scaled_err = result.params['Qc_scaled'].stderr
    fr = result.params['fr'].value
    fr_err = result.params['fr'].stderr
    aphi0 = result.params['aphi0'].value
    aphi0_err = result.params['aphi0'].stderr

    # print the fitting result
    print(fit_report(result))
    return a, a_err, phi0, phi0_err, Qi, Qi_err, Qc_scaled, Qc_scaled_err, fr, fr_err, aphi0, aphi0_err, result
    
def Fit_SkewedLorentizian_Func(params, f, t):
    A1 = params['A1'].value
    A2 = params['A2'].value
    A3 = params['A3'].value
    A4 = params['A4'].value
    fr = params['fr'].value
    Qr = params['Qr'].value

    func = 10*np.log10(A1 + A2*(f-fr) + (A3 + A4*(f-fr))/(1 + 4*Qr*Qr*((f-fr)/fr)**2))
    # return the residual
    residual = func - t
    return residual
    
def Fit_SkewedLorentizian(f,t):
    params = Parameters()
    params.add('A1', value = t[0], min = -50, max = 30) # Background
    params.add('A2', value = 0)#, min = -0.5, max = 0.5)  # Slope
    params.add('A3', value = np.amin(t))#, min = -60, max = 30)    # Lowest point
    params.add('A4', value = 0)
    params.add('fr', value = np.median(f), min = 1e9, max = 8e9)
    params.add('Qr', value = 10000, min = 1e3, max = 1e8)
    result = minimize(Fit_SkewedLorentizian_Func, params, args=(f, t))
    
    # print the fitting result
    print(fit_report(result))
    # get fitted value and 1 sigma error value
    A1 = result.params['A1'].value
    A1_err = result.params['A1'].stderr
    A2 = result.params['A2'].value
    A2_err = result.params['A2'].stderr
    A3 = result.params['A3'].value
    A3_err = result.params['A3'].stderr
    A4 = result.params['A4'].value
    A4_err = result.params['A4'].stderr
    fr = result.params['fr'].value
    fr_err = result.params['fr'].stderr
    Qr = result.params['Qr'].value
    Qr_err = result.params['Qr'].stderr
    return A1, A1_err, A2, A2_err, A3, A3_err, A4, A4_err, fr, fr_err, Qr, Qr_err, fit_report(result)
    
def Fit_7para_Func(params, freq, t):
    a = params['a'].value
    alpha = params['alpha'].value
    tau = params['tau'].value
    phi0 = params['phi0'].value
    fr = params['fr'].value
    Qr = params['Qr'].value
    Qc = params['Qc'].value

    func = a * np.exp(1j*alpha) * np.exp(-2*np.pi*1j*freq*tau) * (1 - (Qr/Qc*np.exp(1j*phi0))/(1 + 2*1j*Qr*(freq-fr)/fr))
    # return the residual
    residual = np.abs(func - t)
    return residual
    
def Fit_7para(freq,t,estimateparas):
    params = Parameters()
    params.add('a', value = estimateparas[0])#, min = -50, max = 50)
    params.add('alpha', value = estimateparas[1], min = -np.pi, max = np.pi)
    params.add('tau', value = estimateparas[2], min = 0e-9, max = 80e-9)
    params.add('phi0', value = estimateparas[3], min = -np.pi, max = np.pi)
    params.add('fr', value = estimateparas[4], min = freq[0], max = freq[len(freq)-1])
    params.add('Qr', value = estimateparas[5], min = 1e3, max = 1e8)
    params.add('Qc', value = estimateparas[6], min = 1e3, max = 1e8)
    result = minimize(Fit_7para_Func, params, args=(freq, t))
    
    # print the fitting result
    print(fit_report(result))
    # get fitted value and 1 sigma error value
    a = result.params['a'].value
    a_err = result.params['a'].stderr
    alpha = result.params['alpha'].value
    alpha_err = result.params['alpha'].stderr
    tau = result.params['tau'].value
    tau_err = result.params['tau'].stderr
    phi0 = result.params['phi0'].value
    phi0_err = result.params['phi0'].stderr
    fr = result.params['fr'].value
    fr_err = result.params['fr'].stderr
    Qr = result.params['Qr'].value
    Qr_err = result.params['Qr'].stderr
    Qc = result.params['Qc'].value
    Qc_err = result.params['Qc'].stderr
    return a, a_err, alpha, alpha_err, tau, tau_err, phi0, phi0_err, fr, fr_err, Qr, Qr_err, Qc, Qc_err,fit_report(result)

def Fit_7para_tau(freq,t,estimateparas):
    params = Parameters()
    params.add('a', value = estimateparas[0])#, min = -50, max = 50)
    params.add('alpha', value = estimateparas[1], min = -np.pi, max = np.pi)
    params.add('tau', value = estimateparas[2], vary = False)
    params.add('phi0', value = estimateparas[3], min = -2*np.pi, max = 2*np.pi)
    params.add('fr', value = estimateparas[4], min = freq[0], max = freq[len(freq)-1])
    params.add('Qr', value = estimateparas[5], min = 1e3, max = 1e8)
    params.add('Qc', value = estimateparas[6], min = 1e3, max = 1e8)
    result = minimize(Fit_7para_Func, params, args=(freq, t))
    
    # print the fitting result
    print(fit_report(result))
    # get fitted value and 1 sigma error value
    a = result.params['a'].value
    a_err = result.params['a'].stderr
    alpha = result.params['alpha'].value
    alpha_err = result.params['alpha'].stderr
    tau = result.params['tau'].value
    tau_err = result.params['tau'].stderr
    phi0 = result.params['phi0'].value
    phi0_err = result.params['phi0'].stderr
    fr = result.params['fr'].value
    fr_err = result.params['fr'].stderr
    Qr = result.params['Qr'].value
    Qr_err = result.params['Qr'].stderr
    Qc = result.params['Qc'].value
    Qc_err = result.params['Qc'].stderr
    return a, a_err, alpha, alpha_err, tau, tau_err, phi0, phi0_err, fr, fr_err, Qr, Qr_err, Qc, Qc_err,fit_report(result)
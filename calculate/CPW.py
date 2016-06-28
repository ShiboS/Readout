import numpy as np
from scipy.constants import mu_0, pi, epsilon_0
from scipy.special import ellipk # Elliptic integral

def kparameter(CPW_C, CPW_G, Die_thickness):
    # CPW k parameter
    k = CPW_C / (CPW_C+CPW_G*2)
    k_1 = np.sinh(pi*CPW_C/4/Die_thickness)/np.sinh(pi*(CPW_C+2*CPW_G)/4/Die_thickness)
    k_prime = np.sqrt(1-k*k)
    # CPW k_prime parameter
    k_1_prime = np.sqrt(1-k_1*k_1) 
    # The definition of elliptic integral function is different. In scipy it is m number, but here is modulus k
    K_k = ellipk(k*k)                 
    K_k_prime = ellipk(k_prime*k_prime)
    
    # for calculating dielectric loss
    K_k_1 = ellipk(k_1*k_1)
    K_k_1_prime = ellipk(k_1_prime*k_1_prime)
    q = 0.5 * K_k_prime*K_k_1/K_k_1_prime/K_k # filling factor
    return k, k_prime, k_1, k_1_prime, K_k, K_k_prime, K_k_1, K_k_1_prime, q

def GeoFactor(CPW_C, CPW_G, thickness, k, K_k):
    # Geometric factor g_c (center) and g_g (ground)
    if (thickness < CPW_C/20.0) and (k<0.8):
        g_c = 1.0/(4.0*CPW_C*(1.0-k*k)*(K_k**2.0))*(pi+np.log(4.0*pi*CPW_C/thickness)-k*np.log((1.0+k)/(1.0-k)))
        g_g = k/(4.0*CPW_C*(1.0-k*k)*(K_k**2.0))*(pi+np.log(4.0*pi*(CPW_C+2*CPW_G)/thickness)-(1.0/k)*np.log((1.0+k)/(1.0-k)))
        
    else:
        print "!!!!!!!!!!!!!!!!!thickness > CPW_C/20.0!!!!!!!!!!!!!!!!!!!"
        g_c = 1.0/(4.0*CPW_C*(1.0-k*k)*(K_k**2.0))*(pi+np.log(4.0*pi*CPW_C/thickness)-k*np.log((1.0+k)/(1.0-k)))
        g_g = k/(4.0*CPW_C*(1.0-k*k)*(K_k**2.0))*(pi+np.log(4.0*pi*(CPW_C+2*CPW_G)/thickness)-(1.0/k)*np.log((1.0+k)/(1.0-k)))
    return g_c, g_g

def EffEpsilon(epsilon):
    epsilon_eff = (1.0+epsilon)/2.0
    return epsilon_eff

def GeoInductance(K_k_prime, K_k):
    L_g = mu_0*K_k_prime/K_k/4.0
    return L_g

def GeoCapacitance(epsilon_eff, K_k, K_k_prime):
    C_l = 4.0*epsilon_0*epsilon_eff*K_k/K_k_prime
    return C_l

### For CPW with same material for central and ground part
def Imp_Simple(CPW_C, CPW_G, epsilon, thickness, R_s, L_s):
    # Default parameter: substrate thickness: 350um
    Die_thickness = 350e-6
    k, k_prime, k_1, k_1_prime, K_k, K_k_prime, K_k_1, K_k_1_prime, q = kparameter(CPW_C, CPW_G, Die_thickness)
    
    ### Inductance, capcitance and impedance
    # Geometric inductance
    L_g = GeoInductance(K_k_prime, K_k)
    # Effective epsilon
    epsilon_eff = EffEpsilon(epsilon)
    # Geometric capcitance
    C_l = GeoCapacitance(epsilon_eff, K_k, K_k_prime)
    
    # Geometric factor g_c (center) and g_g (ground)
    g_c, g_g = GeoFactor(CPW_C, CPW_G, thickness, k, K_k)
    
    # Kinetic inductance
    L_k = g_c*L_s + g_g*L_s
    
    L = L_g + L_k
    # Line impedace
    impedance = np.sqrt(L/C_l)
    # Kinetic inductance ratio
    alpha = L_k / L
    # Attenuation alpha
    atten_alpha = (R_s*g_c + R_s*g_g)/2./ impedance
    return impedance, alpha, atten_alpha
    
def Imp_Hybrid(CPW_C, CPW_G, epsilon, C_thickness, G_thickness, C_R_s, C_L_s, G_R_s, G_L_s):
    # Default parameter: substrate thickness: 350um
    Die_thickness = 350e-6
    k, k_prime, k_1, k_1_prime, K_k, K_k_prime, K_k_1, K_k_1_prime, q = kparameter(CPW_C, CPW_G, Die_thickness)
    
    ### Inductance, capcitance and impedance
    # Geometric inductance
    L_g = GeoInductance(K_k_prime, K_k)
    # Effective epsilon
    epsilon_eff = EffEpsilon(epsilon)
    # Geometric capcitance
    C_l = GeoCapacitance(epsilon_eff, K_k, K_k_prime)
    
    # Geometric factor g_c (center) and g_g (ground)
    # Always ground plane is thicker, so we use ground thickness here to check its relation with CPW geometry
    g_c, g_g = GeoFactor(CPW_C, CPW_G, G_thickness, k, K_k)
    
    # Kinetic inductance Visser P74
    L_k = g_c*C_L_s + g_g*G_L_s
    L = L_g + L_k
    L_k_ratio = g_c*C_L_s/L_k
    # Line impedace
    impedance = np.sqrt(L/C_l)
    # Attenuation alpha
    atten_alpha = (C_R_s*g_c + G_R_s*g_g)/2./ impedance
    # Kinetic inductance ratio
    alpha = L_k / L
    
    return impedance, alpha, L_k_ratio, atten_alpha
### Working directory
import sys
import site
site.addsitedir('/Users/lauraelsler/Dropbox/current_projects/VENICE/CODE')
sys.path

#### Modules
import numpy as np
from parameters import *

############### Initialize variables ###############################
M = np.zeros(tmax) # area of salt marshes
G = np.zeros(tmax) # area of seagrass beds
F_dam = np.zeros(tmax) # flood damage
B_val = np.zeros(tmax) # value of biotope
preF = np.zeros(tmax) # preferences in flood protection
W = np.zeros(tmax) # principal welfare
UTILITY = np.zeros(tmax) # Utility of the population
Inv_f_p = np.zeros(tmax) # investment in flood protection
Inv_b_p = np.zeros(tmax) # investment in biotopes
Inv_potF = np.zeros(tmax) # open investment in flood protection
Inv_potB = np.zeros(tmax) # open investment in biotopes
C_preF = np.zeros(tmax) # preferences in flood protection
C_pot = np.zeros(tmax) # funding of concessionaire
A_preG = np.zeros(tmax) # government responsiveness to lobbying
A_preF = np.zeros(tmax) # preferences in flood protection
Inv_f_a = np.zeros(tmax) # decision-maker investment in flood protection
Inv_b_a = np.zeros(tmax) # decision-maker investment in biotopes
TIME = np.arange(1970,2050,1) # for plots

#! Costs of floods (no investment and with: $K)
costs_f1  = np.array([0,0,0,0,0,0,0,521640,6492555,21452445,64348020,125761815,164987280,176202540, \
    181586610,182434275,182639205,182881395])
costs_f2  = np.array([0,0,0,0,0,0,0,0,0,0,370000,370000,370000,370000,370000, \
    370000,370000,370000])
costs_tot_noinv  = costs_f1 + costs_f2
costs_tot_yesinv = costs_f1 + costs_f2
costs_tot_yesinv[11:] = 0

#! Initial conditions
M[0] = M0
G[0] = G0
Inv_f_p[0] = pot/2
Inv_b_p[0] = pot/2
pre_past = 0.5
Bampl =  1
preF[-1:0] = 0.5
Inv_f_a[0] = pot/2
Inv_b_a[0] = pot/2
A_preG[-1:0] = 0

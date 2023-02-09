#### Routines (Modules)

#! Modules
from parameters import * # get all parameters
import csv
import os.path
from matplotlib import pyplot as plt
from scipy import stats
import numpy as np
import matplotlib.patches as mpatches
from numpy import genfromtxt


#### Social
## PRINCIPAL
#! Preferences

def func_Ppref(B_val, M_max, M_st, M_fl, G_max, G_st, G_fl, F_dam, F_dam0, preF): # load whole array F_dam
    B_delta = (M_max * M_st) + (M_max * M_fl * 1) + (G_max * G_st) + (G_max * G_fl * 1) - (B_val) # difference current state to a desirable level
    F_delta = F_dam0- np.sum(F_dam) # difference current state to a desirable level
    I_delta = abs(B_delta) + abs(F_delta)
    preF = preF - (1 - pre_past) * preF + (1-pre_past) * (F_dam/(B_val + F_dam))+((abs(F_delta)/ I_delta))
    return preF

## CONCESSIONAIRE
#! calculation of investment preferences
def func_Cinv(sum_invf, F_thr, M, M_max, G, G_max, share_b, share_f): # Inv_f whole array, M, G at [time]
    Inv_potF = (F_thr - sum_invf)* share_f
    Inv_potB = ((G_max - G) * p_m + (M_max - M) * p_m) * share_b # share_b = percentage of works which go to the concessionaire
    if  Inv_potB <= 0:
        C_preF = 0
    elif Inv_potB <= Inv_potF:
        C_preF = 1
    elif Inv_potB > Inv_potF:
        C_preF = 0
    return C_preF

##def func_Cinv(sum_invf, F_thr, M, M_max, G, G_max, share_b, share_f, preF, w): # Inv_f whole array, M, G at [time]
##    Inv_potF = (F_thr - sum_invf)* share_f
##    Inv_potB = ((G_max - G) * p_m + (M_max - M) * p_m) * share_b # share_b = percentage of works which go to the concessionaire
##    if Inv_potB < Inv_potF:
##        C_preF = (1-w) * 1 + w * (preF)
##    else:
##        C_preF = (1-w) * 0 + w * (preF)
##    return C_preF

## AGENT
def func_Ainv(C_pay, preF,  C_preF, pot, time, A_preG):
	if C_pay[time] > C_pay[time-1]:
            A_preG= A_preG+ f_preG
        else:
            A_preG= A_preG- f_preG
	f_a = A_preG * (C_preF/ 100) + (1 - A_preG) * preF
	Inv_f_a = f_a * pot
	Inv_b_a = pot - Inv_f_a
	return Inv_f_a, Inv_b_a, A_preG

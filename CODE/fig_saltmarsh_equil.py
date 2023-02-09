### Working directory
import sys
import os
import site
site.addsitedir('/Users/lauraelsler/Dropbox/current_projects/VENICE/CODE') # add repo to check
sys.path # all repos
os.getcwd() # working directory

#### Modules
import numpy as np
import matplotlib.pylab as plt

#### Stuff to run the model
from routines import *
from parameters import *
from initialcon import *

#### Initialize variables
M_qs = np.zeros(tmax) # accretion
zeq1 = np.zeros(tmax)
zeq2 = np.zeros(tmax)

a = 0.0001875 # the rate of slr
beta = M_bio - M_sed # total maximum accretion rate when z=0 analogous to k for Venice marshes

TIME = np.arange(1970,2050,1) # for plots

slr_b50    = 1.039895503 # dmnl # 0.5m slr
slr_b100   = 1.047128548 # dmnl  1m slr

#SLR_7010 = np.load("./Data/SLR_rate1970_2010.npy")
x = np.arange(0,81)
slr_fut50 = np.diff(slr_b50**x)/100

#SLR_7010 = np.load("./Data/SLR_rate1970_2010.npy")
x = np.arange(0,81)
slr_fut100 = np.diff(slr_b100**x)/100

slr = np.zeros(tmax)

for time in np.arange(1,tmax):

    slr[time] = slr[time-1] + a

    #! Salt marshes
    zeq50 = Hmax * ((1 - (slr_fut50 - M_sed)/(M_bio - M_sed)))
    M_qs[time] = slr_fut50 - ((M_bio - M_sed) / Hmax) * (z0 - zeq)* np.exp(-(M_sed - M_bio) / Hmax * time)

    zeq100 = Hmax * ((1 - (slr_fut100 - M_sed)/(M_bio - M_sed)))
    M_qs[time] = slr_fut100 - ((M_bio - M_sed) / Hmax) * (z0 - zeq)* np.exp(-(M_sed - M_bio) / Hmax * time)

    zeq[time]= z0 + a * Hmax / beta* (Hmax/ beta - Hmax/ beta * np.exp(beta/Hmax * time)+ time)
    if zeq[time] > Hmax:
        print 'Venice case: you are supratidal. Need to turn inorganic accretion off'
        zeq[time]= z0 + a*Hmax/M_bio* (Hmax/M_bio - Hmax/M_bio * np.exp(M_bio/ Hmax * time)+ time)
    elif zeq[time] < 0:
        zeq[time] = 0
        print 'Venice case: you are drowning. Out of model reach.'
    else:
        zeq[time]= z0 + a * Hmax / beta* (Hmax/ beta - Hmax/ beta * np.exp(beta/Hmax * time)+ time)
        print "survive"



## PLOT
plt.figure()
SLR1, = plt.plot(TIME1, zeq100, color=[.0,.5,.0], linewidth =2, label = "Sea level rise [1.0m]")
SLR2, = plt.plot(TIME1, zeq50, color=[.5,.2,.0], linewidth =2, label = "Salt marsh accretion")
plt.tick_params(axis='both', which='minor', labelsize=30)
plt.legend(handles=[SLR1, SLR2], loc="best")
plt.xlabel("Time period [yr]",fontsize=17)
plt.ylabel("Rate of change [mm]",fontsize=15)
#plt.savefig("./Figs/PNG/Cha_31_050_MqsSLR.png",dpi=600)
#np.save("./Data/Cha_31_050_MqsSLR.npy", M_qs)
plt.show()

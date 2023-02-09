#### Modules
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

#### Stuff to run the model
from routines import *
from parameters import *
from initialcon import *

TIME = np.arange(1970,2050,1) # for plots

#### Load data
#! All data runs with 100cm SLR and show Welfare
PA = np.load("/Users/lauraelsler/Dropbox/current_projects/VENICE/DATA/DEF_1_100_PA_W.npy") # PA normal
PM = np.load("/Users/lauraelsler/Dropbox/current_projects/VENICE/DATA/DEF_1_100_PM_W.npy") # PM normal
I0 = np.load("/Users/lauraelsler/Dropbox/current_projects/VENICE/DATA/DEF_1_100_PA_W_0inv.npy") # 0 investments
IFA100 = np.load("/Users/lauraelsler/Dropbox/current_projects/VENICE/DATA/DEF_1_100_PA_W_InvFA100.npy") # Inv_f_a = 100%
IBA100 = np.load("/Users/lauraelsler/Dropbox/current_projects/VENICE/DATA/DEF_1_100_PA_W_InvBA100.npy") # Inv_b_a = 100%

##PLOT
# PA normal, PM normal, 0inv
plt.figure()
no, = plt.plot(TIME, PA/(10**9), color=[0.5,.7,.2], label="Principal-agent investment")
fifty, = plt.plot(TIME, PM/(10**9), color=[1,.7,.4], label="Principal investment")
hundred, = plt.plot(TIME, I0/(10**9), color=[0.,.7,.4], label="No investment")
#plt.axhline(np.mean(PA)/(10**9), color=[0.5,.7,.2], linewidth=2)
#plt.axhline(np.mean(PM)/(10**9), color=[1.,.7,.4], linewidth=2)
#plt.axhline(np.mean(I0)/(10**9), color=[0.,.7,.4], linewidth=2)
plt.title("Different investment cases", fontsize=18)
plt.xlabel("Time [yr]",fontsize=15)
plt.ylabel("Welfare [bn EUR]",fontsize=15)
plt.legend(handles=[no, fifty, hundred], loc="best")
#plt.savefig("./Figs/DEF_1_0Inv.png",dpi=600)
plt.show()

# PA normal, PM normal, IFA100, IBA100
plt.figure()
one, = plt.plot(TIME, PA/(10**9), color=[0.5,.7,.2], label="Principal-agent investment")
two, = plt.plot(TIME, PM/(10**9), color=[1,.7,.4], label="Principal investment")
three, = plt.plot(TIME, IFA100/(10**9), color=[0.1,.6,.4], label="Flood protection investment")
four, = plt.plot(TIME, IBA100/(10**9), color=[0.5,.6,.8], label="Biotope investment")
plt.axhline(np.mean(PA)/(10**9), color=[0.5,.7,.2], linewidth=2)
plt.axhline(np.mean(PM)/(10**9), color=[1.,.7,.4], linewidth=2)
plt.axhline(np.mean(IFA100)/(10**9), color=[0.1,.6,.4], linewidth=2)
plt.axhline(np.mean(IBA100)/(10**9), color=[0.5,.6,.8], linewidth=2)
plt.title("Zero investment cases", fontsize=18)
plt.xlabel("Time [yr]",fontsize=15)
plt.ylabel("Welfare [bn EUR]",fontsize=15)
plt.legend(handles=[one,two, three, four], loc="best")
#plt.savefig("./Figs/DEF_1_BF0Inv_wavergages.png",dpi=600)
plt.show()

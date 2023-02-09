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
import matplotlib.gridspec as gridspec
import seaborn as sns

#### Stuff to run the model
from routines import *
from parameters import *
from initialcon import *

#### Scenarios
#flagSL = 000 # slr 0m
#flagSL = 050
flagSL = 100

#flagMod = 1 # PM
flagMod = 2 # PAM

flagPar = 0 # 0 parameter model
#flagPar = 1
#flagPar = 2


######################## Load data ######################################
#! Floods
if flagSL == 000:
    F_h = np.load("/Users/lauraelsler/Dropbox/current_projects/VENICE/DATA/Data_FH_tot_000.npy") # noSLR
    slr_b     = 0 # dmnl SLR 0m
    md = 100 # salt marsh drowns in 100 yr
elif flagSL == 050:
    F_h = np.load("/Users/lauraelsler/Dropbox/current_projects/VENICE/DATA/Data_FH_tot_050.npy") # 50SLR
    slr_b    = 1.039895503 # dmnl # 0.5m slr
    md = 75 # salt marsh drowns after 75 yr
elif flagSL == 100:
    F_h = np.load("/Users/lauraelsler/Dropbox/current_projects/VENICE/DATA/Data_FH_tot_100.npy") # 100SLR
    slr_b    = 1.047128548 # dmnl  1m slr
    md = 45 # salt marsh drowns after 45 yr

#SLR_7010 = np.load("./Data/SLR_rate1970_2010.npy")
x = np.arange(0,81)
slr_fut = np.diff(slr_b**x)/100
#SLR = np.concatenate((SLR_7010,slr_fut)) #<- sea level rise rate


########################### Define the model ################################
def run_model(pref, Bampl, flagMod):

    pre_past = pref
    B_ampl = Bampl # for 1-parameter model leave as it is

    for time in np.arange(1,tmax):

                #! Sea level rise (rate)
                slr = slr_fut[time]

                #! Calc accumulated investment in floods
                if flagMod == 2:
                    cum_inv = np.sum(Inv_f_a[0:time])
                elif flagMod == 1:
                    cum_inv = np.sum(Inv_f_p[0:time])

                #! Flood damage
                if cum_inv < F_thr:  # if last year's investment > F_thr
                        F_dam[time] = np.sum(costs_tot_noinv * F_h[time])
                else:
                        F_dam[time] = np.sum(costs_tot_yesinv * F_h[time])

                #! Salt marshes drowning
                if md <= time:
                        m = 0
                else:
                        m =  M[time-1]

                #! Extension of biotopes (adding invested amount)
                if m < M_max: # investment is initially only in salt marshes (ASSUMPTION)
                    if flagMod == 1:
                        M[time] = m + (Inv_b_p[time-1]/ p_m) # added area of investment in salt marsh
                        G[time] = G[time-1]
                    elif flagMod == 2:
                        M[time] = m + (Inv_b_a[time-1]/ p_m) # added area of investment in salt marsh
                        G[time] = G[time-1]
                else:
                    if flagMod == 1:
                        G[time] = G[time-1] + ((Inv_b_p[time-1]/ p_g)* G_surv) # added area of investment in seagrasses
                        M[time] = M[time-1]
                    elif flagMod == 2:
                        G[time] = G[time-1] + ((Inv_b_a[time-1]/ p_g)* G_surv) # added area of investment in seagrasses
                        M[time] = M[time-1]

                #! Value of biotopes
                M_val= ((M[time] * M_st) + (M[time] * M_fl * 1))* B_ampl # value of salt marsh area in EUR; (rate*1year)
                G_val= ((G[time] * G_st) + (G[time] * G_fl * 1))* B_ampl # value of sea grass area in EUR; (rate*1year)
                B_val[time]= M_val + G_val

                #! Principal preferences
                preF[time] = preF[time-1] - (1- pre_past) * preF[time-1] + (1 - pre_past) * (F_dam[time]/(B_val[time] + F_dam[time]))

                #! Welfare
                W[time] = B_val[time] - F_dam[time]

                #! Investment
                Inv_f_p[time] = preF[time] * pot
                Inv_b_p[time] = (1 - preF[time]) * pot

                #! Utility
                UTILITY[time] = ((Inv_f_p[time]/p_f)**preF[time]) * ((Inv_b_p[time]/p_m) **(1 - preF[time]))

                #! Concessionaire investment preferences
                C_preF[time] = func_Cinv(cum_inv, F_thr, M[time], M_max, G[time], G_max, share_b, share_f)

                #! Concessionaire transactions
                C_pot[time] = (Inv_f_a[time-1] * share_f) + (Inv_b_a[time-1] * share_b)# accumulated funding available to the concessionaire

                #! Agent investment
                if C_pot[time] > C_pot[time-1]:
                        A_preG[time]= A_preG[time-1]+ f_preG
                else:
                        A_preG[time]= A_preG[time-1]- f_preG

                if A_preG[time] > 1:
                        A_preG[time]= 1
                if A_preG[time] < 0:
                        A_preG[time]= 0

                A_preF[time] = A_preG[time] * C_preF[time] + (1 - A_preG[time]) * preF[time]
                Inv_f_a[time] = A_preF[time] * pot
                Inv_b_a[time] = (1-A_preF[time]) * pot

    if flagMod == 1:
        print "I am PM"
        return W, UTILITY, Inv_b_p, Inv_f_p, B_val, F_dam, preF
    elif flagMod == 2:
        print "I am PAM"
        return W, UTILITY, Inv_b_a, Inv_f_a, B_val, F_dam, preF, C_preF, A_preF


##########################################MODEL###############################################
if flagPar == 0:

    pref = 0.5
    Bampl = 1
    OUT = np.zeros(W.shape[0])
    OUT2 = np.zeros(W.shape[0])
    for i in np.arange(0,1):
        if flagMod == 1:
            W, UTILITY, Inv_b_p, Inv_f_p, B_val, F_dam, preF = run_model(pref,Bampl,flagMod)
        elif flagMod == 2:
            W, UTILITY, Inv_b_a, Inv_f_a, B_val, F_dam, preF, C_preF, A_preF = run_model(pref,Bampl,flagMod)
        OUT = W
        OUT2 = Inv_b_a

    #####! PLOT ORIGINAL MODEL
    # Welfare
    plt.figure()
    plt.plot(OUT/(10**9))
    #plt.plot(OUT2/(10**9))
    #plt.axhline(np.mean(W)/(10**9), color='r', linewidth=2)
    #plt.annotate('Mean welfare [bn EUR]', color='r',xy=(55, -3.))
    #plt.tick_params(axis='both', which='minor', labelsize=30)
    #plt.title("Principal-agent model with 1m SLR", fontsize = 15)
    #plt.legend(handles=[SLR1, SLR2, SLR3], loc="best")
    #plt.xlabel("Time period [yr]",fontsize=15)
    #plt.ylabel("Welfare of principal [bn EUR]",fontsize=15)
    #plt.savefig("./Figs/PNG/Cha_5_050_PRAG_W_Ginv.png",dpi=600)
    #np.save("./Data/Cha_5_050_PRAG_W_Ginv.npy", W) # SAVE DATA
    plt.show()


##########################################MODEL###############################################
if flagPar == 1:
    #! 1 parameter
    pref = np.arange(0.,1,0.1)
    Bampl = 1
    OUT = np.zeros((pref.shape[0], W.shape[0]))
    OUT2 = np.zeros(pref.shape[0])
    for i in np.arange(0,pref.shape[0]):
        if flagMod == 1:
            W, UTILITY, Inv_b_p, Inv_f_p, B_val, F_dam, preF = run_model(pref[i],Bampl,flagMod)
        elif flagMod == 2:
            W, UTILITY, Inv_b_a, Inv_f_a, B_val, F_dam, preF, C_preF, A_preF = run_model(pref[i],Bampl,flagMod)
        OUT[i] = W
        OUT2[i] = np.mean(W)

    ##! PLOT 1 PARAMETER MODEL
    # Mean
    plt.figure()
    plt.plot(pref, OUT2/(10**9))
    #plt.axhline(np.mean(OUT2)/(10**9), color='r', linewidth=2)
    #plt.annotate('Mean welfare distribution', color='r',xy=(0.6, -4.5))
    plt.tick_params(axis='both', which='minor', labelsize=30)
    plt.title("1m SLR", fontsize= 17)
    plt.xlabel("Principal preferences [dmnl]",fontsize=17)
    plt.ylabel("Mean welfare [bn EUR]",fontsize=17)
    #plt.savefig("./Figs/PNG/Cha_5_050_PRAG_meanW_prepast.png",dpi=600)
    #np.save("./Data/Cha_5_100_PRAG_meanW_prepast.npy", W)
    plt.show()


    # Whole period
    x = TIME #  x axis
    y = pref #  y axis
    z = OUT/(10**9) #  output data
    fig1 = plt.figure(figsize=[8,6])
    gs = gridspec.GridSpec(1,1,bottom=0.1,left=0.1,right=0.9)
    ax = fig1.add_subplot(gs[0,0])
    pcObject = ax.pcolormesh(x,y,z)
    ax.set_xlabel('Time period [yr]', fontsize = 16)
    ax.set_ylabel('Availability of yearly investments [mio EUR]', fontsize = 16)
    ax.tick_params(axis=1,length=20)
    plt.pcolormesh(x, y, z, cmap="RdYlGn")
    cb = plt.colorbar()
    #plt.clim([0,1])
    #plt.xlim(0,0.9)
    #plt.ylim(0,0.9)
    cb.set_label("Welfare of principal [bn EUR]", fontsize = 16)
    #fig1.savefig("./Figs/PNG/Cha_5_100_PRAG_W_prepast.png",dpi=600)
    plt.show()



##########################################MODEL###############################################
elif flagPar == 2:
    Bampl = np.arange(0.,1.,0.01)
    pref = np.arange(0.,1.,0.01)
    OUT = np.zeros((pref.shape[0],Bampl.shape[0]))
    OUT2 = np.zeros((pref.shape[0],Bampl.shape[0]))
    for i in np.arange(0,pref.shape[0]):
        for j in np.arange(0,Bampl.shape[0]):
            if flagMod == 1:
                W, UTILITY, Inv_b_p, Inv_f_p, B_val, F_dam, preF = run_model(pref[i],Bampl[j], flagMod)
            elif flagMod == 2:
                W, UTILITY, Inv_b_a, Inv_f_a, B_val, F_dam, preF, C_preF, A_preF = run_model(pref[i],Bampl[j], flagMod)
            OUT[i,j] = np.mean(W)
            OUT2[i,j] = W[-1]

    ##! PLOT 2 PARAMETER MODEL
    x = pref #  x axis
    y = Bampl #  y axis
    z = OUT/(10**9) #  output data
    fig1 = plt.figure(figsize=[8,6])
    gs = gridspec.GridSpec(1,1,bottom=0.1,left=0.1,right=0.9)
    ax = fig1.add_subplot(gs[0,0])
    pcObject = ax.pcolormesh(x,y,z)
    ax.set_xlabel('Responsiveness of agent [dmnl]', fontsize = 15)
    ax.set_ylabel('Preference of principal [dmnl]', fontsize = 15)
    ax.tick_params(axis=1,length=20)
    plt.pcolormesh(x, y, z, cmap="RdYlGn")
    cb = plt.colorbar()
    #plt.xlim(0,0.9)
    #plt.ylim(0,0.9)
    #plt.clim([0,1])
    cb.set_label("Welfare of principal [bn EUR]", fontsize = 15)
    #fig1.savefig("./Figs/PNG/Cha_5_100_PRAG_prefApref.png",dpi=600)
    plt.show()

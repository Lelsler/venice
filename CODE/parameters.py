#### Parameters
## Global
tmax      = 80 # year

## Peak floods
F_thr    = 5272000000 # EUR
p_f      = 3379487.179 # EUR/m

# Biotopes
M_max   = 9000 # hectare
M_bio   = 0.0025 # m/year
M_sed   = 0.0055 # m/year
p_m     = 218440.45 # EUR/hectare
p_g     = 138206.33 # EUR/hectare
G_max   = 9417 # hectare
G_surv  = 0.7 # in
Hmax    = 0.5 # m
M_st    = 197041.39 # EUR/hectare
M_fl    = 7253.69 # EUR/hectare
G_st    = 129570.50 # EUR/hectare
G_fl    = 65.82 # EUR/hectare
B_ampl  = 1 # dmnl # sweep parameter

## Principal agent
Inv_mx  = F_thr + (M_max * p_m) + (G_max * p_g) # EUR
pot     = (F_thr + (M_max * p_m) + (G_max * p_g))/(tmax/2) # EUR/year
share_b = 0.38 # %
share_f = 0.98 # %
pre_past = 0.5
f_preG = 0.1 # change in preferences to balance

# Not exactly parameters:)
B_mxv = (M_max * M_st) + (M_max * M_fl * 1) + (G_max * G_st)+ (G_max * G_fl)

##### Initial variables
## Biotopes
M0      = 6425 # hectare
G0      = 5493 # hectare
Inv_b   = pot/2 # EUR
z0      = 0 # m

### Peak floods
Inv_f   = pot/2 # EUR

## Principal agent
C_pot   = 0 # EUR

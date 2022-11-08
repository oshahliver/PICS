# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 15:07:45 2018

@author: os18o068
"""
from PIMPphysicalparams import m_earth, r_earth

dur = 0.
time_round = 3
mass_round = 4
pres_round = 4
radius_round = 3
temp_round = 2
dens_round = 3
layerbisection_limit = 50
shell_iteration_limit = 1000 #max number of shell iterations before interupt
iteration_limit = 0 #max number of iteration steps per planet to match R and M
coreiteration_limit = 0
pressureiteration_limit = 0
bisectionstep_limit = 15
bisection_counter_list = []
bisectionstep_counter_list = []

parameter_mask = ['Mg_number',
                  'radius',
                  'moment_of_inertia',
                  'Si_number',
                  'Si_number_mantle',
                  'x_Fe_mantle',
                  'pres_core_segregation',
                  'temp_core_segregation',
                  'w_S_outer_core',
                  'w_Si_outer_core',
                  'w_O_outer_core',
                  'x_FeS_outer_core',
                  'x_FeSi_outer_core',
                  'x_FeO_outer_core',
                  'T0_CMB',
                  'radius_core',
                  'radius_inner_core',
                  'radius_HMI',
                  'temperature_TBL',
                  'x_SiO2_mantle',
                  'x_FeO_mantle',
                  'temp_center',
                  'pres_center',
                  'log_oxygen_fug',
                  'delta_temp_MTZ',
                  'mass_water',
                  'mass_water_mantle', 
                  'Fe_number_outer_core',
                  'core_mass_frac',
                  'temp_CMB',
                  'pres_CMB',
                  'dens_CMB',
                  'temp_ICB', 
                  'pres_ICB',
                  'dens_ICB',
                  'temp_MTZ',
                  'pres_MTZ', 
                  'dens_MTZ',
                  'x_MgO_mantle',
                  'radius_MTZ',
                  'x_S_outer_core',
                  'x_S_mantle',
                  'S_to_Fe',
                  'Si_to_Fe',
                  'Mg_to_Fe',
                  'S_to_Si', 
                  'mass',
                  'inner_core_mass_frac',
                  'water_mass_frac',
                  'pres_surface',
                  'w_liquid', 
                  'w_supercrit',
                  'w_solid', 
                  'h_liquid', 
                  'h_supercrit', 
                  'h_solid', 
                  'w_liquid_to_w_H2O', 
                  'w_supercrit_to_w_H2O', 
                  'w_solid_to_w_H2O',
                  'vol_liquid', 
                  'vol_supercrit', 
                  'vol_solid', 
                  'gravity', 
                  'hydro_structure', 
                  'temp_HMI',
                  'pres_HMI', 
                  'dens_HMI',
                  'bulk_structure']

#water phase regions
water_phases = ['ice Ih', 'high pressure Mazevet', 'high pressure French', 'IAPWS']

# Coefficients for external temperature profiles from Cammarano et al. 2006
external_temp_profiles = [# Cold
                        [[1200, 0, 0],
                        [1200, 0, 0],
                        [1200, -0.5, -0.0004655],
                        [1200, -0.5, -0.0004655],
                        [273, 0, 0]],
                        # Hot1
                        [[1476., -0.01106, -0.00006433],
                         [1476., -0.01106, -0.00006433],
                         [1437., 0.02399, -0.00003742],
                         [1437., 0.02399, -0.00003742],
                         [273., 0, 0]],
                        # Hot 2
                        [[1888, -.01253, -.00008785],
                         [1888, -.01253, -.00008785],
                         [1453, -.00301, -.0000274],
                         [1453, -.00301, -.0000274],
                         [273., 0, 0]]
                        ]

#Different types of hydrosphere structures

hydro_structures = {'a':21020,
                        'b':2120,
                        'c':1210,
                        'd':1201,
                        'e':210,
                        'f':1020,
                        'g':120,
                        'h':202,
                        'i':20,
                        'j':2,
                        'k':0}

param_labels = [r'$\T \ [K]$',
                  r'$\P \ [Pa]$',
                  r'$\rho \ [kg/m^3]$',
                  r'$\ (dT/dP)_S \ [K \ Pa^{-1}]$',
                  r'$\ (dP/d \rho )_T \ [m^2 / s^2]$',
                  r'$\alpha_{th} \ [K^{-1}]$',
                  r'$c_P \ [\rm J \ kg^{-1} K^{-1}]$',
                  r'$\rho \ [kg/m^3]$',
                  r'$\rho \ [kg/m^3]$']


plot_units = {'Pa': 1.,
              'kPa': 1.0e3,
              'MPa': 1.0e6,
              'GPa': 1.0e9,
              'TPa': 1.0e12,
              'bar': 1.0e5,
              'kbar': 1.0e8,
              'Mbar': 1.0e11,
              'g': 1.0e-3,
              'kg': 1.,
              't': 1.0e3,
              'kt': 1.0e6,
              'Mt': 1.0e9,
              'm_earth': m_earth,
              'r_earth': r_earth,
              'mm': 1.0e-3,
              'cm': 1.0e-2,
              'm': 1.,
              'km': 1.0e3,
              'Mm': 1.0e6,
              'K': 1.,
              'kg/m3': 1.,
              'gcc': 1.0e-3}

dens_max = 2.0e4
dens_min = 5.0e2
eps_P = 1.0e-4
eps_h = 1.0e-2
eps_r = .25
eps_layerfix = 1.0e-6
eps_layer = eps_layerfix
#eps_majorconstrain = 1.0e-4
eps_FeSi = 1.0e-6
eps_Mtot = 1.0e-6
eps_Rtot = 1.0e-6
eps_Psurf = 1.0e-3
eps_Tsurf = 1.0e-3
eps_Pspace = 1.0e-5
eps_Mg_number = 1.0e-6
acc_Mg_number = 1.0e-3
acc_M_surface = 1.0e-3
acc_T_surface = 1.0e-3

eos_pres_trans = 1.0e9

#pressure switch for H2O table eos
pressure_switch_H2O = 1.0e10

#max allowed iron content of the mantles
xi_Fe_mantle_max = 5e-1

#some plot parameters
plotrad_min = 0.0
plotdens_min = 0.0
plotpres_min = 0.0
plotmass_min = 0.0
plottemp_min = 0.0
plotrad_max = 1.4e0
plotdens_max = 1.5e4
plotpres_max = 4.0e2
plotmass_max = 1.5
plottemp_max = 6.0e3


material_plot_list_fort = [r'$\rm H_2O$',
                      r'$\rm Fe$',
                      'SiO2',
                      r'$\rm MgO$',
                      'MgSiO3',
                      'Mg2SiO4',
                      'Mg2Si2O6',
                      'FeS',
                      'Mg(OH)2']

#define colors for parameters
pres_color = (.4, .5, .7)
dens_color = (.8, .4, .0)
mass_color = (.2, .8, .2)
temp_color = (.8, .2, .2)
vesc_color = (.5, .5, .5)
grav_color = (.5, .5, .0)

param_colors = [pres_color, mass_color, dens_color, temp_color, grav_color, 
                vesc_color]

pure_curves_color_list = [(.5,.5,1), #water
                          (.5,.5,.5), #Fe
                          (0,.5,.5), #SiO2
                          (1,.5,.5) #MgO
                          ]

layerColors = {
            'liquid':(.25,.5,1),
            'supercritical':(.5,0.25,1),
            'solid':(.75,.8,1),
            'vapor': (1,0,0),
            'gas':(0,1,0),
            'inner core':(.75,.75,.75),
            'outer core':(1., .5, .25),
            'inner mantle':(.4,.25,0),
            'outer mantle': (.5, .3, 0.)}

layerCodes = {1:'supercritical',
              2:'solid',
              0:'liquid',
              3:'inner core',
              4:'outer core',
              5:'inner mantle',
              6:'outer mantle'}

#define color scheme for fancy plots
color_list = [(.7, .2, .6),
                (.6, .4, 1.), 
              (.2, .4, 1.), 
              (.2,.6,.9), 
              (.2, .8, .8), 
              (.2, .8, .4), 
              (.6, .8, .4), 
              (.6, .6, .2), 
              (.8, .4, .2),
              (1., .2, .2),
              (1., .5, .5),
              (.7, .7, .7),
              (.5, .5, .5),
              (.2, .2, .2),
              (.0, .0, .0)
              ]

#define parameter limits for plots
param_lims = [[0, 10000], #T
              [0, 1.0e11], #P
              [0, 10000], #rho
              [0, 1.0e-7], #dPdT_S
              [0, 1.0e8], #dPdrho_T
              [0, 1.0e-4], #alpha
              [0, 5000], #cp
              [0., 0], #s
              [0, 0], #u
              [0, 5] #phase
              ]
              
#define plot color for materials
#Conventions are:
#BM (0), MGD (1), 
#liquid water (0), Mg2SiO4 (1), Mg2Si2O6 (2), Fe2SiO4 (3), Fe2Si2O6 (4), MgO (5), 
#MgSiO3 (6), FeO (7), FeSiO3 (8), Fe (9), FeS (10), water ice VII (11)
material_colors = []

#suffix for different output files
suffix = {'planet':'.pl',
          'layer':'.lay',
          'shell':'.shl'} #.shl to avoid confusion with .sh shell scripts

lwdht = 1.
laytranslwdht = 1.2
tlfntsize = 8
lfntsize = 10
gridalpha = .25
legendalpha = .75

#color for axis grid on plots
grid_color= (.6, .6, 1.)

#background color for figures
background_color = (1., 1., 1.)

plot_params = {'lwdt':lwdht,
               'laytranslwdht': laytranslwdht,
               'tlfntsize': tlfntsize,
               'lfntsize': lfntsize,
               'gridcolor':grid_color,
               'gridalpha':gridalpha,
               'legendalpha':legendalpha,
               'legendedgecolor':'None',
               'backgroundcol':background_color,
               'pad':5,
               'majorticklen':10,
               'minorticklen':5,
               'lwdthgridminor':1,
               'lwdthgridmajor':2}

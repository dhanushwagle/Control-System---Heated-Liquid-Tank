# Importing pyplot and numpy

import matplotlib.pyplot as plt
import numpy as np

# Time settings

ts = 1  # Time-step [s]
t_start = 0  # Start Time[s]
t_stop = 2000  # Stop Time[s]
N_sim = int((t_stop-t_start)/ts) + 1 # Total Simulation Step

# Constant and Parameters

F = 0.00025 # Liquid flow, m^3/s
c = 4200 # Specific heat capacity of liquid, J/kg.K
rho = 1000 # Density of liquid, kg/m^3
V = 0.2 # Liquid volume in tank, m^3
U = 1000 # Heat transfer coefficient in tank, W/K
t_delay = 60  # Time delay, seconds

# Initialization of time delay

u_delayed_init = 0.0
N_delay = int(round(t_delay/ts)) + 1
delay_array = np.zeros(N_delay) + u_delayed_init

# Initializing arrays

T_plot_array = np.zeros(N_sim)
T_env_plot_array = np.zeros(N_sim)
T_in_plot_array = np.zeros(N_sim)
P_plot_array = np.zeros(N_sim)
t_plot_array = np.zeros(N_sim)
P_delayed_plot_array = np.zeros(N_sim)

# Initial condition

# P = 0 # Supplied power, watts
T = 293 # Temperature of liquid, kelvin
T_env = 293 # Environmental temperature, kelvin
T_in = 293 # Temperature of liquid inflow, kelvin

# Simulation for-loop

for k in range(0, N_sim):
    
    t = k*ts  # Time

    # Selecting inputs:
    if (t >= t_start and t < 250):
        P = 0
    elif (t >= 250 and t < 500):
        P = 10000
    elif (t >= 500 and t < 750):
        P = 0
    elif (t >= 750 and t < 1000):
        P = 10000
    elif (t >= 1000 and t < 1250):
        P = 0
    elif (t >= 1250 and t < 1500):
        P = 10000
    elif (t >= 1500 and t < 1750):
        P = 0
    elif (t >= 1750 and t <= t_stop):
        P = 10000
    
    # Time delay
    P_delayed = delay_array[-1]
    delay_array[1:] = delay_array[0:-1]
    delay_array[0] = P

    # Euler-forward discretization  
    dT_dt = (1/(c*rho*V))*(P_delayed+(c*rho*F*(T_in - T))+(U*(T_env - T)))
    T_p1 = T + (ts*dT_dt)
    
    # Storage for plotting
    t_plot_array[k] = k
    T_plot_array[k] = T_p1
    T_env_plot_array[k] = T_env
    T_in_plot_array[k] = T_in
    P_plot_array[k] = P
    P_delayed_plot_array[k] = P_delayed
    
    # Time shift
    T = T_p1

# Plotting

plt.close('all')
plt.figure(1)

# First Plot
plt.subplot(2, 1, 1)
plt.plot(t_plot_array, T_plot_array, 'r')
plt.plot(t_plot_array, T_env_plot_array, 'b--')
plt.plot(t_plot_array, T_in_plot_array, 'y--')
plt.legend(labels=('T', 'T_Env', 'T_In'), loc='upper right')
plt.grid()
plt.xlabel('t [s]')
plt.ylabel('[Kelvin]')

# Second Plot
plt.subplot(2, 1, 2)
plt.plot(t_plot_array, P_plot_array, 'g')
plt.plot(t_plot_array, P_delayed_plot_array, 'r')
plt.grid()
plt.xlabel('[Seconds]')
plt.ylabel('[Watt]')
plt.legend(labels=('P_Real', 'P_Delayed'), loc='upper right')
plt.show()
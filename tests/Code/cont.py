import control as ctrl
import matplotlib.pyplot as plt
import numpy as np

# System transfer function
numerator = [1]
denominator = [685, 1]
system = ctrl.TransferFunction(numerator, denominator)

# Add dead time to the system
dead_time = 30.0  # Specify the dead time in seconds

# Pade approximation for dead time
numerator_dead_time, denominator_dead_time = ctrl.pade(dead_time, 3)
dead_time_tf = ctrl.TransferFunction(numerator_dead_time, denominator_dead_time)


system_with_dead_time = ctrl.series(system, dead_time_tf)


# PID controller transfer function
#zigler Ko: 36.5 To: 119 (315-196)
Ku = 36.5
Tu = 119
Kp = 0.35*Ku  # Proportional gain 7.3
Ki = 0.03*(Ku/Tu)  # Integral gain 0.122689
Kd = 0.0066*(Ku*Tu)  # Derivative gain 286.671
print(f"{Kp},{Ki},{Kd}")
#12.774999999999999,0.009201680672268907,28.6671
controller = ctrl.TransferFunction([Kd, Kp, Ki], [1, 0])

# Open-loop system
open_loop_system = ctrl.series(controller, system_with_dead_time)

# Time vector
time = np.linspace(0, 1000, 1000)


# # Setpoint parameters
# max_value_ramp1 = 100  # Maximum value of the first ramp
# stop_time_ramp1 = 200  # Time at which the first ramp stops growing

# # Create the first ramp function
# ramp1 = np.clip(time / stop_time_ramp1 * max_value_ramp1, 0, max_value_ramp1)

setpoint = np.zeros(1000)
for i in range(1000):
    setpoint[i] = 150
# Combine the two ramp functions
#setpoint = ramp1
# j = 1
# for i in range(1000):
#     if i > 300 and i<500:
#         if(i % 4 == 0):
#             setpoint[i] += j
#             j +=1
#         else:
#             setpoint[i] = setpoint[i-1]
#     elif i>499 and i< 600:
#         setpoint[i] = setpoint[i-1]
#     elif i > 599 and i<800:
#         if(i % 2 == 0):
#             setpoint[i] += j
#             j +=1
#         else:
#             setpoint[i] = setpoint[i-1]
#     elif i>799 and i< 950:
#         setpoint[i] = setpoint[i-1]
#     elif i>950:
#         setpoint[i] = 0
# Saturation limits

# Closed-loop system
closed_loop_system = ctrl.feedback(open_loop_system)

time, response, state = ctrl.forced_response(closed_loop_system, time, setpoint,return_x = True)
control_signal = state[0]

plt.plot(time, control_signal)
plt.xlabel('Time')
plt.ylabel('Control Signal')
plt.title('Control Signal Response (PID)')
plt.grid(True)

# Plot the response
plt.plot(time, setpoint, label='Setpoint', linestyle='--')
plt.plot(time, response, label='Resposta')
plt.title('Simulação Sistema Com Atraso')
plt.xlabel('Tempo (s)')
plt.ylabel('Resposta')
plt.legend()
plt.grid(True)
plt.show()

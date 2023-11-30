import control as ctrl
import matplotlib.pyplot as plt
import numpy as np

# System transfer function
numerator = [1]
denominator = [444, 1]
system = ctrl.TransferFunction(numerator, denominator)

# Add dead time to the system
dead_time = 50.0  # Specify the dead time in seconds

# Pade approximation for dead time
numerator_dead_time, denominator_dead_time = ctrl.pade(dead_time, 3)
dead_time_tf = ctrl.TransferFunction(numerator_dead_time, denominator_dead_time)

print(numerator_dead_time)
print(denominator_dead_time )
system_with_dead_time = ctrl.series(system, dead_time_tf)

# PID controller transfer function
Kp = 6.0  # Proportional gain
Ki = 1.0  # Integral gain
Kd = 2.4  # Derivative gain
controller = ctrl.TransferFunction([Kd, Kp, Ki], [1, 0])

# Open-loop system
open_loop_system = ctrl.series(controller, system_with_dead_time)

# Closed-loop system
closed_loop_system = ctrl.feedback(open_loop_system)

# Time vector
time = np.linspace(0, 1000, 1000)


# Setpoint parameters
max_value_ramp1 = 100  # Maximum value of the first ramp
stop_time_ramp1 = 200  # Time at which the first ramp stops growing

# Create the first ramp function
ramp1 = np.clip(time / stop_time_ramp1 * max_value_ramp1, 0, max_value_ramp1)


# Combine the two ramp functions
setpoint = ramp1
j = 1
for i in range(1000):
    if i > 300 and i<500:
        if(i % 4 == 0):
            setpoint[i] += j
            j +=1
        else:
            setpoint[i] = setpoint[i-1]
    elif i>499 and i< 600:
        setpoint[i] = setpoint[i-1]
    elif i > 599 and i<800:
        if(i % 2 == 0):
            setpoint[i] += j
            j +=1
        else:
            setpoint[i] = setpoint[i-1]
    elif i>799 and i< 950:
        setpoint[i] = setpoint[i-1]
    elif i>950:
        setpoint[i] = 0

time, response, state = ctrl.forced_response(closed_loop_system, time, setpoint,return_x = True)

# Plot the response
plt.plot(time, setpoint, label='Setpoint', linestyle='--')
plt.plot(time, response, label='Resposta')
plt.title('Simulação Sistema Com Atraso')
plt.xlabel('Tempo (s)')
plt.ylabel('Resposta')
plt.legend()
plt.grid(True)
plt.show()

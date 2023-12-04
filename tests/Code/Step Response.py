import control as ctrl
import matplotlib.pyplot as plt
import numpy as np

# System transfer function
numerator = [1]
denominator = [685, 1]
system = ctrl.TransferFunction(numerator, denominator)

# Time vector
time = np.linspace(0, 1000, 5000)  # Adjust the time range and resolution as needed

# Add dead time to the system
dead_time = 60.0  # Specify the dead time in seconds

# Pade approximation for dead time
numerator_dead_time, denominator_dead_time = ctrl.pade(dead_time, 3)
dead_time_tf = ctrl.TransferFunction(numerator_dead_time, denominator_dead_time)

print(numerator_dead_time)
print(denominator_dead_time )
system_with_dead_time = ctrl.series(system, dead_time_tf)

# Apply a step input to the system
time, response = ctrl.step_response(system_with_dead_time, time)

# Plot the step response
plt.plot(time, response)
plt.xlabel('Time')
plt.ylabel('System Response')
plt.title('Step Response of the System')
plt.grid(True)
plt.show()
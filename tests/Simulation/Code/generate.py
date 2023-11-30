import numpy as np
import matplotlib.pyplot as plt

def generate_temperature_curve(actual_temperature, target_temperature, response_time, maintenance_time):
    # Generate a second-degree curve for the response time
    a = (target_temperature - actual_temperature) / (response_time ** 2)
    b = 0
    c = actual_temperature

    # Create an array of time values for the response time
    t_values_response = np.linspace(0, response_time, 100)

    # Calculate temperature values for the response time using the quadratic equation
    temperature_values_response = a * (t_values_response ** 2) + b * t_values_response + c

    # Extend the curve by repeating the last temperature value for maintenance time
    t_values_maintenance = np.linspace(response_time, response_time + maintenance_time, 100)
    temperature_values_maintenance = np.full_like(t_values_maintenance, target_temperature)

    # Concatenate the response and maintenance curves
    t_values = np.concatenate((t_values_response, t_values_maintenance))
    temperature_values = np.concatenate((temperature_values_response, temperature_values_maintenance))

    return t_values, temperature_values

# Example usage
actual_temperature = 20  # actual starting temperature
target_temperature = 120  # desired temperature
response_time = 60  # time for the initial response
maintenance_time = 50  # additional time to maintain the temperature

t_values, temperature_values = generate_temperature_curve(actual_temperature, target_temperature, response_time, maintenance_time)

print(temperature_values)

# Plot the curve
plt.plot(t_values, temperature_values, label='Temperature Curve')
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.title('Second Degree Temperature Curve with Maintenance')
plt.legend()
plt.show()

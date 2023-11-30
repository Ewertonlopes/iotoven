import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import derivative

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



def model():


    # Example usage
    actual_temperature = 25  # actual starting temperature
    target_temperature = 150  # desired temperature
    response_time = 60 # time for the initial response
    maintenance_time = 50  # additional time to maintain the temperature
    omega = 30

    t_values, temperature_curve = generate_temperature_curve(actual_temperature, target_temperature, response_time, maintenance_time)
    temp_size = len(temperature_curve) - omega
    
    
    beta = 0.036791372
    alfa = 0.08206783414342446

    #potency = 0.013835*tension**2
    #temp_window = np.zeros()
    temperature = np.zeros(temp_size+omega)
    app_pot = np.zeros(temp_size+omega)

    for i in range(30):
        temperature[i] = 25
        app_pot[i] = (temperature_curve[i+omega] - (1-beta)*temperature[i+omega])/alfa
        if(app_pot[i]>700):
            app_pot[i] = 700
        elif(app_pot[i]<0):
            app_pot[i] = 0

    t_range = np.linspace(0, temp_size+omega, temp_size+omega)

    for i in range(30,temp_size):
        temperature[i] = (1-beta)*temperature[i-omega] + alfa*app_pot[i-omega]

        app_pot[i] = (temperature_curve[i+omega] - (1-beta)*temperature[i])/alfa
        if(app_pot[i]>700):
            app_pot[i] = 700
        elif(app_pot[i]<0):
            app_pot[i] = 0

        alfa = (alfa + ((temperature[i] - temperature[i-omega]*(1-beta))/app_pot[i-omega]))/2
        

    plt.plot(t_range, temperature_curve, label=f'Curva Gerada',color = 'green')
    plt.plot(t_range, temperature, label=f'Previsão',color = 'red')
    #plt.plot(t_range, app_pot, label=f'Potencia Aplicada',color = 'yellow')

    # Add labels and legend
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.legend()

    # Show the plot
    plt.show()

if __name__ == "__main__":
    model()
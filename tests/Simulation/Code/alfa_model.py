import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import derivative

def custom_function(x,a):
    return (x - 25) * a

def plot_interpolation(csv_file, degree=3):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Extract time and temperature columns
    ftime = df['time'][0]
    time = df['time'] - ftime
    temperature = df['temperature']
    
    #T[i+20] = T[i] + a*P[i] - b*T[i]
    tension = 110

    omega = 30
    beta = 0.036791372
    alfa = 0
    potency = 0.013835*tension**2

    t_range = np.linspace(0, 900+omega, 900+omega)
    testT = np.zeros(900+omega)
    temp_interesse = np.zeros(900+omega)

    for i in range(30,900):
        alfa = (alfa + ((temperature[i] - temperature[i-omega]*(1-beta))/potency))/2
        testT[i+omega] = potency*alfa + temperature[i]*(1-beta)
        temp_interesse[i] = temperature[i]

    plt.plot(t_range, temp_interesse, label=f'Data Colected',color = 'green')
    plt.plot(t_range, testT, label=f'Previsão',color = 'red')

    # Add labels and legend
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.legend()

    # Show the plot
    plt.show()

if __name__ == "__main__":
    # Replace 'your_file.csv' with the actual file path
    csv_file_path = 'Data/upup.csv'
    plot_interpolation(csv_file_path)
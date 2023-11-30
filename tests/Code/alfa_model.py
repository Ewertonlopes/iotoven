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

    omega = 150
    beta = 0
    alfa = 0
    potency = 0.013835*tension**2

    t_range = np.linspace(0, 900+omega, 900+omega)
    testT = np.zeros(900+omega)
    temp_interesse = np.zeros(900+omega)

    for i in range(omega,900):
        alfa = (alfa + ((temperature[i] - temperature[i-omega]*(1-beta))/potency))/2
        testT[i+omega] = potency*alfa + temperature[i]*(1-beta)
        temp_interesse[i] = temperature[i]

    plt.plot(t_range, temp_interesse, label=f'Data Colected',color = 'green')
    plt.plot(t_range, testT, label=f'Previsão',color = 'red')

    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Temperature', fontsize=12)
    plt.title('Modelo Com o Alpha Recursivo', fontsize=14)
    plt.legend(fontsize=10)

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tick_params(axis='both', which='both', labelsize=10)


    # Show the plot
    plt.show()

if __name__ == "__main__":
    # Replace 'your_file.csv' with the actual file path
    csv_file_path = 'Data/upup.csv'
    plot_interpolation(csv_file_path)
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

    temp_range = np.linspace(266,50,1881)
    omega = 30
    betas = np.zeros(800)

    for i in range(800):
        betas[i] = 1 - temperature[i+omega]/temperature[i]
    beta = np.mean(betas)
    print(beta) # beta = 0.036791372

    t_range = np.linspace(0, 1300+omega, 1300+omega)
    testT = np.zeros(1300+omega)
    temp_interesse = np.zeros(1300+omega)
    for i in range(1300):
        testT[i+omega] = temperature[i]*(1-beta)
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
    csv_file_path = 'Data/decay.csv'
    plot_interpolation(csv_file_path)
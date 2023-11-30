import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import derivative

def plot_interpolation(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    time = df['time']
    temperature = df['temperature']
    t_size = len(time)
    #T[i+20] = T[i] + a*P[i] - b*T[i]

    omega = 60
    beta = 0
    betas = np.zeros(t_size-omega)
    for i in range(t_size - omega):
        betas[i] = temperature[i+omega] - temperature[i]
    beta = np.mean(betas)
    print(beta)
    testT = np.zeros(t_size)
    temp_interesse = np.zeros(t_size)

    for i in range(t_size-omega):
        testT[i+omega] = temperature[i]*(beta)
        temp_interesse[i] = temperature[i]

    mmk = 0
    for i in range(omega,t_size - 2*omega):
        mmk += (temp_interesse[i] - testT[i])**2

    print(mmk)
    #print(beta) # beta = 0.036791372
    plt.plot(time, temp_interesse, label=f'Data Colected',color = 'green')
    plt.plot(time, testT, label=f'Previsão',color = 'red')
    plt.text(100, 10, f'Beta: {beta:.6f}', fontsize=10, color='blue')
    # Add labels and legend 
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Temperature', fontsize=12)
    plt.title('Modelo Com o Beta', fontsize=14)
    plt.legend(fontsize=10)

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tick_params(axis='both', which='both', labelsize=10)

    # Show the plot
    plt.show()

if __name__ == "__main__":
    # Replace 'your_file.csv' with the actual file path
    csv_file_path = 'Data/decay.csv'
    plot_interpolation(csv_file_path)
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import derivative


def model(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Extract time and temperature columns
    ftime = df['time'][0]
    time = df['time'] - ftime
    temperature = df['temperature']

    temp_size = len(temperature)
    
    #T[i+20] = T[i] + a*P[i] - b*T[i]
    pwm = 4096
    tension = (pwm/8192)*220
    omega = 30
    beta = 0.036791372
    alfa = 0.08206783414342446
    potency = 0.013835*tension**2

    app_pot = np.zeros(temp_size+omega)
    for i in range(temp_size-omega):
        app_pot[i] = potency

    t_range = np.linspace(0, temp_size+omega, temp_size+omega)
    testT = np.zeros(temp_size+omega)
    temp_interesse = np.zeros(temp_size+omega)
    potency_model = np.zeros(temp_size+omega)

    for i in range(30,temp_size-omega):
        alfa = (alfa + ((temperature[i] - temperature[i-omega]*(1-beta))/app_pot[i-omega]))/2
        testT[i+omega] = potency*alfa + temperature[i]*(1-beta)
        temp_interesse[i] = temperature[i]
        potency_model[i] = (testT[i+omega] - (1-beta)*temperature[i])/alfa

    print(np.mean(potency_model))
    plt.plot(t_range, temp_interesse, label=f'Data Coletada',color = 'green')
    plt.plot(t_range, testT, label=f'Previsão',color = 'red')
    plt.plot(t_range, potency_model, label=f'Previsão Potencia',color = 'blue')
    plt.plot(t_range, app_pot, label=f'Potencia Aplicada',color = 'yellow')

    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Temperature', fontsize=12)
    plt.title('Modelo Utilizado Em Outros Dados', fontsize=14)
    plt.legend(fontsize=10)

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tick_params(axis='both', which='both', labelsize=10)

    # Show the plot
    plt.show()

if __name__ == "__main__":
    # Replace 'your_file.csv' with the actual file path
    csv_file_path = 'Data/upup.csv'
    model(csv_file_path)
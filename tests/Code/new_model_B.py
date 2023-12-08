import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import derivative


def plot_interpolation(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    i_time = df['time'][0]
    time = df['time'] - i_time
    temperature = df['temperature']
    time_s = len(time)
    #T[i+1] = T[i] + f(P) + f(T)
    #f(T) = -0.001458*T[i] + 0.05183
    #T[i+1] = T[i] + f(P,T)
    #f(P,T) = aP - 0.001458*T[i] + 0.05183
    #(f(P,T) + 0.001458*T[i] - 0.05183)/P = a

    omega = 60
    #Qf = Qf + Potencia*dt - Qo
    decays = np.array([])
    temps = np.array([])

    # for i in range(time_s - omega):
    #     if i % omega == 0:
    #         adec = (temperature[i + omega] - temperature[i]) / temperature[i]
    #         if adec < 0:

    for i in range(20):
        window_time = time[60+60*i:120+60*i]
        window_temp = temperature[60+60*i:120+60*i]
        # Fit a second-degree polynomial
        coefficients = np.polyfit(window_time, window_temp, 1)
        fit_function = np.poly1d(coefficients)
        decays = np.append(decays, fit_function[1])
        temps = np.append(temps, temperature[60+60*i])

    coefficients2 = np.polyfit(temps, decays, 1)
    fit_function2 = np.poly1d(coefficients2)
    # Generate points for the fitted curve
    fit_temps = np.linspace(min(temps), max(temps), 20)
    fit_decays = fit_function2(fit_temps)
    print(1/fit_function2[1])

    testT = np.zeros(time_s)
    testT[0] = temperature[0]
    for i in range(time_s-1):
        testT[i+1] = 0.998542*testT[i] + 0.05183

    # Plotting
    plt.plot(time,temperature,'o',label='Data Capturada')
    #plt.plot(time, testT, 'o', label='Constructed Data')
    # plt.scatter(temps,decays)
    # plt.plot(fit_temps, fit_decays, linestyle='-', color='b', label='Temperatura x Variação')

    # Adding grid lines for better readability
    plt.grid(True, linestyle='--', alpha=0.7)

    # Adding title to the plot
    plt.title('Resfriamento do Forno')

    # Adding labels to the axes with a larger font size
    plt.xlabel('Tempo(s)', fontsize=12)
    plt.ylabel('Temperatura (ºC)', fontsize=12)

    # Adding legend with a shadow for better visibility
    plt.legend(shadow=True)

    # Display the plot
    plt.show()


if __name__ == "__main__":
    # Replace 'your_file.csv' with the actual file path
    csv_file_path = 'Data/decay.csv'
    plot_interpolation(csv_file_path)
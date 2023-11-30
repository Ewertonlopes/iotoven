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
    #T[i+20] = T[i] + a*P[i] - b*T[i]

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
    fit_temps = np.linspace(min(temps), max(temps), 100)
    fit_decays = fit_function2(fit_temps)
    print(fit_function2)

    testT = np.zeros(time_s)
    testT[0] = temperature[0]
    for i in range(time_s-1):
        testT[i+1] = testT[i] -0.001458*testT[i] + 0.05183

    # Plotting
    plt.plot(time,temperature,'o',label='Original Data')
    plt.plot(time, testT, 'o', label='Constructed Data')
    #plt.plot(fit_temps, fit_decays, label='Fitted Curve')
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # Replace 'your_file.csv' with the actual file path
    csv_file_path = 'Data/decay.csv'
    plot_interpolation(csv_file_path)
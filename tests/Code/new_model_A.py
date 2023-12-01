import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import derivative
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
import warnings

def getBeta(T):
    return -0.001458*T + 0.05183

def plot_interpolation(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    i_time = df['time'][0]
    time = df['time'] - i_time
    temperature = df['temperature']
    time_s = len(time)
    #T[i+1] = T[i] + a*Pacc -0.001458*T[i] + 0.05183
    #T[i+1] + 0.001458T[i] - 0.05183 = T[i] + a*Pacc

    #a = (T[i] - 0.998542*T[i-1] - 0.05183)/167.4

    tension = 110
    potency = 0.013835*tension**2
    decays = np.array([])
    temps = np.array([])
    window_time = np.zeros(60)
    window_temp = np.zeros(60)


    # for i in range(15):
    #     window_time = time[60*i:60+60*i]
    #     window_temp = temperature[60*i:60+60*i] #+ 0.001458*temperature[60+60*i] - 0.05183
    #     # Fit a second-degree polynomial
    #     coefficients = np.polyfit(window_time, window_temp, 1)
    #     fit_function = np.poly1d(coefficients)
    #     decays = np.append(decays, fit_function[1])
    #     temps = np.append(temps, temperature[60*i])


    # coefficients2 = np.polyfit(temps, decays, 1)
    # fit_function2 = np.poly1d(coefficients2)

    # # Generate points for the fitted curve
    # fit_temps = np.linspace(min(temps), max(temps), 100)
    # fit_decays = fit_function2(fit_temps)
    # print(fit_function2)

    # testT = np.zeros(time_s)
    # testT[0:60] = temperature[0:60]
    # window_temp = temperature[0:60]
    # window_time = time[0:60]
    # actual = 0
    # acce = 0
    delay = 60
    omega = 0.0152 #0.01
    minorerror = 1000000000000
    minoromega = 0
    for j in range(1):
        testT = np.zeros(time_s)
        actual = 0
        testT[0:delay] = temperature[0:delay]
        window_temp = temperature[0:delay]
        window_time = time[0:delay]
        acce = 0
        for i in range(delay,time_s-delay):
            if i>120: 
                error = (temperature[i] - testT[i])
            else:
                error = 0
            print(window_temp)
            print(window_time)
            acce += omega*error
            window_temp[actual] = temperature[i]
            window_time[actual] = delay
            actual = (actual + 1)%delay
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=np.RankWarning)
                coefficients = np.polyfit(window_time, window_temp, 1)
            fit_function = np.poly1d(coefficients)
            print(fit_function)
            testT[i+delay] = fit_function(delay) + acce

        mmq = np.sum(np.sqrt((temperature[200:] - testT[200:])**2))
        print(mmq)
        if mmq < minorerror:
            minorerror = mmq
            minoromega = omega
            print(minorerror)
            print(minoromega)
        omega += 0.0001
        #print(omega)

    # print(minoromega)


    # for i in range(60,time_s-60):
    #     acce += omega*(temperature[i] - testT[i])
    #     window_temp[actual] = temperature[i]
    #     window_time[actual] = 60
    #     actual = (actual + 1)%60
    #     with warnings.catch_warnings():
    #         warnings.simplefilter("ignore", category=np.RankWarning)
    #         coefficients = np.polyfit(window_time, window_temp, 1)
    #     fit_function = np.poly1d(coefficients)
    #     testT[i+60] = fit_function(60) + acce

    # mmq = np.sum(np.sqrt((temperature[200:] - testT[200:])**2))
    # print(mmq)
    # # Plotting
    #plt.plot(temps,decays)
    plt.plot(time, temperature,'o',label='Original Data')
    plt.plot(time, testT, 'o', label='Constructed Data')
    #plt.plot(fit_temps, fit_decays, label='Fitted Curve')
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # Replace 'your_file.csv' with the actual file path
    csv_file_path = 'Data/FullCarac.csv'
    plot_interpolation(csv_file_path)
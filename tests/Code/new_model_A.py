import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import derivative
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor

def plot_interpolation(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    i_time = df['time'][0]
    time = df['time'] - i_time
    temperature = df['temperature']
    time_s = len(time)
    #T[i+1] = T[i] + a*Pacc -0.001458*T[i] + 0.05183
    #T[i+1] + 0.001458T[i] - 0.05183 = T[i] + a*Pacc

    #a = (T[i] - 0.998542*T[i-1] - 0.05183)/Pacc

    tension = 110
    potency = 0.013835*tension**2

    window_pot = np.zeros(10)
    window_temp = np.zeros(10)
    it_pot = 0

    Potacc = np.zeros(time_s-1)
    fvalue = np.zeros(time_s-1)

    mmtemp = np.zeros(time_s-1)

    for i in range(time_s-1):
        window_temp[it_pot] = temperature[i]
        window_pot[it_pot] = potency
        it_pot = (it_pot + 1)%10
        Potacc[i] = np.mean(window_pot)
        mmtemp[i] = np.mean(window_temp)

    for i in range(time_s-2):
        fvalue[i] = mmtemp[i+1] - mmtemp[i] 
    
    X = np.column_stack((Potacc[30:], mmtemp[30:]))
    model = MLPRegressor(hidden_layer_sizes=(100, ), max_iter=1000)
    model.fit(X, fvalue[30:])

    testT = np.zeros(time_s)
    testT[0] = temperature[0]
    test = model.predict(np.column_stack((Potacc, testT[1:])))
    print(test)
    for i in range(time_s-1):
        testT[i+1] = 0.998542*testT[i] + test[i]

    # # Plotting
    plt.plot(time[30:-1],mmtemp[30:],'o',label='Original Data')
    plt.plot(time[30:], testT[30:], 'o', label='Constructed Data')
    # #plt.plot(fit_temps, fit_decays, label='Fitted Curve')
    # plt.xlabel('Time')
    # plt.ylabel('Temperature')
    # plt.legend()
    plt.show()


if __name__ == "__main__":
    # Replace 'your_file.csv' with the actual file path
    csv_file_path = 'Data/alpha.csv'
    plot_interpolation(csv_file_path)
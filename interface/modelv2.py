import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import derivative

def cubic_interpolation_tangent(csv_file, dcont = 7000, dini = 1000):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Extract time and temperature columns
    time = df['time']
    temperature = df['temperature']

    # Perform cubic interpolation
    sept_interp = np.poly1d(np.polyfit(time, temperature, 5))
    print(sept_interp)
    # Define the derivative of sept_interp
    derivative_sept_interp = np.polyder(sept_interp)
    
    # Find the roots (where derivative is equal to 0)
    roots = np.roots(derivative_sept_interp)

    # Filter out real roots (ignore complex roots)
    real_roots = roots[np.isreal(roots)].real

    sderivative_sept_interp = np.polyder(derivative_sept_interp)

    sroots = np.roots(sderivative_sept_interp)

    # Filter out real roots (ignore complex roots)
    real_sroots = sroots[np.isreal(sroots)].real

    min_time, max_time = min(time), max(real_roots)

    # Calculate the difference between the minimum and maximum values of temperature
    temp_diff =  sept_interp(real_roots[0]) - temperature[0]
    
    initial_value = temperature[0]
    threshold_value = 1.01 * initial_value
    tau_dead = (time[next(i for i, temp in enumerate(temperature) if temp >= threshold_value)] - time[0])/60
    
    
    # Calculate the tangent point as a percentage of the temperature difference
    tangent_point = sept_interp(real_sroots[0])

    # Generate values for the cubic interpolation
    time_interp = np.linspace(min_time, max_time, 100)
    temperature_interp = sept_interp(time_interp)

    # Find the index of the point on the interpolated curve closest to the tangent point
    index = np.argmin(np.abs(temperature_interp - tangent_point))

    # Calculate the tangent slope using the derivative of the cubic interpolation
    tangent_slope = sept_interp.deriv()(time_interp[index])

    # Calculate the tangent line using point-slope form
    tangent_line = tangent_slope * (time_interp - time_interp[index]) + tangent_point

    tau_planta = ((((sept_interp(real_roots[0]) - tangent_point))/tangent_slope + time_interp[index]) - tau_dead)/60
    
    print("\n")
    print("Open-Loop Data")
    print(f"Delta_controle: {dcont} units")
    print(f"Delta_planta: {temp_diff} ºC")
    print(f"Tau_dead: {tau_dead} Minutes")
    print(f"Tau_planta: {tau_planta} Minutes")
    print("\n")

    Rplant = tau_dead/ tau_planta
    bK_0 = ((dcont/8196)/(temp_diff/366))*Rplant

    cca = (sept_interp(real_roots[0])/temperature[0])*Rplant

    print(f"R: {Rplant}")
    print(f"K0: {bK_0}")
    print("\n")

    zK_p = 1.2/cca
    zK_i = zK_p/(2 * tau_dead)
    zK_d = zK_p*(0.5 * tau_dead)

    print("Ziegler-Nichols Method")
    print(f"Kp: {zK_p}")
    print(f"Ki: {zK_i}")
    print(f"Kp: {zK_d}")
    print("\n")
    
    cctau = tau_dead/(tau_dead+tau_planta)
    
    
    ccK_p = 1.35/cca*(1+((0.18*cctau)/(1-cctau)))
    ccK_i = ccK_p/(((2.5-2.0*cctau)/(1-0.39*cctau))*tau_dead)
    ccK_d = ccK_p*(((0.37-0.37*cctau)/(1-0.81*cctau))*tau_dead)

    print("Cohen-Coon Method")
    print(f"Kp: {ccK_p}")
    print(f"Ki: {ccK_i}")
    print(f"Kp: {ccK_d}")
    print("\n")
    
    plt.scatter(time, temperature, label='Data')
    plt.plot(time_interp, temperature_interp, label='Cubic Interpolation', color='r')
    plt.plot(time_interp, tangent_line, label='Tangent Line', linestyle='--', color='g')
    plt.title('Temperature vs Time with Interpolation and Tangent Line')
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (ºC)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Replace 'your_file.csv' with the actual file path
    csv_file_path = 'Data/interesse.csv'
    cubic_interpolation_tangent(csv_file_path,1000,500)
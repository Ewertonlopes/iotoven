import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Define the exponential function
def exponential_function(x, a, b, c):
    return a * np.exp(b * x) + c

# Generate some example data
x_data = np.array([1, 2, 3, 4, 5])
y_data = np.array([2.3, 3.4, 8.1, 18.7, 40.2])

# Fit the exponential function to the data
params, covariance = curve_fit(exponential_function, x_data, y_data)

# Extract the fitted parameters
a_fit, b_fit, c_fit = params

# Generate the fitted curve
x_fit = np.linspace(min(x_data), max(x_data), 100)
y_fit = exponential_function(x_fit, a_fit, b_fit, c_fit)

# Plot the original data and the fitted curve
plt.scatter(x_data, y_data, label='Original Data')
plt.plot(x_fit, y_fit, label='Fitted Curve', color='red')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()
plt.show()
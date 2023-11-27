import numpy as np
import matplotlib.pyplot as plt

# dT/dt
def my_function(P,T,t):
    return 0.3 - 0.03*(T-26)

# Generate t values
t_values = np.linspace(0, 100, 100)

# Calculate y values for each x
y_values = np.zeros(100)
y_values[0] = 26
for i in range(99):
    y_values[i+1] = y_values[i] + my_function(300,y_values[i],i+1) 

# Plot the function
plt.plot(t_values, y_values, label='T(t) = T + dT/dt')
plt.title('Function Plot')
plt.xlabel('t')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()

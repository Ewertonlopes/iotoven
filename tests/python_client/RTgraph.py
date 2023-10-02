import matplotlib.pyplot as plt
import numpy as np
from itertools import count
from matplotlib.animation import FuncAnimation

# Initialize empty lists to store data points
x_data = []
y_data = []

# Create a function to add new data points
def add_data():
    x_data.append(next(index))
    y_data.append(np.random.randint(0, 100))  # Replace this with your actual data source

# Create a counter for the x-axis
index = count()

# Create a function to update the graph
def update_graph(i):
    add_data()
    plt.cla()  # Clear the previous plot
    plt.plot(x_data, y_data, label='Data')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()

# Create an animated plot
ani = FuncAnimation(plt.gcf(), update_graph, interval=1000)  # Update every 1 second (1000 milliseconds)

# Show the plot
plt.tight_layout()
plt.show()

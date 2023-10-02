import http.client
import time
import matplotlib.pyplot as plt
import csv
from matplotlib.animation import FuncAnimation
from requests.exceptions import ConnectionError

x_data = []
t_data = []

starttime = time.time()

conn = http.client.HTTPConnection("localhost:8000")
endpoint = "/"
csv_filename = "data/Graphs.csv"

def add_data():
    global conn
    try:
        conn.request("GET", endpoint)
        r1 = conn.getresponse()
        while chunk := r1.read(200):
            output = float(chunk.decode())
        
        actualtime = time.time() - starttime

        x_data.append(output)
        t_data.append(actualtime)

        with open(csv_filename, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([actualtime, output])

        conn.close()
    except ConnectionRefusedError as e:
        print(f"Connection error: {e}")     


def update_graph(i):
    add_data()
    plt.cla()  # Clear the previous plot
    plt.plot(t_data, x_data, label='Data')
    plt.xlabel('t-axis')
    plt.ylabel('x-axis')
    plt.legend()

ani = FuncAnimation(plt.gcf(), update_graph, frames=None,repeat=False, interval=250)  # Update every 1 second (1000 milliseconds)

plt.tight_layout()
plt.show()
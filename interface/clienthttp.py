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

    # Customize the plot aesthetics
    plt.plot(t_data, x_data, label='Temperature', color='b', linewidth=2, marker='o', markersize=5)
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.title('Temperature Caracterization',fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper left')
    
    # Beautify the x-axis timestamps (optional)
    plt.gcf().autofmt_xdate()

    plt.gca().set_facecolor('#f5f5f5')  # Set background color

ani = FuncAnimation(plt.gcf(), update_graph, frames=None,repeat=False, interval=250)  # Update every 1 second (1000 milliseconds)

plt.tight_layout()
plt.show()
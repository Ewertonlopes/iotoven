import http.client
import time
import matplotlib.pyplot as plt
import csv
from matplotlib.animation import FuncAnimation
from requests.exceptions import ConnectionError
import numpy as np
import warnings

x_data = []
x_pred = []
t_data = []

for i in range(120):
    x_pred.append(0)

starttime = time.time()

conn = http.client.HTTPConnection("192.168.4.1:80")
endpointget = "/"
endpointpost = "/receiver"
csv_filename = "data/Graphs.csv"

window_time = np.zeros(60)
window_temp = np.zeros(60)

running = 0
delay = 60
acce = 0
omega = 0.0152
actual = 0

def predict_future(temperature,xpred,window_dt,window_t):
    error = (temperature - xpred)
    if running > 119 :
        acce += omega*error

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=np.RankWarning)
        coefficients = np.polyfit(window_dt, window_t, 1)
    fit_function = np.poly1d(coefficients)
    return fit_function(delay) + acce

def send_future(fp):
    fp = "0"
    postmes = "mod:0,fp:"+fp

    conn.request("POST", endpointpost,postmes)

    conn.close()


def add_data():
    global conn
    try:
        conn.request("GET", endpointget)
        r1 = conn.getresponse()
        while chunk := r1.read(200):
            output = float(chunk.decode())
        
        actualtime = time.time() - starttime

        x_data.append(output)
        t_data.append(actualtime)

        conn.close()

        window_temp[actual] = output
        window_time[actual] = delay
        actual = (actual + 1)%delay

        if(running>59):
            future = predict_future(output,x_pred[running],window_time,window_temp)
            send_future(future)

        x_pred.append(future)
        running += 1

        with open(csv_filename, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([actualtime, output])

    except ConnectionRefusedError as e:
        print(f"Connection error: {e}")     


def update_graph(i):
    add_data()
    plt.cla()  # Clear the previous plot

    # Customize the plot aesthetics
    plt.plot(t_data, x_data, label='Temperature', color='b', linewidth=0, marker='o', markersize=5)
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.title('Temperature Caracterization',fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper left')
    
    # Beautify the x-axis timestamps (optional)
    plt.gcf().autofmt_xdate()

    plt.gca().set_facecolor('#f5f5f5')  # Set background color

ani = FuncAnimation(plt.gcf(), update_graph, frames=None,repeat=False, interval=1000)  # Update every 1 second (1000 milliseconds)

plt.tight_layout()
plt.show()




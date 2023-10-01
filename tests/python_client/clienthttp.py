import http.client
import time
import matplotlib.pyplot as plt
import numpy as np
from IPython import display

x = np.array([])
t = np.array([])
corr = 0.0
freq = int(input('Enter Frequency of Test:'))
tottime = freq*int(input('Enter Time of Test:'))
periodo = 1/freq

start_time = time.time()

for i in range(tottime):
    conn = http.client.HTTPConnection("192.168.4.1")
    conn.request("GET", "/")

    r1 = conn.getresponse()
    output = 0.0
    
    while chunk := r1.read(200):
        output = float(chunk.decode())

    actualtime = time.time()

    conn.close()
    x = np.append(x,output)
    t = np.append(t,actualtime - start_time)
    time.sleep(periodo)

plt.title("Temperature Caracterization")
plt.plot(t,x, 'o') 
plt.show()

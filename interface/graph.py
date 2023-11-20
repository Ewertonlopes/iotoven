import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from random import randint
import threading
import time
import http.client
import csv
import datetime
import tkinter.filedialog as filedialog
import numpy as np

class LiveGraphApp:
    def __init__(self, root):
        # Create the main frame
        self.root = root
        self.root.title("Live Temperature from the Oven")

        self.update_interval = 0.25
        self.csv_filename = None
        # Create and pack the live graph frame
        self.frame_graph = ttk.Frame(self.root)
        self.frame_graph.pack(side=tk.LEFT, padx=10)

        self.loc = 1
        self.scurve = 0
        self.h = 0
        self.lasttime = 0

        self.curvetime = []
        self.curvedata = []

        self.fig, self.ax = plt.subplots()
        self.ax.set_xticks(np.arange(0, 600, 60))
        self.ax.set_yticks(np.arange(0, 350, 20))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_graph)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.data_points = []
        self.t_values = []
        self.max_data_points = 3500

        self.stop_button = ttk.Button(self.frame_graph, text="Send Curve", command=self.send_curve)
        self.stop_button.pack(side=tk.LEFT)

        self.stop_button = ttk.Button(self.frame_graph, text="Stop Data", command=self.stop_update)
        self.stop_button.pack(side=tk.BOTTOM)

        self.start_button = ttk.Button(self.frame_graph, text="Get Data", command=self.start_update)
        self.start_button.pack(side=tk.BOTTOM)

        # Create and pack the PID control frame
        self.frame_pid = ttk.Frame(self.root)
        self.frame_pid.pack(side=tk.RIGHT, padx=10)

        label_ip = ttk.Label(self.frame_pid, text="IP Address:")
        label_ip.pack(pady=5)
        self.entry_ip = ttk.Entry(self.frame_pid)
        self.entry_ip.pack(pady=5)

        label_mode = ttk.Label(self.frame_pid, text="Select Mode:")
        label_mode.pack(pady=5)
        self.var = tk.IntVar()
        radio_mode0 = ttk.Radiobutton(self.frame_pid, text="Setpoint", variable=self.var, value=0)
        radio_mode1 = ttk.Radiobutton(self.frame_pid, text="Tuning", variable=self.var, value=1)
        radio_mode2 = ttk.Radiobutton(self.frame_pid, text="Control Signal", variable=self.var, value=2)
        self.radio_mode3 = ttk.Radiobutton(self.frame_pid, text="Local", variable=self.var, value=3)
        radio_mode0.pack()
        radio_mode1.pack()
        radio_mode2.pack()
        self.radio_mode3.pack()

        # PID Parameters Entry (visible only when Mode 1 is selected)
        self.label_kp = ttk.Label(self.frame_pid, text="Enter Kp:")
        self.entry_kp = ttk.Entry(self.frame_pid)

        self.label_ki = ttk.Label(self.frame_pid, text="Enter Ki:")
        self.entry_ki = ttk.Entry(self.frame_pid)

        self.label_kd = ttk.Label(self.frame_pid, text="Enter Kd:")
        self.entry_kd = ttk.Entry(self.frame_pid)

        # s Value Entry (visible only when Mode 0 is selected)
        self.label_s = ttk.Label(self.frame_pid, text="Enter setpoint:")
        self.entry_s = ttk.Entry(self.frame_pid)

        self.label_cs = ttk.Label(self.frame_pid, text="Enter control signal:")
        self.entry_cs = ttk.Entry(self.frame_pid)

        # Initial state: Mode 0 (visible), Mode 1 (hidden)
        self.label_kp.pack_forget()
        self.entry_kp.pack_forget()
        self.label_ki.pack_forget()
        self.entry_ki.pack_forget()
        self.label_kd.pack_forget()
        self.entry_kd.pack_forget()
        self.label_s.pack_forget()
        self.entry_s.pack_forget()
        self.label_cs.pack_forget()
        self.entry_cs.pack_forget()

        def show_params():
            if self.var.get() == 1:
                self.label_kp.pack()
                self.entry_kp.pack()
                self.label_ki.pack()
                self.entry_ki.pack()
                self.label_kd.pack()
                self.entry_kd.pack()
                self.label_s.pack_forget()
                self.entry_s.pack_forget()
                self.label_cs.pack_forget()
                self.entry_cs.pack_forget()
            elif self.var.get() == 0:
                self.label_kp.pack_forget()
                self.entry_kp.pack_forget()
                self.label_ki.pack_forget()
                self.entry_ki.pack_forget()
                self.label_kd.pack_forget()
                self.entry_kd.pack_forget()
                self.label_s.pack()
                self.entry_s.pack()
                self.label_cs.pack_forget()
                self.entry_cs.pack_forget()
            elif self.var.get() == 2:
                self.label_kp.pack_forget()
                self.entry_kp.pack_forget()
                self.label_ki.pack_forget()
                self.entry_ki.pack_forget()
                self.label_kd.pack_forget()
                self.entry_kd.pack_forget()
                self.label_s.pack_forget()
                self.entry_s.pack_forget()
                self.label_cs.pack()
                self.entry_cs.pack()
            else:
                self.label_kp.pack_forget()
                self.entry_kp.pack_forget()
                self.label_ki.pack_forget()
                self.entry_ki.pack_forget()
                self.label_kd.pack_forget()
                self.entry_kd.pack_forget()
                self.label_s.pack_forget()
                self.entry_s.pack_forget()
                self.label_cs.pack_forget()
                self.entry_cs.pack_forget()
                

        # Update parameters visibility when the mode is changed
        self.var.trace("w", lambda name, index, mode: show_params())

        # Submit Button for PID Control
        submit_button = ttk.Button(self.frame_pid, text="Send Request", command=self.send_request)
        submit_button.pack(pady=10)

        # Response Label for PID Control
        self.result_label_pid = ttk.Label(self.frame_pid, text="")
        self.result_label_pid.pack()

        # Create and pack the file selection frame
        self.frame_file = ttk.Frame(self.root)
        self.frame_file.pack(side=tk.TOP, pady=10)

        self.file_button = ttk.Button(self.frame_file, text="Curve", command=self.select_file)
        self.file_button.pack(side=tk.RIGHT)

    def send_curve(self):
        self.scurve = 1
        self.update_running = True
        self.h = 0
        self.lasttime = 0
        self.start_update()

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select a CSV file", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.curvetime = []
            self.curvedata = []
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file, delimiter=',')

                next(csv_reader)

                for row in csv_reader:

                    time = round(float(row[0]),2)
                    temperature = round(float(row[1]),2)

                    self.curvetime.append(time)
                    self.curvedata.append(temperature)
                
                self.ax.clear()
                self.ax.plot(self.curvetime, self.curvedata, marker='o',color='blue')
                self.ax.set_title("Temperature")
                self.ax.set_xlabel("Tempo(s)")
                self.ax.set_ylabel("Temperatura(ºC)")

                self.canvas.draw()

    def send_request(self):
        ESPADDRESS = self.entry_ip.get()  # Get IP address from the entry widget
        mod = self.var.get()  # Get the value of the radio button (0 or 1)

        conn = http.client.HTTPConnection(ESPADDRESS)
        endpoint = "/receiver"

        if mod == 0:
            s = self.entry_s.get()
            postmes = "mod:0,s:" + s
        elif mod == 1:
            kp = self.entry_kp.get()
            ki = self.entry_ki.get()
            kd = self.entry_kd.get()
            postmes = "mod:1,kp:" + kp + ",ki:" + ki + ",kd:" + kd
        elif mod == 2:
            c = self.entry_cs.get()
            postmes = "mod:2,o:" +c
        elif mod == 3:
            self.loc = not (self.loc)
            if(self.loc):
                self.radio_mode3.text = "Local"
            else:
                self.radio_mode3.text = "Fog"
            postmes = f"mod:3,loc:{self.loc}"

        conn.request("POST", endpoint, postmes)
        response = conn.getresponse()
        conn.close()

        self.result_label_pid.config(text=response.read().decode())

    def delete_data(self):
        self.data_points = []
        self.t_values = []
        self.ax.clear()
        self.ax.set_title("Temperature")
        self.ax.set_xlabel("Tempo(s)")
        self.ax.set_ylabel("Temperatura(ºC)")
        self.canvas.draw()

    def add_data(self):
        try:
            ESPADDRESS = self.entry_ip.get()
            ENDPOINT = "/"
            conn = http.client.HTTPConnection(ESPADDRESS)
            conn.request("GET", ENDPOINT)
            r1 = conn.getresponse()
            while chunk := r1.read(200):
                output = float(chunk.decode())
            
            actualtime = time.time() - self.starttime

            self.data_points.append(output)
            self.t_values.append(actualtime)

            with open(self.csv_filename, mode='a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([actualtime, output])

            conn.close()
        except ConnectionRefusedError as e:
            print(f"Connection error: {e}") 

    def start_update(self):
        self.update_running = True
        self.starttime = time.time()
        self.t_values = []
        self.data_points = []

        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%d-%m-%Y_%H-%M-%S")
        self.csv_filename = f"data/graph_{formatted_time}.csv"

        with open(self.csv_filename, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["time","temperature"])

        self.start_button['state'] = tk.DISABLED
        self.stop_button['state'] = tk.NORMAL
        self.update_data()

    def stop_update(self):
        self.update_running = False
        self.start_button['state'] = tk.NORMAL
        self.stop_button['state'] = tk.DISABLED

    def update_data(self):
        if self.update_running:
            self.add_data()
            if self.scurve:
                if(float(self.curvetime[self.h]) > self.lasttime):
                    ESPADDRESS = self.entry_ip.get()
        
                    data = self.curvedata[self.h]
                    conn = http.client.HTTPConnection(ESPADDRESS)
                    endpoint = "/receiver"
                    s = data
                    postmes = "mod:0,s:" + s
                    conn.request("POST", endpoint, postmes)
                    response = conn.getresponse()

                    self.result_label_pid.config(text=response.read().decode())
                    conn.close()
                    self.lasttime = self.curvetime[self.h]
                    self.h +=1
                    if self.h == len(self.curvedata):
                        self.scurve = 0
                        self.update_running = False

            if len(self.data_points) > self.max_data_points:
                self.data_points.pop(0)
                self.t_values.pop(0)

            self.ax.clear()
            self.ax.plot(self.t_values, self.data_points, marker='o',color='red')
            self.ax.plot(self.curvetime, self.curvedata, marker='o',color='blue')
            self.ax.set_title("Temperature")
            self.ax.set_xlabel("Tempo(s)")
            self.ax.set_ylabel("Temperatura(ºC)")
            # Set the interval for ticks on the x and y axes

            self.canvas.draw()

            self.root.after(int(self.update_interval * 1000), self.update_data)
        else:
            print("Update stopped.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LiveGraphApp(root)
    root.mainloop()

import tkinter as tk
import http.client

def send_request():
    ESPADDRESS = entry_ip.get()  # Get IP address from the entry widget
    mod = var.get()  # Get the value of the radio button (0 or 1)

    conn = http.client.HTTPConnection(ESPADDRESS)
    endpoint = "/receiver"

    if not mod:
        s = entry_s.get()
        postmes = "mod:0,s:" + s
    else:
        kp = entry_kp.get()
        ki = entry_ki.get()
        kd = entry_kd.get()
        postmes = "mod:1,kp:" + kp + ",ki:" + ki + ",kd:" + kd

    conn.request("POST", endpoint, postmes)
    response = conn.getresponse()
    
    result_label.config(text=response.read().decode())

# Create the main window
root = tk.Tk()
root.title("ESP8266 Controller")

# IP Address Entry
label_ip = tk.Label(root, text="ESP8266 IP Address:")
label_ip.pack(pady=5)
entry_ip = tk.Entry(root)
entry_ip.pack(pady=5)

# Mode Selection
label_mode = tk.Label(root, text="Select Mode:")
label_mode.pack(pady=5)
var = tk.IntVar()
radio_mode0 = tk.Radiobutton(root, text="Mode 0", variable=var, value=0)
radio_mode1 = tk.Radiobutton(root, text="Mode 1", variable=var, value=1)
radio_mode0.pack()
radio_mode1.pack()

# PID Parameters Entry (visible only when Mode 1 is selected)
label_kp = tk.Label(root, text="Enter Kp:")
entry_kp = tk.Entry(root)

label_ki = tk.Label(root, text="Enter Ki:")
entry_ki = tk.Entry(root)

label_kd = tk.Label(root, text="Enter Kd:")
entry_kd = tk.Entry(root)

# s Value Entry (visible only when Mode 0 is selected)
label_s = tk.Label(root, text="Enter s:")
entry_s = tk.Entry(root)

# Initial state: Mode 0 (visible), Mode 1 (hidden)
label_kp.pack_forget()
entry_kp.pack_forget()
label_ki.pack_forget()
entry_ki.pack_forget()
label_kd.pack_forget()
entry_kd.pack_forget()
label_s.pack_forget()
entry_s.pack_forget()

def show_params():
    if var.get() == 1:
        label_kp.pack()
        entry_kp.pack()
        label_ki.pack()
        entry_ki.pack()
        label_kd.pack()
        entry_kd.pack()
        label_s.pack_forget()
        entry_s.pack_forget()
    else:
        label_kp.pack_forget()
        entry_kp.pack_forget()
        label_ki.pack_forget()
        entry_ki.pack_forget()
        label_kd.pack_forget()
        entry_kd.pack_forget()
        label_s.pack()
        entry_s.pack()

# Update parameters visibility when the mode is changed
var.trace("w", lambda name, index, mode: show_params())

# Submit Button
submit_button = tk.Button(root, text="Send Request", command=send_request)
submit_button.pack(pady=10)

# Response Label
result_label = tk.Label(root, text="")
result_label.pack()

# Start the GUI event loop
root.mainloop()

import http.client

ESPADDRESS = "192.168.4.1:80"

conn = http.client.HTTPConnection(ESPADDRESS)
endpoint = "/receiver"
mod = 3
if(mod == 3):
    loc = "0"
    postmes = "mod:3,loc:"+loc
elif(mod == 2):
    o = "0"
    postmes = "mod:2,s:"+o
elif(mod == 1):
    kp = "6.0"
    ki = "0.06"
    kd = "396"
    postmes = "mod:1,kp:"+kp+",ki:"+ki+",kd:"+kd
elif(mod == 0):
    s = "0"
    postmes = "mod:0,o:"+s

conn.request("POST", endpoint,postmes)

response = conn.getresponse()
print(response.read().decode())
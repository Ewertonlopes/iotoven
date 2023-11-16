import http.client

ESPADDRESS = "192.168.4.1:80"

conn = http.client.HTTPConnection(ESPADDRESS)
endpoint = "/receiver"
mod = 0
if(not mod):
    s = "0"
    postmes = "mod:0,s:"+s
else:
    kp = "6.0"
    ki = "0.06"
    kd = "396"
    postmes = "mod:1,kp:"+kp+",ki:"+ki+",kd:"+kd

conn.request("POST", endpoint,postmes)

response = conn.getresponse()
print(response.read().decode())
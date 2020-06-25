from socket import *

import os
s=os.popen('ipconfig/all')
o=s.read()
a=list()
a=o.split('\n')
a

def start():
    import os
    import re
    s=os.popen('ipconfig/all')
    o=s.read()
    a=o.split('\n')
    e=''
    for i in a:
        if i.startswith('Wireless LAN adapter Wi-Fi:'):
            b=a.index(i)+8
            c=a[b]
            d=re.findall(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}',c)
    for j in d:
        e=e+j
    return e
f=start()

HOST = f #replaced with the server's IP
PORT = 2000

#Replace with your methods.
def startstopgesture():
    return print("Start or Stop Gesture")
def startfacedetection():
    return print("Start Face Detection")
def takeoff():
    return print("Take Off")
def land():
    return print("Land")
def moveforward():
    return print("Move Forward")
def movebackward():
    return print("Move Backward")
def moveup():
    return print("Move Up")
def movedown():
    return print("Move Down")
def moveleft():
    return print("Move Left")
def moveright():
    return print("Move Right")
def captureimage():
    return print("Capture Image")
def record():
    return print("Record")
def stayatonepoint():
    return print("Stay at one Point")

s = socket(AF_INET, SOCK_STREAM)
s.bind(('HOST', PORT))
s.listen(1)
conn, addr = s.accept()
print("Connected by: " , addr)
while True:
    data=conn.recv(40960)
    break

b=data.decode()

print(b)

if "11" in b:
    startstopgesture()
if "12" in b:
    startfacedetection()
if "13" in b:
    takeoff() 
if "14" in b:
    land()
if "15" in b:
    moveforward()
if "16" in b:
    movebackward()
if "17" in b:
    moveup()
if "18" in b:
    movedown()
if "19" in b:
    moveleft()
if "20" in b:
    moveright()
if "21" in b:
    captureimage()
if "22" in b:
    record()
if "23" in b:
    stayatonepoint()

conn.close() 
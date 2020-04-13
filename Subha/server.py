from socket import *
HOST = "192.168.43.82" #replaced with the server's IP
PORT = 21
b=''

#Replace with your methods.
def takeoff():
    return print("Drone Take Off")
def land():
    return print("Drone Land")
def moveright():
    return print("Drone Move Right")
def moveleft():
    return print("Drone Move Left")
def capturevideo():
    return print("Drone Capture Video")

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print("Connected by: " , addr)
while True:
    data=conn.recv(40960)
    if not data:
        break
    b=data.decode()
print(b)
if "Take Off" in b:
    takeoff() 
if "Land" in b:
    land()
if "Move Right" in b:
    moveright()
if "Move Left" in b:
    moveleft()
if "Capture Video" in b:
    capturevideo()
conn.close() 
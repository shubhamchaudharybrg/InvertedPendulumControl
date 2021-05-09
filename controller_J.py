# This is the remote controller from simulated inverted pendulum.
# It utilizes PID control for stabalizing the pendulum.

import socket, time
import random
from pyconsys.Control import Control
from pyconsys.PIDControl import PIDControl
import numpy as np

IP_ADDRESS = "127.0.0.1" #"127.0.0.1" #"192.168.43.98" #"192.168.137.1"
PORT = 12345
DISCONNECT_MESSAGE = "DISCONNECT"
MESSAGE_LENGTH = 130 #13
PID_CONTROL = PIDControl(105, 83, 28)  # Kp, Ki, Kd
angList = []
_max = 0
SIMULATION_TIME = 25 # in sec

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP_ADDRESS,PORT))
s.listen()

def getControl(angle):
    desiredAngle = float(0)
    error = (desiredAngle - angle*-1)
    # print(f"error calculated : {error}")
    control = PID_CONTROL.get_xa(error) # Applying PID
    # print(f"control calculated : {control}") 
    return control

connection, adreess = s.accept()
print("Connected")

ts = time.time(); te = time.time()
while True:
    # print(f"te-ts : {te-ts}")
    introducedJitter = np.random.uniform(0,0.01)
    if te-ts > SIMULATION_TIME:
        break

    time.sleep(introducedJitter)  # Introduces Jitter 

    ang = connection.recv(MESSAGE_LENGTH).decode()

    if ang == DISCONNECT_MESSAGE:
        break
   
    ang = ang.split('/n')[:-1:1]
    # print(ang)
    
    angList.extend(ang)
    # print(angList)

    _angle = float(angList.pop(0))
    if abs(_angle) > _max:
        _max = abs(_angle)
    
    ctrl = getControl(_angle)
    print(introducedJitter)
    connection.send(bytes(str(round(ctrl, 10)), "utf-8"))
    te = time.time()
    
print(f"Max Angle : {_max*180/np.pi}")
connection.close()
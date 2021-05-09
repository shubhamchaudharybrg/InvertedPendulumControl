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
count1 = 0
count2 = 0
while True:
    # print(f"te-ts : {te-ts}")
    currentTime = te-ts
    if currentTime > SIMULATION_TIME:
        break

    ang = connection.recv(MESSAGE_LENGTH).decode()
    if ang == DISCONNECT_MESSAGE:
        break
   
    ang = ang.split('/n')[:-1:1]
    # print(len(ang))

    angList.extend(ang)
    # print(len(angList))

    _angle = float(angList.pop(0))
    
    ctrl = getControl(_angle)

    ############################################################################
    # if currentTime < 8: # Adds disturbance
    #     connection.send(bytes("0","utf-8"))
        # print("Sent")

    # Simulting Packet Loss(in %)
    # else:
    if 0.1 <= np.random.uniform(0,1) < 0.6 :
        connection.send(bytes(str(round(ctrl, 10)), "utf-8"))
        count1 += 1
    
    else:
        count2 += 1
    ############################################################################
    # if currentTime > 18:
    if abs(_angle) > _max:
        _max = abs(_angle)

    te = time.time()
    
print(f"Max Angle : {_max*180/np.pi} ; Packet Loss % : {count2/(count1+count2)}")
connection.close()
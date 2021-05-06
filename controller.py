# This is the remote controller from simulated inverted pendulum.
# It utilizes PID control for stabalizing the pendulum.

import socket, time
import random
from pyconsys.Control import Control
from pyconsys.PIDControl import PIDControl
import simulatedScenarios as ss

IP_ADDRESS = "127.0.0.1"
PORT = 5432
DISCONNECT_MESSAGE = "DISCONNECT"
# ACKNOWELEDGE_MESSAGE = "ACK"
# RTS = "RTS"
# CTS = "CTS"
MESSAGE_LENGTH = 13
PID_CONTROL = PIDControl(105, 100, 60)  # Kp, Ki, Kd 105, 83, 28

pendulumAngle = 0 # Receives from simulated pendulum

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP_ADDRESS,PORT))
s.listen()

connection, adreess = s.accept()
print("Connected")

def getControl(angle):
    desiredAngle = float(0)
    error = (desiredAngle - angle*-1)
    # print(f"error calculated : {error}")
    control = PID_CONTROL.get_xa(error) # Applying PID
    # print(f"control calculated : {control}") 
    return control

# count = 0
# data = 0

while True:
# for ii in range(10):
    # print(f"Data Before : {data}")
    # ss.latency(0.2)
    data = connection.recv(MESSAGE_LENGTH).decode()
    newData = data[0:12]
    # print(f"Data After : {data}")
    
    if data == DISCONNECT_MESSAGE:
        break
    else:
        # if count <= 300: 

        controlData = getControl(float(data))
        print(f"Angle : {data} , Control : {controlData}")
        print(f"newData : {newData}")

        ss.latency(0.2)
        connection.send(bytes(str(round(controlData, 10)), "utf-8"))
        
        # elif count > 450:
            # count = 0
    # print(count)
    # count += 1
connection.close()
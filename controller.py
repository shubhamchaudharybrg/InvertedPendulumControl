# This is the remote controller from simulated inverted pendulum.
# It utilizes PID control for stabalizing the pendulum.

import socket, time
import random
from pyconsys.Control import Control
from pyconsys.PIDControl import PIDControl

IP_ADDRESS = "127.0.0.1"
PORT = 5432
DISCONNECT_MESSAGE = "DISCONNECT"
ACKNOWELEDGE_MESSAGE = "ACK"
RTS = "RTS"
CTS = "CTS"
MESSAGE_LENGTH = 128
PID_CONTROL = PIDControl(105, 83, 28)  # Kp, Ki, Kd

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

while True:
# for ii in range(10):
    if random.randint(1, 1000) == 8:
        time.sleep(20)

    _angle = float(connection.recv(MESSAGE_LENGTH).decode())
    
    ctrl = getControl(_angle)
    print(f"angle : {_angle} , control : {ctrl}")
    connection.send(bytes(str(round(ctrl, 10)), "utf-8"))

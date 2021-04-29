# This is the remote controller from simulated inverted pendulum.
# It utilizes PID control for stabalizing the pendulum.

import socket, time
from pyconsys.PIDControl import PIDControl

IP_ADDRESS = "127.0.0.1"
PORT = 12345
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
    desiredAngle = 0
    error = (desiredAngle - pendulumAngle*-1)
    control = PID_CONTROL.get_xa(error) # Applying PID

    # pendelumLJoin.maxMotorTorque = 1000
    # pendelumRJoin.maxMotorTorque = 1000
    # pendelumLJoin.motorSpeed = y
    # pendelumRJoin.motorSpeed = y
    return control

while True:
    while connection.recv(MESSAGE_LENGTH).decode() != RTS:
        print("Waiting for RTS Message....")   
    print("Received RTS") 

    connection.send(bytes(CTS, "utf-8"))
    print("CTS Sent")

    # while connection.recv(MESSAGE_LENGTH) == None:
    #     print("Waiting for data....")

    time.sleep(0.0001)  # 100 micro-second
    _angle = float(connection.recv(MESSAGE_LENGTH).decode())
    print(f"Received angle : {_angle}")
    
    ctrl = getControl(_angle)
    print(f"Control : {ctrl}")

    connection.send(bytes(ACKNOWELEDGE_MESSAGE, "utf-8"))
    print("ACK Message Sent")

    connection.send(bytes(str(round(ctrl, 10)), "utf-8"))

# connection.send(bytes(DISCONNECT_MESSAGE, "utf-8"))
# connection.close()
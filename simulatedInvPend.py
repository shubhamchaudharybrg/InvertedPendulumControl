# Simuated Inverted Pendulum controlled remotely
import socket
import cv2
from invertedPendulum import InvertedPendulum

IP_ADDRESS = "127.0.0.1"
PORT = 1234
DISCONNECT_MESSAGE = "DISCONNECT"
ACKNOWELEDGE_MESSAGE = "ACK"
MESSAGE_LENGTH = 512

pendulum = InvertedPendulum()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP_ADDRESS, PORT))
print("Connected")

receivedData = ""

while receivedData != DISCONNECT_MESSAGE:
    s.send(bytes(ACKNOWELEDGE_MESSAGE, "utf-8"))

    receivedMsg = s.recv(MESSAGE_LENGTH).decode()
    print(receivedData)
    tmpMsg = receivedMsg.split(",")
    msg = [float(i) for i in tmpMsg]
    print(msg)

    rendered = pendulum.step( [msg[0], msg[1], msg[2], msg[3]], msg[4] )
    cv2.imshow( 'image', rendered )
    cv2.moveWindow( 'image', 100, 100 )
    
    if cv2.waitKey(30) == ord('q'):
        break

    s.send(bytes(ACKNOWELEDGE_MESSAGE, "utf-8"))
    
    # if cv2.waitKey(30) == ord('q'):
    #     break
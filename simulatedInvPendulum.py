from InvertedPendulum import InvertedPendulum
import socket

IP_ADDRESS = "127.0.0.1"
PORT = 1234
DISCONNECT_MESSAGE = "DISCONNECT"
MESSAGE_LENGTH = 32

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP_ADDRESS,PORT))
s.listen()

connection, adreess = s.accept()
print("Connected")
receivedData = ""

while receivedData != DISCONNECT_MESSAGE:
    receivedMessage = connection.recv(MESSAGE_LENGTH).decode()
    if receivedMessage == DISCONNECT_MESSAGE:
        break

connection.close()

pendulum = InvertedPendulum()

for i, t in enumerate(sol.t):
    rendered = pendulum.step( [sol.y[0,i], sol.y[1,i], sol.y[2,i], sol.y[3,i] ], t )
    cv2.imshow( 'im', rendered )
    cv2.moveWindow( 'im', 100, 100 )

    if cv2.waitKey(30) == ord('q'):
        break

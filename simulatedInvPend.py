import socket, time
from Box2D.examples.framework import (Framework, Keys, main)
from Box2D import (b2EdgeShape, b2FixtureDef, b2PolygonShape, b2CircleShape)
from pyconsys.Control import Control
from pyconsys.PIDControl import PIDControl

IP_ADDRESS = "127.0.0.1"
PORT = 12345
DISCONNECT_MESSAGE = "DISCONNECT"
ACKNOWELEDGE_MESSAGE = "ACK"
RTS = "RTS"
CTS = "CTS"
MESSAGE_LENGTH = 128

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP_ADDRESS, PORT))
print("Connected")


class BodyPendulum(Framework):
    name = "Inverted Pendulum"
    description = "Remotely Controlled"
    speed = 3

    def __init__(self):
        super(BodyPendulum, self).__init__()
        self.createWorld()

    def createWorld(self):
        self._isLiving = True
        self._auto = True
        # self._pid_control = PIDControl(105, 83, 28)  # kp, ki, kd


        self.ground = self.world.CreateBody(
            shapes=b2EdgeShape(vertices=[(-25, 0), (25, 0)])
        )

        self.carBody = self.world.CreateDynamicBody(
            position=(0, 3),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(5, 1)), density=1)

        )

        self.carLwheel = self.world.CreateDynamicBody(
            position=(-3, 1),
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=1), density=2, friction=1)

        )

        self.carRwheel = self.world.CreateDynamicBody(
            position=(3, 1),
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=1), density=2, friction=1)

        )

        self.pendulum = self.world.CreateDynamicBody(
            position=(0, 13),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(0.5, 10)), density=1),

        )

        self.pendelumJoin = self.world.CreateRevoluteJoint(
            bodyA=self.carBody,
            bodyB=self.pendulum,
            anchor=(0, 3),
            maxMotorTorque=1,
            enableMotor=True
        )

        self.pendelumRJoin =self.world.CreateRevoluteJoint(
            bodyA=self.carBody,
            bodyB=self.carRwheel,
            anchor=(3, 1),
            maxMotorTorque=1,
            enableMotor=True,
            # motorSpeed=10
        )

        self.pendelumLJoin = self.world.CreateRevoluteJoint(
            bodyA=self.carBody,
            bodyB=self.carLwheel,
            anchor=(-3, 1),
            maxMotorTorque=1,
            enableMotor=True,
            # motorSpeed=10
        )


    def destroyWorld(self):
        self.world.DestroyBody(self.carBody)
        self.world.DestroyBody(self.carLwheel)
        self.world.DestroyBody(self.carRwheel)
        self.world.DestroyBody(self.pendulum)
        self._isLiving = False


    def Keyboard(self, key):
    #     if key == Keys.K_a:
    #         if self._isLiving:
    #             self._auto = True

    #     elif key == Keys.K_m:
    #         self._auto = False
    #         if self._isLiving:
    #             self.pendelumLJoin.motorSpeed = 0
    #             self.pendelumLJoin.maxMotorTorque = 1
    #             self.pendelumRJoin.motorSpeed = 0
    #             self.pendelumRJoin.maxMotorTorque = 1
        
        if key == Keys.K_n:
            if self._isLiving:
                self.destroyWorld()
                self.createWorld()
        
        elif key == Keys().K_q:
            self.destroyWorld()
            s.send(bytes(DISCONNECT_MESSAGE, "utf-8"))
            s.close()

    def Step(self, settings):
        super(BodyPendulum, self).Step(settings)

        s.send(bytes(RTS, "utf-8"))
        print("RTS Message Sent")

        while s.recv(MESSAGE_LENGTH).decode() != CTS:
            print("Waiting for CTS Message....")
        print("CTS Received")
        print(f"Current Angle : {self.pendulum.angle}, Round : {round(self.pendulum.angle,10)}")
        s.send(bytes(str(round(self.pendulum.angle,10)), "utf-8"))
        print("Angle Sent")

        while s.recv(MESSAGE_LENGTH).decode() != ACKNOWELEDGE_MESSAGE:
            print("Waiting for ACK Message....")
        print("ACK Received")

        # while s.recv(MESSAGE_LENGTH) != None:
        #     print("Waiting for control....")

        time.sleep(0.000001)  # 1 micro-second
        controlSignal = float(s.recv(MESSAGE_LENGTH).decode())
        print(controlSignal)
    
        # if receivedMsg == DISCONNECT_MESSAGE:
        #     s.close()

        if self._auto == True and self._isLiving == True:
            self.pendelumLJoin.maxMotorTorque = 1000
            self.pendelumRJoin.maxMotorTorque = 1000
            self.pendelumLJoin.motorSpeed = controlSignal
            self.pendelumRJoin.motorSpeed = controlSignal


if __name__ == "__main__":
    main(BodyPendulum)

# while True:
#     s.send(bytes(ACKNOWELEDGE_MESSAGE, "utf-8"))
#     print("ACK Sent")

#     receivedMsg = s.recv(MESSAGE_LENGTH).decode()
#     # print(receiveqdData)
    
#     if receivedMsg == DISCONNECT_MESSAGE:
#         s.close()
#         break

#     tmpMsg = receivedMsg.split(",")
#     msg = [float(i) for i in tmpMsg]
#     print(msg)

#     rendered = pendulum.step( [msg[0], msg[1], msg[2], msg[3]], msg[4] )
#     cv2.imshow( 'image', rendered )
#     cv2.waitKey(100)
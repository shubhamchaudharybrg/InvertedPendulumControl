import socket, time
from Box2D.examples.framework import (Framework, Keys, main)
from Box2D import (b2EdgeShape, b2FixtureDef, b2PolygonShape, b2CircleShape)
from pyconsys.Control import Control
from pyconsys.PIDControl import PIDControl
# import simulatedScenarios as ss

IP_ADDRESS = "127.0.0.1"
PORT = 12345
DISCONNECT_MESSAGE = "DISCONNECT"
MESSAGE_LENGTH = 130 #16

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP_ADDRESS, PORT))
s.setblocking(False)
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
        self.count = 0

        self.ground = self.world.CreateBody(
            shapes=b2EdgeShape(vertices=[(-40, 0), (40, 0)])
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
        self.pendulum.angle = 0.04 # intial angle of pendulum


    def destroyWorld(self):
        self.world.DestroyBody(self.carBody)
        self.world.DestroyBody(self.carLwheel)
        self.world.DestroyBody(self.carRwheel)
        self.world.DestroyBody(self.pendulum)
        self._isLiving = False


    def Keyboard(self, key):
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
        
        controlSignal = 0

        a = self.pendulum.angle

        to_send = str(round(a,10))+'/n'
        # print(to_send)
        s.send(bytes(to_send, "utf-8"))

        try : 
            controlSignal = float(s.recv(MESSAGE_LENGTH).decode())
            self.pendelumLJoin.maxMotorTorque = 1000
            self.pendelumRJoin.maxMotorTorque = 1000
            self.pendelumLJoin.motorSpeed = controlSignal
            self.pendelumRJoin.motorSpeed = controlSignal
            print(1)
        except :
            self.pendelumLJoin.maxMotorTorque = 1
            self.pendelumRJoin.maxMotorTorque = 1
            self.pendelumLJoin.motorSpeed = 0
            self.pendelumRJoin.motorSpeed = 0
            print(0)
        
        self.count += 1
        print(self.count)
        # print(f"angle sent : {a} , control received : {controlSignal}")
        # print(controlSignal)

if __name__ == "__main__":
    main(BodyPendulum)
 

# Inverted Pendulum Control

This repo has the necessary files of the project which studied the effect of network parameters like high latency, jitter, packet loss, etc. on the stability of an simulated Inverted Pendulum remotely controlled using PID controller.
The pendulum was simulated on a Raspberry Pi which was controlled by a remote controller in a Laptop. Control signals were sent through socket connection.
Full details and result can be found in the project report here https://drive.google.com/file/d/1hGd4g3C7lx4cL41pKRfeLu9efZ-ha6If/view?usp=sharing

**controller_J.py**\
Has code to simulate jitter in the socket connection between controller on Laptop and pendulum on RPi.

**controller_L.py**\
Has code to simulate High Latency in the socket connection between controller on Laptop and pendulum on RPi.

**controller_PL_Random.py**
Has code to simulate random packet loss in the socket connection between controller on Laptop and pendulum on RPi.

**simulatedInvPend.py**\
It has the code to simulate inverted pendulum. The implementation is done in Python. \
The simulated inverted pendulum used in the project was a already available at https://github.com/mck-sbs/Pendulum 
Special Thanks to Metin Karatas (mck-sbs).\
Some modifications have been done as per our requirements.

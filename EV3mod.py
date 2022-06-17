#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

from time import gmtime, strftime
import time
import sys
import random
import threading

# 초기 설정
ev3 = EV3Brick()

PumpMotor = Motor(Port.D)
SortMotor = Motor(Port.C)
SeesawMotor = Motor(Port.B)
WheelMotor = Motor(Port.A)

ColorSensor = ColorSensor(Port.S4)

SortMotorSpeed = 1000
PumpMotorSpeed = 800
SeesawMotorSpeed = 1000
WheelMotorSpeed = 900

ev3.speaker.beep()

# 파란색 공만 우측길 허용
sortRightArrayColors = [Color.BLUE] 

# 좌/우 소팅 방향 결정
def sortDirection(direction):

    if direction == "L":
        SortMotor.run_angle(SortMotorSpeed, -120, Stop.BRAKE, True)
        SortMotor.reset_angle(0)
        
    elif direction == "R":
        SortMotor.run_angle(SortMotorSpeed, 120, Stop.BRAKE, True)
        SortMotor.reset_angle(0)
    else:
        sys.exit(1)

#sortRightArrayColor에서 설정한 색깔로 소터가 좌/우 중 어디로 가야하는지 판단
def trySort():
    while True:
        time.sleep(0.1)

        curColor = ColorSensor.color()

        # if there is no ball wait
        if curColor == None:
            time.sleep(0.1)

        else:
            # if the ball should be sorted right call sort function
            if curColor in sortRightArrayColors:
                sortDirection("R")
                time.sleep(0.15)

            # else the ball should be sorted left call sort function
            else:
                sortDirection("L")
                time.sleep(0.15)    

#Pump start
PumpMotor.run(PumpMotorSpeed)
wait(100)

#Seesaw start
SeesawMotor.run(SeesawMotorSpeed)
wait(100)

#Wheel start
WheelMotor.run(WheelMotorSpeed)
wait(100)

#run trysort()
t1 = threading.Thread(target=trySort, args=())
t1.daemon = True
t1.start()

#연속적인 실행위한 반복문설정
while True:
    wait(100)

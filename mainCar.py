from CarIRClass import CARIR
import _thread
import time as t
from machine import Pin,PWM

ENAPIN:int = 13
ENBPIN:int = 33

IN1PIN:int = 14
IN2PIN:int = 27
IN3PIN:int = 26 
IN4PIN:int = 25

ENCPIN:int = 23
ENDPIN:int = 5

IN5PIN:int = 18
IN6PIN:int = 19
IN7PIN:int = 21
IN8PIN:int = 22

FREQ = 1000
AVGSPEED = 350

RIleft_pin = [32,35]
RIright_pin = [39,34]
RIcente_pin:int = 15

trig_pin = 4
echo_pin = 2

car = CARIR(IN1PIN, IN2PIN, IN3PIN, IN4PIN, IN5PIN, IN6PIN, IN7PIN, IN8PIN, ENAPIN, ENBPIN, ENCPIN, ENDPIN, AVGSPEED, FREQ,RIleft_pin,RIright_pin,RIcente_pin)

distance = 0


def Straight(avg_speed):
    while car.flag:
        IR = car.readIR()
        distance = car.obstacleDetector(trig_pin, echo_pin)

        if distance <= 20 and distance >=15:
            print("obstacle detected")
            t.sleep(0.1)
            car.evasionRoutine(avg_speed,avg_speed)

        else:
            car.GOstraight(IR,avg_speed,avg_speed)

             
def MappingServ():
    while True:
        for i in range(0,50):
            moveServo(17,i)
            t.sleep(0.1)

def moveServo(servo,angle):
    """
     Move the servo to a given position.
    """
    servo = PWM(Pin(servo),freq=50)
        
    min_duty = 1
    max_duty = 250
    duty = min_duty + (max_duty - min_duty) * angle // 180
    servo.duty(duty)

def dischargeRoutine(avgSpeed,switch):
    if switch:
        car.setFlag()
        car.stop()
        t.sleep(1)
        moveServo(16,35)
        t.sleep(1)
        moveServo(16,angle=10)

        t.sleep(0.5)
        car.move_backward(avgSpeed,avgSpeed)
        t.sleep(1)
        car.rotate_180_right(0.3,avgSpeed,avgSpeed)
        t.sleep(1)
        Straight(avgSpeed)

def chargeRoutine(avgSpeed,switch):

    if switch:
        car.stop()
        t.sleep(1) 
        moveServo(16,10)
        t.sleep(1)
        moveServo(16,35)
        t.sleep(2)
        moveServo(16,75)
        t.sleep(.5) 

        t.sleep(1)
        car.move_backward(avgSpeed,avgSpeed)
        t.sleep(1)
        car.rotate_180_left(0.3,avgSpeed,avgSpeed)
        t.sleep(1)
        Straight(avgSpeed) 

def CheckFlagCharge(avgSpeed):
    while True:
        if (car.flag):
            chargeRoutine(avgSpeed,1) 
            dischargeRoutine(avgSpeed,0)
        else:
            dischargeRoutine(avgSpeed,1)
            chargeRoutine(avgSpeed,0)


def main(): 
    _thread.start_new_thread(MappingServ, ())
    _thread.start_new_thread(CheckFlagCharge, [AVGSPEED])


#chargeRoutine(AVGSPEED,1)
#CheckFlagCharge(AVGSPEED)
#Straight(AVGSPEED)
#UltrasonicMap()
main()
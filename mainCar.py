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
            t.sleep(0.1)
            car.evasionRoutine(avg_speed+10,avg_speed+10)

        elif car.turnFlag:
            break 

        else:
            car.GOstraight(IR,avg_speed-20,avg_speed-20)
        

def tournUntilLine(avgspeed):
    car.stop()
    t.sleep(0.1)
    car.rotate_180_left(avgspeed,avgspeed)
    t.sleep(0.4
    )
    
    while True:

        car.readIR()

        if car.lineDetected == 1:
            car.rotate_180_left(avgspeed-30,avgspeed-30)
            car.turnFlag = True
        else:
            car.turnFlag = False
            break

    return bool(car.turnFlag)

  
             
def MappingServ():
    while True:
        for i in range(0,15):
            moveServo(17,i)
            t.sleep(0.1)

def moveServo(servo,angle):
    """
     Move the servo to a given position.
    """ 
    servo = PWM(Pin(servo),freq=20)
        
    min_duty = 1
    max_duty = 350
    duty = min_duty + (max_duty - min_duty) * angle // 180
    servo.duty(duty)

def dischargeRoutine(avgSpeed,switch):
    if switch:
        #car.setFlag()
        t.sleep(0.5)
        car.stop()
        t.sleep(1)
        moveServo(16,angle=10)
        t.sleep(1)
        moveServo(16,angle=35)

        t.sleep(0.5)
        car.move_backward(avgSpeed,avgSpeed)
        t.sleep(0.5)
        car.flag = False
        bandera = tournUntilLine(avgSpeed)
        t.sleep(0.1)
        car.flag =True
        if bandera == False:
            Straight(avgSpeed)
        else:
            pass

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
        car.move_backward(avgSpeed,avgSpeed)
        t.sleep(0.5)
        car.flag = False
        bandera = tournUntilLine(avgSpeed)
        t.sleep(0.1)
        car.flag =True

        if bandera == False:
            Straight(avgSpeed)
        else:
            pass 


def CheckFlagCharge(avgSpeed):
    while True:
        print(car.flag)
        if (car.flag):
            chargeRoutine(avgSpeed,1) 
            dischargeRoutine(avgSpeed,0)
            car.flag = False
            car.ischarged = True
        else:
            dischargeRoutine(avgSpeed,1)
            chargeRoutine(avgSpeed,0)
            car.flag = True
            car.ischarged = False



def main(): 
    _thread.start_new_thread(MappingServ, ())
    _thread.start_new_thread(CheckFlagCharge, [AVGSPEED])


main()
 
    

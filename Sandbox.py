import machine as m
from machine import PWM,Pin
import time as t
import HCSRC04 as u


servo_pin = 16
servo = PWM(Pin(servo_pin), freq=50) 

def Gripper(PinNum,angle):
    """
    Open or close the gripper.
    """
    servo = PWM(Pin(PinNum),freq=50)

    moveServo(servo,angle)

    
def moveServo(servo,angle):
    """
    Move the servo to a given position.
    """
    servo = PWM(Pin(servo),freq=50)

    min_duty = 1
    max_duty = 300

    duty = min_duty + (max_duty - min_duty) * angle // 180
    servo.duty(duty)

moveServo(servo_pin,10)
t.sleep(1)
moveServo(servo_pin,35)
t.sleep(2)
moveServo(servo_pin,75)
t.sleep(.5) 
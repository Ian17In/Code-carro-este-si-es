import machine as m
import time as t
import HCSRC04 as u
from machine import Pin,PWM

class CARIR():
    """
    Initialize the CARIR class.
    """
    def __init__(self,in1,in2,in3,in4,in5,in6,in7,in8,ENA,ENB,ENC,END,avgSpeed,frequency,RIleft_pin:list,RIright_pin:list,RIcenter_pin):
        #normal frequency: 1000
        #normal duty cycle: 512 (between 0 and 1023) it means half of power
        
        self.in1 = m.Pin(in1,m.Pin.OUT)
        self.in2 = m.Pin(in2,m.Pin.OUT) #wheel above right
        self.in3 = m.Pin(in3,m.Pin.OUT)
        self.in4 = m.Pin(in4,m.Pin.OUT) #wheel above left
        self.in5 = m.Pin(in5,m.Pin.OUT)
        self.in6 = m.Pin(in6,m.Pin.OUT) #wheel below right
        self.in7 = m.Pin(in7,m.Pin.OUT)
        self.in8 = m.Pin(in8,m.Pin.OUT) #wheel below left

        self.avgSpeed = avgSpeed # average speed of the car
        self.freq = frequency

        self.ENA = m.PWM(ENA,self.freq,duty=self.avgSpeed) #wheel above right
        self.ENB = m.PWM(ENB,self.freq,duty=self.avgSpeed) #wheel above left
        self.ENC = m.PWM(ENC,self.freq,duty=self.avgSpeed) #wheel below right
        self.END = m.PWM(END,self.freq,duty=self.avgSpeed) #wheel above left

        self.RIleft = [m.Pin(pin, m.Pin.IN) for pin in RIleft_pin]
        self.RIright = [m.Pin(pin, m.Pin.IN) for pin in RIright_pin]
        self.RIcenter = m.Pin(RIcenter_pin, m.Pin.IN)

        self.flag = True
    
    def setSpeed(self,speed1,speed2):
        """
        Set the wheels speed
        """
        self.ENA.duty(speed1)
        self.ENB.duty(speed2)
        self.ENC.duty(speed1)
        self.END.duty(speed2)
    
    def setSpeed2(self,speed1,speed2):
        """
        Set the wheels speed
        """
        self.ENA.duty(speed1)
        self.ENB.duty(speed2)
        self.ENC.duty(speed1)
        self.END.duty(speed2)

    def move_forward(self,speed1,speed2):
        """
        Move the car forward at the given speed.
        """
        self.in1.value(0)
        self.in2.value(1)

        self.in3.value(0)
        self.in4.value(1)

        self.in5.value(0)
        self.in6.value(1)

        self.in7.value(0)
        self.in8.value(1)

        self.setSpeed(speed1,speed2)
        
    def move_backward(self,speed1,speed2):
        """
        Move the car backward at the given speed.
        """
        self.in1.value(1)
        self.in2.value(0)

        self.in3.value(1)
        self.in4.value(0)

        self.in5.value(1)
        self.in6.value(0)

        self.in7.value(1)
        self.in8.value(0)

        self.setSpeed(speed1,speed2)
    
    def stop(self):
        """
        Stop the car.
        """
        self.in1.value(0)
        self.in2.value(0)

        self.in3.value(0)
        self.in4.value(0)

        self.in5.value(0)
        self.in6.value(0)

        self.in7.value(0)
        self.in8.value(0)
    
    def Left(self,speed1,speed2):
        """
        Move the car to the left.
        """
        self.in1.value(0)
        self.in2.value(1)

        self.in3.value(1)
        self.in4.value(0)

        self.in5.value(1)
        self.in6.value(0)

        self.in7.value(0)
        self.in8.value(1)

        self.setSpeed2(speed1,speed2)
    
    def Right(self,speed1,speed2):
        """
        Move the car to the right.
        """
        self.in1.value(1)
        self.in2.value(0)

        self.in3.value(0)
        self.in4.value(1)

        self.in5.value(0)
        self.in6.value(1)

        self.in7.value(1)
        self.in8.value(0)

        self.setSpeed2(speed1,speed2)
    
    def Gripper(self,PinNum,angle):
        """
        Open or close the gripper. 
        """
        servo = PWM(Pin(PinNum),freq=50)

        self.moveServo(servo,angle)

    def moveServo(self,servo,angle):
        """
        Move the servo to a given position.
        """
        servo = PWM(Pin(servo),freq=50)
        
        min_duty = 1
        max_duty = 300

        duty = min_duty + (max_duty - min_duty) * angle // 180
        servo.duty(duty)

    def obstacleDetector(self,triggerPin,echoPin):
        """
        Detect obstacles using a Ultrasonic sensor
        """
        sensor = u.HCSR04(triggerPin,echoPin)
        distance = sensor.distance_cm()

        return distance
    
    def evasionRoutine(self,speed1,speed2):
        """
        Evasion routine for obstacles.
        """

        self.Right(speed1+50,speed2+50)
        t.sleep(2)
        self.stop()
        t.sleep(0.5)
        self.move_forward(speed1,speed2) 
        t.sleep(2)
        self.stop()
        t.sleep(0.5)
        self.Left(speed1+50,speed2+50)
        t.sleep(2)

    def readIR(self):
        """
        Lee los valores de los sensores IR.
        """

        left_values = [sensor.value() for sensor in self.RIleft]
        right_values = [sensor.value() for sensor in self.RIright]
        center_value = self.RIcenter.value()

        # Crear una lista de resultados en el orden: izquierdo1, izquierdo2, central, derecho1, derecho2
        IR = left_values + [center_value] + right_values

        # Opcional: agregar un retardo si es necesario
        t.sleep(0.01)

        return IR

    def rotate_180_right(self,duration,speed1,speed2):
        """
        Gira el robot 180 grados.
        """
        self.setSpeed2(speed1,speed2)

        self.in1.value(1) #r
        self.in2.value(0)

        self.in3.value(0) #l
        self.in4.value(1)

        self.in5.value(1) #r
        self.in6.value(0)

        self.in7.value(0) #l
        self.in8.value(1)

        t.sleep(duration)

    def rotate_180_left(self, duration,speed1,speed2):
        """
        Gira el robot 180 grados en sentido contrario.
        """
        self.setSpeed2(speed1,speed2)

        self.in1.value(0) #l
        self.in2.value(1)
        
        self.in3.value(1) #r
        self.in4.value(0)

        self.in5.value(0) #l
        self.in6.value(1)

        self.in7.value(1) #r
        self.in8.value(0)

        t.sleep(duration)

    def setFlag(self):
        """
        Cambia el stado de carga
        """
        if self.flag == True:
            self.flag = False
            print(self.flag)
        else:
            self.flag = True
            print(self.flag)
   
    
    def GOstraight(self, IR: list, speed1, speed2):
        """
        Controla el movimiento del robot basado en los valores de 5 sensores IR.
        IR: Lista con los valores de los sensores [izq1, izq2, central, der1, der2].
        El valor 0 indica detección de línea, y el valor 1 indica que no hay línea.
        """
        sensor_izq2, sensor_izq1, sensor_central, sensor_der2, sensor_der1 = IR
        #print(IR)

        # Caso 1: Solo el sensor central detecta la línea (continuar recto)
        if sensor_central == 0 and sensor_izq1 == 1 and sensor_izq2 == 1 and sensor_der1 == 1 and sensor_der2 == 1:
            #print("Línea central detectada, avanzando recto.")
            self.move_forward(speed1, speed2)
        elif sensor_central == 1 and sensor_izq1 == 0 and sensor_der1 == 1 and sensor_izq2==1 and sensor_der2 == 1:
            #print("ajuste a la izquierda.")
            self.Right(speed1, speed2)
        elif sensor_central == 1 and sensor_izq1 == 1 and sensor_der1 == 1 and sensor_izq2==1 and sensor_der2 == 0:
            #print("ajuste a la derecha.")
            self.Left(speed1, speed2)

        elif sensor_central == 0 and sensor_izq1 == 0 and sensor_izq2 == 0 and sensor_der1 == 1 and sensor_der2 == 1:
            #print("giro duro a la izquierda")
            self.stop()
            t.sleep(0.01)
            self.rotate_180_right(0.6,speed1,speed2)
            t.sleep(0.01)
            self.stop()
        elif sensor_central == 0 and sensor_der1 == 0 and sensor_der2 == 0 and sensor_izq1 == 1 and sensor_izq2 == 1:
            #print("giro duro a la derecha")
            self.stop()
            t.sleep(0.01)
            self.rotate_180_left(0.6,speed1,speed2)
            t.sleep(0.01)
            self.stop()
        
        elif sensor_central == 1 and sensor_der1 == 1 and sensor_der2 == 1 and sensor_izq1 == 1 and sensor_izq2 == 1:
            self.move_forward(speed1,speed2)

        elif sensor_central == 0 and sensor_der1 == 0 and sensor_der2 == 0 and sensor_izq1 == 0 and sensor_izq2 == 0:
            #print("Stop")
            #print(self.counterFlag)
            self.setFlag()
            self.stop()
            t.sleep(1)



    
    

if __name__ == '__main__':
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
 
import RPi.GPIO as GPIO 
from time import sleep  
GPIO.setmode(GPIO.BOARD)             #1
Motor1A = 33 
Motor1B = 35 
Motor1E = 37
GPIO.setwarnings(False)
GPIO.setup(Motor1A,GPIO.OUT)         #2
GPIO.setup(Motor1B,GPIO.OUT) 
GPIO.setup(Motor1E,GPIO.OUT)
try:
    print("Turning motor on")
    GPIO.output(Motor1A,GPIO.HIGH)   #3
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    sleep(5)
    print("Stopping motor")
    GPIO.output(Motor1E,GPIO.LOW)    #4
finally:
    GPIO.output(Motor1E,GPIO.LOW)    #5
    GPIO.cleanup()                   #6
import RPi.GPIO as GPIO
import time

raindrop = 12
ledPin = 40
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) # use PHYSICAL GPIO Numbering
    GPIO.setup(raindrop, GPIO.IN)
    GPIO.setup(ledPin, GPIO.OUT) # set the ledPin to OUTPUT mode
    GPIO.output(ledPin, GPIO.LOW)

def Print(x):
    if x == 1:
        print("NOT RAINING")
        GPIO.output(ledPin, GPIO.LOW)
        
    if x == 0:
        print(" RAINING")
        GPIO.output(ledPin, GPIO.HIGH)
        
def loop():
    status = 1
    while True:
        tmp = GPIO.input(raindrop)
        if tmp != status:
            Print(tmp)
            status = tmp
        time.sleep(1)
       
       
def destroy():
    GPIO.cleanup() # Release all GPIO
if __name__ == '__main__': # Program entrance
    print ('Program is starting ... \n')
    setup()
try:
    loop()
except KeyboardInterrupt: # Press ctrl-c to end the program.
    destroy()
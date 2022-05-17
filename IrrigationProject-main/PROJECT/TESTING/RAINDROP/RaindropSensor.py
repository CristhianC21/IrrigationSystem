# raindrop sensor DO connected to GPIO18
# HIGH = no rain, LOW = rain detected
# Buzzer on GPIO13
from time import sleep
from gpiozero import Buzzer, InputDevice, LED
import time


buzz    = Buzzer(13)
no_rain = InputDevice(18)
ledPin = LED(21)

def rain():
 while True:
        if not no_rain.is_active:
            print("It's raining - get the washing in!")
            ledPin.on()

            
        sleep(1)
        if no_rain.is_active:
            print("It's not raining!")
            ledPin.off()

    
if __name__ == '__main__': # Program entrance
    print ('Program is starting ... \n')
try:
    rain()
except KeyboardInterrupt: # Press ctrl-c to end the program.
    destroy()


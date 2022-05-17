import RPi.GPIO as GPIO
import spidev # To communicate with SPI devices
from numpy import interp  # To scale values
from time import sleep  # To add delay
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
import Freenove_DHT as DHT
import time
from gpiozero import InputDevice


spi = spidev.SpiDev() # Created an object
spi.open(0,0)
DHTPin = 11     #define the pin of DHT11 
GPIO.setwarnings(False)

no_rain = InputDevice(18)

def RAINDROP():
     while True:
        dry = "NO"
        wet = "YES"
        if not no_rain.is_active:
            print("It's raining - get the washing in!")
            GPIO.output(ledPin, GPIO.HIGH)
            return wet
            # insert your other code or functions here
            # e.g. tweet, SMS, email, take a photo etc.
        sleep(1)
        if no_rain.is_active:
            print("It's not raining!")
            GPIO.output(ledPin, GPIO.HIGH)

            return dry

def DHT11sensor():
    dht = DHT.DHT(DHTPin)   #create a DHT class object
    counts = 0 # Measurement counts
    chk = dht.readDHT11()     #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
    if (chk == dht.DHTLIB_OK):      #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
        pass   
    time.sleep(2)
    print(" \t Temperature : %.1f \n"%(dht.temperature))
    sleep(0.1)
    return dht.temperature
# Read MCP3008 data
def analogInput(channel):
    spi.max_speed_hz = 1350000
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data


      
def soilMoisture():
    output = analogInput(1) # Reading from CH0
    output = interp(output, [300, 1023], [100, 0])
    output = int(output)
    print("Moisture:", output, "%")
    sleep(2)
    return output

def lcdscreen():
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    while(True):         
      # lcd.clear()
       # lcd.setCursor(1,0)  # set cursor position
       # lcd.message( 'M: ' + str(soilMoisture())+'%' )# display CPU temperature
      #  lcd.setCursor(1,1)  # set cursor position
       # lcd.message( 'T: ' + str(DHT11sensor())+'C' )# display CPU temperature
        lcd.setCursor(7,1)  # set cursor position
        lcd.message( 'RAIN: ' + str(RAINDROP()) )# display CPU temperature

        sleep(1)
       
def loop():
   lcdscreen()  
    
def destroy():
    lcd.clear()
    GPIO.cleanup()

PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.    


try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
   
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
    finally:
        destroy()


        
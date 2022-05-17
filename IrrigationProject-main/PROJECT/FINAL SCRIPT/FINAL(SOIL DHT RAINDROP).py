import spidev # To communicate with SPI devices
from numpy import interp  # To scale values
from time import sleep  # To add delay
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
import Freenove_DHT as DHT
import time
import RPi.GPIO as GPIO


spi = spidev.SpiDev() # Created an object
spi.open(0,0)
DHTPin = 11     #define the pin of DHT11 
raindrop = 12
ledPin = 38

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) # use PHYSICAL GPIO Numbering
    GPIO.setup(raindrop, GPIO.IN)
    GPIO.setup(ledPin, GPIO.OUT) # set the ledPin to OUTPUT mode
    GPIO.output(ledPin, GPIO.LOW)

        
def raindropSensor():
    status = 1
    tmp = GPIO.input(raindrop)
    if tmp == 0:
        print(" RAINING")
        GPIO.output(ledPin, GPIO.HIGH)
    if tmp == 1:
        print("NOT RAINING")
        GPIO.output(ledPin, GPIO.LOW)
    time.sleep(1)        
        
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
        lcd.setCursor(1,0)  # set cursor position
        lcd.message( 'M: ' + str(soilMoisture())+'%' )# display CPU temperature
        lcd.setCursor(1,1)  # set cursor position
        lcd.message( 'T: ' + str(DHT11sensor())+'C' )# display CPU temperature
        raindropSensor()  
        sleep(1)
        print("-------------------")
       
def loop():
    lcdscreen()
    

    
def destroy():
    lcd.clear()
    GPIO.cleanup()
    
#LCD SCREEN SETUP

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
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
    finally:
        destroy()


    
import spidev # To communicate with SPI devices
from numpy import interp  # To scale values
from time import sleep  # To add delay
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
import Freenove_DHT as DHT
import RPi.GPIO as GPIO


spi = spidev.SpiDev() # Created an object
spi.open(0,0)

DHTPin = 11   #DHT PIN

#RAINDROP PIN
ledPin = 40
raindrop = 12

#PHOTORESISTOR PINS
spi_ch = 0
ledPinPhoto = 38

#MOTOR PINS 
Motor1A = 33 
Motor1B = 35 
Motor1E = 37


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) # use PHYSICAL GPIO Numbering
    GPIO.setup(raindrop, GPIO.IN)
    GPIO.setup(ledPin, GPIO.OUT) # set the ledPin use with raindrop to OUTPUT mode
    GPIO.output(ledPin, GPIO.LOW)
    GPIO.setup(ledPinPhoto, GPIO.OUT) # set the ledPinPhoto to OUTPUT mode
    GPIO.output(ledPinPhoto, GPIO.LOW)
    
    # set motor pins to OUTPUT mode
    GPIO.setup(Motor1A,GPIO.OUT)      
    GPIO.setup(Motor1B,GPIO.OUT) 
    GPIO.setup(Motor1E,GPIO.OUT)
        
def raindropSensor():
     tmp = GPIO.input(raindrop)
    
    if tmp == 0:
        GPIO.output(ledPin, GPIO.HIGH)
    if tmp == 1:
        GPIO.output(ledPin, GPIO.LOW)
    return tmp  #Return a boolean/ turn LED on if value is 0

def printRaindrop(prRaindrop): #Function that shows if its raining or not in  output
    rainStatus =["4. RAINING","4. NOT RAINING"]
    if prRaindrop == 0:
        print(rainStatus[0])
    if prRaindrop == 1:
        print(rainStatus[1])
    
        
def DHT11sensor():
    dht = DHT.DHT(DHTPin)   #create a DHT class object
    chk = dht.readDHT11()     #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
    if (chk == dht.DHTLIB_OK):      #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
        pass   
    return dht.temperature
    

# Read MCP3008 data
def analogInput(channel):
    spi.max_speed_hz = 1350000
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data


      
def soilMoisture():
    
    output = analogInput(1) # Reading from CH0
    output = interp(output, [300, 1023], [100, 0]) #RANGE OF VALUES FOR SOIL MOISTURE SENSOR/ DISPLAY IN A RANGE FROM 0 TO 100
    output = int(output)
    
    
    
    return output

def moistureLCD(LcdMoisture): # Function that prints moisture percentage in LCD screen
    mois = ["M:  ","M: ","M:"]
    print("1. Moisture:", LcdMoisture, "%")
    if LcdMoisture >= 0 and LcdMoisture <= 9:
        return mois[0]
    elif LcdMoisture >= 10 and LcdMoisture <= 99:
        return mois[1]
    else:
        return mois[2]
 

def readPhotoresistorADC(adc_ch, vref = 3.3):

    # Make sure ADC channel is 0 or 1
    if adc_ch != 0:
        adc_ch = 1

    # Construct SPI message
    #  First bit (Start): Logic high (1)
    #  Second bit (SGL/DIFF): 1 to select single mode
    #  Third bit (ODD/SIGN): Select channel (0 or 1)
    #  Fourth bit (MSFB): 0 for LSB first
    #  Next 12 bits: 0 (don't care)
    msg = 0b11
    msg = ((msg << 1) + adc_ch) << 5
    msg = [msg, 0b00000000]
    reply = spi.xfer2(msg)

    # Construct single integer out of the reply (2 bytes)
    adc = 0
    for n in reply:
        adc = (adc << 8) + n

    # Last bit (0) is not part of ADC value, shift to remove it
    adc = adc >> 1

    # Calculate voltage form ADC value
    voltage = (vref * adc) / 1024

    return voltage

def photoresistorLed():
        adc_0 = readPhotoresistorADC(0)
       
       
        return round(adc_0, 2)
        
def photoresistorLCD(LcdPhotoresistor): # Function that prints voltage in output, turn on a led and returns if its day or night for showing in LCD screen 
        
        timeDay = ["DAY  ","NIGHT"]
        
        print("3. PHOTORESISTOR VOLTAGE:", LcdPhotoresistor, "V")
        
        if LcdPhotoresistor < 0.3:
            GPIO.output(ledPinPhoto, GPIO.HIGH)
            print("  3.1 LED IN DARKNESS")
            return timeDay[1]  
        else:
            GPIO.output(ledPinPhoto, GPIO.LOW)
            print("  3.1 LED IN LIGHT CONTACT")
            return timeDay[0]        
        
        
def motor(soil,dht,photo,rain):# MOTOR function which receives every sensor value as a parameter
    if(soil < 10) and (dht < 40) and (photo < 0.3) and (rain == 1):
        print("MOTOR WATERING")
        GPIO.output(Motor1A,GPIO.HIGH)   #
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)
    else:
        GPIO.output(Motor1E,GPIO.LOW)
            

    
def lcdscreen():
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    while(True):

        
      # lcd.clear()
        lcd.setCursor(1,0)  # set cursor position for showing soil moisture percentage
        lcd.message( str(moistureLCD(soilMoisture())) + str(soilMoisture())+'%' )# display moisture percentage

        lcd.setCursor(1,1)  # set cursor position for showing room temperature
        lcd.message( "T:"+ str(DHT11sensor()) +'C' )# display room temperature
        print("2. ROOM TEMPERATURE : %.1f "%(DHT11sensor())) ]# print in output temperature

        lcd.setCursor(10,0) # set cursor position for day time
        lcd.message(str(photoresistorLCD(photoresistorLed())) )]#display "day" or "night" depending on photoresistor voltage 
        printRaindrop(raindropSensor()) #print in output if its raining or not
        sleep(1)
        
        motor(soilMoisture(),DHT11sensor(),photoresistorLed(),raindropSensor()) # Motor function called with parameters every sensor
       
    
        print("-------------------")
        

def loop():
    lcdscreen() 
    
    
def destroy():
    lcd.clear()
    GPIO.cleanup()
    spi.close()
    
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
    except RuntimeError:
        quit()
    finally:
        GPIO.output(Motor1E,GPIO.LOW)
        destroy()


    
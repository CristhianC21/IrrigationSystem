import time
import spidev
import RPi.GPIO as GPIO

spi_ch = 0
ledPin = 38
# Enable SPI



def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) # use PHYSICAL GPIO Numbering
    GPIO.setup(ledPin, GPIO.OUT) # set the ledPin to OUTPUT mode
    GPIO.output(ledPin, GPIO.LOW)


def read_adc(adc_ch, vref = 3.3):

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

# Report the channel 0 and channel 1 voltages to the terminal
try:
    setup()
    while True:
        adc_0 = read_adc(0)
        print("Ch 0:", round(adc_0, 2), "V")
        time.sleep(1)
        if round(adc_0, 2) < 0.3:
            GPIO.output(ledPin, GPIO.HIGH)
            print("LED IN LIGHT CONTACT")
        else:
            GPIO.output(ledPin, GPIO.LOW)
            print("LED IN DARKNESS") 
        time.sleep(0.5)

finally:
    spi.close()
    GPIO.cleanup()
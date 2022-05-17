import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

from numpy import interp  # To scale values


# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create a differential ADC channel between Pin 0 and Pin 1
chan = AnalogIn(mcp, MCP.P0)

print('Differential ADC Value: ', chan.value)
print('Differential ADC Voltage: ' + str(chan.voltage) + 'V')

output = interp(chan, [16192, 65472], [100, 0])
output = int(output)
print(output)  
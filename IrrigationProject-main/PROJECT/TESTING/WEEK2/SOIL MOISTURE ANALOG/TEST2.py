import time
import spidev
import SPI as SPI
import Adafruit_MCP3008

from numpy import interp

SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SpiDev(SPI_PORT, SPI_DEVICE))

while True:
    value = mcp.read_adc(0)
    scale = interp(value, [300.1023], [100,0])
    output = int(scale)

    print("Channel 0 value reads: {0}".format(value)+" and equals Moisture: {0}".format(output)+"%")
    time.sleep(1)
from smbus import SMBus
import time
import bme280

bus_number  = 1
bme280_address = 0x76

bus = SMBus(bus_number)

if __name__ == '__main__':
	
	bme280.setup(bus,bme280_address)
	
#	print bme280.readData(bus,bme280_address)
	temperature, pressure, humidity = bme280.readData(bus, bme280_address)
#	print bme280.digT

	print temperature

from smbus import SMBus
import time
import bme280
import ADS

bus_number  = 1
bme280_address = 0x76
ADS_address = 0x48

bus = SMBus(bus_number)

if __name__ == '__main__':

	bme280.setup(bus,bme280_address)

	ADC_config = \
	ADS._CONFIG_OS['START'] | ADS._CONFIG_MUX['0G'] | ADS._CONFIG_CONV_MODE['SINGLE'] \
	| ADS._CONFIG_RANGE['2V'] | ADS._CONFIG_RATE['128SPS'] \
	| ADS._CONFIG_COMP_QUE_DISABLE | ADS._CONFIG_COMP_RANGE['NORM']

	ADS.setCondition(bus, ADS_address, ADC_config)

	print ADS.readout(bus,ADS_address)

	temperature, pressure, humidity = bme280.readData(bus, bme280_address)
#	print bme280.digT

	print temperature

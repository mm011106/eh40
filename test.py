from smbus import SMBus
import time
import bme280
import ADS

bus_number  = 1
bme280_address = 0x76
ADS_address = 0x48

bus = SMBus(bus_number)

if __name__ == '__main__':

	# bme280.setup(bus,bme280_address)

	ADS.init(bus, ADS_address)

	ADC_config = ADS._CONFIG_DEFAULT
	ADS.setCondition(bus, ADS_address, ADC_config)

	print ADS.readoutMulti(bus, ADS_address)

	ADC_config = ADS._CONFIG_DEFAULT
	ADC_config = ADC_config & (~ ADS._MASK_RATE) | ADS._CONFIG_RATE[ '8SPS' ]
	ADS.setCondition(bus, ADS_address, ADC_config)

	print ADS.readoutMulti(bus, ADS_address)


#	temperature, pressure, humidity = bme280.readData(bus, bme280_address)
#	print bme280.digT

#	print temperature

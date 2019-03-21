from smbus import SMBus
from time import sleep

_POINTER_CONVERSION         = 0x00
_POINTER_CONFIG             = 0x01

_CONFIG_OS = {
    'START':0x8000
}

_CONFIG_MUX={
    '01': 0x0000,
    '03': 0x1000,
    '13': 0x2000,
    '23': 0x3000,
    '0G': 0x4000,
    '1G': 0x5000,
    '2G': 0x6000,
    '3G': 0x7000
}
_MASK_MUX=0x7000

_CONFIG_RANGE = {
    '6V':    0x0000,
    '4V':    0x0200,
    '2V':    0x0400,
    '1V':    0x0800,
    '0.5V':  0x0A00,
    '0.25V': 0x0C00
}
_MASK_RANGE=0x0E00

_CONFIG_RATE = {
    '8SPS':    0x0000,
    '16SPS':   0x0020,
    '32SPS':   0x0040,
    '64SPS':   0x0060,
    '128SPS':  0x0080,
    '250SPS':  0x00A0,
    '475SPS':  0x00C0,
    '860SPS':  0x00E0
}
_MASK_RATE=0x00E0

_CONFIG_CONV_CONTINUOUS = 0x0000
_CONFIG_CONV_SINGLE = 0x0100

_CONFIG_CONV_MODE={
  'CONTINUOUS'  :0x0000,
  'SINGLE'      :0x0100
}

_CONFIG_COMP_QUE_DISABLE    = 0x0003
_CONFIG_COMP_RANGE = {
    'NORM':  0x0000,
    'WIND':  0x0010
}


def init(bus, address):
#	insert code for ininitalize ADC
	return 0

def setCondition(bus, address, config):
	command = [config>>8, config & 0xFF ]
	bus.write_i2c_block_data(address, _POINTER_CONFIG,command)
	return 0

def readCondition(bus, address):
	rawData = bus.read_i2c_block_data(address, _POINTER_CONFIG,2)
	return rawData[0] * 256 + rawData[1]

def waitReady(bus, address):
	while True if readCondition(bus, address) >> 15 == 0 else False :
		pass

	return 0

def readout(bus, address):
	waitReady(bus, address)
	raw = bus.read_i2c_block_data(address,_POINTER_CONVERSION,2)
	adc = raw[0] * 256 + raw[1]
	if adc > 32767:
		adc -= 65535
	return adc

def readout_all_SE(bus, address):

	result = []

	ADC_config = \
	_CONFIG_OS['START'] | _CONFIG_MUX['0G'] | _CONFIG_CONV_MODE['SINGLE'] \
	| _CONFIG_RANGE['2V'] | _CONFIG_RATE['128SPS'] \
	| _CONFIG_COMP_QUE_DISABLE | _CONFIG_COMP_RANGE['NORM']

	print format(ADC_config, "04x")
	setCondition(bus, address, ADC_config)
	result.append(readout(bus, address))

	ADC_config = ADC_config & (~ _MASK_MUX) | _CONFIG_MUX['1G']
	print format(ADC_config, "04x")
	setCondition(bus, address, ADC_config)
	result.append(readout(bus, address))

	ADC_config = ADC_config & (~ _MASK_MUX) | _CONFIG_MUX['2G']
	print format(ADC_config, "04x")
	setCondition(bus, address, ADC_config)
	result.append(readout(bus, address))

	ADC_config = ADC_config & (~ _MASK_MUX) | _CONFIG_MUX['3G']
	print format(ADC_config, "04x")
	setCondition(bus, address, ADC_config)
	result.append(readout(bus, address))

	for value in result:
		print '{0:x}'.format(result)

	return 0

def readout_all_DIFF(bus, address):
	return 0

if __name__ == '__main__':

	bus_number  = 1
	address = 0x48

	bus = SMBus(bus_number)

	init(bus, address)

	ADC_config = \
	_CONFIG_OS['START'] | _CONFIG_MUX['0G'] | _CONFIG_CONV_MODE['SINGLE'] \
	| _CONFIG_RANGE['2V'] | _CONFIG_RATE['128SPS'] \
	| _CONFIG_COMP_QUE_DISABLE | _CONFIG_COMP_RANGE['NORM']

	while True:

		setCondition(bus, address, ADC_config)

		print readout(bus,address)

		print '>', format(readCondition(bus, address), "04x")

		readout_all_SE(bus, address):

		sleep(0.5)

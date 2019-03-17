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

_CONFIG_RANGE = {
    '6V':    0x0000,
    '4V':    0x0100,
    '2V':    0x0200,
    '1V':    0x0300,
    '0.5V':  0x0400,
    '0.25V': 0x0500
}

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

def readout(bus,address):
#  !!! need to wait until the conversion is completed
	raw = bus.read_i2c_block_data(address,_POINTER_CONFIG,2)
	adc = raw[0] * 256 + raw[1]
	if adc > 32767:
		adc -= 65535
	return adc

bus_number  = 1
address = 0x48

bus = SMBus(bus_number)

if __name__ == '__main__':
	ADC_config = _CONFIG_OS['START'] | _CONFIG_MUX['0G'] | _CONFIG_CONV_MODE['CONTINUOUS']\
	| _CONFIG_RANGE['2V'] | _CONFIG_RATE['128SPS'] | _CONFIG_COMP_QUE_DISABLE | _CONFIG_COMP_RANGE['NORM']

	print "CONFIG CODE:", format(ADC_config, "04x")


	bus.write_i2c_block_data(address, 0x01, [0xD5, 0x83])

	while True:
		bus.write_i2c_block_data(address, _POINTER_CONVERSION,[0xD5,0x83])

		# data=bus.read_i2c_block_data(address,0x00,2)
		# print data
		print readout(bus,address)
		sleep(0.5)

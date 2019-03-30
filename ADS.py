#!/usr/bin/env python
# -*- coding: utf-8 -*-


from smbus import SMBus
from time import sleep


# ------  CONST

_DEFAULT_ADDRESS			= 0x48

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
    '1V':    0x0600,
    '0.5V':  0x0800,
    '0.25V': 0x0A00
}
_MASK_RANGE=0x0E00

_CONFIG_CONV_MODE={
  'CONTINUOUS'  :0x0000,
  'SINGLE'      :0x0100
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
_MASK_RATE=0x00E0

_CONFIG_COMP_QUE_DISABLE    = 0x0003
_CONFIG_COMP_RANGE = {
    'NORM':  0x0000,
    'WIND':  0x0010
}

_CONFIG_DEFAULT = \
	  _CONFIG_OS['START']    | _CONFIG_MUX['0G'] \
	| _CONFIG_RANGE['2V']    | _CONFIG_CONV_MODE['SINGLE'] \
	| _CONFIG_RATE['128SPS'] | _CONFIG_COMP_RANGE['NORM']  \
	| _CONFIG_COMP_QUE_DISABLE


# ----  Functions

def init(bus, address):
#	insert code for ininitalize ADC
	setCondition(bus, address, _CONFIG_DEFAULT)
	readout(bus, address)

	return 0

def setCondition(bus, address, config):
	command = [config>>8, config & 0xFF ]
	bus.write_i2c_block_data(address, _POINTER_CONFIG,command)
	return 0

def readCondition(bus, address):
	rawData = bus.read_i2c_block_data(address, _POINTER_CONFIG,2)
	return rawData[0] * 256 + rawData[1]

	return 0

def waitReady(bus, address):
	while (True if readCondition(bus, address) >> 15 == 0 else False) :
		# the MSB of condition register indicating ADC is busy'0' or ready'1'
		pass

	return 0

def readout(bus, address):
	waitReady(bus, address)
	raw = bus.read_i2c_block_data(address,_POINTER_CONVERSION,2)
	adc = raw[0] * 256 + raw[1]
	if adc > 32767:
		adc -= 65535
	return adc

def readoutMulti(bus, address, read_channels=None):
#	readout_channelsのリストで指定されたチャネルを計測して、結果をリストで返す
#		デフォルト：SEで全チャネルを測定する

	result = []

	if read_channels is None:
		read_channels=['0G','1G','2G','3G']

#	ADC_config = _CONFIG_DEFAULT
	ADC_config = readCondition(bus, address)

#	print format(ADC_config, "04x")

	for ch in read_channels:
		ADC_config = ADC_config & (~ _MASK_MUX) | _CONFIG_MUX[ ch ]
		#print format(ADC_config, "04x")
		setCondition(bus, address, ADC_config)
		result.append(readout(bus, address))
		print format(readCondition(bus, address), "04X")

	# for i, value in enumerate(result):
	# 	print i,": ", '{0:x}'.format(value)

	return result

def readout_all_DIFF(bus, address):
	return 0

if __name__ == '__main__':

	bus_number  = 1
	address = _DEFAULT_ADDRESS
#	address = 0x48

	bus = SMBus(bus_number)
	init(bus, address)

	ADC_config = _CONFIG_DEFAULT

	while True:

		# setCondition(bus, address, ADC_config)
		#
		# print readout(bus,address)
		#
		# print '>', format(readCondition(bus, address), "04x")

		print readoutMulti(bus, address)
		print

		sleep(1)

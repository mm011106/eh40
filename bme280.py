#coding: utf-8

#  expecting following parameters:
#      bus:  i2c bus instance
#      address:	BME280 reg_address
#

# global val for calibration data
digT = []
digP = []
digH = []

t_fine = 0.0

def get_calib_param(bus, address):
	global digT, digP, digH

	calib = []

	for i in range (0x88,0x88+24):
		calib.append(bus.read_byte_data(address,i))
	calib.append(bus.read_byte_data(address,0xA1))
	for i in range (0xE1,0xE1+7):
		calib.append(bus.read_byte_data(address,i))

	digT.append((calib[1] << 8) | calib[0])
	digT.append((calib[3] << 8) | calib[2])
	digT.append((calib[5] << 8) | calib[4])
	digP.append((calib[7] << 8) | calib[6])
	digP.append((calib[9] << 8) | calib[8])
	digP.append((calib[11]<< 8) | calib[10])
	digP.append((calib[13]<< 8) | calib[12])
	digP.append((calib[15]<< 8) | calib[14])
	digP.append((calib[17]<< 8) | calib[16])
	digP.append((calib[19]<< 8) | calib[18])
	digP.append((calib[21]<< 8) | calib[20])
	digP.append((calib[23]<< 8) | calib[22])
	digH.append( calib[24] )
	digH.append((calib[26]<< 8) | calib[25])
	digH.append( calib[27] )
	digH.append((calib[28]<< 4) | (0x0F & calib[29]))
	digH.append((calib[30]<< 4) | ((calib[29] >> 4) & 0x0F))
	digH.append( calib[31] )

	for i in range(1,2):
		if digT[i] & 0x8000:
			digT[i] = (-digT[i] ^ 0xFFFF) + 1

	for i in range(1,8):
		if digP[i] & 0x8000:
			digP[i] = (-digP[i] ^ 0xFFFF) + 1

	for i in range(0,6):
		if digH[i] & 0x8000:
			digH[i] = (-digH[i] ^ 0xFFFF) + 1

#	print digT,digH,digP

def readData(bus, address):
	global digT, digP, digH

	data = []
	for i in range (0xF7, 0xF7+8):
		data.append(bus.read_byte_data(address,i))
	pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
	temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
	hum_raw  = (data[6] << 8)  |  data[7]

#	print compensate_T(temp_raw, digT)
#	print compensate_P(pres_raw, digP)
#	print compensate_H(hum_raw,  digH)
	return compensate_T(temp_raw, digT), compensate_P(pres_raw, digP), compensate_H(hum_raw, digH)

def compensate_P(adc_P, cal_P):
	global  t_fine

	pressure = 0.0

	v1 = (t_fine / 2.0) - 64000.0
	v2 = (((v1 / 4.0) * (v1 / 4.0)) / 2048) * cal_P[5]
	v2 = v2 + ((v1 * cal_P[4]) * 2.0)
	v2 = (v2 / 4.0) + (cal_P[3] * 65536.0)
	v1 = (((cal_P[2] * (((v1 / 4.0) * (v1 / 4.0)) / 8192)) / 8)  + ((cal_P[1] * v1) / 2.0)) / 262144
	v1 = ((32768 + v1) * cal_P[0]) / 32768

	if v1 == 0:
		return 0
	pressure = ((1048576 - adc_P) - (v2 / 4096)) * 3125
	if pressure < 0x80000000:
		pressure = (pressure * 2.0) / v1
	else:
		pressure = (pressure / v1) * 2
	v1 = (cal_P[8] * (((pressure / 8.0) * (pressure / 8.0)) / 8192.0)) / 4096
	v2 = ((pressure / 4.0) * cal_P[7]) / 8192.0
	pressure = pressure + ((v1 + v2 + cal_P[6]) / 16.0)

#	print "pressure : %7.2f hPa" % (pressure/100)

	return pressure/100

def compensate_T(adc_T, cal_T):
	global t_fine
	v1 = (adc_T / 16384.0 - cal_T[0] / 1024.0) * cal_T[1]
	v2 = (adc_T / 131072.0 - cal_T[0] / 8192.0) * (adc_T / 131072.0 - cal_T[0] / 8192.0) * cal_T[2]
	t_fine = v1 + v2
	temperature = t_fine / 5120.0
#	print "temp : %-6.2f ℃" % (temperature)

	return temperature

def compensate_H(adc_H, cal_H):
	global t_fine
	var_h = t_fine - 76800.0
	if var_h != 0:
		var_h = (adc_H - (cal_H[3] * 64.0 + cal_H[4]/16384.0 * var_h)) * (cal_H[1] / 65536.0 * (1.0 + cal_H[5] / 67108864.0 * var_h * (1.0 + cal_H[2] / 67108864.0 * var_h)))
	else:
		return 0
	var_h = var_h * (1.0 - cal_H[0] * var_h / 524288.0)
	if var_h > 100.0:
		var_h = 100.0
	elif var_h < 0.0:
		var_h = 0.0
#	print "hum : %6.2f ％" % (var_h)

	return var_h

def setup(bus, address):
	osrs_t = 1			#Temperature oversampling x 1
	osrs_p = 1			#Pressure oversampling x 1
	osrs_h = 1			#Humidity oversampling x 1
	mode   = 3			#Normal mode
	t_sb   = 5			#Tstandby 1000ms
	filter = 0			#Filter off
	spi3w_en = 0			#3-wire SPI Disable

	ctrl_meas_reg = (osrs_t << 5) | (osrs_p << 2) | mode
	config_reg    = (t_sb << 5) | (filter << 2) | spi3w_en
	ctrl_hum_reg  = osrs_h

	try:
		bus.write_byte_data(address, 0xF2, ctrl_hum_reg)
	except Exception as e:
		print '=== error details ==='
		print 'type:' + str(type(e))
		print 'args:' + str(e.args)
    	print 'message:' + e.message
    	print 'e:' + str(e)

	bus.write_byte_data(address, 0xF4, ctrl_meas_reg)
	bus.write_byte_data(address, 0xF5, config_reg)

	get_calib_param(bus, address)

# setup()
# get_calib_param()


if __name__ == '__main__':
	from smbus import SMBus

	bus_number  = 1
	i2c_address = 0x76

	bus = SMBus(bus_number)

	setup(bus, i2c_address)
	try:
		readData(bus, i2c_address)
	except KeyboardInterrupt:
		pass

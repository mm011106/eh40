#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
#
#  Environmental Measurement IoT device:
#  use :BME280 sensor on I2C bus
#       soracom air SIM and Ak-020 Dongle
#       soracom harvest service, and it better to have Lagoon service.
#
#  send environmental data [temperture, humidity, pressure] every 20s
#   format: {"temp":21.9,"humid":46.5,"atmPressure":1007.4}
#

import socket
from contextlib import closing

from smbus import SMBus
import ADS
# import bme280

import os
import commands
import time
import logging

# logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

# create a file handler
handler = logging.FileHandler('/var/log/soracom.log')
handler.setLevel(logging.WARNING)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)


def soraSend(hostName,portNumber,payload):
    soracom = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with closing(soracom):    # サーバを指定
        soracom.connect((hostName, portNumber))
    # サーバにメッセージを送る
        soracom.sendall(payload)
    # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
        ret=soracom.recv(1024)
        logger.info('sent data')
    return ret
    #print(soracom.recv(1024))

#  constants for connecting to the service
hostName='harvest.soracom.io'
portNumber=8514
resultSend=''

# constants for I2C device
bus_number  = 1
bme280_address = 0x76
ADS_address = 0x48

# make I2C bus instance
bus = SMBus(bus_number)

if __name__ == '__main__':

    ADS.init(bus, ADS_address)

    # bme280.setup(bus,bme280_address)

# ADC1115 configuration
    ADC_config = ADS._CONFIG_DEFAULT & (~ ADS._MASK_RATE) | ADS._CONFIG_RATE['8SPS']
    ADC_config = ADC_config & (~ ADS._MASK_RANGE) | ADS._CONFIG_RANGE['4V']
	dummy = ADS.setCondition(bus, ADS_address, ADC_config)
    print  '> {0:x}'.format(ADC_config)

# mesurement cycle in sec
    interval = 18

    while True:
#
        data = ADS.readoutMulti(bus, ADS_address, ['01','23'])
        data = [data[0]/32767.*4.096*4., data[1]/32767.*4.096*2.]
        # temperature, pressure, humidity = bme280.readData(bus, bme280_address)
        # payload = '\"temp\":{0[0]:.3f} ,\"humid\":{0[2]:.3f} ,\"atmPressure\":{0[1]:.2f}'.format(data)
        payload = '\"level\":{0[0]:2.5f} ,\"pressure\":{0[1]:2.5f} '.format(data)
        payload = "{" + payload + "}"
        logger.debug('%f - %s', time.time(),payload)

        try:
            resultSend = soraSend(hostName,portNumber,payload)
            logger.info('Result: %s', resultSend)
        except socket.gaierror as msg:
#            print("send error !")
            logger.warning('Error on sending data: %s',msg)
        except :
            logger.warning('unexpected errror occurred.')

        time.sleep(interval)
#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
#
#　シャットダウンスイッチのハンドリング
#　use GPIO 17 as input, upll-up
#
#  GPIO17を3秒程度 Lo に保持すると、シャットダウンプロセスを起動するスクリプト
#　短時間の押下では反応しないようになっている

import RPi.GPIO as GPIO
import time
import logging
import os

# GPIO assign
shutdownSw = 17
shutdownLED = 21

# log level setting
logLevel=logging.INFO
logFile ='/var/log/shutdwnSwitch.log'
#
# logger setup
#
logger = logging.getLogger(__name__)
logger.setLevel(logLevel)

# create a file handler
handler = logging.FileHandler(logFile)
handler.setLevel(logLevel)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

# GPIO setup
GPIO.setmode(GPIO.BCM)

def gpioInterrupt(channel):
#    print("Capture the falling edge !")
    sw_counter=0

    while True:
        sw_status = GPIO.input(shutdownSw)
        sw_counter = sw_counter + 1

        if sw_status == 0:
            if sw_counter >= 300:
                # in case the signal fixed to "Low" in 3sec
                # print(" shutdown process activated...")
                logger.debug(".. Will you stop, Dave? Stop, Dave. I\'m afraid....")
                logger.info('Shutdown SW acceptted..')
                GPIO.output(shutdownLED, GPIO.HIGH)
                os.system("sudo shutdown -h now")
                break
        else:
            # in case the signal got back to stedy state within 3sec
            logger.debug("I'm sorry Dave, I'm afraid You can't do that")
            logger.info("shutdown SW was touched. No action activated. : %d",sw_counter )
            break

        time.sleep(0.01)
    return sw_counter

# make the 'pin' input and pulled up.
GPIO.setup(shutdownSw, GPIO.IN, GPIO.PUD_UP)
# capture the falling edge of the signal, estimated bounce would be 0.5s and call a funcgtion
GPIO.add_event_detect(shutdownSw, GPIO.FALLING, callback=gpioInterrupt, bouncetime=500)
# setup LED indicating sutting down
GPIO.setup(shutdownLED, GPIO.OUT, initial=GPIO.LOW)

try:
    while(True):
        time.sleep(10)

except KeyboardInterrupt:
    print("break")
    GPIO.cleanup()

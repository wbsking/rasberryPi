#-*- coding:utf-8 -*-

import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

while True:
    GPIO.out(11, GPIO.HIGH)
    time.sleep(1)
    GPIO.out(11, GPIO.LOW)
    time.sleep(1)

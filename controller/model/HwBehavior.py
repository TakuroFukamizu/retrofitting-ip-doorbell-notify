# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

PIN_SWITCH  = 4  #GPIO  4 : PIN  7
PIN_BELL    = 17 #GPIO 17 : PIN 11
PIN_RUNNING = 26 #GPIO 26 : PIN 37

class HwBehavior:
    def __init__(self):
        # setup GPIO
        GPIO.setwarnings(False)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_SWITCH , GPIO.IN)
        GPIO.setup(PIN_BELL   , GPIO.OUT)
        GPIO.setup(PIN_RUNNING, GPIO.OUT)

        GPIO.output(PIN_BELL   , False)
        GPIO.output(PIN_RUNNING, False)

    def set_status_running(self):
        GPIO.output(PIN_RUNNING, True)

    def check_knock(self):
        ''' fetch swtich status -- 5 times/1 sec
        '''
        knocked = False
        for var in range(0, 5):
            value = GPIO.input(PIN_SWITCH)
            time.sleep(0.2)
            if value == 0:
                knocked = True
        return knocked

    def ring_bell(self):
        GPIO.output(PIN_BELL, True)
        time.sleep(1.5)
        GPIO.output(PIN_BELL, False)

    def cleanup(self):
        # clean up GPIO
        GPIO.output(PIN_BELL   , False)
        GPIO.output(PIN_RUNNING, False)
        GPIO.cleanup()
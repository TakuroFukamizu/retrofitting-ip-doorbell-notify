#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import atexit
import json
import time
from datetime import datetime
from model.LineNotifyRequest import *
from model.LocalChilds import LocalChildBellClient

import RPi.GPIO as GPIO

import bottle

# ----------

PIN_SWITCH  = 4  #GPIO  4 : PIN  7
PIN_BELL    = 17 #GPIO 17 : PIN 11
PIN_RUNNING = 26 #GPIO 26 : PIN 37

# ----------

def load_properties():
    basedir = os.path.dirname(os.path.abspath(__file__))
    pf = open(os.path.join(basedir, 'properties.json'), 'r')
    properties = json.load(pf)
    pf.close()
    return properties

def create_knock_message():
    msg_template = 'someone knock a door at {time}'
    attime = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    return msg_template.format(time=attime)

def ring_bell():
    GPIO.output(PIN_BELL, True)
    time.sleep(1.5)
    GPIO.output(PIN_BELL, False)
    
def goodbye():
    # clean up GPIO
    GPIO.output(PIN_BELL   , False)
    GPIO.output(PIN_RUNNING, False)
    GPIO.cleanup()

# ----------

app = application = bottle.default_app()

@bottle.route('/_api/bell/main/test', method='GET')
def test_main_bell():
    ring_bell()
    bottle.response.headers['Content-Type'] = 'application/json'
    return json.dumps({ 'status': True })

# ----------

if __name__ == "__main__":
    # start api server
    bottle.run(host = '0.0.0.0', port=80)

    atexit.register(goodbye) # Exit handler

    # setup GPIO
    GPIO.setwarnings(False)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_SWITCH , GPIO.IN)
    GPIO.setup(PIN_BELL   , GPIO.OUT)
    GPIO.setup(PIN_RUNNING, GPIO.OUT)

    GPIO.output(PIN_BELL   , False)
    GPIO.output(PIN_RUNNING, False)

    # read private config
    properties = load_properties()
    api_token = properties['line_api_token']

    GPIO.output(PIN_RUNNING, True)

    while True:
        # fetch swtich status -- 5 times/1 sec
        knocked = False
        for var in range(0, 5):
            value = GPIO.input(PIN_SWITCH)
            time.sleep(0.2)
            if value == 0:
                knocked = True

        if knocked:
            print 'knock. knock.'

            # send signal to child bells
            childs = LocalChildBellClient()
            childs.ring()

            try:
                # send Line notify
                req = LineNotifyRequest()
                req.setToken(api_token)
                req.setMessage(create_knock_message())
                print req.send()
            except:
                print 'Unexpected error on Line Notify:', sys.exc_info()[0]

            # ring door bell
            ring_bell()

            time.sleep(3.5) # long wait

    GPIO.cleanup()




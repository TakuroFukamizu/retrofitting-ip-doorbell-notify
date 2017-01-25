#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Local Child Bell node for ESP8266
"""

from socket import *
import machine
import time
import sys

HOST = ''
PORT = 5008

MSG_RECV_RING = "RECV RING"

# buzzer : IO4
pin_buzzer = machine.Pin(4, machine.Pin.OUT)
pin_buzzer.low()

s = socket(AF_INET, SOCK_DGRAM)
s.bind((HOST, PORT))

while True:
    msg, address = s.recvfrom(8192)

    print "message:", msg, "from", address

    if msg == MSG_RECV_RING:
        print MSG_RECV_RING
        pin_buzzer.high()
        time.sleep(1.5)
        pin_buzzer.low()

s.close()
sys.exit()
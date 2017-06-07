#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Local Child Bells supporter class
"""

import paho.mqtt.client as mqtt

class LocalChildBellClient:
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password
        client = mqtt.Client()
        client.on_connect = lambda client, userdata, rc: self.on_connect(userdata, rc)
        client.on_disconnect = lambda client, userdata, rc: self.on_disconnect(userdata, rc)
        client.on_message = lambda client, userdata, msg: self.on_message(userdata, msg)
        client.on_publish = lambda client, userdata, mid: self.on_publish(userdata, mid)
        client.username_pw_set(self.user, self.password)
        client.connect(self.url, 1883, 60)
        # client.loop_forever()
        client.loop_start()
        self.client = client

    def on_connect(self, userdata, rc):
        print("Connected with result code " + str(rc))
        self.client.subscribe("hello/world")
    
    def on_disconnect(self, userdata, rc):
        if  rc != 0:
            print("Unexpected disconnection.")

    def on_message(self, userdata, msg):
        print("Received message '" + str(msg.payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

    def on_publish(self, userdata, mid):
        print("publish: {0}".format(mid))

    def ring(self):
        self.client.publish("doorbell","request-ring")

if __name__ == '__main__':
    # test code
    from time import sleep
    child = LocalChildBellClient()
    while True:
        child.ring()
        sleep(3)
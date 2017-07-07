#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import atexit
import json
import time
from datetime import datetime
from model.LineNotifyRequest import *
from model.LocalChilds import LocalChildBellClient
from model.HwBehavior import HwBehavior

import bottle
from ListenKnockThread import ListenKnockThread

# ----------

hw = HwBehavior()

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

# ----------
app = application = bottle.default_app()

@bottle.route('/_api/bell/main/test', method='GET')
def test_main_bell():
    hw.ring_bell()
    bottle.response.headers['Content-Type'] = 'application/json'
    return json.dumps({ 'status': True })

# @bottle.route('/_api/notify/line/test', method='GET')

# ----------

if __name__ == "__main__":
    atexit.register(hw.cleanup()) # Exit handler

    # read private config
    properties = load_properties()
    api_token = properties['line_api_token']
    mqtt_url = properties['mqtt']['address']
    mqtt_user = properties['mqtt']['user']
    mqtt_password = properties['mqtt']['password']

    childs = LocalChildBellClient(mqtt_url, mqtt_user, mqtt_password)
    
    th = ListenKnockThread(hw, api_token, childs)
    th.start()
    hw.set_status_running()
    print('hoge')
    
    # start api server
    bottle.run(host='0.0.0.0', port=8080)
    # wsgiapp = bottle.default_app()
    # httpd = wsgiserver.Server(wsgiapp)
    # httpd.serve_forever()

    # while True:
    #     # fetch swtich status -- 5 times/1 sec
    #     if hw.check_knock():
    #         print('knock. knock.')

    #         # send signal to child bells
    #         childs.ring()

    #         try:
    #             # send Line notify
    #             req = LineNotifyRequest()
    #             req.setToken(api_token)
    #             req.setMessage(create_knock_message())
    #             print(req.send())
    #         except:
    #             print('Unexpected error on Line Notify:', sys.exc_info()[0])

    #         # ring door bell
    #         hw.ring_bell()

    #         time.sleep(3.5) # long wait




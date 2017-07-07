# -*- coding: utf-8 -*-

from __future__ import print_function
import threading
import time
import sys
from model.LineNotifyRequest import *

def create_knock_message():
    msg_template = 'someone knock a door at {time}'
    attime = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    return msg_template.format(time=attime)

class ListenKnockThread(threading.Thread):
    """listen knock event"""

    def __init__(self, hw, line_token, childs):
        super(ListenKnockThread, self).__init__()
        self.hw = hw
        self.childs = childs

    def run(self):
        while True:
            # fetch swtich status -- 5 times/1 sec
            if self.hw.check_knock():
                print('knock. knock.')

                # send signal to child bells
                self.childs.ring()

                try:
                    # send Line notify
                    req = LineNotifyRequest()
                    req.setToken(self.api_token)
                    req.setMessage(create_knock_message())
                    print(req.send())
                except:
                    print('Unexpected error on Line Notify:', sys.exc_info()[0])

                # ring door bell
                self.hw.ring_bell()

                time.sleep(3.5) # long wait
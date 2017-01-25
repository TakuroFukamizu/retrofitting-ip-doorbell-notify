#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Local Child Bells supporter class
"""

from socket import *

MSG_RECV_RING = "RECV RING"

class LocalChildBellClient:
    __port = 5008
    __host = ''
    __addres = "255.255.255.255"

    def _sendBroadcast(self, message):
        s = socket(AF_INET, SOCK_DGRAM)
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        s.bind((self.__host, self.__port))
        s.sendto(message, (self.__addres, self.__port))
        s.close()

    def ring(self):
        self._sendBroadcast(MSG_RECV_RING)

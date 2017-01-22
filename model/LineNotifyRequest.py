#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urllib

class LineNotifyRequest:
    __url = 'https://notify-api.line.me/api/notify'
    __apiToken = None;
    __message = None;

    def setToken(self, token):
        self.__apiToken = token

    def setMessage(self, message):
        self.__message = message

    def send(self):
        values = { 'message' : self.__message }
        headers = { 'Authorization' : 'Bearer {t}'.format(t=self.__apiToken) }

        data = urllib.urlencode(values)
        req = urllib2.Request(self.__url, data, headers)
        response = urllib2.urlopen(req)
        the_page = response.read()
        return the_page

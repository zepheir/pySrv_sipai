# -*- coding: utf-8 -*-
'''
Created on 2011-4-19

@author: Administrator
'''

import threading
import socket

_DEBUG = True

#------------------------------------------------------------------------------ 
# Modbus base class
#------------------------------------------------------------------------------ 
class BaseModbus(threading.Thread):
    ''' Base Modbus '''
#------------------------------------------------------------------------------ 
# Initial the Modbus
    def __init__(self, address):
        self.host, self.port = address

        self.connectionstate = False

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(0.2)
        self.connect()

#------------------------------------------------------------------------------ 
    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
        except socket.error:
            if _DEBUG: print 'Can not connect to %s' % self.host
            self.connectionstate = False
        else:
            self.connectionstate = True
            if _DEBUG: print '%s:%s connection established!' % (self.host, self.port)

#------------------------------------------------------------------------------ 
    def Close(self):
        if self.connectionstate:
            try:
                self.socket.close()
            except socket.error:
                if _DEBUG: print 'Can not KILL the socket link!'
            else:
                if _DEBUG: print '%s:%s connection is CLOSED!' % (self.host, self.port)
                self.connectionstate = False

#------------------------------------------------------------------------------ 
    def run(self):
        ''' Sample the module '''
        print 'I am base running!'

    def __del__(self):
#        self.Close()
        print 'Ended!'

def testfunciton():
    DMP_Address = (('192.168.127.254', 4001), ('192.168.127.254', 4002))
    DMP1 = BaseModbus(DMP_Address[0])
    DMP1.run()
    pass

if __name__ == '__main__':
    testfunciton()

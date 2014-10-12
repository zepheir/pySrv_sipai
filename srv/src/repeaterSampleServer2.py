#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2012-3-5

@author: zepheir
'''
import sys
sys.path.append('/app/srv/src')

from binascii import b2a_hex

try:
    from twisted.internet import epollreactor
    epollreactor.install()
except:
    pass

from twisted.internet import reactor
from twisted.python import log
from twisted.application import service

from zhyDB import ZhyDB

import Zoro
from ussop import temp_meter as TM
import time

import config
from config import *

# ECHO = True
# DEBUG = True


# 常量
zhy = ZhyDB()

# ElecMeterDict = zhy.listElecMeters(allSDS=None, allMods=True)
TempMeterDict = zhy.listTempMeters()
# factoryDict = {}
# modules = {}


class SampleServer(object):
    """docstring for SampleServer"""
    def __init__(self, *sds):
        super(SampleServer, self).__init__()
        self.sds = sds
        self.host,self.port = self.sds[0], int(self.sds[1])
        self.nowtype=''

        self.pointer = 0

        self.modules = 0
        self.mod = TM.Repeater(addr='000000000108')
        self.factory = Zoro.SetupTempRepeaterConnect(self.host, self.port, self.ReceiveData, reConnectMode=False)
        self.factory.spendtime = 10

        self.setup()

        
        

    def setup(self):
        # self.modules += ElecMeterDict[self.sds]
        self.sampletimer = ElectroMeterTimer
        if ECHO: print "*********** Time pass from start: %s"%(time.ctime()), self.factory.connection.getDestination(),self.factory.getState()

        self.pointer = zhy.readTempRepeaterPointer()
        

    def ReceiveData(self, *data):
        # if DEBUG: print ' ===> Received Data:', data
        # # global zhy
        _result = self.mod.realdata(data[2])
        if type(_result) == type({}):
            if 'pointer' in _result.keys():
                _pointer = int(_result['pointer'])
                print ' ===> Received Data:', data, _pointer
                # print '----------result---------',_result
                print data[0],data[1],zhy.updateTempRepeaterResult(
                        ip=data[1][0],
                        port=data[1][1],
                        addr=data[0],
                        value=_pointer
                    )
                self.modules = _pointer - self.pointer
            else:
                print ' ===> Received Data:', _result
                print data[0],data[1],zhy.updateTempMeterResults(
                    ip=data[1][0],
                    port=str(data[1][1]),
                    addr=_result['addr'],
                    value=_result['value']
                    )
        else:
            print ' ===> Received Data:', b2a_hex(data[2])


    def update(self):
        if DEBUG: print "[",self.sds,"] starting in the SampleServer Class!"

        if self.modules>0:
            print 'modules:',self.modules

            _cmd = self.mod.readRecordData(self.pointer)
            reactor.callLater(0.1, self.factory.protocol.SendCmd, _cmd)
            print b2a_hex(_cmd )

            self.modules = 0

        else:
            _cmd = self.mod.readRecordMount()
            zhy.setTempRepeaterState(
                ip=self.host,
                port=str(self.port),
                addr='000000000108',
                type='repeater',
                state='reading'
                )
            if DEBUG: print "===> Output command:",b2a_hex(_cmd)
            reactor.callLater(0.1, self.factory.protocol.SendCmd, _cmd)

    
        if SERVERRECONNECT:
            reactor.callLater(3, self.factory.connection.disconnect)
            reactor.callLater(8,self.factory.connection.connect)
        reactor.callLater(9,self.setup)
        reactor.callLater(10, self.update)
        # reactor.callLater(SdsConnectTimer+self.factory.spendtime, self.update)


servs ={}

def main():
    # for sds in ElecMeterDict:
    #     servs[sds]=SampleServer(sds[0],sds[1])
    #     servs[sds].update()
        # time.sleep(0.2)

    servs1=SampleServer('130.139.200.49','10003')
    # servs1.update()


   
if __name__ == '__main__':
    import sys

    main()

    reactor.run()
    print 'reactor stopped!'

    sys.exit(1)
elif __name__ =="__builtin__":
    import sys

    main()
    application = service.Application("TEMP1")


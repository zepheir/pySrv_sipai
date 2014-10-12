#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2012-2-5

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
from ussop import sipai as Sipai
import time

import config
from config import *

def ReceiveData(*data):
   if DEBUG: print 'print data----------------', data

# 常量
# ZDB = SipaiDB()
zhy = ZhyDB()

SipaiModsDict = zhy.listSipaiMods(allSDS=None)
# factoryDict = {}
# modules = {}


class SampleServer(object):
    """docstring for SampleServer"""
    def __init__(self, *sds):
        super(SampleServer, self).__init__()
        self.sds = sds
        self.host,self.port = self.sds[0], int(self.sds[1])

        self.modules = []
        self.mod = object
        self.nowtype=''
        self.factory = Zoro.SetupModbusConnect(self.host, self.port, self.ReceiveData, reConnectMode=False)
        self.factory.spendtime = 0.3

        self.setup()

        
        

    def setup(self):
        self.modules += SipaiModsDict[self.sds]
        self.sampletimer = SipaiSampleTimer
        if ECHO: print "*********** Time pass from start: %s"%(time.ctime()), self.factory.connection.getDestination(),self.factory.getState()
        

    def ReceiveData(self, *data):
        if DEBUG: print ' ===> Received Data:', data, b2a_hex(data[2])
        # global zhy
        _result = self.mod.dealdata(data[2])
        print '----------result---------',_result       
        print data[0],data[1],zhy.updateSipaiResults(
                ip=data[1][0],
                port=data[1][1],
                addr=data[0],
                type=self.nowtype,
                # value=b2a_hex(data[2])
                value=_result
            )


    def update(self):
        if DEBUG: print "[",self.sds,"] starting in the SampleServer Class!"

        if len(self.modules)>0:
            modinfo=self.modules.pop(0)
            self.nowtype = modinfo['type']
            self.mod = Sipai.createspm(type=modinfo['type'], address=modinfo['addr'])
            _cmd = self.mod.cmd(self.mod.CMD_READDATA)
            zhy.setSipaiModState(
                ip=self.host,
                port=str(self.port),
                addr=modinfo['addr'],
                type=self.nowtype,
                state='reading'
                )
            if DEBUG: print "===> Output command:",b2a_hex(_cmd)
            reactor.callLater(0.1, self.factory.protocol.SendCmd, _cmd)
            reactor.callLater(self.factory.spendtime, self.update)
            self.sampletimer-=self.factory.spendtime


        else:
            if SERVERRECONNECT:
                reactor.callLater(self.factory.spendtime, self.factory.connection.disconnect)
                reactor.callLater(SdsConnectTimer,self.factory.connection.connect)
            reactor.callLater(SdsConnectTimer,self.setup)
            reactor.callLater(self.sampletimer-SdsConnectTimer, self.update)
            # reactor.callLater(SdsConnectTimer+self.factory.spendtime, self.update)


servs ={}

def main():
    for sds in SipaiModsDict:
        servs[sds]=SampleServer(sds[0],sds[1])
        servs[sds].update()
        # time.sleep(0.2)
    # if DEBUG:
    #     # servs1=SampleServer('130.139.200.50','6020')
    #     servs2=SampleServer('130.139.200.51','10001')
    #     # servs3=SampleServer('130.139.200.56','10001')
    #     # servs1.update()
    #     servs2.update()
    #     # servs3.update()
    # else:
    #     for sds in SipaiModsDict:
    #         servs[sds]=SampleServer(sds[0],sds[1])
    #         servs[sds].update()
    #         time.sleep(0.2)
   
if __name__ == '__main__':
    import sys

    main()

    reactor.run()
    print 'reactor stopped!'

    sys.exit(1)
elif __name__ =="__builtin__":
    import sys

    main()
    application = service.Application("SIPAI")


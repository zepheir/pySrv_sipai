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
from ussop import elec_meter as EM
import time

import config
from config import *

# ECHO = True
# DEBUG = True


# class MyDb(HaiyanDB):
#     ''''''

#     def __init__(self):

#         if ECHO: print " ** Start Initialization"


# #        if DEBUG:HaiyanDB.__init__(self, ip='127.0.0.1')
# #        else: HaiyanDB.__init__(self, ip='192.168.192.250')

#         HaiyanDB.__init__(self, ip='127.0.0.1')

# #        # setup the conneciton of the mongodb
# #        try:
# #            conn = Connection('127.0.0.1', 27017)
# #        except:
# #            print 'db connection error!'
# #            conn = None
# #
# #        if conn != None:
# #            # print the dbs in the mongodb
# #            print conn.database_names()
# #
# #        # create database object from connecting database name
# #        self.db = conn[u'hyegdb']

#         self.loadMods()
#         records = self.db.temp2.find()
#         self.record = records[0]

#         if DEBUG: print self.collectionNames()

#         if ECHO: print " ** End Initialization"


#     def loadMods(self):
#         mods = self.db.ElecMeters.find()
#         self.modDict = {}
#         if DEBUG:
#             self.modDict = {(u'192.168.192.100', u'6020'): [(u'1040', u'000012046365')],
# #                           (u'192.168.192.100', u'6021'): [(u'1001', u'4'), (u'1030', u'7'), (u'1020', u'8')],
#                            }
#         else:
#             for mod in mods:
#                 ip = mod['IP']
#                 port = mod['PORT']
#                 addr = mod['ADDRESS']
#                 type = mod['Type']
#                 if addr != '':
#                     try:
#                         self.modDict[ip, port].append((type, addr))
#                     except:
#                         self.modDict[ip, port] = [(type, addr), ]

#         self.devices = self.modDict.keys()
# #        print self.modDict



# # setup Database
# HYDB = MyDb()
# #HYDB.loadMods()

# devices = HYDB.devices
# #result = HYDB.readResults()
# factoryDict = {}
# modules = {}


# def update():
#     if ECHO: print " -- Each Second! --"

#     t1 = time.clock()

#     factorys = factoryDict.keys()

#     for factory in factorys:
#         for i, mod in enumerate(factoryDict[factory]):
#             _cmds = (mod.readPower(), mod.readPowerNow(), mod.readVoltage(), mod.readCurrent(), mod.readCos(), mod.readReactivePower())
#             spt = factory.spendtime * i * len(_cmds)
#             for ii, _cmd in enumerate(_cmds):
#                 reactor.callLater(spt + factory.spendtime * ii, factory.protocol.SendCmd, _cmd)

#     t2 = time.clock()
#     print t2 - t1

#     reactor.callLater(30, update)


# def ReceiveData(*data):
# #    print 'print data----------------', data

#     # ȷ�� module
#     mod = modules[(data[0], data[1])]
#     # deal with data
#     result = mod.dealdata(data[2])
# #    # get string data

# #    print 'final result:', result
# #    # save to mongodb 
#     key = str(data[1][0].split('.')[-1]) + '-' + str(data[1][1]) + '-' + str(data[0])
# #    records = HYDB.db.temp2.find().sort('_id', pymongo.DESCENDING)
# #    record = records[0]
# #    record.pop('_id')
# #    print 'record', record
# #    for record in records:
# #        for ch, _result in enumerate(result[1]):
# #            _key = key + '-' + str(result[0] + ch)
# #            record[_key] = _result
# #            print _key
# #        HYDB.db.temp2.insert(record)
#     for ch, _result in enumerate(result[1]):
#         _key = key + '-' + str(result[0] + ch)
#         HYDB.record[_key] = _result
#     HYDB.db.temp2.save(HYDB.record)


# def main():
#     '''  初始化  '''
#     # Initial states

#     print devices

#     # define factoryDict
#     for dev in devices:
#         factory = Zoro.SetupElecMeterConnect(dev[0], int(dev[1]), ReceiveData,
#                                              reConnectMode=True)
#         factoryDict[factory] = []
#         for mod in HYDB.modDict[dev]:
# #            _mod = Sipai.createspm(None, type=mod[0], address=mod[1])
#             _mod = ElecMeter.createElMeter(None, mod[1])
#             factoryDict[factory].append(_mod)
#             # define modules
#             modules[mod[1], (dev[0], int(dev[1]))] = _mod

#     print factoryDict
#     print modules


#     # Main loop
#     if ECHO: print " -- Main loop running! --"
#     reactor.callLater(0, update)

#     reactor.run()


# 常量
zhy = ZhyDB()

ElecMeterDict = zhy.listElecMeters(allSDS=None, allMods=True)
# factoryDict = {}
# modules = {}


class SampleServer(object):
    """docstring for SampleServer"""
    def __init__(self, *sds):
        super(SampleServer, self).__init__()
        self.sds = sds
        self.host,self.port = self.sds[0], int(self.sds[1])
        self.nowtype=''

        self.modules = []
        self.mod = object
        # self.factory = Zoro.SetupModbusConnect(self.host, self.port, self.ReceiveData, reConnectMode=False) 
        self.factory = Zoro.SetupElecMeterConnect(self.host, self.port, self.ReceiveData, reConnectMode=False)
        self.factory.spendtime = 1

        self.setup()

        
        

    def setup(self):
        self.modules += ElecMeterDict[self.sds]
        self.sampletimer = ElectroMeterTimer
        if ECHO: print "*********** Time pass from start: %s"%(time.ctime()), self.factory.connection.getDestination(),self.factory.getState()
        

    def ReceiveData(self, *data):
        if DEBUG: print ' ===> Received Data:', data
        # global zhy
        _result = self.mod.dealdata(data[2])
        # print '----------result---------',_result
        print data[0],data[1],zhy.updateElectroResults(
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
            self.mod = EM.createEMTR(addr=modinfo['addr'],type=modinfo['type'])
            _cmd = self.mod.readdata()
            zhy.setElectroMeterState(
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
    for sds in ElecMeterDict:
        servs[sds]=SampleServer(sds[0],sds[1])
        servs[sds].update()
        # time.sleep(0.2)
    # if DEBUG:
    #     servs1=SampleServer('130.139.200.50','6021')
    #     servs2=SampleServer('130.139.200.52','10002')
    #     # servs3=SampleServer('130.139.200.56','10001')
    #     servs1.update()
    #     servs2.update()
    #     # servs3.update()
    # else:
    #     for sds in SipaiModsDictWithout30:
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
    application = service.Application("ELECTRO")


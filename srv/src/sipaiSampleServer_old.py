#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2012-2-5

@author: zepheir
'''

#import pymongo
#from pymongo import Connection
from binascii import b2a_hex

from twisted.internet import reactor
from twisted.python import log
from twisted.application import service

from zhyDB import ZhyDB

import Zoro
from ussop import sipai as Sipai
import time

import config
from config import *



# ECHO = True
# DEBUG = True


# class SipaiDB(ZhyDB):
#     ''''''

#     def __init__(self):

#         if ECHO: print " ** Start Initialization"

#         # if DEBUG:ZhyDB.__init__(self, ip='127.0.0.1')
#         ZhyDB.__init__(self, ip=config.serverIP)

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

#         records = self.db.results.find()
#         self.record = records[0]


#         if DEBUG: print self.collectionNames()

#         if ECHO: print " ** End Initialization"


# #----------------------------------------------------------
# #   Sipai Module functions
# #----------------------------------------------------------

#     # def readSipaiMods(self):
#     #     ''' Read Sipai Modules '''
#     #     if self.db:
#     #         mods = list(self.db.devices.find({"manufacturer":IDFSipai}))
#     #         if DEBUG: print dbgIDF+"SipaiModules:",mods
#     #         return mods
#     #     else:
#     #         if DEBUG: print dbgIDF+"SipaiModules:",False
#     #         return False


#     # def readSipaiVars(self):
#     #     ''' Read Sipai Module Vars '''
#     #     if self.db:
#     #         _vars = list(self.db.vars.find({"manufacturer":IDFSipai}))
#     #         if DEBUG: print dbgIDF+"SipaiVars:",_vars
#     #         return _vars
#     #     else:
#     #         if DEBUG: print dbgIDF+"SipaiVars:",False
#     #         return False


#     def loadMods(self):
#         # mods = self.db.SipaiMods.find()
#         mods = self.readSipaiMods()
#         self.modDict = {}

#         for mod in mods:
#             _ip = mod['ip']
#             _port = mod['port']
#             _addr = mod['addr']
#             _type = mod['type']
#             try:
#                 self.modDict[_ip, _port].append((_type, _addr))
#             except:
#                 self.modDict[_ip, _port] = [(_type, _addr), ]

#         # if DEBUG:
#         #     self.modDict = {#(u'192.168.192.100', u'6020'): [(u'1040', u'5')],
#         #                    (u'192.168.192.100', u'6021'): [(u'1001', u'4'), (u'1030', u'7'), (u'1020', u'8')],
#         #                    }
#         # else:
#         #     for mod in mods:
#         #         ip = mod['IP']
#         #         port = mod['PORT']
#         #         addr = mod['ADDRESS']
#         #         type = mod['MODTYPE']
#         #         try:
#         #             self.modDict[ip, port].append((type, addr))
#         #         except:
#         #             self.modDict[ip, port] = [(type, addr), ]

#         self.devices = self.modDict.keys()
#         if DEBUG: print dbgIDF+"modules:",self.modDict


def ReceiveData(*data):
   if DEBUG: print 'print data----------------', data

    # 确定 module
    # mod = modules[(data[0], data[1])]
    # deal with data
    # result = mod.dealdata(data[2])
    # print result

#    # get string data

#     # save to mongodb 
#     key = str(data[1][0].split('.')[-1]) + '-' + str(data[1][1]) + '-' + str(data[0])

# #    records = ZDB.db.temp.find()
# #    for record in records:
# #        for ch, _result in enumerate(result):
# #            _key = key + '-' + str(ch)
# #            record[_key] = _result
# #        ZDB.db.temp.save(record)
#     for ch, _result in enumerate(result):
#         _key = key + '-' + str(ch)
#         ZDB.record[_key] = _result
# #    ZDB.db.temp.save(ZDB.record)



# 常量
# ZDB = SipaiDB()
zhy = ZhyDB()

#ZDB.loadMods()

# devices = ZDB.devices
# devices = ZDB.readSipaiMods()
#result = ZDB.readResults()
SipaiModsDict = zhy.listSipaiMods(None)
factoryDict = {}
modules = {}


# alltimes = 1 * 60 / 3 - 1  # 10 minutes * 60 seconds / 3 seconds

# global nowtimes
nowtimes = 1

# def update():
#     # global nowtimes

#     if ECHO: print " -- Now Times: %04d --"%nowtimes

#     t1 = time.clock()

#     # ZDB.db.temp.save(ZDB.record)

#     factorys = factoryDict.keys()

#     # for factory in factorys:
#     #     for i, mod in enumerate(factoryDict[factory]):
#     #         _cmd = mod.readdata()
#     #         reactor.callLater(factory.spendtime * i, factory.protocol.SendCmd, _cmd)

#     t2 = time.clock()
#     print t2 - t1

#     nowtimes+=1

#     reactor.callLater(3, update)


# #    if nowtimes < alltimes:
# #        reactor.callLater(3, update)
# #        nowtimes += 1
# #    else:
# #        reactor.stop()

#     reactor.callLater(0, reactor.stop)



def main():

    '''  初始化  '''
    # Initial states

    # print devices


    factory = Zoro.SetupModbusConnect('130.139.200.50', int(6021), ReceiveData,
                                          reConnectMode=False)
    factory.modules += SipaiModsDict['130.139.200.50','6021']
    factory.spendtime =0.2

    # for sds in SipaiModsDict:
    #     factoryDict[sds[0],sds[1]] = Zoro.SetupModbusConnect(sds[0], int(sds[1]), ReceiveData,
    #                                  reConnectMode=False)
    #     factoryDict[sds[0],sds[1]].modules += SipaiModsDict[sds[0],sds[1]]
    #     factoryDict[sds[0],sds[1]].spendtime = 0.2

    #     if DEBUG: print "===> factory modules: ", factoryDict[sds[0],sds[1]].modules

    # for dev in SipaiModsDict:
    #     # print dev
    #     # factory = Zoro.SetupModbusConnect(dev[0], int(dev[1]), ReceiveData,
    #     #                                   reConnectMode=False)
    #     factoryDict[factory] = []
    #     # for mod in ZDB.modDict[dev]:
    #     #     _mod = Sipai.createspm(None, type=mod[0], address=mod[1])
    #     #     factoryDict[factory].append(_mod)
    #     #     # 定义modules
    #     #     modules[int(mod[1]), (dev[0], int(dev[1]))] = _mod

    # print factoryDict
    # print modules


    # Main loop
    if ECHO: print " -- Main loop running! --"


    def upd():
        print 'in upd program:',factory
        
        if len(factory.modules)>0:
            modinfo = factory.modules.pop(0)
            # modinfo = factory.modules[0]
            # mod = Sipai.SIPAIModule(address=modinfo['addr'])
            mod = Sipai.createspm(type=modinfo['type'], address=modinfo['addr'])
            _cmd = mod.cmd(mod.CMD_READDATA)
            if DEBUG: print "===> Output command:",b2a_hex(_cmd)
            reactor.callLater(0, factory.protocol.SendCmd, _cmd)

          
            reactor.callLater(factory.spendtime,upd)
        else:
            # _host,_port = factory.connection.host, str(factory.connection.port)
            reactor.callLater(factory.spendtime,factory.connection.disconnect)
            # factory.modules += SipaiModsDict[_host, _port]
            # print factory
            reactor.callLater(factory.spendtime+1, main)
            # reactor.callLater(factory.spendtime+1,upd)



    # def update(_factory):
        
    #     if len(_factory.modules)>0:
    #         modinfo = _factory.modules.pop(0)
    #         # modinfo = _factory.modules[0]
    #         # mod = Sipai.SIPAIModule(address=modinfo['addr'])
    #         mod = Sipai.createspm(type=modinfo['type'], address=modinfo['addr'])
    #         _cmd = mod.cmd(mod.CMD_READDATA)
    #         if DEBUG: print "===> Output command:",b2a_hex(_cmd)
    #         # reactor.callLater(0, _factory.protocol.SendCmd, _cmd)

          
    #         reactor.callLater(_factory.spendtime,update,_factory)
    #     else:
    #         _host,_port = _factory.connection.host, int(_factory.connection.port)
    #         reactor.callLater(_factory.spendtime,_factory.connection.disconnect)
    #         reactor.callLater(_factory.spendtime+1,reload, _host,_port)
    #         # reactor.callLater(_factory.spendtime+1, main)


    # for key in factoryDict:
    #     reactor.callLater(1,update, factoryDict[key])

    reactor.callLater(1, upd)
    # reactor.run()

    




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


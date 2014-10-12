#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2011-9-29

Modify on 2012.8.9: Add Timeout function.
- BaseProtocol(Protocol) -> BaseProtocol(Protocol, TimeoutMixin)

Modify on 2013.12.1: Add ScanSDS function.

@author: zepheir
'''
#from twisted.internet import wxreactor
#wxreactor.install()

import sys

# from twisted.internet import epollreactor
# epollreactor.install()

from twisted.internet import reactor

from twisted.internet.protocol import ClientFactory, Protocol
from twisted.protocols.policies import TimeoutMixin
#from twisted.protocols.basic import LineReceiver
#from twisted.internet.protocol import Protocol
#from twisted.internet.endpoints import TCP4ClientEndpoint

from binascii import b2a_hex
from struct import unpack
from time import ctime

from ussop import crc16

import config
from config import *

class BaseProtocol(Protocol, TimeoutMixin):

    def __init__(self, callback=None):
        # 接收缓存
        self.rawdata = ""
        # 接收地址
#        self.receivedAddr = object
        # 接收数据
#        self.receivedData = ''
        # 回调方法
        self.callback = callback
#        print "call back:", self.callback
        # 最小字长
        self.MINBYTES = 4

    def connectionMade(self):
        ''' 1. 设置数据接收方式: self.setRawMode() or self.setLineMode(extra)
            2. 设置self.protocol: self.protocol=BaseProtocol'''
        # Default timeout time: None
        self.protocol.setTimeout(None)
        # self.protocol.setTimeout(60 * 1) # Timeout period = 60 * 1 minutes


    def SendCmd(self, cmd):
        if self.transport:
            try:
#                self.sendLine(cmd)
                self.transport.write(cmd)
#                print self.transport.getPeer(), "send line OK:", b2a_hex(cmd)
                return True
            except:
                print self.transport.getPeer(), "send line ERROR!!!(%s)" % b2a_hex(cmd)
                return False
        else:
            print "[%s] Connection lost!" % ctime()
            return False


    def dataReceived(self, data):
        # print 'data receicved:', b2a_hex(data)
        # Reset Protocol Time out 
        self.resetTimeout()

        self.rawdata = self.rawdata + data
        # 接收缓存 self.rawdata >= 4 可以调用处理函数

        if len(self.rawdata) > 64:
            print "---------------length error--------------------"
            self.rawdata = ""
        elif len(self.rawdata) >= self.MINBYTES:
            if DEBUG: print '[%s]' % ctime(), ' buffer length:', len(self.rawdata)
            self.dealdata()
            # print b2a_hex(self.rawdata)



    def connectionLost(self, reason):
        ''''''
        # 清除缓存中的值
        self.rawdata = ''


    def timeoutConnection(self):
#        self.transport.unregisterProducer()
        self.transport.loseConnection()
#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
## Should be override as your wish
#    def start(self):
#        ''''''
#
#        self.rawdata = ''
#        self.step = 0
#        self.t1 = clock()
#        def foo(step):
#            self.rawdata = ''
#            self.step = step
#            try:
#                self.sendLine(chr(self.Addr[step]) +
#                               self.Module[step].ReadData())
#                print 'foo:', step, 'sendline OK!'
#                print b2a_hex(chr(self.Addr[step]) + self.Module[step].ReadData())
#            except:
#                self.sendLine('error')
#
#        for i in range(len(self.Module)):
#            t = 0.1 * i
#            reactor.callLater(t, foo, i)
#        reactor.callLater(1, self.end)
#
#
#
##------------------------------------------------------------------------------ 
#    def dealdata(self):
#        if len(self.rawdata) > 4:
#            print b2a_hex(self.rawdata)
#            if (len(self.rawdata) - 5) == int(b2a_hex(self.rawdata[2]), 16):
##                if self.Module[self.step].CheckModuleType( self.rawdata ):
#                    print b2a_hex(self.rawdata)
#                    try:
##                        print  self.transport.getPeer().host, self.transport.getPeer().port, self.Module[self.step].DealRawData( self.rawdata )
#                        self.data = self.Module[self.step].DealRawData(self.rawdata)
##                        print  self.data
##                        if self.step == 0:
##                            self.cur.execute( self.Module[self.step].sql, self.data )
#                    except:
#                        print 'step %d error!' % (self.step)
##                    else:
##                        self.rawdata = ''
##                        self.step += 1
##                    self.end()
##                    reactor.callLater( 0, self.next )
#------------------------------------------------------------------------------ 
    def end(self):
#        self.transport.loseConnection()
#        self.t2 = clock()
#        print self, '**spend time:', self.t2 - self.t1
        pass
#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
class Modbus(BaseProtocol):
    ''' 专注于 Modbus 协议 '''

    def connectionMade(self):
#        print 'connect made:', self.transport.getPeer().host, self.transport.getPeer().port

        self.setTimeout(None)

#        self.setRawMode()
#        self.transport.loseConnection()
        self.protocol = Modbus

        # 清除缓存中的数值
        self.rawdata = ''
        self.MINBYTES = 7

#        self.start()

    def dealdata(self):
        ''' Modbus 数据处理方法 '''
        if self.rawdata[1] == "\x2b": # 设备型号命令
            databytes = int(b2a_hex(self.rawdata[3]), 16)
            if (len(self.rawdata) - 6) == databytes:

                # TODO: deal device type
                # ...

                receivedAddr = int(b2a_hex(self.rawdata[0]), 16)
                receivedData = self.rawdata[4:4 + databytes]
                self.rawdata = ''
#                print self.receivedAddr, b2a_hex(self.receivedData), self.receivedData
                if self.callback:
                    self.callback(receivedAddr, self.transport.getPeer(), receivedData)

        elif self.rawdata[1] == "\x10": # 设备
            self.rawdata = ''

        elif self.rawdata[1] == '\x03': # 读取数据命令
            # 数据长度
            databytes = int(b2a_hex(self.rawdata[2]), 16)
            # 校验数据长度
            if (len(self.rawdata) - 5) == databytes:

                # TODO: deal device data
                # ...
                # 接收到的地址
                receivedAddr = int(b2a_hex(self.rawdata[0]), 16)
                # 接收到的实际数据
                receivedData = self.rawdata[3:3 + databytes]
                # 清除接收数据缓存
                self.rawdata = ''
                # 回调函数
                if self.callback:
                    self.callback(receivedAddr,
                                  (self.transport.getPeer().host, self.transport.getPeer().port),
                                  receivedData)
#                    print self.receivedAddr, b2a_hex(self.receivedData), self.receivedData
        else:
            self.rawdata = ''
#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
class ElecMeterProtocol(BaseProtocol):
    ''' 电表通讯协议 '''

    def connectionMade(self):
#        print 'connect made:', self.transport.getPeer().host, self.transport.getPeer().port
        # 设置接收数据方式
#        self.setRawMode()

        self.setTimeout(None)

        # 设置 protocol 属性
        self.protocol = ElecMeterProtocol

        # 清除缓存中的数值
        self.rawdata = ''
        self.MINBYTES = 9

    def dealdata(self):
        ''' 电表数据处理方法 '''

        # 去除唤醒字节 FEH
        self.rawdata = self.rawdata.lstrip('\xfe')

        # 判断命令
        print b2a_hex(self.rawdata)

        if len(self.rawdata) > 12:

            if self.rawdata[8] == '\x81':
                # 数据长度
#                databytes = int(b2a_hex(self.rawdata[9]), 16)
                databytes = unpack('<B', self.rawdata[9])[0]
#                print 'databytes:', databytes
                # 校验数据长度
                if (len(self.rawdata) - 12) == databytes:

                    # TODO: deal device data
                    # ...
                    # 接收到的地址, 转化为正常次序
                    addr = ''
                    for i in range(6, 0, -1):
                        addr += self.rawdata[i]
                    receivedAddr = b2a_hex(addr)
                    # 接收到的实际数据: 根据协议所有数据须要减去0x33
#                    DI0 = hex(int(b2a_hex(self.rawdata[10]), 16) - 0x33)
#                    DI1 = hex(int(b2a_hex(self.rawdata[11]), 16) - 0x33)

#                    DI0 = unpack('B', self.rawdata[10])[0] - 0x33
#                    DI1 = unpack('B', self.rawdata[11])[0] - 0x33

#                     realdata = ''
#                     for i in range(databytes - 2):
# #                        x = int(b2a_hex(self.rawdata[12 + i]), 16) - 0x33
#                         x = unpack('B', self.rawdata[12 + i])[0] - 0x33
#                         realdata = chr(x) + realdata

#                    receivedData = b2a_hex(realdata)
                    receivedData = self.rawdata
                    # 清除接收数据缓存
                    self.rawdata = ''
                    # 回调函数
                    if self.callback:
                        self.callback(receivedAddr, 
                            (self.transport.getPeer().host, self.transport.getPeer().port),
                            receivedData)
            else:
                self.rawdata = ''


#        datalen = int(b2a_hex(data[10]), 16) - 2
#        print "data length:", datalen
#        datac = data[13:(13 + datalen)]
#
#        realdata = ''
#        for i in range(datalen):
#            x = int(b2a_hex(datac[i]), 16) - 0x33
#            realdata = chr(x) + realdata
#        return  realdata


# -----------------------------------------------------------------------------
class TempRepeaterProtocol(BaseProtocol):
    ''' 无线温度协议1 '''

    def connectionMade(self):
#        print 'connect made:', self.transport.getPeer().host, self.transport.getPeer().port
        # 设置接收数据方式
#        self.setRawMode()

        self.setTimeout(None)

        # 设置 protocol 属性
        self.protocol = TempRepeaterProtocol

        # 清除缓存中的数值
        self.rawdata = ''
        self.MINBYTES = 9

        self.pointer = 0

    def dealdata(self):
        ''' 电表数据处理方法 '''

        # 去除唤醒字节 FFH
        self.rawdata = self.rawdata.lstrip('\xff')

        # 判断命令
        print b2a_hex(self.rawdata)

        if len(self.rawdata) > 12:

            if self.rawdata[8] == '\x81' or self.rawdata[8]=='\x01':
                # 数据长度
#                databytes = int(b2a_hex(self.rawdata[9]), 16)
                databytes = unpack('<B', self.rawdata[9])[0]
#                print 'databytes:', databytes
                # 校验数据长度
                if (len(self.rawdata) - 12) == databytes:

                    # TODO: deal device data
                    # ...
                    # 接收到的地址, 转化为正常次序
                    addr = ''
                    for i in range(6, 0, -1):
                        addr += self.rawdata[i]
                    receivedAddr = b2a_hex(addr)

                    receivedData = self.rawdata
                    # 清除接收数据缓存
                    self.rawdata = ''
                    # 回调函数
                    if self.callback:
                        self.callback(receivedAddr, 
                            (self.transport.getPeer().host, self.transport.getPeer().port),
                            receivedData)
            else:
                self.rawdata = ''

    def setPointer(self, pointer=0):
        self.pointer = int(pointer)



#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
class MyClientFactory(ClientFactory):

    def __init__(self, reConnectMode=False):
        self.reConnectMode = reConnectMode
        self.bandrate = 9600
        self.spendtime = 0.2
        self.connection = object()
        self.modules = []
        self.state = ''

    def getState(self):
        return self.state

    def SetReConnectMode(self, Mode=False):
        self.reConnectMode = Mode

    def GetReConnectMode(self):
        return self.reConnectMode

    def startedConnecting(self, connector):
        self.connector = connector
        self.state='connecting'
        if DEBUG: print '**[%s] Started to connect ->' % ctime(), self.connector.getDestination()


    def buildProtocol(self, addr):
        self.state="connected"
        if ECHO: print '**[%s] Connected' % ctime(), addr.host, addr.port
        return self.protocol

    # def Disconnect(self):
    #     print '**[%s] Disconnect ->' % ctime(), self.connector.getDestination()
    #     self.connector.disconnect()

    def clientConnectionLost(self, connector, reason):
        self.state="connectlost"
        if DEBUG: print '**[%s] %s %s Lost connection, Reason:' % (ctime(),connector.host, connector.port), reason.value
        # 清除缓存中的数值
        self.protocol.rawdata = ""
        self.modules = []
        
        if self.reConnectMode == True:
            connector.connect()
        else:
            if DEBUG: print '**Release Connector: ', connector.getDestination()
            pass

    def clientConnectionFailed(self, connector, reason):
        self.state="connectfail"
        if DEBUG: print '**[%s] %s %s Connection failed. Reason:' % (ctime(),connector.host, connector.port), reason
        # 清除缓存中的数值
        self.protocol.rawdata = ''
        if self.reConnectMode == True:
            connector.connect()
#        reactor.stop()



def SetupModbusConnect(IP, Port, callback, reConnectMode=False):
#    import sys
#    print sys.modules['twisted.internet.reactor']

#    reactor.disconnectAll()
    DisconnectAll()

    # create factory
    factory = MyClientFactory(reConnectMode)
    factory.spendtime = 0.3
    # set factory protocol
    factory.protocol = Modbus(callback)
    # reactor connect host with factory
    factory.connection = reactor.connectTCP(IP, Port, factory)

    return factory


def SetupElecMeterConnect(IP, Port, callback, reConnectMode=False):
#    import sys
#    print sys.modules['twisted.internet.reactor']

#    reactor.disconnectAll()
    DisconnectAll()

    # create factory
    factory = MyClientFactory(reConnectMode)
    factory.spendtime = 0.5
    # set factory protocol
    factory.protocol = ElecMeterProtocol(callback)
    # reactor connect host with factory
    factory.connection = reactor.connectTCP(IP, Port, factory)

    return factory


def SetupTempRepeaterConnect(IP, Port, callback, reConnectMode=False):
#    import sys
#    print sys.modules['twisted.internet.reactor']

#    reactor.disconnectAll()
    DisconnectAll()

    # create factory
    factory = MyClientFactory(reConnectMode)
    factory.spendtime = 0.5
    # set factory protocol
    factory.protocol = TempRepeaterProtocol(callback)
    # reactor connect host with factory
    factory.connection = reactor.connectTCP(IP, Port, factory)

    return factory    


def DisconnectAll():
    reactor.disconnectAll()

def StopReactor():
    reactor.stop()

def PrintData(a, b, c):
    print a, b, c

def ReceiveData(self, *data):
    print "received data:", data

#------------------------------------------------------------
#   Scan Serial Device Server funcion
# -----------------------------------------------------------
def ScanSDS(ip_from='127.0.0.1',ip_to='127.0.0.1',port=(6020,6021)):
    ''' Scan Serial Device Server '''

    import struct, socket

    print " ----- I am Zoro! I am ScanSDS!! -----"

    sdsMods = []

    class ScanFactory(MyClientFactory):
        """docstring for ScanFactory"""
            
        def buildProtocol(self, addr):
            print '**[%s] Connected' % ctime(), addr.host, addr.port
            sdsMods.append((addr.host,addr.port))
            # print ' ==> sdsMods:',sdsMods
            return self.protocol


    def UpdateDB():
        from myDB import MyDB
        from ussop.sds import SdsDB

        # _db = MyDB()
        _db = SdsDB()

        # print sdsMods
        for mod in sdsMods:
            # print zhy.db.devices.find({'ip':mod[0],'port':str(mod[1]),'type':'sds'}).count()
            # print zhy.findSdsMods(ip=mod[0],port=mod[1])

            if _db.findSdsMods(ip=mod[0],port=mod[1]) == 0:
                _db.newSdsMods({
                    "ctrlbox": "",
                    "ip": mod[0],
                    "manufacturer": "HLH",
                    "port": str(mod[1]),
                    "position": "",
                    "type": "sds"
                    })

        # print zhy.readSdsMods()

        reactor.callLater(0, reactor.stop)


    ip_from_int = struct.unpack("!I",socket.inet_aton(ip_from))[0]
    ip_to_int = struct.unpack("!I",socket.inet_aton(ip_to))[0]+1

    for ip in range(ip_from_int, ip_to_int):

        ip_str = socket.inet_ntoa(struct.pack("!I",ip))
        # create factory
        factory1 = ScanFactory()
        # set factory protocol
        factory1.protocol = Modbus(PrintData)
        # reactor connect host with factory
        reactor.connectTCP(ip_str, int(port[0]), factory1)


        # create factory
        factory2 = ScanFactory()
        # set factory protocol
        factory2.protocol = Modbus(PrintData)
        # reactor connect host with factory
        reactor.connectTCP(ip_str, int(port[1]), factory2)



    reactor.callLater(3, DisconnectAll)

    reactor.callLater(3.5,UpdateDB)

    reactor.run()


#------------------------------------------------------------
#   Scan Sipai Modules funcion
# -----------------------------------------------------------
def ScanSipaiMods(addr_from=1,addr_to=255):
    ''' Scan Sipai Modules funcion '''

    import struct, socket
    from ussop.sipai import SIPAIModule

    from zhyDB import ZhyDB

    print "I am Zoro! I am scanning Sipai Modules!!!"

    zhy = ZhyDB()
    sdsMods = zhy.readSdsMods()

    def foo(cmd):
        print '==> Output command:',b2a_hex(cmd)
        factory.protocol.SendCmd(cmd)


    def _connect(ip,port,_factory):
        # reactor connect host with factory
        reactor.connectTCP(ip, int(port), _factory)        

    def UpdateDB(maddr, naddr, mtype):

        # print maddr, naddr.host, naddr.port, mtype
        
        if zhy.findSipaiMods(ip=naddr.host,port=naddr.port,addr=maddr) == 0:
            print '==> Add New Sipai Module:', maddr, naddr, str(mtype)
            zhy.newSipaiMods({
                "addr": str(maddr),
                "ctrlbox": "",
                "ip": naddr.host,
                "manufacturer": "SIPAI",
                "port": str(naddr.port),
                "position": "",
                "type": str(mtype),
                "state":'ok',
                'value':'',
                'timeout':10
                })
            if str(mtype) in SIPAIDOUBLEMODS:
                print '==> Add New Sipai Module:', maddr, naddr, str(mtype)+"a"
                zhy.newSipaiMods({
                    "addr": str(maddr),
                    "ctrlbox": "",
                    "ip": naddr.host,
                    "manufacturer": "SIPAI",
                    "port": str(naddr.port),
                    "position": "",
                    "type": str(mtype)+'a',
                    "state":'ok',
                    'value':'',
                    'timeout':10
                })

    i = 1

    # create factory
    factory = MyClientFactory()
    # set factory protocol
    # factory.protocol = Modbus(PrintData)
    factory.protocol = Modbus(UpdateDB)

    for sds in sdsMods:
        reactor.callLater(factory.spendtime*i,_connect,sds['ip'],sds['port'],factory)
        i+=1
        for addr in range(addr_from,addr_to+1):
            mod = SIPAIModule(address=addr)
            cmd = mod.cmd(SIPAIModule.CMD_READTYPE)
            reactor.callLater(factory.spendtime*i, foo,cmd)
            i+=1


    reactor.callLater(factory.spendtime*i+1, DisconnectAll)

    reactor.callLater(factory.spendtime*i+2, reactor.stop)

    reactor.run()


#------------------------------------------------------------
#   Scan ElecMeter funcion
# -----------------------------------------------------------
def ScanElecMeters(addr_from='000013059740', addr_to='000013059895'):
    ''' Scan Sipai Modules funcion '''

    import struct, socket
    from ussop.elec_meter import MODTYPES
    from ussop.elec_meter import ElecMeterBase as ElecMeter

    from zhyDB import ZhyDB

    print "I am Zoro! I am scanning Elec Meters!!!"

    zhy = ZhyDB()
    sdsMods = zhy.readSdsMods()

    def foo(_factory, cmd):
        print '==> Output command:',b2a_hex(cmd)
        _factory.protocol.SendCmd(cmd)


    def _connect(ip,port,_factory):
        # reactor connect host with factory
        reactor.connectTCP(ip, int(port), _factory)        

    def UpdateDB(maddr, naddr, data):

        print maddr, naddr[0], naddr[1], data
        _host,_port = naddr[0], naddr[1]
        
        if zhy.findElecMeters(ip=_host,port=_port,addr=maddr) == 0:
            print '==> Add New Elec Meter:', maddr, naddr, data

            for _type in MODTYPES:
                zhy.newElecMeter({
                    "addr": str(maddr),
                    "ctrlbox": "",
                    "ip": _host,
                    "manufacturer": "DAHUA" ,
                    "port": str(_port),
                    "position": "",
                    "type": _type,
                    "state":'ok',
                    'value':'',
                    'timeout':10
                    })


    i = 1
    SPENDTIME = 0.3
    # Create factorys
    factorys = []
    for sds in sdsMods:
        factory = MyClientFactory(reConnectMode=False)
        factory.protocol = ElecMeterProtocol(UpdateDB)
        factorys.append(factory)
        factory.spendtime = SPENDTIME
        reactor.callLater(0,_connect,sds['ip'],sds['port'],factory)
        


    # # create factory
    # factory = MyClientFactory()
    # # set factory protocol
    # # factory.protocol = ElecMeterProtocol(PrintData)
    # factory.protocol = ElecMeterProtocol(UpdateDB)
    # factory.spendtime = 0.3

    # for sds in sdsMods:
    #     reactor.callLater(factory.spendtime*i,_connect,sds['ip'],sds['port'],factory)
    #     i+=1
    #     for addr in range(int(addr_from),int(addr_to+1)):
    #         mod = ElecMeter(addr='%012d'%addr)
    #         cmd = mod.readaddr()
    #         reactor.callLater(factory.spendtime*i, foo,cmd)
    #         i+=1


    # reactor.callLater(factory.spendtime*i,_connect,'130.139.200.57','10002',factory)
    # i+=1
    # for addr in range(int(addr_from),int(addr_to+1)):
    #     mod = ElecMeter(addr='%012d'%addr)
    #     cmd = mod.readaddr()
    #     reactor.callLater(factory.spendtime*i, foo,cmd)
    #     i+=1

    for addr in range(int(addr_from),int(addr_to+1)):
        mod = ElecMeter(addr='%012d'%addr)
        cmd=mod.readaddr()
        for factory in factorys:
            reactor.callLater(factory.spendtime*i, foo, factory, cmd)

        i+=1

    # reactor.callLater(factory.spendtime*i,_connect,'130.139.200.55','10002',factory)
    # i+=1
    # mod = ElecMeter(addr='000013036855')
    # cmd = mod.readCurrent()
    # # for factory in factorys:
    # #     reactor.callLater(factory.spendtime*i, foo, factory, cmd)
    # reactor.callLater(factory.spendtime*i, foo, factory, cmd)

    # reactor.callLater(factory.spendtime*i+1, DisconnectAll)

    reactor.callLater(SPENDTIME*i+2, reactor.stop)

    reactor.run()


#------------------------------------------------------------
#   Scan TempMeter funcion
# -----------------------------------------------------------
def ScanTempMeters(addr_from='000013059740', addr_to='000013059895'):
    ''' Scan Temp Modules funcion '''

    import struct, socket
    from ussop.temp_meter import MODTYPES
    from ussop.temp_meter import Repeater

    from zhyDB import ZhyDB

    print "I am Zoro! I am scanning Temp Meters!!!"

    zhy = ZhyDB()
    sdsMods = zhy.readSdsMods()


    def foo(_factory, cmd):
        print '==> Output command:',b2a_hex(cmd)
        _factory.protocol.SendCmd(cmd)


    def _connect(ip,port,_factory):
        # reactor connect host with factory
        reactor.connectTCP(ip, int(port), _factory)        

    def UpdateDB(maddr, naddr, data):

        print maddr, naddr[0], naddr[1], data
        _host,_port = naddr[0], naddr[1]
        
        if zhy.findTempMeters(ip=_host,port=_port,addr=maddr) == 0:
            print '==> Add New Temp Meter:', maddr, naddr, data

            for _type in MODTYPES:
                zhy.newElecMeter({
                    "addr": str(maddr),
                    "ctrlbox": "",
                    "ip": _host,
                    "manufacturer": "TEMP" ,
                    "port": str(_port),
                    "position": "",
                    "type": _type,
                    "state":'ok',
                    'value':'',
                    'timeout':10
                    })

    def PrintData(maddr, naddr, data):

        _rp = Repeater()
        mount = _rp.realdata(data)

        print '==> From Temp Repeater:', maddr, naddr[0], naddr[1], mount
        _host,_port = naddr[0], naddr[1]

        zhy.updateTempRepeaterResult(ip=_host,port=_port,addr=maddr, value=mount['pointer'])



    i = 1
    SPENDTIME = 0.3

    # create factory
    factory = MyClientFactory()
    # set factory protocol
    factory.protocol = TempRepeaterProtocol(PrintData)
    # factory.protocol = TempMeterProtocol(UpdateDB)
    factory.spendtime = 0.3


    # reactor.callLater(factory.spendtime,_connect,'130.139.200.48','10001',factory)
    # i+=1
    # for addr in range(int(addr_from),int(addr_to+1)):
    #     mod = ElecMeter(addr='%012d'%addr)
    #     cmd = mod.readaddr()
    #     reactor.callLater(factory.spendtime*i, foo,cmd)
    #     i+=1

    # for addr in range(int(addr_from),int(addr_to+1)):
    #     mod = Repeater(addr='%012d'%addr)
    #     cmd = mod.readRecordMount()
    #     for factory in factorys:
    #         reactor.callLater(factory.spendtime*i, foo, factory, cmd)

    #     i+=1

    reactor.callLater(factory.spendtime*i,_connect,'130.139.200.48','10001',factory)
    i+=1
    mod = Repeater(addr='000000000108')
    cmd = mod.readRecordMount()
    # for factory in factorys:
    #     reactor.callLater(factory.spendtime*i, foo, factory, cmd)
    reactor.callLater(factory.spendtime*i, foo, factory, cmd)
    

    # reactor.callLater(factory.spendtime*i+1, DisconnectAll)

    reactor.callLater(SPENDTIME*i+2, reactor.stop)

    reactor.run()


def Test():
    print "I am Zoro!"
    import sys
    print sys.modules['twisted.internet.reactor']

#    # create factory
    # factory1 = MyClientFactory()
#    # set factory protocol
    # factory1.protocol = Modbus(PrintData)
#    # reactor connect host with factory
    # reactor.connectTCP("130.139.200.50", 6020, factory1)

    # create factory
    factory2 = MyClientFactory()
    # set factory protocol
    factory2.protocol = Modbus(PrintData)
    # reactor connect host with factory
    reactor.connectTCP("130.139.200.50", 6020, factory2)


#    # create factory
#    factory3 = ModbusClientFactory()
#    # set factory protocol
#    factory3.protocol = Modbus(PrintData)
#    # reactor connect host with factory
#    reactor.connectTCP("192.168.192.102", 6021, factory3)

#    # create factory
    # factory4 = MyClientFactory(True)
#    # set factory protocol
    # factory4.protocol = ElecMeterProtocol(ReceiveData)
#    # reactor connect host with factory
##    point = TCP4ClientEndpoint(reactor, "192.168.192.100", 6021)
##    point.connect(factory4)
#    reactor.connectTCP("192.168.192.100", 6020, factory4)
#
#    cmd = '\x68\xaa\xaa\xaa\xaa\xaa\xaa\x68\x01\x02\x65\xf3\x27\x16'
#    print cmd
#    reactor.callLater(0.1, factory4.protocol.SendCmd, cmd)



    # reactor.callLater(0.1, factory2.protocol.SendCmd, 40, '\x2b\x0e\x01\x2b\x2b')
    cmd = '\x28\x2b\x0e\x01'
    _crc = crc16.calcString(cmd,crc16.INITIAL_MODBUS)
    _crc_H = chr((_crc & 0xff00) >> 8)
    _crc_L = chr(_crc & 0xff)
    cmd = cmd+_crc_L+_crc_H
    print b2a_hex(cmd)
    reactor.callLater(0.1, factory2.protocol.SendCmd, cmd)
#    reactor.callLater(0.1, factory4.protocol.SendCmd, 10, '\x2b\x0e\x01\x2b\x2b')
#    reactor.callLater(0.6, factory.protocol.SendCmd, 3, '\x2b\x0e\x01\x2b\x2b')
#    reactor.callLater(0.7, factory.protocol.SendCmd, 4, '\x2b\x0e\x01\x2b\x2b')

#    reactor.callLater(1, factory.stopFactory)
#    reactor.callLater(1, DelFactory, factory)

    reactor.callLater(1.5, DisconnectAll)

    reactor.callLater(2, reactor.stop)


    reactor.run()



if __name__ == "__main__":
    import readline

    helpdoc = '''
    Please input the argvs:
    1. python Zoro.py scansds
    2. python Zoro.py scansipai 10 45
    3. python Zoro.py listsipai
    4. python Zoro.py removesipai
    5. python Zoro.py scanelec
    6. python Zoro.py listelecmeter
    7. python Zoro.py removelec
    8. python Zoro.py scantemp

    '''    
    if len(sys.argv) < 2:
        print helpdoc
        y = raw_input("Function Choice:")
        # scansds
        if y=='1':
            print " <- Scan Serial Device Server ->"
            _ip_from=raw_input("IP From(%s):"%SDSIPFrom)
            if _ip_from == "": _ip_from = SDSIPFrom
            print _ip_from
            _ip_to=raw_input("IP To(%s):"%SDSIPEnd)
            if _ip_to == "": _ip_to = SDSIPEnd
            print _ip_to
            _port1=raw_input("Port1(%d):"%SDSPort1)
            if _port1 == "": _port1=SDSPort1
            print _port1
            _port2=raw_input("Port2(%d):"%SDSPort2)
            if _port2 == "": _port2=SDSPort2
            print _port2

            ScanSDS(ip_from=_ip_from, ip_to=_ip_to,port=(int(_port1),int(_port2)))

        # scansipai
        elif y=='2':
            print " <- Scan Sipai Modules -> "
            _addr_from = raw_input("Address from(10):")
            if _addr_from == "": _addr_from = '10'
            print _addr_from
            _addr_to = raw_input("Address to(50):")
            if _addr_to == "": _addr_to = '50'
            print _addr_to

            try:
                ScanSipaiMods(int(_addr_from),int(_addr_to))
            except:
                print "ERROR"

        elif y=='3':
            from zhyDB import ZhyDB
            zhy = ZhyDB()
            y = raw_input('All the Serial Device Server?(y/n)')
            if y == "n":
                sipaiModDict = zhy.listSipaiMods(None)
            else:
                sipaiModDict = zhy.listSipaiMods()            
            # print sipaiModDict
            keys = sipaiModDict.keys()
            keys.sort()
            print "======================================================"
            count=0
            for key in keys:
                count+=len(sipaiModDict[key])
                print key,len(sipaiModDict[key]),':',sipaiModDict[key]
            print "======================================================"
            print "===================== Total: %04d ===================="%count            
        
        elif y=='4':
            from zhyDB import ZhyDB
            zhy = ZhyDB()
            sipaiModDict = zhy.listSipaiMods()
            print "======================================================"
            count=0
            for key in sipaiModDict:
                count+=len(sipaiModDict[key])
            if count>0:
                y=raw_input("========= Are you SURE to DELETE ALL the %04d SIPAI Modules? ========:(y/n)"%count)
                if y=='y':
                    zhy.removeSipaiMods()
                    print '========== %04d SIPAI Modules Deleted! ========='%count
            else:
                print ' ========== There is no SIPAI Modules in Database! ========='

        # scan electro meters
        elif y=='5':
            from zhyDB import ZhyDB
            zhy = ZhyDB()

            print '<========== Scan ElecMeter ===========>'
            _addr_from = raw_input("Address from(000013059740):")
            if _addr_from == "": _addr_from = '000013059740'
            print _addr_from
            _addr_to = raw_input("Address to(%012d):"%(int(_addr_from)))
            if _addr_to == "": _addr_to = _addr_from
            print _addr_to
            try:
                ScanElecMeters(int(_addr_from),int(_addr_to))
            except Exception,ex:
                print Exception,":",ex

        elif y=='6':
            from zhyDB import ZhyDB
            zhy = ZhyDB()
            y = raw_input('All the Serial Device Server?(y/n)')
            if y == "n":
                elecMeterDict = zhy.listElecMeters(None,allMods=False)
            else:
                elecMeterDict = zhy.listElecMeters(allMods=False)            
            # print elecMeterDict
            keys = elecMeterDict.keys()
            keys.sort()
            print "======================================================"
            count=0
            for key in keys:
                count+=len(elecMeterDict[key])
                print key,len(elecMeterDict[key]),':',elecMeterDict[key]
            print "======================================================"
            print "===================== Total: %04d ===================="%count    

        elif y=='7':
            from zhyDB import ZhyDB
            zhy = ZhyDB()
            ElecMeterDict = zhy.listElecMeters()
            print "======================================================"
            count=0
            for key in ElecMeterDict:
                count+=len(ElecMeterDict[key])
            if count>0:
                y=raw_input("========= Are you SURE to DELETE ALL the %04d ElecMeters? ========:(y/n)"%count)
                if y=='y':
                    zhy.removeElecMeters()
                    print '========== %04d ElecMeters Deleted! ========='%count
            else:
                print "========= There is no ElecMeter in Database! =========="

        # scan temp meters
        elif y=='8':
            from zhyDB import ZhyDB
            zhy = ZhyDB()

            print '<========== Scan TempMeter ===========>'
            try:
                ScanTempMeters()
            except Exception,ex:
                print Exception,":",ex

        sys.exit(1)
    elif sys.argv[1] == "scansds":
        if len(sys.argv)==2:
            ScanSDS(ip_from='130.139.200.48',ip_to='130.139.200.49',port=(10001,10002))
            # sys.exit(1)
        elif len(sys.argv)==6:
            try:
                ScanSDS(ip_from=sys.argv[2],ip_to=sys.argv[3],port=(sys.argv[4],sys.argv[5]))
            except:
                print helpdoc
                sys.exit(1)
        else:
            print helpdoc
            sys.exit(1)
    elif sys.argv[1] == 'scansipai':
        if len(sys.argv) == 2:
            ScanSipaiMods(10,50)
            # sys.exit(1)
        elif len(sys.argv) == 4:
            try:
                ScanSipaiMods(int(sys.argv[2]),int(sys.argv[3]))
            except:
                print helpdoc
                sys.exit(1)
        else:
            print helpdoc
            sys.exit(1)
    elif sys.argv[1]=='listsipai':
        if len(sys.argv)==2:
            from zhyDB import ZhyDB
            zhy = ZhyDB()
            sipaiModDict = zhy.listSipaiMods()

            # print sipaiModDict
            keys = sipaiModDict.keys()
            keys.sort()
            print "======================================================"
            count=0
            for key in keys:
                count+=len(sipaiModDict[key])
                print key,len(sipaiModDict[key]),':',sipaiModDict[key]
            print "======================================================"
            print "===================== Total: %04d ===================="%count
        else:
            print helpdoc
            sys.exit(1)
    elif sys.argv[1]=='removesipai':
        if len(sys.argv)==2:
            from zhyDB import ZhyDB
            zhy = ZhyDB()
            sipaiModDict = zhy.listSipaiMods()
            print "======================================================"
            count=0
            for key in sipaiModDict:
                count+=len(sipaiModDict[key])
            y=raw_input("========= Are you SURE to DELETE ALL the %04d SIPAI Modules? ========:(y/n)"%count)
            if y=='y':
                zhy.removeSipaiMods()
                print '========== %04d SIPAI Modules Deleted! ========='%count
        else:
            print helpdoc
            sys.exit(1)            
    else:
        print helpdoc
        sys.exit(1)
        
    # Test()
    sys.exit(1)


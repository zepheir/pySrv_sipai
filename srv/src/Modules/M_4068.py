#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2012-10-24

@author: zepheir

version: 0.1
'''
from binascii import b2a_hex
from struct import pack, unpack
from ModbusDriver import BaseModbus
from BaseModuleDriver import BaseModuleDriver
from time import sleep


#================================================================================
# ADAM 4017+ Module
#================================================================================
class Module_4068(BaseModuleDriver):
    '''
    Moudle of Adam 4068
    '''

    def __init__(self, sokt, M_addr=0, addr=('', 4001)):

        self.host, self.port = addr
        self.addr = chr(M_addr)
        self.sokt = sokt

        BaseModuleDriver.__init__(self, self.sokt, addr)

    def readData(self):

        _cmd = self.addr + '\x01\x00\x16\x00\x01' #

        self.SendCmd(_cmd, crcflag=True)
        sleep(0.2)
        _recv = self.ReadData()
        if _recv:
            if len(_recv) > 3 and _recv[1] == '\x01':
                print b2a_hex(_recv)
                return unpack('!B', _recv[3:4])

    def setRelay(self, ch=0):
        _ch = pack('!B', ch + 16)
        _cmd = self.addr + '\x05\x00' + _ch + '\xff\x00' #

        self.SendCmd(_cmd, crcflag=True)
        sleep(0.1)
        _recv = self.ReadData()

    def clearRelay(self, ch=0):
        _ch = pack('!B', ch + 16)
        _cmd = self.addr + '\x05\x00' + _ch + '\x00\x00' #

        self.SendCmd(_cmd, crcflag=True)
        sleep(0.1)
        _recv = self.ReadData()

def Test():
    DMP_Address = ('192.168.192.100', 6021)
    ss1 = BaseModbus(DMP_Address)

    m1 = Module_4068(ss1.socket, M_addr=3, addr=DMP_Address)
#    data = m1.readData()
#    print data
#    m1.clearRelay(0)
    m1.setRelay(0)
    sleep(5)
    m1.setRelay(1)
    sleep(5)
    m1.setRelay(2)
    sleep(5)
    m1.clearRelay(0)
    sleep(5)
    m1.clearRelay(1)
    sleep(5)
    m1.clearRelay(2)



if __name__ == "__main__":
    Test()

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
class Module_4017(BaseModuleDriver):
    '''
    Moudle of Adam 4017
    '''

    def __init__(self, sokt, M_addr=0, addr=('', 4001)):

        self.host, self.port = addr
        self.addr = chr(M_addr)
        self.sokt = sokt

        BaseModuleDriver.__init__(self, self.sokt, addr)

        self._result = object

    def readData(self):

        _cmd = self.addr + '\x03\x00\x00\x00\x08' #

        self.SendCmd(_cmd, crcflag=True)
        sleep(0.2)
        _recv = self.ReadData()
        if _recv:
            if len(_recv) > 3 and _recv[1] == '\x03':
                print b2a_hex(_recv)
                self._result = unpack('!HHHHHHHH', _recv[3:19])
                return self._result

    def transData2Temp(self, type=0, min=0, max=100):
        ''' type 0 : +/- 20mA '''
        if type == 0:
#            return tuple([round(min + (d - 0x9998) * (max - min) / 26214.0, 2)
            return tuple([round(min + (d - 0x3333) * (max - min) / 52428.0, 2)
                          for d in self._result])

def Test():
    DMP_Address = ('192.168.192.100', 6021)
    ss1 = BaseModbus(DMP_Address)

    m1 = Module_4017(ss1.socket, M_addr=2, addr=DMP_Address)
    data = m1.readData()
#    print data

    print m1.transData2Temp()



if __name__ == "__main__":
    Test()

# -*- coding: utf-8 -*-
'''
Created on 2011.3.30

@author: wan
'''
import socket
from binascii import b2a_hex
import crc16
import time

class BaseModuleDriver():
    ''' Base Module '''
#------------------------------------------------------------------------------ 
# Define the Module type
    MODULE_DI_PULSE = '1001'
    MODULE_DI = '1020'
    MODULE_DO = '1030'
    MODULE_AI_TEMP = '1040'
    MODULE_AI_ELECTRIC = '1041'
    MODULE_AI_STEAM = '1042'

#------------------------------------------------------------------------------ 
# Initial the Modbus
    def __init__(self, sokt, address):
        self.host, self.port = address
        self.sokt = sokt

#------------------------------------------------------------------------------ 
    def SendCmd(self, cmd, crcflag=False , _debug=False):
        if not _debug:
            if crcflag == True:
                __crc = crc16.calcString(cmd, crc16.INITIAL_MODBUS)
                __crc_H = chr((__crc & 0xff00) >> 8)
                __crc_L = chr(__crc & 0xff)
                try:
                    _cmd = cmd + __crc_L + __crc_H
                    print 'Send Command:', b2a_hex(_cmd)
                    self.sokt.send(_cmd)

                except socket.error, e:
                    print 'Socket Error: %s' % e
            else:
                try:
                    self.sokt.send(cmd + '\x00\x00')
                except socket.error, e:
                    print 'Socket Error: %s' % e
        else:
            print b2a_hex(cmd)

#------------------------------------------------------------------------------ 
    def ReadData(self , _debug=False):
        if not _debug:
            try:
                return self.sokt.recv(128)
            except socket.error, e:
                print 'Socket Error: %s' % e
                return None
        else:
            return None

    def SetAddress(self, addr , debug=False):
        ''' addr: The new module address. 
            It is a string of decimal such as '123'. '''
        cmd = self.addr + self.CMD_SET_ADDR + addr + chr(int(addr))
        self.SendCmd(cmd, crcflag=True , _debug=debug)

    def SetBand(self, BandLevel , debug=False):
        ''' Band Level is from 4 to 9.
            Default Band Level is 6.
            Band = {4:2400, 5:4800, 6:9600, 7:19200, 8:38400, 9:57600}
        '''
        if BandLevel > 3 and BandLevel <= 9:
            cmd = self.addr + self.CMD_SET_BAND + '\x00' + chr(BandLevel)
            self.SendCmd(cmd, crcflag=True , _debug=debug)
        else:
            #raise TypeError, 'BandLevel'
            print 'Band Level error!'

    def SendCmdReadAll(self , debug=False):
        cmd = self.addr + self.CMD_READ_ALL
        self.SendCmd(cmd, crcflag=True , _debug=debug)

    def ReadType(self, debug=False):
        cmd = self.addr + self.CMD_READ_TYPE
        self.SendCmd(cmd, crcflag=True , _debug=debug)
        time.sleep(0.2)
        data = self.ReadData(_debug=debug)
        if data:
            self.type = b2a_hex(data[3:5])
            return self.type


if __name__ == "__main__":
    pass

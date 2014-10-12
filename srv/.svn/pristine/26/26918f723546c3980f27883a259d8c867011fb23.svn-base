#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2012-10-28

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
class Module_ElecMeter(BaseModuleDriver):
    '''
    Moudle of ElecMeter
    
    '''
    # 标记
    CHAR_WAKEUP = '\xfe'
    CHAR_HEAD = '\x68'
    CHAR_END = '\x16'


    # 功能码 (只从主站考虑)
    READ_DATA = '\x01' #读数据
    READ_NEXTDATA = '\x02' #读后续数据
    READ_AGAIN = '\x03' #重读数据
    WRITE_DATA = '\x04' #写数据
    BROADCAST = '\x08' #广播校时
    WRITE_ADDRESS = '\x0a' #写设备地址
    CHANGE_BAUDRATE = '\x0c' #更改通信速率
    CHANGE_PASSWORD = '\x0f' #修改密码
    CLEAR_MAX_REQUIRE = '\x10' #最大需量清零


    #    当前正向有功功率总电能
    CMD_RD_ACTIVEPOWER_TOTAL = '\x68\x01\x02\x43\xc3'
#    当前正向有功功率尖
    CMD_RD_ACTIVEPOWER_FEE1 = '\x68\x01\x02\x44\xc3'
#    当前正向有功功率峰
    CMD_RD_ACTIVEPOWER_FEE2 = '\x68\x01\x02\x45\xc3'
#    当前正向有功功率平
    CMD_RD_ACTIVEPOWER_FEE3 = '\x68\x01\x02\x46\xc3'
#    当前正向有功功率谷
    CMD_RD_ACTIVEPOWER_FEE4 = '\x68\x01\x02\x47\xc3'
#    读取表号(地址)
    CMD_RD_ADDRESS = '\x68\x01\x02\x65\xf3'
#    读取电压: Ua Ub Uc
    CMD_RD_VOLTAGE = '\x68\x01\x02\x52\xE9'
#    读取电流: Ia Ib Ic
    CMD_RD_CURRENT = '\x68\x01\x02\x62\xE9'
#    读取瞬时有功功率: 瞬时有功功率 Pa Pb Pc 正向有功功率上限 反向有功功率上限
    CMD_RD_POWER_NOW = '\x68\x01\x02\x72\xE9'
#    读取无功功率: 瞬时无功功率 RPa RPb RPc
    CMD_RD_REACTIVEPOWER_NOW = '\x68\x01\x02\x82\xE9'
#    读取功率因素: 总功率因素 Ca Cb Cc
    CMD_RD_COS = '\x68\x01\x02\x92\xE9'



    def __init__(self, sokt, M_addr=u'000012046365', addr=('', 4001)):

        self.host, self.port = addr
        self.addr = M_addr
        self.sokt = sokt

        BaseModuleDriver.__init__(self, self.sokt, addr)

        self._result = object

    def realaddr(self):
        _addr = ''
        for i in range(0, len(self.addr), 2):
            _addr = chr(int(self.addr[i:i + 2], 16)) + _addr
#        _addr = pack('!BBBBBB', '000012046365')
#        print self.addr, b2a_hex(_addr)
        return _addr

    def cmd(self, cmd):
        cs = 0
#        cmd = self.CHAR_HEAD + self.address + cmd
        cmd = self.CHAR_HEAD + self.realaddr() + cmd
#        print 'cmd-command:', b2a_hex(cmd)
        for i in range(len(cmd)):
            cs = cs + int(b2a_hex(cmd[i]), 16)
        cs &= 0xff
        return  self.CHAR_WAKEUP + cmd + chr(cs) + self.CHAR_END

    def readaddr(self):
        return self.cmd(self.CMD_RD_ADDRESS)

    def readPower(self):
        return self.cmd(self.CMD_RD_ACTIVEPOWER_TOTAL)

    def readVoltage(self):
        return self.cmd(self.CMD_RD_VOLTAGE)

    def readCurrent(self):
        return self.cmd(self.CMD_RD_CURRENT)

    def readCos(self):
        return self.cmd(self.CMD_RD_COS)

    def readPowerNow(self):
        return self.cmd(self.CMD_RD_POWER_NOW)

    def readReactivePower(self):
        return self.cmd(self.CMD_RD_REACTIVEPOWER_NOW)

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

    def realdata(self, data):
        ''' 将字符串倒转 并减去 0x33 '''


        databytes = len(data)
        realdata = ''

        self.rawdata = data

        # 去除唤醒字节 FEH
        self.rawdata = self.rawdata.lstrip('\xfe')

        _position = self.rawdata.find('\x68\x81')

        if _position != -1:
            self.rawdata = self.rawdata[_position:]
#            print b2a_hex(self.rawdata)
            databytes = unpack('<B', self.rawdata[2])[0]
#            print 'databytes:', databytes, len(self.rawdata)
            if len(self.rawdata) - 5 == databytes:

                if self.rawdata[3:5] == self.CMD_RD_ACTIVEPOWER_TOTAL[-2:]:
                    for i in range(4):
                        x = int(b2a_hex(self.rawdata[5 + i]), 16) - 0x33
                        realdata = chr(x) + realdata

                    return round(int(b2a_hex(realdata)) / 100.0, 2)
                # 电压
                elif self.rawdata[3:5] == self.CMD_RD_VOLTAGE[-2:]:
                    realdata = ''
                    for i in range(6):
                        x = int(b2a_hex(self.rawdata[5 + i]), 16) - 0x33
                        realdata = chr(x) + realdata
                    return round(
                                 (int(b2a_hex(realdata[0:2])) +
                                  int(b2a_hex(realdata[2:4])) +
                                  int(b2a_hex(realdata[4:6]))) * 1.732 / 3, 2)
                # 电流
                elif self.rawdata[3:5] == self.CMD_RD_CURRENT[-2:]:
                    realdata = ''
                    for i in range(6):
                        x = int(b2a_hex(self.rawdata[5 + i]), 16) - 0x33
                        realdata = chr(x) + realdata
                    return (round(int(b2a_hex(realdata[4:6])) / 100.0, 2),
                            round(int(b2a_hex(realdata[2:4])) / 100.0, 2),
                            round(int(b2a_hex(realdata[0:2])) / 100.0, 2)
                            )
                # 瞬时功率
                elif self.rawdata[3:5] == self.CMD_RD_POWER_NOW[-2:]:
                    realdata = ''
                    for i in range(3):
                        x = int(b2a_hex(self.rawdata[5 + i]), 16) - 0x33
                        realdata = chr(x) + realdata
#                    print b2a_hex(realdata)
                    return round(int(b2a_hex(realdata[0:3])) / 10000.0, 2)
#                    return self.rawdata[5:12]
                elif self.rawdata[3:5] == self.CMD_RD_REACTIVEPOWER_NOW[-2:]:
                    return self.rawdata[5:6]
                elif self.rawdata[3:5] == self.CMD_RD_COS[-2:]:
                    return self.rawdata[5:6]
                else:
                    return False
        else:
            return False



def Test():
    DMP_Address = ('130.139.200.55', 10002)
    ss1 = BaseModbus(DMP_Address)

    m1 = Module_ElecMeter(ss1.socket, M_addr=u'000013036855', addr=DMP_Address)

#    print b2a_hex(m1.readVoltage())
    m1.SendCmd(m1.readVoltage(), crcflag=False, _debug=False)
    sleep(0.5)
    result = m1.ReadData()
    print m1.realdata(result)

    m1.SendCmd(m1.readCurrent())
    sleep(0.5)
    result = m1.ReadData()
    print m1.realdata(result)


    m1.SendCmd(m1.readPowerNow())
    sleep(0.5)
    data = m1.ReadData()
    print m1.realdata(data)


    m1.SendCmd(m1.readPower())
    sleep(0.5)
    data = m1.ReadData()
    print m1.realdata(data)


if __name__ == "__main__":
    Test()

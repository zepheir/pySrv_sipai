# -*- coding: utf-8 -*-
'''
Created on 2012-7-18

@author: Administrator
'''
from binascii import b2a_hex
from struct import pack, unpack
from ModbusDriver import BaseModbus
from BaseModuleDriver import BaseModuleDriver
from time import clock, sleep


#================================================================================
# VF100 变频器
#================================================================================
class Module_VF100(BaseModuleDriver):
    ''' Module for VF100 '''

    def __init__(self, sokt, M_addr=0, addr=('', 4001)):

        self.host, self.port = addr
        self.addr = chr(M_addr)
        self.sokt = sokt

        BaseModuleDriver.__init__(self, self.sokt, addr)


    def setFreq(self, freq=50):

        _f = min(max(int(freq), 50), 5000)

        _cmd = self.addr + '\x06\x00\xed' + pack('!h', _f)

        self.SendCmd(_cmd, crcflag=True)

        sleep(0.2)

        _recv = self.ReadData()


    def setRunON(self):
        _cmd = self.addr + '\x05\x0f\xa0\xff\x00' # 输入运行状态 R250-0

        self.SendCmd(_cmd, crcflag=True)

        sleep(0.2)

        _recv = self.ReadData()


    def setRunOFF(self):
        _cmd = self.addr + '\x05\x0f\xa0\x00\x00' # 输入运行状态 R250-0

        self.SendCmd(_cmd, crcflag=True)

        sleep(0.2)

        _recv = self.ReadData()

    def readMotorU(self):
        _cmd = self.addr + '\x03\x01\x2f\x00\x01' # 读取电压

        self.SendCmd(_cmd, crcflag=True)

        sleep(0.3)

        _recv = self.ReadData()

        if _recv:
            if len(_recv) > 3 and _recv[1] == '\x03':
                return unpack('!h', _recv[3:5])

    def readMotorI(self):
        _cmd = self.addr + '\x03\x01\x2e\x00\x01' # 读取电流

        self.SendCmd(_cmd, crcflag=True)

        sleep(0.3)

        _recv = self.ReadData()

        if _recv:
            if len(_recv) > 3 and _recv[1] == '\x03':
                return unpack('!h', _recv[3:5])

    def readMotorData(self):
        _cmd = self.addr + '\x03\x01\x2d\x00\x04' # 读取频率,电流,电压,内部直流电压

        self.SendCmd(_cmd, crcflag=True)

        sleep(0.1)

        _recv = self.ReadData()

        if _recv:
            if len(_recv) > 3 and _recv[1] == '\x03':
#                print b2a_hex(_recv)
                ll = unpack('!B', _recv[2])[0]
                return unpack('!%s' % ('h' * (ll / 2)), _recv[3:3 + ll])

        return 0, 0, 0, 0,




#================================================================================
# Test the function
#================================================================================
def testfunction():
    ''''''

    DMP_Address = ('192.168.192.100', 6021)
#    a_tuple = (1, 2, 3, 4, 5, 6, 7, 8)
#------------------------------------------------------------------------------ 
    ss1 = BaseModbus(DMP_Address)

    module1 = Module_VF100(ss1.socket, M_addr=6, addr=DMP_Address)
    clk1 = clock()

#    cmd = module1.addr + '\x06\x00\xed\x00\x32' # 频率设定寄存器 DT237 0050
#    cmd = module1.addr + '\x06\x00\xed\x03\xe8' # 频率设定寄存器 DT237 1000
#    cmd = module1.addr + '\x06\x00\xed\x07\xd0' # 频率设定寄存器 DT237 2000
#    cmd = module1.addr + '\x06\x00\xed\x09\xc4' # 频率设定寄存器 DT237 2500
#    cmd = module1.addr + '\x06\x00\xed\x13\x88' # 频率设定寄存器 DT237 5000
#    cmd = module1.addr + '\x03\x01\x31\x00\x01' # 读取设定频率 DT305
#    cmd = module1.addr + '\x01\x13\x70\x00\x01' # 读取运行状态 R311-0
#    cmd = module1.addr + '\x03\x01\x37\x00\x01' # 读取运行状态 R311
#    cmd = module1.addr + '\x05\x0f\xa0\x00\x00' # 输入运行状态 R250-0
#    module1.SendCmd(cmd, crcflag=True)

    module1.setFreq(freq=3000)
#    print module1.readMotorData()

#    module1.setRunOFF()
    module1.setRunON()

#    sleep(0.5)

#    recv = module1.ReadData()
#    print b2a_hex(recv)

    clk5 = clock()
    print clk5 - clk1

#------------------------------------------------------------------------------ 
#    ss1.Close()

if __name__ == '__main__':
    testfunction()

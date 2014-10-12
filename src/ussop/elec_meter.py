#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2011-10-21

Modify_1: 2012.7.27 加强垃圾清理 self.rawdata=''

引用规约: <DL/T645-1997通讯规约>

适用范围: 该通信规约适用于本地系统中多功能表的费率装置与手持单元（HHU）
         或其它数据终端设备进行点对点的或一主多从的数据交换方式，
         规定了它们之间的物理连接、通信链路及应用技术规范。
         
<DL/T645-1997通讯规约>引用标准:
GB/T3454-1994    数据通信基本型控制规程
GB/T9387-1995    信息处理系统  开放系统互连   基本参考模型
DL/T614-1997     多功能电能表
IEC1107-1996     读表、费率和负荷控制的数据交换---直接本地数据交换
IEC1142--1993    读表、费率和负荷控制的数据交换---本地总线数据交换
ITU-TV.24-1993   非平衡双流接口电路的点特性
ITU-TV.28-1993   数据终端设备（DTE）和数据电路终接设备（DCE）之间的接口电路定义表
         
字节格式:
起始位 数据 偶校验位 停止位
  1     8     1      1
  
帧格式:
-起始符:    68H
-地址域:    A0~A5(6字节, 每字节2位BCD码, 不足6字节时用AAH代替. 出厂时为表号.)
-起始符:    68H
-控制码:    C-D7:传送方向,0主站发出命令,1从站发出应答
            -D6:从站异常标志,1为从站异常
            -D5:后继标志,1为有后继数据
            -D4~D0:功能码
                   00000：保留
                   00001：读数据
                   00010：读后续数据
                   00011：重读数据
                   00100：写数据
                   01000：广播校时
                   01010：写设备地址
                   01100：更改通信速率
                   01111：修改密码
                   10000：最大需量清零

-数据长度:  L (读数据时L≤200,写数据时L≤50,L=0 表示无数据域)
-数据:      DATA (传输时发送方按字节进行加33H处理,接收方按字节进行减33H处理)
-校验码:    CS (从帧起始符开始到校验码之前的所有各字节的模256的和,即各字节二进制算术和,不计超过256的溢出值)
-结束符:    16H

传输:
-前导字节: FEH, 以唤醒接收方
-传输次序: 数据先低后高
-传输响应: 收到命令帧后的响应延时Td:20ms≤Td≤500ms, 字节之间停顿时间Tb:Tb≤500ms.
-传送速率: 初始:1200bps, 标准: 300,600,1200,2400,4800,9600

数据标识: DI1 DI0
DI1h:1001   电能量
     1010   最大需量
     1011   变量
     1100   参变量
     1101   负荷曲线
     1110   厂家功能扩展
     1111   保留

DI1l:00 当前     00 有功
     01 上月     01 无功
     10 上上月   10 保留
     11 集合     11 集合
     
DI0:0001 正向电能        0000 总电能
    0010 反向电能        0001 费率1
    0011 一象限无功      0010 费率2
    0100 四象限无功      0011 费率3
    0101 二象限无功      0100 费率4
    0110 三象限无功      0101∽1110 保留
    0111∽1110 保留      1111本数据块集合
    1111 集合

   
@author: zepheir
'''

import device

import socket
from binascii import b2a_hex
from struct import unpack,pack
import time

MODTYPES = 'power','voltage','current','cos','reactive','total'


class ElecMeterBase(object):
    """docstring for ElecMeterBase"""

    TYPE = 'EL_MTR'

    # 标记
    CHAR_WAKEUP = '\xfe'*4
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

    CMD_READDATA = CMD_RD_ADDRESS

    def __init__(self, addr='999999999999'):
        super(ElecMeterBase, self).__init__()
        self.addr = '%012d'%int(addr)

        # initial the result
        self.resultstring = ''


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


    def readdata(self):
        return self.cmd(self.CMD_READDATA)

    def realdata(self, data):
        ''' 将字符串倒转 并减去 0x33 '''
        return data

    def exchanger(self, data):
        databyte = len(data)
        newdata = ''
        for i in range(databyte):
#            newdata = newdata + chr(int(b2a_hex(data[i]), 16) - 0x33)
            newdata = newdata + chr((unpack('B', data[i])[0] - 0x33)&0xff)
        return newdata


    def realaddr(self):
        _addr = ''
        for i in range(0, len(self.addr), 2):
            _addr = chr(int(self.addr[i:i + 2], 16)) + _addr
#        print b2a_hex(_addr)
        return _addr


    def dealdata(self, data):
        ''''''

#        print 'data received', data

        self.data = self.realdata(data)

#        self.resultstring = '%.2f' % (int(data[0]) / 100.0)

        return self.data


class ElecMeterTotal(ElecMeterBase):
    """docstring for ElecMeterCurrent"""

    TYPE = 'total'

#    当前正向有功功率总电能
    CMD_READDATA = ElecMeterBase.CMD_RD_ACTIVEPOWER_TOTAL

    def __init__(self, addr='999999999999'):
        super(ElecMeterTotal, self).__init__(addr)
        
    def realdata(self, data):
        ''' 将字符串倒转 并减去 0x33 '''
        databytes = len(data)
        realdata = ''

        self.rawdata = data

        if self.rawdata[10:12] == self.CMD_READDATA[-2:]:
            return '%.2f'%(int(b2a_hex(self.exchanger(self.rawdata[12:16])[::-1])) * 0.01,)
        else:
            return ''    



class ElecMeterCurrent(ElecMeterBase):
    """docstring for ElecMeterCurrent"""

    TYPE = 'current'

#    读取电流: Ia Ib Ic
    CMD_READDATA = ElecMeterBase.CMD_RD_CURRENT

    def __init__(self, addr='999999999999'):
        super(ElecMeterCurrent, self).__init__(addr)
        
    def realdata(self, data):
        ''' 将字符串倒转 并减去 0x33 '''
        databytes = len(data)
        realdata = ''

        self.rawdata = data

        if self.rawdata[10:12] == self.CMD_READDATA[-2:]:
            _ia = int(b2a_hex(self.exchanger(self.rawdata[12:14])[::-1]))
            _ib = int(b2a_hex(self.exchanger(self.rawdata[14:16])[::-1]))
            _ic = int(b2a_hex(self.exchanger(self.rawdata[16:18])[::-1]))
            _i = _ia+_ib+_ic
            return '%.1f,%.1f,%.1f,%.1f,%.1f'%(_i*0.01, _ia*0.01, _ib*0.01, _ic*0.01, _i*0.01/3)
        else:
            return ''


class ElecMeterVoltage(ElecMeterBase):
    """docstring for ElecMeterVoltage"""

    TYPE = 'voltage'

#    读取电流: Ia Ib Ic
    CMD_READDATA = ElecMeterBase.CMD_RD_VOLTAGE

    def __init__(self, addr='999999999999'):
        super(ElecMeterVoltage, self).__init__(addr)
        
    def realdata(self, data):
        ''' 将字符串倒转 并减去 0x33 '''
        databytes = len(data)
        realdata = ''

        self.rawdata = data

        if self.rawdata[10:12] == self.CMD_READDATA[-2:]:
            _va = int(b2a_hex(self.exchanger(self.rawdata[12:14])[::-1]))
            _vb = int(b2a_hex(self.exchanger(self.rawdata[14:16])[::-1]))
            _vc = int(b2a_hex(self.exchanger(self.rawdata[16:18])[::-1]))
            _v = (_va+_vb+_vc)/3
            return '%.3f,%.3f,%.3f,%.3f'%(_v, _va, _vb, _vc)
        else:
            return ''


class ElecMeterCos(ElecMeterBase):
    """docstring for ElecMeterCos"""

    TYPE = 'cos'

    # Read COSa COSb COSc
    CMD_READDATA = ElecMeterBase.CMD_RD_COS

    def __init__(self, addr='999999999999'):
        super(ElecMeterCos, self).__init__(addr)
        
    def realdata(self, data):
        ''' 将字符串倒转 并减去 0x33 '''
        databytes = len(data)
        realdata = ''

        self.rawdata = data

        if self.rawdata[10:12] == self.CMD_READDATA[-2:]:
            _p  = int(b2a_hex(self.exchanger(self.rawdata[12:14])[::-1])) * 0.001
            _pa = int(b2a_hex(self.exchanger(self.rawdata[14:16])[::-1])) * 0.001
            _pb = int(b2a_hex(self.exchanger(self.rawdata[16:18])[::-1])) * 0.001
            _pc = int(b2a_hex(self.exchanger(self.rawdata[18:20])[::-1])) * 0.001

            return '%.3f,%.3f,%.3f,%.3f'%(_p, _pa, _pb, _pc)
        else:
            return ''


class ElecMeterPower(ElecMeterBase):
    """docstring for ElecMeter Power Now """

    TYPE = 'power'

    # Read COSa COSb COSc
    CMD_READDATA = ElecMeterBase.CMD_RD_POWER_NOW

    def __init__(self, addr='999999999999'):
        super(ElecMeterPower, self).__init__(addr)
        
    def realdata(self, data):
        ''' 将字符串倒转 并减去 0x33 '''
        databytes = len(data)
        realdata = ''

        self.rawdata = data

        if self.rawdata[10:12] == self.CMD_READDATA[-2:]:
            _p  = int(b2a_hex(self.exchanger(self.rawdata[12:15])[::-1])) * 0.001
            _pa = int(b2a_hex(self.exchanger(self.rawdata[15:18])[::-1])) * 0.001
            _pb = int(b2a_hex(self.exchanger(self.rawdata[18:21])[::-1])) * 0.001
            _pc = int(b2a_hex(self.exchanger(self.rawdata[21:24])[::-1])) * 0.001

            return '%.3f,%.3f,%.3f,%.3f'%(_p, _pa, _pb, _pc)
        else:
            return ''


class ElecMeterReactivePower(ElecMeterBase):
    """docstring for ElecMeter ReactivePower Now """

    TYPE = 'reactive'

    # Read COSa COSb COSc
    CMD_READDATA = ElecMeterBase.CMD_RD_REACTIVEPOWER_NOW

    def __init__(self, addr='999999999999'):
        super(ElecMeterReactivePower, self).__init__(addr)
        
    def realdata(self, data):
        ''' 将字符串倒转 并减去 0x33 '''
        databytes = len(data)
        realdata = ''

        self.rawdata = data
            
        if self.rawdata[10:12] == self.CMD_READDATA[-2:]:
            _p  = int(b2a_hex(self.exchanger(self.rawdata[12:14])[::-1])) * 0.01
            _pa = int(b2a_hex(self.exchanger(self.rawdata[14:16])[::-1])) * 0.01
            _pb = int(b2a_hex(self.exchanger(self.rawdata[16:18])[::-1])) * 0.01
            _pc = int(b2a_hex(self.exchanger(self.rawdata[18:20])[::-1])) * 0.01

            return '%.1f,%.1f,%.1f,%.1f'%(_p, _pa, _pb, _pc)
        else:
            return ''


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------ 

class ElecMeter_220(ElecMeterBase):

    TYPE = '220'

    def __init__(self, addr='aaaaaaaaaaaa'):
        super(ElecMeter_220, self).__init__(addr)

    def realdata(self, data):
        ''' 将字符串倒转 并减去 0x33 '''
        databytes = len(data)
        realdata = ''

        self.rawdata = data



        if self.rawdata[10:12] == self.CMD_RD_ACTIVEPOWER_TOTAL[-2:]:
            for i in range(databytes):
                x = int(b2a_hex(self.rawdata[12 + i]), 16) - 0x33
                realdata = chr(x) + realdata
            return realdata
        elif self.rawdata[10:12] == self.CMD_RD_VOLTAGE[-2:]:
#            x = [chr(int(b2a_hex(self.rawdata[12 + i]), 16) - 0x33) for i in range(databytes - 1)]
#            return x[1] + x[0], x[3] + x[2], x[5] + x[4]
            return self.rawdata[12:14]
        elif self.rawdata[10:12] == self.CMD_RD_CURRENT[-2:]:
            return self.rawdata[12:14]
        elif self.rawdata[10:12] == self.CMD_RD_POWER_NOW[-2:]:
            return self.rawdata[12:15]
        elif self.rawdata[10:12] == self.CMD_RD_REACTIVEPOWER_NOW[-2:]:
            return self.rawdata[12:14]
        elif self.rawdata[10:12] == self.CMD_RD_COS[-2:]:
            return self.rawdata[12:14]
        else:
            return False

    def exchanger(self, data):
        databyte = len(data)
        for i in range(databyte):
            data[i] = data[i] - 0x33
        return b2a_hex(data)

def createEMTR(addr='aaaaaaaaaaaa', type='current'):
    ''' 创建 电表 接口'''
    
    if type == 'current':
        return ElecMeterCurrent(addr)
    elif type == 'voltage':
        return ElecMeterVoltage(addr)
    elif type == 'total':
        return ElecMeterTotal(addr)
    elif type == 'cos':
        return ElecMeterCos(addr)
    elif type == 'power':
        return ElecMeterPower(addr)
    elif type == 'reactive':
        return ElecMeterReactivePower(addr)
    else:
        return ElecMeterBase(addr)


def test():
    HOST = '130.139.200.60'
    PORT = 10002

    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.connect((HOST, PORT))
    except:
        print 'connection did not establish!'
    else:
        print 'connection established!'

    def readtest(CMD):

        try:
            print b2a_hex(CMD)
            ss.send(CMD)
            time.sleep(0.1)
        except:
            print 'send error'
            return ''
        else:
            data = ss.recv(1024)
            print 'data received', b2a_hex(data)

            # datalen = int(b2a_hex(data[9]), 16)
            # print "data length:", b2a_hex(data[9]),datalen
            # datac = data[12:(12 + datalen)]

            # realdata = ''
            # # for i in range(datalen):
            # #     print datac[i],b2a_hex(datac[i]),datac[i]-0x33
            # #     x = int(b2a_hex(datac[i]), 16) - 0x33
            # #     print "x:",x
            # #     realdata = chr(x) + realdata

            # print b2a_hex(datac)
            # _data = list(unpack('B'*len(datac),datac))
            # _data2 = [(x - 0x33)&0xff for x in _data]
            

            # print _data, _data2
            # for x in _data2:
            #     realdata += pack("B",x)
            # # realdata = pack('BBBBBBBBB',_data2[0],_data2[1],_data2[2],_data2[3],_data2[4],_data2[5],_data2[6],_data2[7],_data2[8])
            # # print b2a_hex(realdata)

            # realdata = 

            return  data


    # try:
    #     print b2a_hex(em1.readCurrent() )
    #     t1 = time.clock()
    #     ss.send(em1.readCurrent())
    #     time.sleep(5)
    # except:
    #     print 'send error'
    #     return ''
    # else:
    #     data = ss.recv(1024)

    #     print 'data received:()', (t2 - t1), b2a_hex(data)
    #     print 'real data', em1.realdata(data)

#    addr = readtest(em1.readdata(em1.CMD_RD_ADDRESS))
#    print 'address:', b2a_hex(addr)
#    _addr = ''
#    for i in range(0, len(addr)):
#        _addr = addr[i] + _addr
#    print u'颠倒address:', b2a_hex(_addr)
#
#    EM1 = ElecMeter(ss , _addr)
#    print int(b2a_hex(readtest(EM1.readdata(EM1.CMD_RD_ACTIVEPOWER_TOTAL)))) / 100.0
#    print int(b2a_hex(readtest(EM1.readdata(EM1.CMD_RD_ACTIVEPOWER_FEE1)))) / 100.0
#    print int(b2a_hex(readtest(EM1.readdata(EM1.CMD_RD_ACTIVEPOWER_FEE2)))) / 100.0
#    print int(b2a_hex(readtest(EM1.readdata(EM1.CMD_RD_ACTIVEPOWER_FEE3)))) / 100.0
#    print int(b2a_hex(readtest(EM1.readdata(EM1.CMD_RD_ACTIVEPOWER_FEE4)))) / 100.0

    print "---------------------------------------"

    ems = [createEMTR('000013059750', _t) for _t in MODTYPES]

    for em in ems:
        data = readtest(em.readdata())
        print b2a_hex(data)
        em.dealdata(data)
        print em.data



    try:
        ss.close()
    except:
        print 'connection closed error!'
    else:
        print 'connection closed!'

    pass



if __name__ == '__main__':
    test()

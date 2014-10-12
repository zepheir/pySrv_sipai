#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2014.3.16

        
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
                   00100：写数据


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
D404: 指定传感器温度值
D406: 设置输出口状态
D405: 读取输入口状态
D40B: 读取模拟电压值

   
@author: zepheir
'''

import device

import socket
from binascii import b2a_hex, a2b_hex
from struct import unpack,pack
import time

MODTYPES = 'temp'


class TempMeterBase(object):
    """docstring for TempMeterBase"""

    TYPE = 'T_MTR'

    # 标记
    # CHAR_WAKEUP = '\xfe'*4
    CHAR_WAKEUP = ''
    CHAR_HEAD = '\x68'
    CHAR_END = '\x16'

    # 功能码 (只从主站考虑)
    READ_DATA = '\x01' #读数据
    WRITE_DATA = '\x04' #写数据


#    指定采集传感器温度值
    CMD_RD_SENSER_TEMP = '\x68\x01\x02\x37\x07'
    CMD_RD_SENSER_VOLTAGE = '\x68\x01\x02\x3e\x07'
    CMD_RD_SENSER_SEND_GAP = '\x68\x01\x02\x35\x07'

    CMD_READDATA = CMD_RD_SENSER_VOLTAGE


    def __init__(self, addr='999999999999'):
        super(TempMeterBase, self).__init__()
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

    def plus33(self, data):
        _data = '%08d'%(int(data)-1)
        # print '_data:',_data
        databyte = len(_data)
        newdata = ''
        # for i in range(databyte):
        #     print _data[i]
        #     newdata = newdata + chr((unpack('B', _data[i])[0]+0x33) & 0xff)
        newdata = chr((int(_data[6:8])+0x33)&0xff)+\
        chr((int(_data[4:6])+0x33)&0xff)+\
        chr((int(_data[2:4])+0x33)&0xff)+\
        chr((int(_data[0:2])+0x33)&0xff)
        # print 'newdata',newdata
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


class Repeater(TempMeterBase):
    """docstring for Repeater """

    TYPE = 'Repeater'

#    读取记录条数
    CMD_RD_REPEATER_RECORD_NUMBER = '\x68\x01\x02\x3a\x07'
    CMD_REPEATER_RECORD_CLEAR = '\x68\x01\x02\x3c\x07'
    CMD_RD_REPEATER_RECORD = '\x68\x01\x07\x3b\x07'
    # CMD_RD_REPEATER_RECORD = '\x68\x01\x07\x3b\x07\x35\x89\x39\x33\x33\x80\x16'

    CMD_READDATA = CMD_RD_REPEATER_RECORD_NUMBER
    CMD_RD_ADDRESS = CMD_RD_REPEATER_RECORD_NUMBER


    def __init__(self, addr='080100000000'):
        super(Repeater, self).__init__(addr)

        self.point = ''

    def readRecordMount(self):
        return self.cmd(self.CMD_RD_REPEATER_RECORD_NUMBER)

    def readRecordData(self, id):
        # print 'id:', id
        # return self.cmd(self.CMD_RD_REPEATER_RECORD+'\x34'+'\x55\xb6\x35\x33')
        return self.cmd(self.CMD_RD_REPEATER_RECORD+'\x34'+self.plus33(id))

    def realdata(self, data):
        ''' 将字符串倒转 并减去 0x33 '''
        databytes = len(data)
        realdata = ''

        try:
            # startpoint = data.index('\xff\xff\xff\xff\x68')
            startpoint = data.index('\x68')
        except:
            startpoint = -1
        # print 'startpoint:',startpoint

        if startpoint != -1:

            self.rawdata = data[startpoint:].lstrip('\xff')

            # print b2a_hex(self.rawdata)
            result = {}

            if self.rawdata[10:12] == self.CMD_RD_REPEATER_RECORD_NUMBER[-2:]:
                # length of the data
                _l = int(b2a_hex(self.rawdata[9]))-2
                self.point = self.rawdata[12:12+_l]
                _lengthOfRecord = '%08d'%(int(b2a_hex(self.exchanger(self.rawdata[12:12+_l])[::-1])))
                result['pointer'] = _lengthOfRecord
                return result
            elif self.rawdata[10:12] == self.CMD_RD_REPEATER_RECORD[-2:]:
                result['addr']=b2a_hex(self.exchanger(self.rawdata[20:26])[::-1])
                result['value']=str(int(b2a_hex(self.exchanger(self.rawdata[28])),16))
                return result
            elif self.rawdata[10:12] == '\x33\x07':
                result['addr']=b2a_hex(self.exchanger(self.rawdata[12:18])[::-1])
                result['value']=str(int(b2a_hex(self.exchanger(self.rawdata[19])),16))
                return result
            else:
                return ''

        else:
            return False



#------------------------------------------------------------------------------

def createRepeater(addr='aaaaaaaaaaaa'):
    ''' 创建 电表 接口'''
    
    return Repeater(addr)


def test():
    HOST = '130.139.200.48'
    PORT = 10001

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
#    EM1 = TempMeter(ss , _addr)
#    print int(b2a_hex(readtest(EM1.readdata(EM1.CMD_RD_ACTIVEPOWER_TOTAL)))) / 100.0
#    print int(b2a_hex(readtest(EM1.readdata(EM1.CMD_RD_ACTIVEPOWER_FEE1)))) / 100.0
#    print int(b2a_hex(readtest(EM1.readdata(EM1.CMD_RD_ACTIVEPOWER_FEE2)))) / 100.0
#    print int(b2a_hex(readtest(EM1.readdata(EM1.CMD_RD_ACTIVEPOWER_FEE3)))) / 100.0
#    print int(b2a_hex(readtest(EM1.readdata(EM1.CMD_RD_ACTIVEPOWER_FEE4)))) / 100.0

    print "---------------------------------------"

    # ems = [createEMTR('000013059750', _t) for _t in MODTYPES]

    # for em in ems:
    #     data = readtest(em.readdata())
    #     print b2a_hex(data)
    #     em.dealdata(data)
    #     print em.data

    em = createRepeater(addr='000000000108')

    data = readtest(em.readRecordMount())
    mount = em.realdata(data)
    print 'mount:',mount
    data = readtest(em.readRecordData(mount['pointer']))
    print em.realdata(data)



    try:
        ss.close()
    except:
        print 'connection closed error!'
    else:
        print 'connection closed!'

    pass



if __name__ == '__main__':
    test()

#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2011-10-12

Modify_1: 2012.7.27: Add crc16 

@author: zepheir
'''
import device

from binascii import b2a_hex
from struct import unpack, pack, calcsize
import crc16


MODTYPES = '1001', '1020', '1030', '1040'

class SIPAIModule(device.ChildDevice):
    '''
    SIPAI module
    
    '''

    BAUDLIST = ["1200", "2400", "3600", "4800", "9600", "19200", "38400"]

#===============================================================================
# 常规命令
#===============================================================================
    CMD_READMANUFACTURER = '\x2b\x0e\x00'
    CMD_READTYPE = '\x2b\x0e\x01'
    CMD_SETMODULEADDR = '\x10\x00\xc1\x00\x02\x04'

    CMD_READDATA = ''
    CMD_SETBAUD = '\x10\x00\xc4\x00\x01\x02\x00'


    def __init__(self, parent=None, address=0):
        '''
        Constructor
        '''
        device.ChildDevice.__init__(self)

        self.setparent(parent)

        # addr 必须在0~255之间
        addr = min(int(address), 255)
        self.setaddress(addr)

        self.producer = "SIPAI"
        # result string
        self.resultstring = ''

        self.timeout = 10
        self.state = 'OK'

#=======================================================================
# module 常规方法
#=======================================================================
#    def setaddress(self, addr):
#        self.address = addr

    def cmd(self, cmd):
        _cmd = chr(self.address) + cmd

        _crc = crc16.calcString(_cmd, crc16.INITIAL_MODBUS)
        _crc_H = chr((_crc & 0xff00) >> 8)
        _crc_L = chr(_crc & 0xff)

        return  _cmd + _crc_L + _crc_H

    def dealdata(self, data=""):
        ''' need override '''
        self.data = data
        return b2a_hex(self.data)


#===============================================================================
# module 设置方法
#===============================================================================
    def readtype(self):
        return self.cmd(self.CMD_READTYPE)

    def setmoduleaddr(self):
        return self.cmd(self.CMD_SETMODULEADDR)

    def readdata(self):
        return self.cmd(self.CMD_READDATA)

    def setbaud(self):
        return self.cmd(self.CMD_SETBAUD)

#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
class SPM_1001(SIPAIModule):
    ''' SIAPI 1001 module # 累积量值 '''

    DATABYTE = 32
    TYPE = '1001'

    # general commands
    CMD_READDATA ='\x03\x01\x12\x00\x10'
    # CMD_READDATA ='\x03\x00\x9e\x00\x10'
    # CMD_READDATA ='\x03\x01\x7a\x00\x10'


    # special commands
    CMD_SETK = ('\x10\x00\xd9\x00\x03\x06',
            '\x10\x00\xde\x00\x03\x06',
            '\x10\x00\xe3\x00\x03\x06',
            '\x10\x00\xe8\x00\x03\x06',
            '\x10\x00\xed\x00\x03\x06',
            '\x10\x00\xf2\x00\x03\x06',
            '\x10\x00\xf7\x00\x03\x06',
            '\x10\x00\xfc\x00\x03\x06')
    CMD_SETSAMPLETIME = '\x10\x01\x09\x00\x08\x10'
    CMD_SETSUMVALUE = ('\x10\x01\x12\x00\x07\x0e',
                       '\x10\x01\x1f\x00\x07\x0e',
                       '\x10\x01\x2c\x00\x07\x0e',
                       '\x10\x01\x39\x00\x07\x0e',
                       '\x10\x01\x46\x00\x07\x0e',
                       '\x10\x01\x53\x00\x07\x0e',
                       '\x10\x01\x60\x00\x07\x0e',
                       '\x10\x01\x6d\x00\x07\x0e')
    CMD_SETSUMPULSE = '\x10\x01\x7a\x00\x10\x20'

    def __init__(self, parent, address):

        SIPAIModule.__init__(self, parent, address)
        self.setid()
        # name: 'SIPAI'
        name = "SPM_%03d" % self.id
        self.setname(name)
        self.type = self.TYPE

    def setk(self):
        return tuple([self.cmd(_cmd) for _cmd in self.CMD_SETK])

    def setsampletime(self):
        return self.cmd(self.CMD_SETSAMPLETIME)

    def setsumvalue(self):
        return tuple([self.cmd(_cmd) for _cmd in self.CMD_SETSUMVALUE])

    def setsumpulse(self):
        return self.cmd(self.CMD_SETSUMPULSE)

    def dealdata(self, data=""):
        # 
        def foo(data):
            return int(b2a_hex(data))        
        # 
        if len(data) == calcsize('I'*8):
            self.data = [foo(data[(0 + i):(4 + i)]) for i in range(0, 32, 4)]            
            # self.data = unpack('!'+'I'*8,data)

            return '%d,%d,%d,%d,%d,%d,%d,%d'%tuple(self.data)
        else:
            return False


class SPM_1001a(SIPAIModule):
    ''' SIAPI 1001a module '''

    # DATABYTE = 16
    TYPE = '1001a'

    # general commands
    CMD_READDATA ='\x03\x00\x9e\x00\x08'
    
    def __init__(self, parent, address):

        SIPAIModule.__init__(self, parent, address)
        self.setid()
        # name: 'SIPAI'
        name = "SPM_%03d" % self.id
        self.setname(name)
        self.type = self.TYPE

    
    def dealdata(self, data=""):
        # 
        if len(data) == calcsize('H'*8):

            # self.data = [foo(data[(0 + i):(4 + i)]) for i in range(0, 32, 4)]
            self.data = unpack('!'+'H'*8,data)

            return '%d,%d,%d,%d,%d,%d,%d,%d'%(tuple(self.data))
        else:
            return False



#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class SPM_1020(SIPAIModule):
    ''' SIAPI 1020 module '''

    DATABYTE = 2
    TYPE = '1020'

    # general commands
    CMD_READDATA = '\x03\x00\x8f\x00\x01'
    CMD_SETBAUD = '\x10\x00\xc5\x00\x01\x02\x00'

    # special commands
    CMD_SETINPUTMODE = '\x10\x00\xc6\x00\x01\x02'

    def __init__(self, parent, address):

        SIPAIModule.__init__(self, parent, address)
        self.setid()
        # name: 'SIPAI'
        name = "SPM_%03d" % self.id
        self.setname(name)
        self.type = self.TYPE

    # def dealdata(self, data=""):
    #     # 
    #     def foo(data):
    #         pass

    #     # 
    #     if len(data) == self.DATABYTE:
    #         self.data = tuple([(ord(data[1]) >> i) & 1 for i in range(8)])

    #         self.resultstring = '%s %s %s %s %s %s %s %s' % self.data
    #         return self.data
    #     else:
    #         return False


class SPM_1020a(SIPAIModule):
    ''' SIAPI 1020a module: read frequency '''

    DATABYTE = 8
    TYPE = '1020a'

    # general commands
    CMD_READDATA = '\x03\x00\xd8\x00\x04'

    def __init__(self, parent, address):

        SIPAIModule.__init__(self, parent, address)
        self.setid()
        # name: 'SIPAI'
        name = "SPM_%03d" % self.id
        self.setname(name)
        self.type = self.TYPE

    # def dealdata(self, data=""):
    #     # 
    #     def foo(data):
    #         pass

    #     # 
    #     if len(data) == self.DATABYTE:
    #         print "frequency data!"
    #         return False
    #     else:
    #         return False




#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class SPM_1030(SIPAIModule):
    ''' SIAPI 1030 module '''

    DATABYTE = 2
    TYPE = '1030'

    # general commands
    CMD_READDATA = '\x03\x00\x9c\x00\x01'
    CMD_SETDATA = '\x10\x00\x9e\x00\x01\x02\x00'
    CMD_SETBAUD = '\x10\x00\xc5\x00\x01\x02\x00'

    # special commands

    def __init__(self, parent, address):

        SIPAIModule.__init__(self, parent, address)
        self.setid()
        # name: such as 'SPM_001'
        name = "SPM_%03d" % self.id
        self.setname(name)
        self.type = self.TYPE

    def readdata(self):
        return self.cmd(self.CMD_READDATA)

    def dealdata(self, data=""):
        # 数据处理
        if len(data) == self.DATABYTE:
            print '-----1030---->',b2a_hex(data)
            self.data = tuple([(ord(data[1]) >> i) & 1 for i in range(8)])

            return '%d,%d,%d,%d,%d,%d,%d,%d'%self.data
        else:
            return False


#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
class SPM_1040(SIPAIModule):
    ''' SIAPI 1040 module '''

    DATABYTE = 32
    TYPE = '1040'

    # general commands
    # read the temperature
    CMD_READDATA = '\x03\x00\x90\x00\x10'
    CMD_SETMODULEADDR = '\x10\x00\xc0\x00\x02\x04'

    # special commands
    CMD_SETK = ('\x10\x00\xd8\x00\x04\x08',
                '\x10\x00\xde\x00\x04\x08',
                '\x10\x00\xe4\x00\x04\x08',
                '\x10\x00\xea\x00\x04\x08',
                '\x10\x00\xf0\x00\x04\x08',
                '\x10\x00\xf6\x00\x04\x08',
                '\x10\x00\xfc\x00\x04\x08',
                '\x10\x01\x02\x00\x04\x08')
    CMD_SETDA = '\x10\x00\xa0\x00\x01\x02\x00'
    CMD_SETINPUTMODE = '\x10\x00\xc5\x00\x01\x02\x00'
    CMD_SETSTATE = '\x10\x01\x08\x00\x08\x10'

    def __init__(self, parent, address):

        SIPAIModule.__init__(self, parent, address)
        self.setid()
        # name: such as 'SPM_001'
        name = "SPM_%03d" % self.id
        self.setname(name)
        self.type = self.TYPE

    def setk(self):
        return tuple([self.cmd(_cmd) for _cmd in self.CMD_SETK])

    def setda(self):
        return self.cmd(self.CMD_SETDA)

    def setstate(self):
        return self.cmd(self.CMD_SETSTATE)

    def setinputmode(self):
        return self.cmd(self.CMD_SETINPUTMODE)

    def dealdata(self, data=""):
        # 数据处理
        if len(data) == calcsize('I'*8):
            # The Temperature
            self.data = ['%.2f'%(x/100.0) for x in unpack('!'+'I'*8,data)]

#            return tuple(self.dataAll)
            return ','.join(self.data)
        else:
            return False

class SPM_1040b(SIPAIModule):
    ''' SIAPI 1040b module '''

    DATABYTE = 32
    TYPE = '1040b'

    # general commands
    # read the A/D code
    CMD_READDATA = '\x03\x01\xf0\x00\x08'

    def __init__(self, parent, address):

        SIPAIModule.__init__(self, parent, address)
        self.setid()
        # name: such as 'SPM_001'
        name = "SPM_%03d" % self.id
        self.setname(name)
        self.type = self.TYPE

    def dealdata(self, data=""):

        # 数据处理
        if len(data) == calcsize('H'*8):
             
            # AD code
            self.data = unpack('!'+'H'*8,data)

#            return tuple(self.dataAll)
            return ','.join(self.data)
        else:
            return False

#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
class SPM_1042(SIPAIModule):
    ''' SIAPI 1042 module '''

    # DATABYTE = 40
    TYPE = '1042'

    # general commands
    # CMD_READDATA = '\x03\x00\x90\x00\x10'
    # Read the sum data from the module
    CMD_READDATA = '\x03\x01\x80\x00\x10'
    # CMD_READTOTAL = '\x03\x01\x80\x00\x10'
    CMD_SETMODULEADDR = '\x10\x00\xc0\x00\x02\x04'

    # special commands
    CMD_SETK = ('\x10\x00\xd8\x00\x04\x08',
                '\x10\x00\xde\x00\x04\x08',
                '\x10\x00\xe4\x00\x04\x08',
                '\x10\x00\xea\x00\x04\x08',
                '\x10\x00\xf0\x00\x04\x08',
                '\x10\x00\xf6\x00\x04\x08',
                '\x10\x00\xfc\x00\x04\x08',
                '\x10\x01\x02\x00\x04\x08')
    CMD_SETDA = '\x10\x00\xa0\x00\x01\x02\x00'
    CMD_SETINPUTMODE = '\x10\x00\xc5\x00\x01\x02\x00'
    CMD_SETSTATE = '\x10\x01\x08\x00\x08\x10'

    def __init__(self, parent, address):

        SIPAIModule.__init__(self, parent, address)
        self.setid()
        # name: such as 'SPM_001'
        name = "SPM_%03d" % self.id
        self.setname(name)
        self.type = self.TYPE

    def setk(self):
        return tuple([self.cmd(_cmd) for _cmd in self.CMD_SETK])

    def setda(self):
        return self.cmd(self.CMD_SETDA)

    def setstate(self):
        return self.cmd(self.CMD_SETSTATE)

    def setinputmode(self):
        return self.cmd(self.CMD_SETINPUTMODE)

    def dealdata(self, data=""):
        # 数据处理
        if len(data) == calcsize('I'*8):
            # 测量值             
            self.data = ['%d'%(x) for x in unpack('!'+'I'*8,data)]

            return ','.join(self.data)
        else:
            return False


class SPM_1042a(SIPAIModule):
    ''' SIAPI 1042a module '''

    # DATABYTE = 40
    TYPE = '1042a'

    # general commands
    CMD_READDATA = '\x03\x00\x90\x00\x10'

    def __init__(self, parent, address):

        SIPAIModule.__init__(self, parent, address)
        self.setid()
        # name: such as 'SPM_001'
        name = "SPM_%03d" % self.id
        self.setname(name)
        self.type = self.TYPE

    def dealdata(self, data=""):
        # 数据处理
        if len(data) == calcsize('I'*8):
            # 测量值             
            self.data = ['%.1f'%(x/10.0) for x in unpack('!'+'I'*8,data)]

            return ','.join(self.data)
        else:
            return False



#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
class SPM_1043(SIPAIModule):
    ''' SIAPI 1043 module '''

    # DATABYTE = 40
    TYPE = '1043'

    # general commands 

    # Read the sum data from the module
    CMD_READDATA = '\x03\x01\x5c\x00\x10'
    # CMD_READTOTAL = '\x03\x01\x5c\x00\x10'

    CMD_SETMODULEADDR = '\x10\x00\xc0\x00\x02\x04'

    # special commands
    CMD_SETK = ('\x10\x00\xdc\x00\x02\x04',
                '\x10\x00\xe0\x00\x02\x04',
                '\x10\x00\xe4\x00\x02\x04',
                '\x10\x00\xe8\x00\x02\x04',
                '\x10\x00\xec\x00\x02\x04',
                '\x10\x00\xf0\x00\x02\x04',
                '\x10\x00\xf4\x00\x02\x04',
                '\x10\x01\xf8\x00\x02\x04')
    CMD_SETDA = '\x10\x00\xa0\x00\x01\x02\x00'
    CMD_SETINPUTMODE = '\x10\x00\xc5\x00\x01\x02\x00'
    CMD_SETSTATE = '\x10\x01\x08\x00\x08\x10'

    def __init__(self, parent, address):

        SIPAIModule.__init__(self, parent, address)
        self.setid()
        # name: such as 'SPM_001'
        name = "SPM_%03d" % self.id
        self.setname(name)
        self.type = self.TYPE

    def setk(self):
        return tuple([self.cmd(_cmd) for _cmd in self.CMD_SETK])

    def setda(self):
        return self.cmd(self.CMD_SETDA)

    def setstate(self):
        return self.cmd(self.CMD_SETSTATE)

    def setinputmode(self):
        return self.cmd(self.CMD_SETINPUTMODE)

    def dealdata(self, data=""):
        # 数据处理
        if len(data) == calcsize('I'*8):
            # 测量值             
            self.data = ['%d'%(x) for x in unpack('!'+'I'*8,data)]

            return ','.join(self.data)
        else:
            return False


#     def dealdata(self, data=""):
#         # 处理函数

#         def foo(data):
#             return int(b2a_hex(data), 16)


#         # 数据处理
#         if len(data) == self.DATABYTE:
#             # 测量值             
#             self.data = tuple([foo(data[(0 + i):(4 + i)]) for i in range(0, 32, 4)])
                         

#             self.resultstring = '%05d %05d %05d %05d %05d %05d %05d %05d' % self.data[0]


# #            return tuple(self.dataAll)
#             return self.data
#         else:
#             return False


class SPM_1043a(SIPAIModule):
    ''' SIAPI 1043a module '''

    # DATABYTE = 40
    TYPE = '1043a'

    # general commands 

    # Read the data from the module
    CMD_READDATA = '\x03\x00\xb0\x00\x09'

    def __init__(self, parent, address):

        SIPAIModule.__init__(self, parent, address)
        self.setid()
        # name: such as 'SPM_001'
        name = "SPM_%03d" % self.id
        self.setname(name)
        self.type = self.TYPE


    def dealdata(self, data=""):
        # 数据处理
        if len(data) == calcsize('H'*9):
            # 测量值
            # print '1043a show data:', b2a_hex(data)
            self.data = ['%d'%(x) for x in unpack('!'+'H'*9,data)]

            return ','.join(self.data)
        else:
            return False

#     def dealdata(self, data=""):
#         # 处理函数

#         def foo(data):
#             return int(b2a_hex(data), 16)


#         # 数据处理
#         if len(data) == self.DATABYTE:
#             # 测量值             
#             self.data = tuple([foo(data[(0 + i):(4 + i)]) for i in range(0, 32, 4)])
                         

#             self.resultstring = '%05d %05d %05d %05d %05d %05d %05d %05d' % self.data[0]


# #            return tuple(self.dataAll)
#             return self.data
#         else:
#             return False


def createspm(parent=None, type="1040", address=40):
    """ create sipai module """
    if type == "1001":
        newmod = SPM_1001(parent, address)
    elif type == "1001a":
        newmod = SPM_1001a(parent, address)        
    elif type == "1020":
        newmod = SPM_1020(parent, address)
    elif type == "1020a":
        newmod = SPM_1020a(parent, address)        
    elif type == "1030":
        newmod = SPM_1030(parent, address)
    elif type == "1040":
        newmod = SPM_1040(parent, address)
    elif type == "1042":
        newmod = SPM_1042(parent, address)
    elif type == "1042a":
        newmod = SPM_1042a(parent, address)        
    elif type == "1043":
        newmod = SPM_1043(parent, address)
    elif type == "1043a":
        newmod = SPM_1043a(parent, address)        
    else:
        newmod = None
    return newmod


def Test():
    mod = SPM_1020(None, 5)
    print mod.getdetail()
#    print mod.setk()
#    print (mod.setsampletime())
#    print mod.setsumvalue()

#    data = ""
#    for i in range(mod.DATABYTE):
#        data += '\x36'
    data = '\x00\xff'
    print data
    print mod.dealdata(data)




if __name__ == "__main__":
    Test()



#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2011-10-12

@author: zepheir
'''
import device

class RootDevice(device.ParentDevice):
    ''' 根器件 
        根器件是虚拟期间, 没有具体的address, baud rate,
        根器件是其他器件的原点, 没有parent, 所以它应该最早被建立
    '''
    def __init__(self):
        device.ParentDevice.__init__(self)

        #  自动设置id
        self.setid()
        self.setparent(None)

#        self.children = {}


class SPS(device.ParentDevice):
    '''
    Serial Ports Server
    串口信号 与 以太网信号 互相转换
    
    '''


    def __init__(self, parent=None, ip="", port=0, baudrate=9600):
        '''
        Constructor
        '''
        device.ParentDevice.__init__(self)

        address = ip, port

        self.setaddress(address)

        self.setparent(parent)

        self.settype("SPS")

        self.baudrate = baudrate


class HHL(SPS):
    ''' 北京海华联 串口服务器 '''

    def __init__(self, parent=None, ip="192.168.192.100", port=6020,
                 baudrate=9600):
        ''' Constructor '''
        SPS.__init__(self, parent, ip, port, baudrate)

#        self.baudrate = baudrate
        # 设置id
        self.setid()

        self.name = "HHL_%03d" % self.id



def Test():
    rootdev = RootDevice()
    print rootdev.id, rootdev.getkey(), rootdev.getdetail()
    dev1 = HHL(rootdev, "192.168.192.100", port=6020)
    print dev1.id, dev1.getkey(), dev1.getdetail()
    dev2 = HHL(rootdev, "192.168.192.100", port=6021)
    print dev2.id, dev2.getkey(), dev2.getdetail()
    print rootdev.addchild(dev1), rootdev.getchildren()
    print rootdev.addchild(dev2), rootdev.getchildren()

    print rootdev.popchildren()

    print rootdev.getchildren()


if __name__ == "__main__":
    Test()

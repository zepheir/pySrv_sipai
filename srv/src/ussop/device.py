#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2011-10-11

@author: zepheir
'''


class BaseDevice():
    '''
    The Base Class of All the Device.
    
    parent: instance
    address: Integer / (IP, Port)
    id: AnyId(-1) / Integer
    type: String
    
    '''

    maxid = 0

    def __init__(self):
        self.parent = object

#        self.id = self.maxid
#        BaseDevice.maxid += 1 #self.__class__.maxid += 1
        self.id = 0

        self.address = object
        self.type = ""
        self.name = ""

#===============================================================================
# 与 parent 相关的 Methods
#===============================================================================
    def setid(self, id=None):
        if id:
            self.id = id
        else:
            self.id = BaseDevice.maxid
            BaseDevice.maxid += 1 #self.__class__.maxid += 1

    def getkey(self):
        ''' address is the key '''
        return self.name

    def getdetail(self):
        return self.address, self.id, self.type, self.name

    def getparent(self):
        return self.parent

    def setparent(self, object):
        self.parent = object

#===============================================================================
# 与 attributes 相关的 Methods
#===============================================================================
    def setaddress(self, addr=object):
        self.address = addr

    def getaddress(self):
        return self.address

    def settype(self, type=""):
        self.type = type

    def setname(self, name=""):
        self.name = name



#------------------------------------------------------------------------------
#------------------------------------------------------------------------------ 
class ParentDevice(BaseDevice):
    ''' ParentDevice 侧重于child的管理, 包含add/del/get/update等方法 '''

    def __init__(self):
        BaseDevice.__init__(self)
        # children
        self.children = {}

#===============================================================================
# 与自身相关的 Methods
#===============================================================================

    def addchild(self, newchild=object):
        key = newchild.getkey()
        if key not in self.children.keys():
            self.children[key] = newchild
            return key
        else:
            return False

    def getchild(self, key=object):
        try:
            return self.children[key]
        except:
            return False

    def getchildren(self):
        keys = self.children.keys()
        keys.sort()
        return [self.children[key] for key in keys]

    def getchildrenkeys(self):
        keys = self.children.keys()
        keys.sort()
        return keys

    def updatechild(self, newchild=object):
        key = newchild.getkey()
        if key in self.children.keys():
            self.children[key] = newchild
            return key
        else:
            return False

    def popchild(self, key=object):
        try:
            if key in self.children.keys():
                _child = self.children.pop(key)
                return _child
        except:
            return False

    def popchildren(self):
        return [self.popchild(key) for key in self.children.keys()]



#------------------------------------------------------------------------------ 
class ChildDevice(BaseDevice):
    ''' ChildDevice 侧重于自身的应用. 主要包含自己的应用逻辑 '''

    def __init__(self):
        BaseDevice.__init__(self)

        self.data = object

#===========================================================================
# 与 data 相关的 methods
#===========================================================================

    def update(self, newdata=object):
        self.data = newdata

    def getdata(self):
        return self.data



def test():
    dev1 = ParentDevice()
    print 'parent device id:', dev1.id
    dev2 = ChildDevice()
    print 'child device 1# id:', dev2.id


    key1 = dev1.addchild(dev2)
    dev2.update('dadadadadate')
    print 'parent device children:', dev1.children
    print 'parent device child 1# key:', dev1.getchild(key1)
    print 'parent device child 1# data:', dev2.getdata()

    print 'delete device:', dev1.popchildren()


    print 'parent device children:', dev1.children
    print 'parent device child 1# key:', dev1.getchild(key1)


if __name__ == "__main__":
    test()

# /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2012-3-4

Modify_1: 2012.7.27

Modify_2: 2013.12.20

@author: zepheir

简介:
-- 这个控制台(Console)运行在服务器端;
-- 将"zhyDB"中的"devices"集中的数据转化为"Vars"集的数据;
-- 转化公式由"Vars"集中的calc来确定, 如果calc为"1"则直接赋值;
'''

import sys
sys.path.append('/app/srv/src')

from zhyDB import ZhyDB

import config
from config import *

try:
    from twisted.internet import epollreactor
    epollreactor.install()
except:
    pass
from twisted.internet import reactor
from twisted.python import log
from twisted.application import service

import time
from time import ctime

from math import *


zhy = ZhyDB()
REFRESHTIMER = RESULT_REFRESH_TIMER


class UpdateServer(object):
    """docstring for UpdateServer"""
    def __init__(self, db=zhy):
        super(UpdateServer, self).__init__()
        self.db = zhy
        self.vars = self.db.getVars()
        self.devices = self.db.getDevices()

        # print self.vars,self.devices

    def update(self):
        ''' update '''

        def calcurate(cmd = '1', val = ''):
            if cmd == '1' or cmd == '' or cmd == None or val == '':
                return val
            else:
                if val.find('.')>0:
                    x = float(val)
                else:
                    x = int(val)
                _result = str(eval(cmd))
                return _result
        
        t1 = time.time()
        for var in self.vars:
            if var['addr']:
                _ip, _port, _maddr, _types, _channel = self.explainAddress(addr=var['addr'])
            else:
                continue

            # sipai modules
            if _types[0] in ELECTROMODS or SIPAIMODS:
                
                # print _ip, _port, _maddr, _types, _channel,                 
                _value = self.db.getDeviceValue(ip=_ip, port=_port, maddr=_maddr, types=_types, channel=_channel)

                # print _ip, _port, _maddr, _types, _channel, _value
                # # calurate the result
                # if var['calc']=='1':
                #     _v= _value[_types[0]]
                # else:
                #     if _value[_types[0]]=='':
                #         _v= _value[_types[0]]
                #     elif _value[_types[0]].find('.')>0:
                #         x = float(_value[_types[0]])
                #     else:
                #         x = int(_value[_types[0]])
                #     _c = var['calc']
                #     _v= str(eval(_c))
                #     # if len(_v)>6: _v2= _v[:6]

                # # save the result
                # if len(_types)==2:

                #     if var['calc2']=='1':
                #         _v2= _value[_types[1]]
                #     else:
                #         if _value[_types[1]]=='':
                #             _v2= _value[_types[1]]
                #         elif _value[_types[1]].find('.')>0:
                #             x = float(_value[_types[1]])
                #         else:
                #             x = int(_value[_types[1]])
                #         _c = var['calc2']
                #         _v2= str(eval(_c))

                #     result = self.db.updateVarsValue(
                #         # addr="52:10001:10:1001a,1001:0",
                #         _id      =var['_id'],
                #         org_value=_value[_types[0]],
                #         cur_value=_v,
                #         # sum_value=_value[_types[1]]
                #         sum_value=_v2
                #         )
                # else:
                #     result = self.db.updateVarsValue(
                #         # addr="52:10001:10:1001a,1001:0",
                #         _id      =var['_id'],
                #         org_value=_value[_types[0]],
                #         cur_value=_v,
                #         sum_value=''
                #         )

                # save the result
                if len(_types)==2:

                    if var['calc2']=='1':
                        _v2= _value[_types[1]]
                    else:
                        if _value[_types[1]]=='':
                            _v2= _value[_types[1]]
                        elif _value[_types[1]].find('.')>0:
                            x = float(_value[_types[1]])
                        else:
                            x = int(_value[_types[1]])
                        _c = var['calc2']
                        _v2= str(eval(_c))

                    result = self.db.updateVarsValue(
                        # addr="52:10001:10:1001a,1001:0",
                        _id      =var['_id'],
                        org_value=_value[_types[0]],
                        cur_value=calcurate(cmd=var['calc'], val=_value[_types[0]]),
                        # sum_value=_value[_types[1]]
                        sum_value=calcurate(cmd=var['calc2'], val=_value[_types[1]])
                        )
                else:
                    result = self.db.updateVarsValue(
                        # addr="52:10001:10:1001a,1001:0",
                        _id      =var['_id'],
                        org_value=_value[_types[0]],
                        cur_value=calcurate(cmd=var['calc'], val=_value[_types[0]]),
                        sum_value=''
                        )




                # if update falsed, print
                if result['updatedExisting']==False: print '[%s]: %s'%(ctime(),result)


        t2 = time.time()

        print t2-t1


    def explainAddress(self, addr="52:10001:40:1040:0"):
        ''' explain the Address from the vars '''
        # "addr": "52:10001:40:1040:0"
        _addr   = addr.split(':')
        _ip     = serverIP.replace('40', _addr[0])
        _port   = _addr[1]
        _maddr  = _addr[2]
        _types  = _addr[3].split(',')
        _chanel = int(_addr[4])

        return _ip, _port, _maddr, _types, _chanel
        

# if DEBUG: server = UpdateServer(zhy)

def repeat():
    ''' repeat '''
    print "===[%s] Updating is started ==="% ctime()
    reactor.callLater(REFRESHTIMER, repeat)

    server= object()
    server = UpdateServer(zhy)
    server.update()

    # if DEBUG: server = UpdateServer(zhy)

    # if not DEBUG:
    #     _server = UpdateServer(zhy)
    #     _server.update()
    # else:
    #     global server
    #     server.update()

    # reactor.callLater(REFRESHTIMER, repeat)


def main():
    """ Main program """
    # Initial 
    print " ---- start Initialization ----"
    print 'Refresh timer:', REFRESHTIMER
    print " ---- end Initialization ----"

    # Main loop
    if ECHO: print " -- Main loop running! --"
    reactor.callLater(REFRESHTIMER, repeat)


if __name__ == '__main__':
    import sys

    main()

    reactor.run()
    print 'reactor stopped!'

    sys.exit(1)
elif __name__ =="__builtin__":
    import sys

    main()
    application = service.Application("RESULT")

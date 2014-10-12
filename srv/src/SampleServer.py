#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2013-12-19

@author: zepheir
'''
try:
    from twisted.internet import epollreactor
    epollreactor.install()
except:
    pass

from twisted.internet import reactor
from twisted.python import log
from twisted.application import service

from sipaiSampleServer import SampleServer as SipaiServer
from eletrSampleServer import SampleServer as ElectServer

import config
from config import *

from zhyDB import ZhyDB

zhy = ZhyDB()
SipaiModsDictWithout30 = zhy.listSipaiModsWithout30(allSDS=None)
ElecMeterDict = zhy.listElecMeters(allSDS=None, allMods=None)

servs ={}

def main():
    for sds in SipaiModsDictWithout30:
        servs[sds]=SipaiServer(sds[0],sds[1])
        servs[sds].update()
        # time.sleep(0.2)
    for sds in ElecMeterDict:
        servs[sds]=ElectServer(sds[0],sds[1])
        servs[sds].update()
    # if DEBUG:
    #     servs1=ElectServer('130.139.200.52','10002')
    #     servs2=SipaiServer('130.139.200.52','10001')
    #     # servs3=SampleServer('130.139.200.56','10001')
    #     servs1.update()
    #     servs2.update()
    #     # servs3.update()
    # else:
    #     for sds in SipaiModsDictWithout30:
    #         servs[sds]=SampleServer(sds[0],sds[1])
    #         servs[sds].update()
    #         time.sleep(0.2)



if __name__ == '__main__':
    import sys

    main()

    reactor.run()
    print 'reactor stopped!'

    sys.exit(1)
elif __name__ =="__builtin__":
    import sys

    main()
    application = service.Application("SAMPLESERVER")
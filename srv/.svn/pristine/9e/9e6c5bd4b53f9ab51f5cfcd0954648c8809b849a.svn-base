# /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2012-7-26

@author: zepheir
'''

from zhyDB import ZhyDB

import config
from config import *

import time

class HistoryConsole(object):
    """docstring for HistoryConsole"""
    def __init__(self):
        super(HistoryConsole, self).__init__()
        self.zhy = ZhyDB()

        self.vars = self.zhy.getVarsValue()
        self.time = int(time.time())/300*300
        self.result = {}
        # print self.time

    def saveHistory(self):
        # savedata = {}
        # for var in self.vars:
        #     # print var['cur_value']
        #     savedata[str(var['_id'])]=var['cur_value']

        # self.result[str(self.time)] = savedata
        # print self.result
        # # _cmd = "self.zhy.db.D%s.save(self.result)" % (time.strftime('%Y_%m_%d'))
        # # print _cmd
        # print eval(_cmd)

        # save all vars data in one time collection
        if HISTORY_TIMEBASE:
            savelist = []
            for var in self.vars:
                savedata = {}            
                # print var['cur_value']
                if var['sum_value']=='' or (not var['sum_value']):
                    # savedata[str(var['vars_id'])]=var['cur_value']
                    savedata[str(var['vars_id'])]=float(var['cur_value'])
                else:
                    # savedata[str(var['vars_id'])]=var['sum_value']
                    savedata[str(var['vars_id'])]=float(var['sum_value'])
                savelist.append(savedata)

            # self.result[str(self.time)] = savedata
            # print savelist
            _cmd = "self.zhy.db.T_%d.insert(savelist)" % (self.time)
            # print _cmd
            eval(_cmd)

        # save one var data in one collection
        else:
            for var in self.vars:
                savedata = {'time':self.time}
                if var['sum_value']=='' or (not var['sum_value']):
                    # savedata['value']=var['cur_value']
                    try:
                        savedata['value']=float(var['cur_value'])
                    except:
                        savedata['value']=0
                    
                else:
                    # transdata for the ON/OFF to 1/0
                    if var['sum_value'] == 'ON':
                        # savedata['value'] = '1'
                        savedata['value'] = 1
                    elif var['sum_value'] == 'OFF':
                        # savedata['value'] = '0'
                        savedata['value'] = 0
                    else:
                        # savedata['value']=var['sum_value']
                        try:
                            savedata['value']=float(var['sum_value'])
                        except:
                            savedata['value']=0
                    # savedata['value']=var['sum_value']
                _cmd = "self.zhy.db.H_%d.save(savedata)" %(var['vars_id'])
                eval(_cmd)


if __name__ == '__main__':
    hstyConsole = HistoryConsole()

    """ Main program """
    print " ---- start Initialization ----"
    
    hstyConsole.saveHistory()

    print " ---- end Initialization ----"

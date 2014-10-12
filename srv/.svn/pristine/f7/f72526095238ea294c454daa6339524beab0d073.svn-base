#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2012-3-5

@author: zepheir

Modified date: 2014-10-11

Project Name: SIPAI R8 Building data sample server program

Samuel Gao
'''

#import pymongo
# from pymongo import Connection
from pymongo import MongoClient
import config
from config import *
import time

from binascii import b2a_hex,a2b_hex

#------------------------------------------------------------------------------
class MyDB():

    def __init__(self, ip='127.0.0.1', port=27017):

        if DEBUG: print " ==> MyDB Initialization"

        self.db = self.setupDB(ip, port)

        settings = self.readSettings()

        # self.vars = self.readVars()

        # self.varClass = self.getVarsClass()

        # if self.db:self.refreshTime = sysValues['Results2VarsTime']
        if DEBUG and self.db:
            self.refreshTime = settings['Timer_Results2Values']
            print dbgIDF+'MyDB.refreshTime: %.2f'%(float(self.refreshTime))


#------------------------------------------------
#   General functions 
#------------------------------------------------            

    # Initial Database
    def setupDB(self, ip, port):
        # setup the conneciton of the mongodb
        try:
            # The function "MongoClient" replace the "Connection"
            # in the new version Pymongo.
            # The connection setup "mongoURL" can be modified in the file "config.py".
            if DEBUG: print dbgIDF+"mongoURL: "+config.mongoURL
            client = MongoClient(config.mongoURL)

            # Setup the db
            db = client.appdb1

        except:
            print dbgIDF+'db connection error!'
            client = None
            db = None

    #    返回值: ZHY能源数据库 MyDB
        if DEBUG: print dbgIDF+"DB information:", db
        return db


    def collectionNames(self):
        """Show all the collection names in current db"""
        if DEBUG: print dbgIDF+"collection names:",self.db.collection_names()
        return self.db.collection_names()


    # -------- del collections ----------
    def removeCollections(self, head='T_'):
        if self.db:
            collections = self.collectionNames()
            for cl in collections:
                if cl[:len(head)] == head:
                    # print cl
                    _cmd = 'self.db.%s.drop()'%cl
                    eval(_cmd)
        else:
            return False
            

    def readSettings(self):
        '''Read the Settings'''
        if self.db:
            table = self.db.settings.find()
            return table[0]
        else:
            return False

#--------------------------------------------------
#   Devices functions
#--------------------------------------------------

    def readDevices(self):
        ''' Read Devices '''
        if self.db:
            mods = list(self.db.devices.find())
            if DEBUG: print dbgIDF+"All Devices:",mods
            return mods
        else:
            if DEBUG: print dbgIDF+"All Devices:",False
            return False



#--------------------------------------------------------
#   Serial Device Server function
#--------------------------------------------------------

    def readSdsMods(self):
        ''' Read Serial Device Servers '''
        if self.db:
            mods = list(self.db.devices.find({"type":'sds'}).sort('ip'))
            # if DEBUG: print dbgIDF+"Serial Device Servers:",mods
            return mods
        else:
            if DEBUG: print dbgIDF+"Serial Device Servers:",False
            return False        


    def findSdsMods(self, ip='',port=''):
        ''' find Serial Device Servers '''
        if self.db:
            _cursor = self.db.devices.find({'ip':ip,'port':str(port),'type':'sds'})
            if _cursor.count() == 0:
                if DEBUG: print dbgIDF+"Serial Device Servers %s %s not FOUND"%(ip,str(port))
                return 0
            else:
                _list = list(_cursor)
                if DEBUG: print dbgIDF+"Serial Device Servers:",_list
                return _list
        else:
            if DEBUG: print dbgIDF+"Serial Device Servers:",False
            return False

    def newSdsMods(self, data={}):
        if self.db:
            if len(data)>0:
                self.db.devices.save(data)
                if DEBUG: print dbgIDF+"The NEW Serial Device Servers Saved!!!!"
                return True
            else:
                if DEBUG: print dbgIDF+"Serial Device Servers data is Empty!!!"
                return False
        else:
            if DEBUG: print dbgIDF+"Serial Device Servers:",False
            return False

    def removeSdsMods(self,ip='',port=''):
        if self.db:
            if ip != '' and port != '':
                self.db.devices.remove({'ip':ip,'port':str(port),'type':'sds'})
                if DEBUG: print dbgIDF+"The %s %s Serial Device Servers are DELETED!!!!"%(ip,str(port))
                return True
            elif port != '':
                self.db.devices.remove({'port':str(port),'type':'sds'})
                if DEBUG: print dbgIDF+"The PORT %s Serial Device Servers are DELETED!!!!"%(str(port))
                return True
            elif ip != '':
                self.db.devices.remove({'ip':ip,'type':'sds'})
                if DEBUG: print dbgIDF+"The IP %s Serial Device Servers are DELETED!!!!"%(ip)
                return True
            else:                
                self.db.devices.remove({'type':'sds'})
                if DEBUG: print dbgIDF+"All the Serial Device Servers are DELETED!!!!"
                return True


        else:
            if DEBUG: print dbgIDF+"Serial Device Servers:",False
            return False        

#----------------------------------------------------------
#   Sipai Module functions
#----------------------------------------------------------

    def findSipaiMods(self, ip='',port='',addr=''):
        ''' find Sipai Modules '''
        if self.db:
            _cursor = self.db.devices.find({'ip':ip,'port':str(port),'addr':str(addr),'manufacturer':'SIPAI'})
            if _cursor.count() == 0:
                if DEBUG: print dbgIDF+"Sipai Modules %s %s %s not FOUND"%(ip,str(port),str(addr))
                return 0
            else:
                _list = list(_cursor)
                if DEBUG: print dbgIDF+"Sipai Modules:",_list
                return _list
        else:
            if DEBUG: print dbgIDF+"Sipai Modules:",False
            return False

    def findSipaiModsbyType(self,type=''):
        ''' find sipai module by type '''
        if self.db:
            _cursor = self.db.devices.find({'type':type,'manufacturer':IDFSipai})
            if _cursor.count()==0:
                if DEBUG: print dbgIDF+"Sipai Modules type %s not FOUND"%(type)
                return 0
            else:
                _list = list(_cursor)
                if DEBUG: print dbgIDF+"Sipai Modules:",_list
                return _list
        else:
            if DEBUG: print dbgIDF+"Sipai Modules:",False
            return False


    def newSipaiMods(self, data={}):
        ''' And New Sipai Modules '''
        if self.db:
            if len(data)>0:
                self.db.devices.save(data)
                if DEBUG: print dbgIDF+"The NEW Sipai Modules Saved!!!!"
                return True
            else:
                if DEBUG: print dbgIDF+"Sipai Modules data is Empty!!!"
                return False
        else:
            if DEBUG: print dbgIDF+"Sipai Modules:",False
            return False

    def listSipaiMods(self, allSDS=True):
        ''' List Sipai Modules '''
        sipaiModDict={}
        if self.db:
            sdsMods = self.readSdsMods()
            for sds in sdsMods:
                _list = list(self.db.devices.find({'ip':sds['ip'],'port':sds['port'],'manufacturer':'SIPAI'},{'type':1,'addr':1,'_id':0}).sort('addr'))
                if allSDS or len(_list)>0:
                    sipaiModDict[(sds['ip'],sds['port'])]=_list

        return sipaiModDict

    def listSipaiModsWithout30(self, allSDS=True):
        ''' List Sipai Modules without 1030 1030a '''
        sipaiModDict={}
        if self.db:
            sdsMods = self.readSdsMods()
            for sds in sdsMods:
                _list = list(self.db.devices.find({'ip':sds['ip'],'port':sds['port'],'type':{'$nin':['1030','1030a']},'manufacturer':'SIPAI'},{'type':1,'addr':1,'_id':0}).sort('addr'))
                if allSDS or len(_list)>0:
                    sipaiModDict[(sds['ip'],sds['port'])]=_list

        return sipaiModDict


    def listSipaiMods30(self, allSDS=True):
        ''' List Sipai Modules 1030 1030a '''
        sipaiModDict={}
        if self.db:
            sdsMods = self.readSdsMods()
            for sds in sdsMods:
                _list = list(self.db.devices.find({'ip':sds['ip'],'port':sds['port'],'type':{'$in':['1030','1030a']},'manufacturer':'SIPAI'},{'type':1,'addr':1,'_id':0}).sort('addr'))
                if allSDS or len(_list)>0:
                    sipaiModDict[(sds['ip'],sds['port'])]=_list

        return sipaiModDict


    def removeSipaiMods(self,ip='',port='',addr=''):
        if self.db:
            if ip != '' and port != '' and addr !='':
                self.db.devices.remove({'ip':ip,'port':str(port),'addr':str(addr),'manufacturer':'SIPAI'})
                if DEBUG: print dbgIDF+"The %s %s %s Sipai Module is DELETED!!!!"%(ip,str(port),str(addr))
                return True
            elif ip != '' and port != '':
                self.db.devices.remove({'ip':ip,'port':str(port),'manufacturer':'SIPAI'})
                if DEBUG: print dbgIDF+"The %s %s Sipai Modules are DELETED!!!!"%(ip,str(port))
                return True                
            elif ip != '':
                self.db.devices.remove({'ip':ip,'manufacturer':'SIPAI'})
                if DEBUG: print dbgIDF+"The IP %s Sipai Modules are DELETED!!!!"%(ip)
                return True
            else:                
                self.db.devices.remove({'manufacturer':'SIPAI'})
                if DEBUG: print dbgIDF+"All the Sipai Modules are DELETED!!!!"
                return True


        else:
            if DEBUG: print dbgIDF+"Sipai Modules DELETE ERR:",False
            return False   

    def readSipaiMods(self):
        ''' Read Sipai Modules '''
        if self.db:
            mods = list(self.db.devices.find({"manufacturer":IDFSipai}))
            if DEBUG: print dbgIDF+"SipaiModules:",mods
            return mods
        else:
            if DEBUG: print dbgIDF+"SipaiModules:",False
            return False


    def readSipaiResult(self,**data):
        ''' Read Sipai Modules result'''
        if self.db:
            _result=list(self.db.devices.find({
                'manufacturer':IDFSipai,
                'ip':data['ip'],
                'port':data['port'],
                'addr':data['addr'],                
                },{
                'value':1,
                '_id':0
                }))[0]['value']
            return a2b_hex(_result)
        else:
            if DEBUG: dbgIDF+"NO Database!"
            return False


    def readSipaiVars(self):
        ''' Read Sipai Module Vars '''
        if self.db:
            _vars = list(self.db.vars.find({"manufacturer":IDFSipai}))
            if DEBUG: print dbgIDF+"SipaiVars:",_vars
            return _vars
        else:
            if DEBUG: print dbgIDF+"SipaiVars:",False
            return False


    def removeSipaiResults(self):
        if self.db:
            try:
                self.db.results.remove({'manufacturer':IDFSipai})
                return True
            except:
                if DEBUG: dbgIDF+"Sipai Results DELETED ERROR!"
                return False
        else:
            if DEBUG: dbgIDF+"NO Database!"
            return False

    # save results in the devices collection
    def setupSipaiResults(self):
        ''' setup Results in the devices collection '''
        if self.db:
            # self.removeSipaiResults()
            mods = self.readSipaiMods()
            for mod in mods:
                self.db.devices.update({
                    'manufacturer':mod['manufacturer'],
                    'ip':mod['ip'],
                    'port':mod['port'],
                    'addr':mod['addr'],                    
                    },{
                    '$set':{
                    'value':"",
                    'state':"ok"
                    }})
        else:
            if DEBUG: dbgIDF+"NO Database!"
            return False 

    # def setupSipaiResults(self):
    #     ''' setup Results '''
    #     if self.db:
    #         self.removeSipaiResults()
    #         mods = self.readSipaiMods()
    #         for mod in mods:
    #             self.db.results.save({
    #             'manufacturer':mod['manufacturer'],
    #             'ip':mod['ip'],
    #             'port':mod['port'],
    #             'addr':mod['addr'],
    #             'value':"",
    #             'state':""
    #             })
    #     else:
    #         if DEBUG: dbgIDF+"NO Database!"
    #         return False 


    def updateSipaiResults(self, **data):
        ''' update Sipai Results '''
        if self.db:
           
            # return self.db.results.update({
            return self.db.devices.update({                
                'manufacturer':IDFSipai,
                'ip':data['ip'],
                'port':str(data['port']),
                'addr':str(data['addr']),
                'type':data['type']
                },{
                '$set':{
                'value':data['value'],
                'state':'ok'
                }})

        else:
            if DEBUG: dbgIDF+"NO Database!"
            return False 

    def  setSipaiModState(self,**data):
        ''' set Sipai Module State '''
        if self.db:
            return self.db.devices.update({
                'manufacturer':IDFSipai,
                'ip':data['ip'],
                'port':str(data['port']),
                'addr':str(data['addr']),
                'type':data['type']
                },{
                '$set':{
                'state':data['state']
                }})
        else:
            if DEBUG: dbgIDF+"NO Database!"
            return False 


# ----------------------------------------------------
#  Function of the ElecMeters 
# ----------------------------------------------------

    def findElecMeters(self, ip='',port='',addr=''):
        ''' find Sipai Modules '''
        if self.db:
            _cursor = self.db.devices.find({'ip':ip,'port':str(port),'addr':str(addr),'manufacturer':"TEMP"})
            if _cursor.count() == 0:
                if DEBUG: print dbgIDF+"Elec Meters %s %s %s not FOUND"%(ip,str(port),str(addr))
                return 0
            else:
                _list = list(_cursor)
                if DEBUG: print dbgIDF+"Elec Meters:",_list
                return _list
        else:
            if DEBUG: print dbgIDF+"Elec Meters:",False
            return False


    def newElecMeter(self, data={}):
        ''' And New Elec Meters '''
        if self.db:
            if len(data)>0:
                self.db.devices.save(data)
                if DEBUG: print dbgIDF+"The NEW Elec Meters Saved!!!!"
                return True
            else:
                if DEBUG: print dbgIDF+"Elec Meters data is Empty!!!"
                return False
        else:
            if DEBUG: print dbgIDF+"Elec Meters:",False
            return False


    def listElecMeters(self, allSDS=True, allMods=True):
        ''' List Electro Meters '''
        ElecMeterDict={}
        if self.db:
            sdsMods = self.readSdsMods()
            for sds in sdsMods:
                if allMods==True: _list = list(self.db.devices.find({'ip':sds['ip'],'port':sds['port'],'manufacturer':"TEMP"},{'type':1,'addr':1,'_id':0}).sort('addr'))
                else:
                    _list = list(self.db.devices.find({'ip':sds['ip'],'port':sds['port'],'type':'power','manufacturer':"TEMP"},{'type':1,'addr':1,'_id':0}).sort('addr'))

                if allSDS or len(_list)>0:
                    ElecMeterDict[(sds['ip'],sds['port'])]=_list

        return ElecMeterDict


    def removeElecMeters(self,ip='',port='',addr=''):
        if self.db:
            if ip != '' and port != '' and addr !='':
                self.db.devices.remove({'ip':ip,'port':str(port),'addr':str(addr),'manufacturer':"TEMP"})
                if DEBUG: print dbgIDF+"The %s %s %s Elec Meter is DELETED!!!!"%(ip,str(port),str(addr))
                return True
            elif ip != '' and port != '':
                self.db.devices.remove({'ip':ip,'port':str(port),'manufacturer':"TEMP"})
                if DEBUG: print dbgIDF+"The %s %s Elec Meters are DELETED!!!!"%(ip,str(port))
                return True                
            elif ip != '':
                self.db.devices.remove({'ip':ip,'manufacturer':"TEMP"})
                if DEBUG: print dbgIDF+"The IP %s Elec Meters are DELETED!!!!"%(ip)
                return True
            else:                
                self.db.devices.remove({'manufacturer':"TEMP"})
                if DEBUG: print dbgIDF+"All the Elec Meters are DELETED!!!!"
                return True


        else:
            if DEBUG: print dbgIDF+"Elec Meters DELETE ERR:",False
            return False  

    def updateElectroResults(self, **data):
        ''' update Electro Meter Results '''
        if self.db:
           
            # return self.db.results.update({
            return self.db.devices.update({                
                'manufacturer':IDFElec,
                'ip':data['ip'],
                'port':str(data['port']),
                'addr':str(data['addr']),
                'type':data['type']
                },{
                '$set':{
                'value':data['value'],
                'state':'ok'
                }})


    def  setElectroMeterState(self,**data):
        ''' set Electro Meter State '''
        if self.db:
            return self.db.devices.update({
                'manufacturer':IDFElec,
                'ip':data['ip'],
                'port':str(data['port']),
                'addr':str(data['addr']),
                'type':data['type']
                },{
                '$set':{
                'state':data['state']
                }})
        else:
            if DEBUG: dbgIDF+"NO Database!"
            return False


# ----------------------------------------------------
#  Function of the TempMeters 
# ----------------------------------------------------

    def findTempRepeater(self, ip='130.139.200.48', port='10001',addr='000000000108'):
        ''' find Temp Repeater for wireless temp sensors '''
        if self.db:
            _cursor = self.db.devices.find({'ip':ip,'port':str(port),'addr':str(addr),'manufacturer':"REPEATER"})
            if _cursor.count() == 0:
                if DEBUG: print dbgIDF+"Temp Repeater %s %s %s not FOUND"%(ip,str(port),str(addr))
                return 0
            else:
                _list = list(_cursor)
                if DEBUG: print dbgIDF+"Temp Repeater:",_list
                return _list 
        else:
            if DEBUG: print dbgIDF+"Temp Repeater:",False
            return False

    def readTempRepeaterPointer(self, ip='130.139.200.48', port='10001',addr='000000000108'):
        ''' Read temp Repeater Pointer '''
        if self.db:
            _cursor = self.db.devices.find({'ip':ip,'port':str(port),'addr':str(addr),'manufacturer':"REPEATER"})
            if _cursor.count() == 0:
                if DEBUG: print dbgIDF+"Temp Repeater %s %s %s not FOUND"%(ip,str(port),str(addr))
                return False
            else:
                _list = list(_cursor)
                if DEBUG: print dbgIDF+"Temp Repeater:",_list
                return _list[0]['value']
        else:
            if DEBUG: print dbgIDF+"Temp Repeater:",False
            return False            


    def updateTempRepeaterResult(self, ip='130.139.200.48', port='10001',addr='000000000108', value='000100'):
        ''' update Temp Repeater Result '''
        if self.db:
           
            # return self.db.results.update({
            return self.db.devices.update({                
                'manufacturer':'REPEATER',
                'ip':ip,
                'port':str(port),
                'addr':str(addr),
                'type':'repeater'
                },{
                '$set':{
                'value':value,
                'state':'ok'
                }})


    def findTempMeters(self, ip='',port='',addr=''):
        ''' find temp meter Modules '''
        if self.db:
            _cursor = self.db.devices.find({'ip':ip,'port':str(port),'addr':str(addr),'type':"temp"})
            if _cursor.count() == 0:
                if DEBUG: print dbgIDF+"Temp Meters %s %s %s not FOUND"%(ip,str(port),str(addr))
                return 0
            else:
                _list = list(_cursor)
                if DEBUG: print dbgIDF+"Temp Meters:",_list
                return _list
        else:
            if DEBUG: print dbgIDF+"Temp Meters:",False
            return False

    def newTempMeter(self, data={}):
        ''' And New Temp Meters '''
        if self.db:
            if len(data)>0:
                self.db.devices.save(data)
                if DEBUG: print dbgIDF+"The NEW Temp Meters Saved!!!!"
                return True
            else:
                if DEBUG: print dbgIDF+"Temp Meters data is Empty!!!"
                return False
        else:
            if DEBUG: print dbgIDF+"Temp Meters:",False
            return False


    def listTempMeters(self, allSDS=True, allMods=True):
        ''' List Temp Meters '''
        TempMeterDict={}
        if self.db:
            sdsMods = self.readSdsMods()
            for sds in sdsMods:
                _list = list(self.db.devices.find({'ip':sds['ip'],'port':sds['port'],'type':"temp"},{'type':1,'addr':1,'_id':0}).sort('addr'))

                if allSDS or len(_list)>0:
                    TempMeterDict[(sds['ip'],sds['port'])]=_list

        return TempMeterDict


    def removeTempMeters(self,ip='',port='',addr=''):
        if self.db:
            if ip != '' and port != '' and addr !='':
                self.db.devices.remove({'ip':ip,'port':str(port),'addr':str(addr),'type':"temp"})
                if DEBUG: print dbgIDF+"The %s %s %s Temp Meter is DELETED!!!!"%(ip,str(port),str(addr))
                return True
            elif ip != '' and port != '':
                self.db.devices.remove({'ip':ip,'port':str(port),'type':"temp"})
                if DEBUG: print dbgIDF+"The %s %s Temp Meters are DELETED!!!!"%(ip,str(port))
                return True                
            elif ip != '':
                self.db.devices.remove({'ip':ip,'type':"temp"})
                if DEBUG: print dbgIDF+"The IP %s Temp Meters are DELETED!!!!"%(ip)
                return True
            else:                
                self.db.devices.remove({'type':"temp"})
                if DEBUG: print dbgIDF+"All the Temp Meters are DELETED!!!!"
                return True


        else:
            if DEBUG: print dbgIDF+"Temp Meters DELETE ERR:",False
            return False  

    def updateTempMeterResults(self, **data):
        ''' update Temp Meter Results '''
        if self.db:
           
            # return self.db.results.update({
            return self.db.devices.update({                
                'manufacturer':'WIRELESS',
                'ip':data['ip'],
                'port':str(data['port']),
                'addr':str(data['addr']),
                'type':'temp'
                },{
                '$set':{
                'value':data['value'],
                'state':'ok'
                }},upsert=True)


    def  setTempRepeaterState(self,**data):
        ''' set Temp Repeater State '''
        if self.db:
            return self.db.devices.update({
                'manufacturer':'REPEATER',
                'ip':data['ip'],
                'port':str(data['port']),
                'addr':str(data['addr']),
                'type':data['type']
                },{
                '$set':{
                'state':data['state']
                }})
        else:
            if DEBUG: dbgIDF+"NO Database!"
            return False

#--------------------------------------------------
#   Results and Values functions
#--------------------------------------------------

    def readValues(self,name=''):
        ''' Read Values '''
        if self.db:
            if name=='':
                values = list(self.db.values.find())
            else:
                values = list(self.db.values.find({"name":name}))
            if DEBUG: print dbgIDF+"Values:",values
            return values
        else:
            if DEBUG: print dbgIDF+"Values:", False
            return False

    def readResults(self):
        """ Read Results """
        if self.db:
            return list(self.db.Results.find())
        else:
            return None

    def readVars(self, contxt=None):
        ''' Read Vars '''
        if self.db:

            if contxt == None:
                vars = self.db.Vars.find().sort('Name')
            else:
                vars = self.db.Vars.find(contxt).sort('Name')

            varlist = []
            for var in vars:
                varlist.append(var)
            return varlist
        else:
            return False

    def setVarsMethod(self):
        ''' set Vars Method '''
        if self.db:
            for var in self.vars:
                var['Method'] = None
                self.db.Vars.save(var)
            return True
        else:
            return False

    def setVarsAddr(self):
        if self.db:
            vars = self.db.Vars.find()
#            print meters

            for var in vars:
                addr = var['Addr'].split('-')

                if addr[2] == '000011029707':

                    var['Addr'] = addr[0] + '-' + addr[1] + '-' + '000011029785' + '-' + addr[3]
                    print addr, var['Addr']
#                    meter['IP'] = '192.168.192.13'

                self.db.Vars.save(var)

            return True
        else:
            return False

    def setVarsStore(self, on=False, collection=None, period=10):
        ''' set Vars whether is Stored '''
        if self.db:
            if collection == None:
                for var in self.vars:
                    var['StoreON'] = on
                    var['Period'] = period
                    self.db.Vars.save(var)
                return True
            else:
                for var in collection:
                    var['StoreON'] = on
                    var['Period'] = period
                    self.db.Vars.save(var)
                return True
        else:
            return False

    def setVarsRate(self, rate=1, collection=None):
        ''' set Vars value rate. The default rate is [1]. '''
        if self.db:
            if collection == None:
                for var in self.vars:
                    var['Rate'] = rate
                    self.db.Vars.save(var)
                return True
            else:
                for var in collection:
                    var['Rate'] = rate
                    self.db.Vars.save(var)
                return True
        else:
            return False


    def setElecMeterRatio(self):
        ''' set Elecicity Meter Ratio '''
        if self.db:
            meters = self.db.ElecMeters.find()

            for meter in meters:
                meter['Ratio'] = "200:5"
                self.db.ElecMeters.save(meter)

            return True
        else:
            return False

    def setElecMeterType(self):
        ''' set Electricity Meter Type '''
        if self.db:
            meters = self.db.ElecMeters.find()

            for meter in meters:
                meter['Type'] = '380'
                self.db.ElecMeters.save(meter)

            return True
        else:
            return False

    def setElecMeterAddr(self):
        ''' set Electricity Meter Address '''
        if self.db:
            meters = self.db.ElecMeters.find()
#            print meters

            for meter in meters:
                print meter
                if meter['IP'] == '192.168.192.78':
                    meter['IP'] = '192.168.192.13'

                self.db.ElecMeters.save(meter)

            return True
        else:
            return False

    def setElecMeterComment(self):
        if self.db:
            import re
            rexp = re.compile('/^e.*[^R]P/')
            metervars = self.db.Vars.find({'Name':rexp})

            for metervar in metervars:
                print metervar


    def removeElecMeterField(self, fieldname):
        ''' remove Electricity Meter field '''
        if self.db:
            meters = self.db.ElecMeters.find()

            for meter in meters:
                meter.pop(fieldname)
                self.db.ElecMeters.save(meter)

            return True
        else:
            return False

    def removeSipaiModsField(self, fieldname):
        ''' remove SipaiMods field '''
        if self.db:
            mods = self.db.SipaiMods.find()

            for mod in mods:
                mod.pop(fieldname)
                self.db.SipaiMods.save(mod)

            return True
        else:
            return False

    def renameVarsField(self, oldname, newname):
        if self.db:
            for var in self.vars:
                var[newname] = var[oldname]
                var.pop(oldname, None)
                self.db.Vars.save(var)
            return True
        else:
            return False

    def renameElecMeterField(self, oldname, newname):
        if self.db:
            meters = self.db.ElecMeters.find()

            for meter in meters:
                meter[newname] = meter[oldname]
                meter.pop(oldname, None)
                self.db.ElecMeters.save(meter)
            return True
        else:
            return False


    def setVarsClass(self):
        if self.db:
            for var in self.vars:
                name = var['Name']
                varClass = var['VarClass']
                if varClass == 'e11':
                    newClass = "e11F"
                    var['VarClass'] = newClass
                    print var['VarClass']
                self.db.Vars.save(var)
            return True
        else:
            return False

    def getVarsClass(self):
        if self.db:
#            varclasses = self.db.Vars.group(['VarClass'], None, {'list':[]}, 'function(obj, prev) {prev.list.push(obj)}')
            varclasses = self.db.Vars.group(['VarClass'], None, {'list':[]}, 'function(obj, prev) {}')
            classlist = []
            for vc in varclasses:
                classlist.append(vc['VarClass'])
#                print vc['VarClass'], len(vc['list'])
            classlist.sort()
            return tuple(classlist)
        else:
            return False

    def propertylist(self):
        if self.db:
            for varclass in self.varClass:
                print "------ Class Name: %s -----" % varclass
                vars = self.db.Vars.find({'VarClass':varclass}, {'Name':1, 'Value':1})
                for var in vars:
                    if type(var['Value']) == type(True): print 'property bool ' + var['Name']
                    else: print 'property double ' + var['Name']

        else:
            return False


    # 13.12.20
    def getDevices(self):
        if self.db:
            deviceDict={}
            devices = list(self.db.devices.find({
                'manufacturer':{'$in':[IDFElec,IDFSipai]}
                },{
                '_id':1,
                'ip':1,
                'port':1,
                'addr':1,
                'type':1
                }))
            for device in devices:
                deviceDict[device['ip'],device['port'],device['addr'],device['type']]=device['_id']
            return deviceDict
        else:
            return False


    def getVars(self):
        if self.db:
            vars = self.db.vars.find({},{
                'name':1,
                'addr':1,
                'calc':1,
                'calc2':1,
                'max_value':1,
                'min_value':1,
                'hl_value':1,
                'll_value':1,
                '_id':1
                }).sort('addr')
            return list(vars)
        else:
            return False


    def getVarsValue(self):
        if self.db:
            vars = self.db.vars.find({},{
                # 'name':1,
                # 'addr':1,
                # 'calc':1,
                # 'max_value':1,
                # 'min_value':1,
                # 'hl_value':1,
                # 'll_value':1,
                '_id':1,
                'cur_value':1,
                'sum_value':1,
                'vars_id':1
                }).sort('addr')
            return list(vars)
        else:
            return False


    def getDeviceValue(self, **args):
        # ip=_ip, port=_port, maddr=_maddr, types=_types, channel=_channel
        # print "----args----->",args
        if self.db:
            results ={}
            for type in args['types']:
                _r = list(self.db.devices.find({
                    'ip':args['ip'],
                    'port':args['port'],
                    'addr':args['maddr'],
                    'type':type,
                    },{
                    'value':1,
                    '_id':1
                    }))
                if len(_r)>0 and _r[0]['value']:
                    # print '----- _r ------>',_r
                    # if type(_r[0]['value'])==type('string'):
                    #     resultvalues = _r[0]['value'].split(',')
                    #     results[type]=resultvalues[args['channel']]
                    # else:
                    #     resultvalues = _r[0]['value']
                    resultvalues = str(_r[0]['value']).split(',')
                    results[type]=resultvalues[args['channel']]
                else:
                    results[type]=''

            return results
        else:
            return False


    def updateVarsValue(self, **args):
        ''' update Vars Value '''
        if self.db:
            # print args
            return self.db.vars.update({
                # 'addr': args['addr']
                '_id': args['_id']
                },{
                '$set':{
                'org_value':args['org_value'],
                'cur_value':args['cur_value'],
                'sum_value':args['sum_value']
                }})
        else:
            return False


    def updateValuesInHistory(self):
        if self.db:
            collectionNames = self.db.collection_names()

            for collectionName in collectionNames:
                if collectionName[:2] == 'H_':
                    print '>>> Now collection is %s!!'%collectionName
                    lists = self.db[collectionName].find()
                    for li in lists:
                        # print li['_id'], li['value']
                        try:
                            va = float(li['value'])
                        except:
                            va =0
                        self.db[collectionName].update({
                            '_id': li['_id']
                            },{
                            '$set':{
                            'value':va
                            }})
                    

        else:
            return False

#    def updateVarsValue(self):
#        ''' Update Vars '''
#        t1 = time.clock()
#        if self.db:
#            results = self.db.Results.find()
#            result = results[0]
#
#            for var in self.vars:
#                addr = var['Addr']
#                if var['Method'] == None: var['Value'] = result[addr]
#                else:
#                    try:
#                        _c = var['Method'].replace('x', 'result[addr]')
#                        var['Value'] = eval(_c)
#                    except:
#                        var['Value'] = result[addr]
#
##                print var['Name'], ':', var['Value']
#                self.db.Vars.save(var)
#
#            t2 = time.clock()
#            if ECHO: print (t2 - t1)
#            return True
#        else:
#            return False


def Test():
    import re
    """ Main program """
    print " ---- start Initialization ----"

    # Modify the mongoUrl configuration in config.py
    myDB = MyDB()
    
    # test functions
    myDB.collectionNames()
    # myDB.readSipaiMods()
    # myDB.readSdsMods()
    # myDB.readValues(re.compile('^.*2$'))
    # myDB.updateValuesInHistory()

    # print "-----------------------------------"
    # print myDB.setupSipaiResults()
    # print myDB.updateSipaiResults(
    #             ip='130.139.200.50',
    #             port="6020",
    #             addr='40',
    #             value=b2a_hex("\x30\x60\x09\x55\x30\x60\x09\x55\x30\x60\x09\x55\x30\x60\x09\x55")
    #             )

    # print myDB.readSipaiResult(
    #             ip='130.139.200.50',
    #             port="6020",
    #             addr='40',
    #     )

    # print myDB.db.vars.update({},
    #     {
    #     '$set':{
    #     # 'storeOn':True,
    #     # 'go_value':0
    #     'calc2':'1'
    #     }},   
    #     multi=True
    #     )

    # print myDB.updateTempRepeaterResult(
    #     ip='130.139.200.48',
    #     port= '10001',
    #     addr= '000000000108',
    #     value='0010000'
    #     )
    


#     print 'Vars Class:', myDB.varClass
#     rexp1 = re.compile('^wS[^H].*[^A]$')
# #    rexp2 = re.compile('RP')
#     tm = myDB.readVars(contxt={'Name':rexp1})
#     for t in tm:
# #        t['Rate'] = 1
#         print 'property real %s_b: %0.2f//%s' % (t['Name'], t['Value'] * t['Rate'] / 1000, t['Comment'])
# #        t['StoreON'] = False
# #        myDB.db.Vars.save(t)
# #    myDB.setVarsStore(True, tm)
# #    myDB.renameVarsField(oldname='VarType', newname='VarClass')
# #    myDB.setVarsClass()
# #    myDB.setVarsAddr()
# #    myDB.setElecMeterRatio()
# #    myDB.setElecMeterType()
# #    myDB.setElecMeterAddr()
# #    myDB.setElecMeterComment()
# #    myDB.removeElecMeterField(fieldname='AMP')
# #    myDB.removeSipaiModsField(fieldname='DATACODE')
# #    sss = myDB.db.Vars.find({}, {'VarClass':1})
# #    myDB.db.ElecMeters.remove({"MODTYPE":{'$ne':None}})
# #    myDB.renameElecMeterField(oldname='ADDRESS', newname='ADDRESS')
# #    myDB.propertylist()
    print " ---- end Initialization ----"

if __name__ == "__main__":
    Test()

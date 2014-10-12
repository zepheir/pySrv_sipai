#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2014-10-12
 
@author: Samuel Gao

'''

import sys

import config
from config import *

import myDB

from myDB import MyDB

SDSName = 'sds'
_SDS = 'Serial Device Servers'

# ----------------------------------------------------------
class SdsDB(MyDB):
	"""docstring for SdsDB"""
	def __init__(self):
		super(SdsDB, self).__init__()
	

	def readMods(self):
		''' Read Serial Device Servers '''
		if self.db:
			mods = list(self.db.devices.find({"type":SDSName}).sort('ip'))
			# if DEBUG: print dbgIDF+"Serial Device Servers:",mods
			return mods
		else:
			if DEBUG: print dbgIDF+_SDS+":",False
			return False


	def findMods(self, ip='',port=''):
		''' find Serial Device Servers '''
		if self.db:
			_cursor = self.db.devices.find({'ip':ip,'port':str(port),'type':SDSName})
			if _cursor.count() == 0:
				if DEBUG: print dbgIDF+_SDS+" %s %s not FOUND"%(ip,str(port))
				return 0
			else:
				_list = list(_cursor)
				if DEBUG: print dbgIDF+_SDS+":",_list
				return _list
		else:
			if DEBUG: print dbgIDF+_SDS+":",False
			return False


	def newMods(self, data={}):
		if self.db:
			if len(data)>0:
				self.db.devices.save(data)
				if DEBUG: print dbgIDF+"The NEW %s Saved!!!!"%_SDS
				return True
			else:
				if DEBUG: print dbgIDF+_SDS+" data is Empty!!!"
				return False
		else:
			if DEBUG: print dbgIDF+_SDS+":",False
			return False


	def removeMods(self,ip='',port=''):
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




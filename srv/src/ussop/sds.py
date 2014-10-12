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

# ----------------------------------------------------------
class SdsDB(MyDB):
	"""docstring for SdsDB"""
	def __init__(self):
		super(SdsDB, self).__init__()
	

	# def readMods(self):
	# 	if self.db:
			



#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-11-19

@author: Samuel Gao

Modified date: 2014-09-17

Project Name: SIPAI R8 Building data sample server program

Samuel Gao
'''
# General setup
ECHO = True
DEBUG = True

SERVERRECONNECT = True

dbgIDF = " ==> "


IDFSDS = "HLH"
IDFSipai = "SIPAI"
IDFElec = "DAHUA"
IDFTemp = 'WIRELESS'
IDFRepeater = 'REPEATER'


# Server setup
serverIP = '132.120.136.151'

# Serial Device Server setup
SDSName1 = 'sds'
SDSIPFrom = '132.120.136.155'
SDSIPEnd = '132.120.136.165'
SDSPort1 = 10001
SDSPort2 = 10002


# Database setup
# MongoDB configuration 
databaseIP = '127.0.0.1'
databasePort = '27017'
databaseUser = 'root'
databasePWD = 'qiqiqi'
mongoURL = 'mongodb://'+databaseUser+':'+databasePWD+'@'+databaseIP+':'+databasePort


# -------------------------------------------------
# SipaiServer & ElectroServer
# -------------------------------------------------
if SERVERRECONNECT:
    SipaiSampleTimer = 10
    ElectroMeterTimer = 60
    TempMeterTimer = 60*5
    RepeaterTimer = 60
else:
    SipaiSampleTimer = 5
    ElectroMeterTimer = 30
    TempMeterTimer = 60*5
    RepeaterTimer = 60
    
SdsConnectTimer = 2

SIPAIMODS = ('1001','1001a','1020','1020a','1030','1040','1042','1042a','1043','1043a')
SIPAIDOUBLEMODS=('1001','1020','1042','1043')

ELECTROMODS = ('power','voltage','current','cos','reactive','total')

# -------------------------------------------------
# result Console 
# -------------------------------------------------
RESULT_REFRESH_TIMER = 1


# -------------------------------------------------
# history Console
# -------------------------------------------------
HISTORY_TIMEBASE = False

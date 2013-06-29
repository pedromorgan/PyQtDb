# -*- coding: utf-8 -*-

import json

from PyQt4 import QtGui, QtCore, QtSql
from PyQt4.QtCore import Qt





class XSettings(QtCore.QSettings):
	
	NS = "PYQTDB"
	SERVERS = NS + "_ssssserverss"
	
	
	def __init__( self, parent=None ):
		QtCore.QSettings.__init__( self, parent )
		
		## Sanity Checks
		if not self.contains(self.SERVERS):
			self.setValue(self.SERVERS, json.dumps({"servers":{}}))
			self.sync()
			
	def get_servers_dic(self):
		qt_str = self.value(self.SERVERS).toString()
		return json.loads( str(qt_str) )['servers']
		
	def get_servers_list(self):
		servers = self.get_servers_dic()
		return [servers[ki] for ki in servers.keys()]
	
	def get_server(self, server):
		
		servers = self.get_servers_dic()
		if not server in servers:
			return None
		return servers[server]
		
	def save_server(self, dic):
		
		qt_str = self.value(self.SERVERS).toString()
		data =  json.loads( str(qt_str) )
		data['servers'][ dic['server'] ] = dic
		s = json.dumps(data)
		print data, s
		print type(s)
		self.setValue(self.SERVERS, s )	
		self.sync()
	
		
		
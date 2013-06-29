# -*- coding: utf-8 -*-

import os
from PyQt4 import QtGui, QtCore


class Ico:
	"""Icons Definition and Loader
	
	  - All icons used are listed as class constants.
	  - Static methods create icons loaded from the file system
	"""
	"""
	@staticmethod
	def get(name, pixmap=False):
		if name[0:3] == "ico":
			name = name[3:]
		s = dIco.__dict__[name]
		if pixmap:
			return dIco.icon(s, pixmap)
		return s
	"""	
	
	@staticmethod
	def icon( file_name, pixmap=False):
		"""Create a new QIcon
		@param file_name: Icon filename to load
		@type file_name: str or L{dIco} attribute
		@param pixmap: Return a pixmap instead of icon object
		@type pixmap: bool
		@return: new Icon
		@rtype: QIcon or pixmap
		"""
		if file_name == None:
			icon = QtGui.QIcon()
		else:
			img_dir = os.path.dirname( __file__ ) + '/images/icons/'
			img_path = img_dir + file_name
			icon = QtGui.QIcon( img_path )
		if pixmap:
			return icon.pixmap( QtCore.QSize( 16, 16 ) )
		return icon
	
	Cancel = "bullet_black.png"
	Save = "accept.png"
	#JobAll = 'geo_default.png'
	
	Servers = "server_database.png"
	Server = 'server.png'
	ServerAdd = 'server_add.png'
	ServerDelete = 'server_delete.png'
	ServerEdit = 'server_edit.png'
	ServerConnect = 'server_connect.png'
	
	#Jobs = 'page_copy.png'
	


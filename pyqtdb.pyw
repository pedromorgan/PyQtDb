#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Peter Morgan <pete@daffodil.uk.com>
"""

import sys
from PyQt4 import QtGui, QtCore

import pyqtdb.DBMainWindow

 
if __name__ == '__main__':


	app = QtGui.QApplication( sys.argv )

	
	splashScreen = pyqtdb.DBMainWindow.show_splash()

	app.processEvents()


	QtGui.QApplication.setOrganizationName( "Daffodil" )
	QtGui.QApplication.setOrganizationDomain( "daffodil.github.com" )
	QtGui.QApplication.setApplicationName( "PyQtDb" )
	QtGui.QApplication.setApplicationVersion( "0.1" )
		

	window = pyqtdb.DBMainWindow.DBMainWindow()

	splashScreen.finish( window )
	window.show()

	sys.exit( app.exec_() )


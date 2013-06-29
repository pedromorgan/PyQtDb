# -*- coding: utf-8 -*-


from PyQt4 import QtGui, QtCore, QtSql
from PyQt4.QtCore import Qt

from . import DBServersWidget


def show_splash():

	splashImage = QtGui.QPixmap( "../images/corp/splash.png" )
	splashScreen = QtGui.QSplashScreen( splashImage )
	splashScreen.showMessage( "Loading . . . " )
	splashScreen.show()
	return splashScreen

class MainWindow(QtGui.QMainWindow):


	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)

		self.debug = False
		
		self.db = None
		
		self.setWindowTitle("PyQtDb")

		self.setMinimumWidth(800)
		self.setMinimumHeight(800)
		
		topBar = QtGui.QToolBar()
		self.addToolBar(Qt.TopToolBarArea, topBar)
		
		topBar.addAction("New Server")
		
		
		self.dockServers = QtGui.QDockWidget("Servers")
		self.dockServers.setFeatures(QtGui.QDockWidget.DockWidgetMovable)
		self.dockServers.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
		self.addDockWidget(Qt.LeftDockWidgetArea, self.dockServers)
		
		self.serversWidget = DBServersWidget.DBServersWidget(self)
		self.dockServers.setWidget(self.serversWidget)

		self.cenWid = QtGui.QWidget()
		self.setCentralWidget(self.cenWid)
		
		self.mainLayout = QtGui.QHBoxLayout()
		self.mainLayout.setContentsMargins(0, 0, 0, 0)
		self.mainLayout.setSpacing(0)
		self.cenWid.setLayout( self.mainLayout )
		
		self.tabWidget = QtGui.QTabWidget()
		self.mainLayout.addWidget(self.tabWidget)
		
		
		
		
	
	
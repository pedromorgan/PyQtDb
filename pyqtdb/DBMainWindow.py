# -*- coding: utf-8 -*-


from PyQt4.QtGui import  QMainWindow, QDockWidget, QPixmap, QSplashScreen, QToolBar, QWidget, QHBoxLayout, QTabWidget
from PyQt4.QtCore import Qt, SIGNAL

import DBServersWidget
import DBBrowser
from img import Ico
import app_globals as G

def show_splash():
    """Show the splash screen"""
    splashImage = QPixmap( "images/splash.png" )
    splashScreen = QSplashScreen( splashImage )
    splashScreen.showMessage( "Loading . . . " )
    splashScreen.show()
    return splashScreen

class DBMainWindow(QMainWindow):
    """Main Window and Portal
    
    .. todo:: Remember the dock position
    """
    
    W_NAME =  "DBMainWindow"

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        
        
        self.db = None
        
        self.setWindowTitle("PyQtDb")
        self.setWindowIcon(Ico.icon(Ico.FavIcon))

        self.setMinimumWidth(800)
        self.setMinimumHeight(800)
        
        """
        topBar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, topBar)
        
        topBar.addAction("New Server")
        """
        
        ## Servers Widget
        self.dockServers = QDockWidget("Servers")
        self.dockServers.setFeatures(QDockWidget.DockWidgetMovable)
        self.dockServers.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockServers)
        
        self.serversWidget = DBServersWidget.DBServersWidget(self)
        """Instance of :py:class:`~pyqtdb.DBServersWidget.DBServersWidget` in dock"""
        self.dockServers.setWidget(self.serversWidget)
        self.connect(self.serversWidget, SIGNAL("open_server"), self.on_open_server)

        self.cenWid = QWidget()
        self.setCentralWidget(self.cenWid)
        
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.cenWid.setLayout( self.mainLayout )
        
        self.tabWidget = QTabWidget()
        """The main tabs"""
        self.tabWidget.setTabsClosable(True)
        self.mainLayout.addWidget(self.tabWidget)
        
        G.settings.restore_window(self)
        
    def on_open_server(self, srv):
        """Opens server by adding a :py:class:`~pyqtdb.DBBrowser.DBBrowser` in the the tabWidget"""
        server = G.settings.get_server( str(srv) )
        print "oopen", srv, server
        widget = DBBrowser.DBBrowser(self, server)
        self.tabWidget.addTab(widget, Ico.icon(Ico.Server), server['server'])
        self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(widget))
    
    def closeEvent( self, event ):
        """Save window settings on close with :py:class:`~pyqtdb.XSettings.XSettings.save_window` """ 
        G.settings.save_window( self )
        
        
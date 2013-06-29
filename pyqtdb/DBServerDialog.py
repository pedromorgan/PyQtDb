# -*- coding: utf-8 -*-


from PyQt4.QtGui import QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, \
                        QLabel, QComboBox, QLineEdit, QPushButton
from PyQt4.QtCore import Qt, SIGNAL

from img import Ico
import app_globals as G



class DBServerDialog(QDialog):
    """Edit a Server entry"""

    def __init__(self, parent=None, server=None):
        QDialog.__init__(self, parent)
        
        self.setWindowTitle("Server")
        self.setWindowIcon(Ico.icon(Ico.ServerEdit if server else Ico.ServerAdd))
        

        m = 20
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(m, m, m, m)
        #self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)
        
        self.grid = QGridLayout()
        self.mainLayout.addLayout(self.grid)
      
        #= Engine
        row = 0
        self.grid.addWidget(QLabel("Engine:"), row, 0, Qt.AlignRight)
        self.comboEngine = QComboBox()
        """Datebase engine selector"""
        self.grid.addWidget(self.comboEngine, row, 1, 1, 3)
        self.comboEngine.addItem("QMYSQL")
          
        #= Server
        row  += 1
        self.grid.addWidget(QLabel("Server Host:"), row, 0, Qt.AlignRight)
        self.txtServer = QLineEdit()
        """Server host"""
        self.grid.addWidget(self.txtServer, row, 1, 1, 3)
        
        #= Port
        row += 1
        self.grid.addWidget(QLabel("Server Port:"), row, 0, Qt.AlignRight)
        self.txtPort = QLineEdit()
        """Port No"""
        self.txtPort.setText("3306")
        self.grid.addWidget(self.txtPort, row, 1, 1, 1)
        # @todo make this only iintegers ?
        
        row += 1
        self.grid.addWidget(QLabel("User Login:"), row, 0, Qt.AlignRight)
        self.txtUser = QLineEdit()
        """Username"""
        self.grid.addWidget(self.txtUser, row, 1, 1, 2)
        
        row += 1
        self.grid.addWidget(QLabel("Password:"), row, 0, Qt.AlignRight)
        self.txtPasswd = QLineEdit()
        """Password"""
        self.grid.addWidget(self.txtPasswd, row, 1, 1, 2)
        
        
        row += 1
        self.lblTest = QLabel("Test")
        self.grid.addWidget(self.lblTest, row, 0, 1, 2, Qt.AlignRight)
        self.buttTest = QPushButton()
        self.buttTest.setText("Test")
        self.buttTest.setIcon(Ico.icon(Ico.ServerConnect))
        self.grid.addWidget(self.buttTest, row, 2, 1, 1)
        self.connect(self.buttTest, SIGNAL("clicked()"), self.on_test)
        
        
        buttonBox = QHBoxLayout()
        buttonBox.addStretch(10)
        self.mainLayout.addLayout(buttonBox)
        
        buttCancel = QPushButton()
        buttCancel.setText("Cancel")
        buttCancel.setIcon(Ico.icon(Ico.Cancel))
        buttonBox.addWidget(buttCancel)
        self.connect(buttCancel, SIGNAL("clicked()"), self.reject)
        
        self.buttSave = QPushButton()
        self.buttSave.setText("Save")
        self.buttSave.setIcon(Ico.icon(Ico.Save))
        buttonBox.addWidget(self.buttSave)
        self.connect(self.buttSave, SIGNAL("clicked()"), self.on_save)
    
        if server:
            data = G.settings.get_server(server)
            if data:
                self.txtServer.setText(data['server'])
                self.txtPort.setText(data['port'])
                self.txtUser.setText(data['user'])
                self.txtPasswd.setText(data['passwd'])
    
                
    def on_test(self):
        print "TODO", "self.on_test"
        
        
    def on_save(self):
        """Save server settings 
        
        Creates a :py:func:`dict` and 
        passes to  :py:meth:`~pyqtdb.XSettings.XSettings.save_server` 
        instance :py:`~pyqtdb.app_globals.settings`
        """	
        data_dic = dict(server = str(self.txtServer.text()), 
                        port=str(self.txtPort.text()),
                        user=str(self.txtUser.text()), 
                        passwd=str(self.txtPasswd.text()))
        G.settings.save_server(	data_dic )
        
        self.accept()
    
        


# -*- coding: utf-8 -*-


from PyQt4.QtGui import QMainWindow, QToolBar, QTreeWidget, QTreeWidgetItem, QAbstractItemView, QTreeView, QWidget, QHBoxLayout 
from PyQt4.QtCore import Qt, SIGNAL



class DBBrowser(QMainWindow):


    def __init__(self, parent, server):
        QMainWindow.__init__(self, parent)

        self.debug = False
        self.server = server
        
        self.db = None
        
        self.setWindowTitle("Database Browser")
        #s#elf.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)


        topBar = QToolBar()
        
        self.addToolBar(Qt.TopToolBarArea, topBar)
        
        

        self.cenWid = QWidget()
        self.setCentralWidget(self.cenWid)
        
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.cenWid.setLayout( self.mainLayout )

        
        
        self.treeTables = QTreeWidget()
        self.mainLayout.addWidget(self.treeTables, 1)
        self.treeTables.setHeaderLabels(["Table"])
        self.treeTables.setSelectionBehavior( QAbstractItemView.SelectRows )
        self.treeTables.setSelectionMode( QTreeView.SingleSelection )
        self.connect( self.treeTables, SIGNAL( 'itemSelectionChanged()' ), self.on_table )
        
        
        self.treeColumns = QTreeWidget()
        self.mainLayout.addWidget(self.treeColumns, 4)
        self.treeColumns.setHeaderLabels(["Column", "Type", "Nullable"])
        
        
        
        #self.fetch()
        
    def on_table(self):
        item = self.treeTables.currentItem()
        if item == None:
            return
        self.fetch( table = str(item.text(0)) )
        
    def fetch(self, table=None):
        
        s_vars = {}
        
        if table:
            url = "/dev0/db/table/%s" % table
            self.treeColumns.clear()
        else:
            url = "/dev0/db/tables"
        
        server = dServerCall( self )
        self.connect( server, QtCore.SIGNAL( 'dataReady' ), self.load_data )
        server.action( url, s_vars, None, True )
        
        
    def load_data(self, data):
        
        
        if "tables" in data:
            
            self.treeTables.clear()
            for t in data['tables']:
                item = TreeWidgetItem()
                item.setText(0, t['table'])
                self.treeTables.addTopLevelItem(item)

        else:
            self.treeColumns.clear()
            for t in data['columns']:
                item = TreeWidgetItem()
                item.setText(0, t['column'])
                item.setText(1, t['type'])
                item.setText(2, "Yes" if t['nullable'] else "-")
                self.treeColumns.addTopLevelItem(item)
                
                
        
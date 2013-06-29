# -*- coding: utf-8 -*-


from PyQt4.QtGui import QWidget, QVBoxLayout, QToolBar, QTreeWidget, QTreeWidgetItem, \
                        QToolButton, QButtonGroup, QHeaderView

from PyQt4.QtSql import QSqlDatabase, QSqlQuery
from PyQt4.QtCore import Qt, SIGNAL

from . import DBServerDialog


from img import Ico

import app_globals as G
#
class C:
    node = 0
    butt = 1
    #widget = 2



class DBServersWidget(QWidget):
    """Displays a list of servers"""

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.debug = False
        
        self.connections = {}
        
        self.setWindowTitle("Servers")
        #s#elf.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)

        #=============================================
        ## Top Toolbar
        topBar = QToolBar()
        topBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.mainLayout.addWidget(topBar)
        
        ## Add the action buttons
        topBar.addAction(Ico.icon(Ico.ServerAdd), "Add", self.on_server_add)
        self.actionServerEdit = topBar.addAction(Ico.icon(Ico.ServerEdit), "Edit", self.on_server_edit)
        self.actionServerDelete = topBar.addAction(Ico.icon(Ico.ServerDelete), "Delete", self.on_server_delete)
        
        #=============================================
        ## Tree
        self.tree = QTreeWidget()
        self.mainLayout.addWidget(self.tree)
        self.tree.setUniformRowHeights(True)
        self.tree.setRootIsDecorated(True)
        
        
        self.tree.setHeaderLabels(["Server", "Butt"]) # set header, but hide anyway
        self.tree.header().hide()
        self.tree.header().setResizeMode(C.node, QHeaderView.Stretch)
        self.tree.setColumnWidth(C.butt, 20)
        
        
        self.connect( self.tree, SIGNAL( 'itemSelectionChanged()' ), self.on_tree_selection_changed )
        self.connect( self.tree, SIGNAL( 'itemDoubleClicked (QTreeWidgetItem *,int)' ), self.on_tree_double_clicked )
    
        self.buttGroup = QButtonGroup(self)
        self.connect(self.buttGroup, SIGNAL("buttonClicked(QAbstractButton*)"), self.on_open_server)
    
        self.on_tree_selection_changed()
    
    
        self.load_servers()
        
    #=======================================
    ##== Tree Events
    def on_tree_selection_changed(self):
        
        disabled = self.tree.selectionModel().hasSelection() == False
        self.actionServerEdit.setDisabled(disabled)
        self.actionServerDelete.setDisabled(disabled)
        
    def on_tree_double_clicked(self):
        self.actionServerEdit.trigger()


    
    #=======================================
    ## Server Actions
    def on_server_add(self):
        self.show_server_dialog(None)
        
    def on_server_edit(self):
        item = self.tree.currentItem()
        if item == None:
            return
        server = str(item.text(C.server))
        self.show_server_dialog(server)
    
    def show_server_dialog(self, server=None):
        d = DBServerDialog.DBServerDialog(self, server)
        if d.exec_():
            self.load_servers()
    

            
    
    def load_servers(self):
        """Load servers from :py:meth:`pyqtdb.XSettings.XSettings.get_servers` """
        
        self.tree.clear()
        
        for butt in self.buttGroup.buttons():
            self.buttGroup.removeButton(butt)
        
        for srv in G.settings.get_servers_list():
            
            item = QTreeWidgetItem()
            item.setText(C.node, srv['server'])
            #item.setText(C.user, srv['user'])
            self.tree.addTopLevelItem(item)
            
            butt = QToolButton()
            butt.setIcon(Ico.icon(Ico.Connect))
            butt.setProperty("server", srv['server'])
            self.tree.setItemWidget(item, C.butt, butt)
            self.buttGroup.addButton(butt)
        
        
    def on_server_delete(self):
        item = self.tree.currentItem()
        if item == None:
            return
        srv = str(item.text(C.server))
        G.settings.delete_server(srv)
        self.load_servers()
        
        
    def on_open_server(self, butt):
        
        # self.emit(SIGNAL("open_server"), butt.property("server").toString())
        srv_ki = str(butt.property("server").toString())
        server = G.settings.get_server(srv_ki)
        db = QSqlDatabase.addDatabase("QMYSQL", srv_ki)
        db.setHostName(server['server'])
        db.setUserName(server['user'])
        db.setPassword(server['passwd'])
        
        ok = db.open()
        if ok:
            #self.connections[srv_ki] = 
            self.load_databases(srv_ki)
            print "open", ok
            
            
    def load_databases(self, srv_ki):
        """Load databases into tree node for server;  executes 'show databases;' or aslike """
        
        sql = "show databases;"
        query = QSqlQuery(QSqlDatabase.database(srv_ki))
        ok = query.exec_(sql)
        print ok, sql, query.result()
        
        # Get the parent node, ie the server node
        pItem = self.tree.findItems(srv_ki, Qt.MatchExactly, C.node)[0]
        
        ## Assumed value(0) is the table.. we need the defs (ie mysql case)
        while query.next():
            table_name =  query.value(0).toString()
            nuItem = QTreeWidgetItem(pItem)
            nuItem.setText(C.node, table_name)
            #print table_name
            
            
        self.tree.setItemExpanded(pItem, True)
        
        
        
            
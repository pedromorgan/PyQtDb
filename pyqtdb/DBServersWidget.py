# -*- coding: utf-8 -*-


from PyQt4.QtGui import QWidget, QVBoxLayout, QToolBar, QTreeWidget, QTreeWidgetItem, \
                        QToolButton, QButtonGroup

from PyQt4.QtCore import Qt, SIGNAL

from . import DBServerDialog


from img import Ico

import app_globals as G
#
class C:
    """Columns enum"""
    server = 0
    user = 1
    widget = 2



class DBServersWidget(QWidget):
    """Displays a list of servers"""

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.debug = False
        
        self.db = None
        
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
        self.tree.setHeaderLabels(["Server", "User", ""])
        self.tree.setUniformRowHeights(True)
        self.tree.setRootIsDecorated(False)
        self.tree.setColumnWidth(C.widget, 20)
        
        
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
       
       
    def on_open_server(self, butt):
        self.emit(SIGNAL("open_server"), butt.property("server").toString())
              
             
    
    def load_servers(self):
        """Load servers from :py:meth:`pyqtdb.XSettings.XSettings.get_servers` """
        
        self.tree.clear()
        
        for butt in self.buttGroup.buttons():
            self.buttGroup.removeButton(butt)
        
        for srv in G.settings.get_servers_list():
            
            item = QTreeWidgetItem()
            item.setText(C.server, srv['server'])
            item.setText(C.user, srv['user'])
            self.tree.addTopLevelItem(item)
            
            butt = QToolButton()
            butt.setIcon(Ico.icon(Ico.Connect))
            butt.setProperty("server", srv['server'])
            self.tree.setItemWidget(item, C.widget, butt)
            self.buttGroup.addButton(butt)
        
        
    def on_server_delete(self):
        #d = DBServerDialog.DBServerDialog(self)
        #d.exec_()
        pass
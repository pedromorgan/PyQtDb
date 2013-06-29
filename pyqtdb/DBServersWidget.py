# -*- coding: utf-8 -*-


from PyQt4.QtGui import QWidget, QVBoxLayout, QToolBar, QTreeWidget, QTreeWidgetItem

from PyQt4.QtCore import Qt, SIGNAL

from . import DBServerDialog
from .ico import Ico

import app_globals as G
#
class C:
	server = 0
	user = 1



class DBServersWidget(QWidget):


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
		self.tree.setHeaderLabels(["Server", "User"])
		self.mainLayout.addWidget(self.tree)
		
		self.connect( self.tree, SIGNAL( 'itemSelectionChanged()' ), self.on_tree_selection_changed )
		self.connect( self.tree, SIGNAL( 'itemDoubleClicked (QTreeWidgetItem *,int)' ), self.on_tree_double_clicked )
	
	
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
		d.exec_()
			
		
	def load_servers(self):
		
		servers = G.settings.get_servers_list()
		for srv in servers:
			
			item = QTreeWidgetItem()
			item.setText(C.server, srv['server'])
			item.setText(C.user, srv['user'])
			self.tree.addTopLevelItem(item)
		
		
	def on_server_delete(self):
		#d = DBServerDialog.DBServerDialog(self)
		#d.exec_()
		pass
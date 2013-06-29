# -*- coding: utf-8 -*-

import os
import json

from PyQt4.QtCore import QSettings
from PyQt4.QtCore import Qt, QVariant, QString




class XSettings(QSettings):
    """
    This class is intended as a central place to hold the config. The idea
    is that later if can use different backends.
    
    Some data such as the server config is serialised as json (a dependancy)
    
    .. warning:: Security risk - the passwords are not encrypted
    
    .. todo:: Inplement yaml backend and json
    """
    
    
    NS = "PYQTDB"
    """Namespace prepended to all keys"""
    
    
    SERVERS = NS + "_serversss"
    """Key that hold the servers data"""
    
    def __init__( self ):
        QSettings.__init__( self )
        
        if os.environ.get('__GEN_DOCS__', None) == None:
            self.initialize()
        
        
    def initialize(self):
        """Initialise and check settings. Executed once on startup"""
        if not self.contains(self.SERVERS):
            print "ADDDDDDDDDDDDDDDDDDDDDDDDDDDddd"
            self.setValue(self.SERVERS, QVariant(json.dumps({"servers":{}})))
            self.sync()
            
    def get_servers_dic(self):
        """
        :return: A :py:func:`dict` with the server details or None if not found
        """
        qt_str = self.value(self.SERVERS).toString()
        return json.loads( str(qt_str) )['servers']
        
    def get_servers_list(self):
        """
         :return: A :py:func:`list` of :py:func:`dict` with the server details or None if not found
        """
        servers = self.get_servers_dic()
        return [servers[ki] for ki in servers.keys()]
    
    def get_server(self, server):
        """
        :param server: The string with server host
        :return: A  :py:func:`dict` with the server details or None if not found
        """
        servers = self.get_servers_dic()
        if not server in servers:
            return None
        return servers[server]
        
    def save_server(self, dic):
        """
        :param dic: The dict with the server details
        """
        qt_str = self.value(self.SERVERS).toString()
        data =  json.loads( str(qt_str) )
        data['servers'][ dic['server'] ] = dic
        s = json.dumps(data)
        self.setValue(self.SERVERS, QVariant(s) )	
        self.sync()
    
        
    def save_window( self, window ):
        """Convenience functin to save window"""
        self.setValue( "window/%s/geometry" % window.W_NAME, QVariant( window.saveGeometry() ) )

    def restore_window( self, window ):
        """Convenience function to restore window"""
        geo = self.value( "window/%s/geometry" % window.W_NAME )
        window.restoreGeometry( geo.toByteArray() )
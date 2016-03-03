# -*- coding: utf-8 -*-
#
# DoubleGuid plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2015 PtitBigorneau - www.ptitbigorneau.fr
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA


__author__  = 'PtitBigorneau www.ptitbigorneau.fr'
__version__ = '1.3'

import b3, threading, thread, time
import b3.plugin
import b3.events
from b3 import clients

class DoubleguidPlugin(b3.plugin.Plugin):
    
    _adminPlugin = None   
    _immunityminlevel = 20
	
    def onLoadConfig(self):
	
        self._immunityminlevel = self.getSetting('settings', 'immunityminlevel', b3.LEVEL, self._immunityminlevel)

    def onStartup(self):
        
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            raise AttributeError('could not find admin plugin')

        self.registerEvent('EVT_CLIENT_AUTH', self.onClientAuth)

    def onClientAuth(self, event):
        """
        Handle EVT_CLIENT_AUTH
        """
           
        client = event.client
            
        for x in self.console.clients.getList():

            if x.guid == client.guid and x.cid != client.cid:

                if x.ip == client.ip:
                            
                    if client.maxLevel < self._immunityminlevel:
                        self._adminPlugin.warnClient(x, '%s ^3connects with your guid, same IP'%client.exactName, None, False, '', 60)
                        client.kick("Double Guid - Same IP",  None)
                        
                if x.ip != client.ip:
                            
                    if client.maxLevel >= self._immunityminlevel:
                                
                        x.message("%s ^3connects with your guid and IP Different"%(client.exactName))
                        x.message("^3Please Quickly Contact the Server Administrator")
                        x.message("^3You will lose your level and be kicker")
                                
                        client.kick("Admin Double Guid - IP Different",  None)
                                
                        self.tgroups()

                        try:

                            group = clients.Group(keyword=self.rgkeyword)
                            group = self.console.storage.getGroup(group)
                
                        except:
                            self.console.write('Error change level!') 
                    
                        x.setGroup(group)
                        x.save()
                                
                        thread.start_new_thread(self.pause, (x,))
                            
                    else:

                        self._adminPlugin.warnClient(x, '%s ^3connects with your guid, IP Different'%client.exactName, None, False, '', 60)
                        client.kick("Double Guid - IP Different",  None)

    def tgroups(self):

        self.rgkeyword = None
    
        cursor = self.console.storage.query("""
        SELECT *
        FROM groups n 
        """)

        if cursor.EOF:
  
            cursor.close()            
            
            return False

        while not cursor.EOF:
        
            sr = cursor.getRow()
            gkeyword = sr['keyword']
            glevel= sr['level']
       
            if int(glevel) == 0:
                self.rgkeyword = gkeyword

            cursor.moveNext()
    
        cursor.close()
        
        return

    def pause(self, xclient):

        time.sleep(30)

        xclient.kick("Admin Double Guid - IP Different",  None)

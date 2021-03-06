'''
Created on Jan 27, 2011

@author: ivan
'''
import gtk
import gobject
import logging

from foobnix.fc.fc import FC
from foobnix.fc.fc_base import FCBase
from foobnix.helpers.menu import Popup
from foobnix.regui.model import FModel, FDModel
from foobnix.util.mouse_utils import is_rigth_click
from foobnix.util.const import LEFT_PERSPECTIVE_LASTFM
from foobnix.util.bean_utils import update_parent_for_beans
from foobnix.regui.treeview.common_tree import CommonTreeControl


class LastFmIntegrationControls(CommonTreeControl):
    def __init__(self, controls):
        CommonTreeControl.__init__(self, controls)
        
        """column config"""
        column = gtk.TreeViewColumn(_("Lasm.fm Integration ") + FCBase().lfm_login, gtk.CellRendererText(), text=self.text[0], font=self.font[0])
        column.set_resizable(True)
        self.set_headers_visible(True)
        self.append_column(column)
        
        self.configure_send_drag()
        self.configure_recive_drag()
        
        self.set_type_tree()
        
        
        self.services = {
                         _("My loved tracks"):self.controls.lastfm_service.get_loved_tracks,
                         _("My top tracks"):self.controls.lastfm_service.get_top_tracks,
                         _("My recent tracks"):self.controls.lastfm_service.get_recent_tracks,
                         _("My top artists"):self.controls.lastfm_service.get_top_artists
                        # _("My friends"):self.controls.lastfm_service.get_friends,
                        #_("My neighbours"):self.controls.lastfm_service.get_neighbours
                         }  
        
        
        for name in self.services:          
            parent = FModel(name)
            bean = FDModel(_("loading...")).parent(parent)
            self.append(parent)        
            self.append(bean)
               
               
        
    def activate_perspective(self):   
        FC().left_perspective = LEFT_PERSPECTIVE_LASTFM
        
    def on_button_press(self, w, e):
        active = self.get_selected_bean()
        if is_rigth_click(e):
            menu = Popup()
            menu.add_item(_('Play'), gtk.STOCK_MEDIA_PLAY, self.controls.play, active)
            menu.add_item(_('Copy to Search Line'), gtk.STOCK_COPY, self.controls.searchPanel.set_search_text, active.text)            
            menu.show(e)
    
    def on_bean_expanded(self, parent):
        logging.debug("expanded %s" % parent)
        def task():
            old_iters = self.get_child_iters_by_parent(self.model, self.get_iter_from_bean(parent));
            childs = self.services[u""+parent.text](FCBase().lfm_login)
            update_parent_for_beans(childs, parent)
            
            
            self.append_all(childs)            
            gobject.idle_add(self.remove_iters,old_iters)        
            
        self.controls.in_thread.run_with_progressbar(task)        

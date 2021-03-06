#-*- coding: utf-8 -*-
'''
Created on 24 авг. 2010

@author: ivan
'''
from foobnix.preferences.configs.last_fm import LastFmConfig
import gtk
from foobnix.fc.fc import FC
from foobnix.fc.fc_base import FCBase

class VkontakteConfig(LastFmConfig):
    
    name = _("Vkontakte")
    
    def __init__(self, controls):
        box = gtk.VBox(False, 0)        
        box.hide()
        
        """LOGIN"""
        lbox = gtk.HBox(False, 0)
        lbox.show()
        
        login = gtk.Label(_("Login"))
        login.set_size_request(150, -1)
        login.show()
        
        self.login_text = gtk.Entry()
        self.login_text.show()
        
        lbox.pack_start(login, False, False, 0)
        lbox.pack_start(self.login_text, False, True, 0)
        
        """PASSWORD"""
        pbox = gtk.HBox(False, 0)
        pbox.show()
        
        password = gtk.Label(_("Password"))
        password.set_size_request(150, -1)
        password.show()
        
        self.password_text = gtk.Entry()
        self.password_text.set_visibility(False)
        self.password_text.set_invisible_char("*")
        self.password_text.show()
        
        link = gtk.LinkButton("http://vkontakte.ru/login.php?app=2234333&layout=popup&type=browser&settings=26", _("Check Foobnix Access (Require)"))
        
        
        pbox.pack_start(password, False, False, 0)
        pbox.pack_start(self.password_text, False, True, 0)
        
        
        box.pack_start(lbox, False, True, 0)
        box.pack_start(pbox, False, True, 0)
        box.pack_start(link, False, True, 0)
        
        self.widget = box
        
    def on_load(self):
        self.login_text.set_text(FCBase().vk_login)
        self.password_text.set_text(FCBase().vk_password)
    
    def on_save(self):
        if FCBase().vk_login != self.login_text.get_text() or FCBase().vk_password != self.password_text.get_text():
            FC().cookie = None
                        
        FCBase().vk_login = self.login_text.get_text()
        FCBase().vk_password = self.password_text.get_text() 
        
        

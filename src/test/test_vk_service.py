#-*- coding: utf-8 -*-
'''
Created on 21 нояб. 2010

@author: ivan
'''
import unittest
from foobnix.regui.service.vk_service import VKService
from foobnix.util.url_utils import get_url_type

class TestVKService(unittest.TestCase):
    vk = VKService()
    
    def test_login(self):
        self.assertTrue(self.vk.get("http://vk.com/gsearch.php?section=audio&q=persiana&name=1").find("Persiana jones") > -1 )

    def test_search_page(self):
        self.assertTrue(self.vk.search("Madonna").find("Madonna") > -1)

    def test_find_tracks_in_page(self):
        page = self.vk.search("Madonna")
        self.assertTrue(len(self.vk.find_tracks_in_page(page)) >0)
    
    def test_find_videos(self):
        list = self.vk.find_video_by_query("Мадонна")
        for bean in list[:10]:
            self.assertNotEquals("text/html", get_url_type(bean.path))
            self.assertTrue(bean.path.startswith("http://")) 
        
    def test_find_track(self):
        bean = self.vk.find_one_track("Мадонна")        
        self.assertTrue(bean.path.startswith("http://"))
    
    def test_bad_link_track(self):
        beans = self.vk.find_video_by_query("akon-cry out of jou(michael jackson tribute")
        "http://cs12907.vkontakte.ru/u87507380/video/bee60bc871.240.mp4"
        path = beans[0].path
        self.assertNotEquals("text/html", get_url_type(path))
                    
    def test_find_by_url(self):
        list = self.vk.find_tracks_by_url("http://vkontakte.ru/audio.php?gid=2849#album_id=0&gid=2849&id=0&offset=200")        
        for bean in list:
            self.assertTrue(bean.path.startswith("http://"))
   
    def test_find_by_url_user(self):
        list = self.vk.find_tracks_by_url("http://vkontakte.ru/audio.php?id=14775382")        
        for bean in list:
            self.assertFalse('\">' in bean.text)
            self.assertTrue(bean.path.startswith("http://"))
    
if __name__ == '__main__':
    unittest.main()
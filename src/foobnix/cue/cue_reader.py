'''
Created on 7  2010

@author: ivan
'''
from foobnix.model.entity import CommonBean
import os
from foobnix.util.time_utils import normilize_time
from AptUrl.Parser import parse
from foobnix.util import LOG, file_utils
'''
Created on 4 

@author: ivan
'''

TITLE = "TITLE"
PERFORMER = "PERFORMER"
FILE = "FILE"
INDEX = "INDEX"

class CueTrack():
    
    def __init__(self, title, performer, index):
        self.title = title
        self.performer = performer
        self.index = index
        self.duration = 0
        self.path = None
    
    def __str__(self):
        return "Track: " + self.title + " " + self.performer + " " + self.index
    
    def get_start_time_str(self):
        return self.index[len("INDEX 01") + 1:]
    
    def get_start_time_sec(self):
        time = self.get_start_time_str()
        "00:00:0"
        m = time[:2]
        s = time[len("00:"):len("00:") + 2]
        return int(m) * 60 + int(s)
            
class CueFile():
    def __init__(self):
        self.title = None
        self.performer = None 
        self.file = None
        
        self.tracks = []
    
    def append_track(self, track):
        self.tracks.append(track)
        
    def __str__(self):
        return "CUEFILE: " + self.title + " " + self.performer + " " + self.file  

class CueReader():
    
    def __init__(self, cue_file):
        self.cue_file = cue_file
        self.is_valid = True
    
    def get_line_value(self, str):
        first = str.find('"') or str.find("'")
        end = str.find('"', first + 1) or str.find("'", first + 1)
        return str[first + 1:end]
    
    def normalize(self, cue_file):
        duration_tracks = []
        tracks = cue_file.tracks
        for i in xrange(len(tracks) - 1):
            track = tracks[i]
            next_track = tracks[i + 1]
            duration = next_track.get_start_time_sec() - track. get_start_time_sec()
            track.duration = duration
            track.path = cue_file.file
            duration_tracks.append(track)
            
        cue_file.tracks = duration_tracks            
        return cue_file
    
    def get_common_beans(self):
        beans = []
        for track  in self.parse().tracks:
            bean = CommonBean(name=track.performer + " - " + track.title, path=track.path, type=CommonBean.TYPE_MUSIC_FILE)
            bean.start_at = track.get_start_time_sec()
            bean.duration = track.duration        
            bean.time = normilize_time(track.duration)
            
            beans.append(bean)    
            
            
        return beans
    
    def is_cue_valid(self):
        self.parse()
        LOG.info("CUE VALID", self.cue_file, self.is_valid)
        return self.is_valid
        
    
    def parse(self):
        file = open(self.cue_file, "r")
        
        is_title = True
        cue_file = CueFile()
        
        for line in file:
            line = str(line).strip()
                    
            if not line:
                continue
            
            if line.startswith(TITLE):
                title = self.get_line_value(line)
                if is_title:
                    cue_file.title = title 
                
            
            if line.startswith(PERFORMER):
                performer = self.get_line_value(line)
                if is_title:
                    cue_file.performer = performer
                
            if line.startswith(FILE):
                file = self.get_line_value(line)
                dir = os.path.dirname(self.cue_file)
                full_file = os.path.join(dir, file)
                LOG.debug("CUE source", full_file)
                exists = os.path.exists(full_file)
                """if there no source cue file"""
                
                if not exists:
                    """try to find other source"""
                    ext = file_utils.get_file_extenstion(full_file)
                    nor = full_file[:-len(ext)]
                    LOG.info("Normilized path", nor)
                    if os.path.exists(nor + ".ape"):
                        full_file = nor + ".ape"
                    elif os.path.exists(nor + ".flac"):
                        full_file = nor + ".flac"
                    elif os.path.exists(nor + ".wav"):
                        full_file = nor + ".wav"
                    else:                                           
                        self.is_valid = False
                        return cue_file
                
                if is_title:
                    cue_file.file = full_file
                    
            if line.startswith(INDEX):
                index = self.get_line_value(line)            
                
            if line.startswith("TRACK") and line.find("AUDIO"):
                if not is_title:           
                    cue_track = CueTrack(title, performer, index)
                    cue_file.append_track(cue_track)
                    
                is_title = False 
        
        return self.normalize(cue_file)     
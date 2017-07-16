# -*- coding: utf-8 -*-
import logging
import threading

from kalliope.core.NeuronModule import NeuronModule
from kodijson import PLAYER_VIDEO
from kodijson import Kodi as Kodi_Control



logging.basicConfig()
logger = logging.getLogger("kalliope")


class Kodi(NeuronModule):
    def __init__(self, **kwargs):
        super(Kodi, self).__init__(**kwargs)
        # the args from the neuron configuration
        # Kodi Commands
        self.kodi_ip = kwargs.get('kodi_ip', 'Localhost')
        self.kodi_port = kwargs.get('kodi_port', 8080)
        self.kodi_login = kwargs.get('kodi_login', None)
        self.kodi_password = kwargs.get('kodi_password', None)        
        self.gui_window = kwargs.get('gui_window', None)
        self.show_video_path = kwargs.get('show_video_path', None)
        self.show_music_path = kwargs.get('show_music_path', None)
        self.input_action = kwargs.get('input_action', None)
        self.repeat_action = kwargs.get('repeat_action', None)
        self.play_file = kwargs.get('play_file', None)
        self.open_addon = kwargs.get('open_addon', None)
        self.scan_video_lib = kwargs.get('scan_video_lib', False)
        self.scan_audio_lib = kwargs.get('scan_audio_lib', False)
        self.skip_video = kwargs.get('skip_video', None)
        self.kodi_exit = kwargs.get('kodi_exit', False)
        self.set_volume = kwargs.get('set_volume', None)
        self.show_context = kwargs.get('show_context', False)
        self.show_osd = kwargs.get('show_osd', False)
        self.mute = kwargs.get('mute', False)
        
        # Search for Movie
        self.search_movie = kwargs.get('search_movie', None) 
        self.abort_orders = kwargs.get('abort_orders', None)
        self.reask = kwargs.get('reask', False)
        
        
        
        if self._is_parameters_ok():
            if self.kodi_login is not None:
                self.kodi = Kodi_Control("http://" + str(self.kodi_ip) + ":" + str(self.kodi_port) + "/jsonrpc", self.kodi_login, self.kodi_password)
            else:
                self.kodi= Kodi_Control("http://" + str(self.kodi_ip) + ":" + str(self.kodi_port) + "/jsonrpc")
          
            kodi_thread = KodiThread(kodi_ip=self.kodi_ip, kodi_port=self.kodi_port, kodi_login=self.kodi_login, kodi_password=self.kodi_password, gui_window=self.gui_window, show_video_path=self.show_video_path, show_music_path=self.show_music_path, input_action=self.input_action, repeat_action=self.repeat_action, play_file=self.play_file, open_addon=self.open_addon, scan_video_lib=self.scan_video_lib, scan_audio_lib=self.scan_audio_lib, skip_video=self.skip_video, kodi_exit=self.kodi_exit, set_volume=self.set_volume, show_context=self.show_context, show_osd=self.show_osd, mute=self.mute)   
            kodi_thread.start()
        
            def search_my_movie(self):        
            
                def say_movie_not_found_search_audio(self, search_audio):
                    """
                    Say searcj_audio not found
                    """
                    if self.search_audio is not None: 
                        self.message = {
                            "movie_not_found": self.search_audio}
                        self.say(self.message)
                    else:
                        self.message = {
                            "movie_not_found": " "}
                        self.say(self.message)
                        

                def say_movie_not_found_search_movie(self, search_movie):
                    """
                    Say search_movie not found
                    """
                    if self.search_movie is not None:
                        self.message = {
                            "movie_not_found": self.search_movie}
                        self.say(self.message)
                    else:
                        self.message = {
                            "movie_not_found": " "}
                        self.say(self.message)
                        
                def say_labels(self, label):
                    """
                    Say the labels
                    """
                    label_form = (", ".join(label))
                    self.message = {
                        "say_labels": label_form}
                    self.say(self.message)
                    
                def search_for_movie(self, search):
                    """
                    Search the movie in the Kodi database
                    """
                    movies = self.kodi.VideoLibrary.GetMovies()['result']['movies']
                    movie = []
                    for m in movies:   
                        if self.search in m['label'].lower():
                            movie.append(m)            
                            logger.debug("Info: Found movie: %s" % movie)
                            self.found_movie = True
                    return movie
            

                def id_search(movie):
                    """
                    Search the ID
                    """
                    movie_id = []
                    for id_search in movie:
                        movie_id.append((id_search)['movieid'])
                        logger.debug("Info: Found movie ID: %s" % movie_id)
                    return movie_id           
            

                def label_search(movie):
                    """
                    Search the label
                    """
                    label = []
                    for label_search in movie:
                        label.append((label_search)['label'])
                        logger.debug("Info: Found label: %s" %  (", ".join(label)))
                    return label
           
                def play_movie(self, movie_id):  
                    """
                    Play the movie by ID.
                    """
                    self.kodi.Playlist.Clear(playlistid=1)
                    self.kodi.Playlist.Add(playlistid=1, item={'movieid': (movie_id[0])})
                    self.kodi.Player.Open(item={'playlistid': 1})
                    logger.debug("Info: Start movie")    
     
                     
                def check_movie(self, movie):
                    """
                    Check the movie if its in the database or if there are similar names 
                    """
                    if self.reask is True:
                        if len(movie) is 1:
                            label = label_search(movie)
                            label_form = (", ".join(label))
                            movie_id = id_search(movie) 
                            play_movie(self, movie_id) 
                            logger.debug("Info: Found movie, start: %s" % label_form)
                            self.finish = True
                     
                        if len(movie) > 1:
                            label = label_search(movie)
                            label_form = (", ".join(label))
                            logger.debug("Info: Multiple movies found with: %s" % label_form)           
                            say_labels(self, label)
                            self.get_audio_from_stt(callback=self.callback)
                            logger.debug("Info: callback received: %s" % self.search_audio) 

                        if len(movie) is 0:
                            logger.debug("Info: Movie not found, ask again")   
                            if self.search_audio is not None:
                                say_movie_not_found_search_audio(self, self.search_audio)
                                self.get_audio_from_stt(callback=self.callback)
                                logger.debug("Info: callback received: %s" % self.search_audio)     
                            
                            if self.search_movie is not None:  
                                say_movie_not_found_search_movie(self, self.search_movie)
                                self.get_audio_from_stt(callback=self.callback)
                                logger.debug("Info: Movie not found: %s" % self.search_movie)     
                                
                def start_movie_no_reask(self, movie):
                    """
                    Start the movie if reask is False
                    """
                    label = label_search(movie)
                    label_form = (", ".join(label))
                    movie_id = id_search(movie) 
                    play_movie(self, movie_id) 
                    logger.debug("Info: Found movie, start: %s" % label_form) 
                    self.finish = True

                
                while self.finish is False:
                    if self.search_movie is not None and self.search_movie is not '':
                        self.search_audio = None
                        logger.debug("Info: Check movie: %s" % self.search_movie)
                        self.search = (self.search_movie).lower()
                        movie = search_for_movie(self, self.search)
                        if self.reask is True:
                            check_movie(self, movie)
                            if self.finish is True:
                                break
                        else:
                            if self.found_movie is True:
                                start_movie_no_reask(self, movie)
                            else:
                                logger.debug("Info: Movie not found: %s" % self.search)
                                say_movie_not_found_search_movie(self, self.search_movie)
                                break
                    else:
                        if self.reask is False:
                            logger.debug("Info: Movie not found reask is False, break loop")
                            say_movie_not_found_search_audio(self, self.search_audio)
                            break
                        
                    if self.reask is True:
                        if self.search_audio is not None and self.search_audio is not '':   
                            self.search_movie = None
                            if self.search_audio in self.abort_orders:
                                logger.debug("Info: Abort by user")
                                break
                            logger.debug("Info: search for: %s" % self.search_audio)
                            self.search = (self.search_audio).lower()
                            movie = search_for_movie(self, self.search)
                            check_movie(self, movie)
                            if self.finish is True:
                                break
                        else:
                            logger.debug("Info: search_audio is None")       
                            say_movie_not_found_search_audio(self, self.search_audio)
                            self.get_audio_from_stt(callback=self.callback)
                            
                        if self.search_audio in self.abort_orders:
                                logger.debug("Info: Abort by user")
                                break

                    
                        
            if self.search_movie is not None:
                self.search_audio = None
                self.finish = False
                self.found_movie = False
                search_my_movie(self)
        
    def callback(self, audio): 
        """
        Our callback to ask again
        """
        self.search_audio = audio
        return self.search_audio
    
    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException
        """
        if self.kodi_login is not None and self.kodi_password is None:
            raise MissingParameterException("You set kodi_login, you also need to set kodi_password")
        if self.kodi_login is None and self.kodi_password is not None:
            raise MissingParameterException("You set kodi_password, you also need to set kodi_login")
        if self.reask is True and self.abort_orders is None:
            raise MissingParameterException("You set reask True, you also need to set abort_orders")
        return True   
        



class KodiThread(threading.Thread):
    """
    This thread is used because Kodi can have sometimes long response time with the Json API

    """
    def __init__(self, kodi_ip, kodi_port, kodi_login, kodi_password, gui_window, show_video_path, show_music_path, input_action, repeat_action, play_file, open_addon, scan_video_lib, scan_audio_lib, skip_video, kodi_exit, set_volume, show_context, show_osd, mute): 
    
        threading.Thread.__init__(self)
        # Kodi action
        self.kodi_ip = kodi_ip
        self.kodi_port = kodi_port
        self.kodi_login = kodi_login
        self.kodi_password = kodi_password    
        self.gui_window = gui_window
        self.show_video_path = show_video_path
        self.show_music_path = show_music_path
        self.input_action = input_action
        self.repeat_action = repeat_action
        self.play_file = play_file
        self.open_addon = open_addon
        self.scan_video_lib = scan_video_lib
        self.scan_audio_lib = scan_audio_lib
        self.skip_video = skip_video
        self.kodi_exit = kodi_exit
        self.set_volume = set_volume
        self.show_context = show_context
        self.show_osd = show_osd
        self.mute = mute
        

    def run(self):
        if self.kodi_login is not None:
            self.kodi = Kodi_Control("http://" + str(self.kodi_ip) + ":" + str(self.kodi_port) + "/jsonrpc", self.kodi_login, self.kodi_password)
        else:
            self.kodi= Kodi_Control("http://" + str(self.kodi_ip) + ":" + str(self.kodi_port) + "/jsonrpc")
        
        
        #open a certain window
        #check here for the window names
        #http://kodi.wiki/view/JSON-RPC_API/v6#GUI.Window
        self.kodi.GUI.ActivateWindow(window= self.gui_window)
            
        #open a path or the Kodi lib
        #check here for the database paths
        #http://kodi.wiki/view/Opening_Windows_and_Dialogs
        self.kodi.GUI.ActivateWindow({"window":"videos","parameters": [self.show_video_path]})
        self.kodi.GUI.ActivateWindow({"window":"music","parameters": [self.show_music_path]})
            
        #control Kodi with repeat the action for x times
        repeat = self.repeat_action           
        if repeat is not None:
            for _ in " "*int(self.repeat_action): self.kodi.Input.ExecuteAction({"action": self.input_action})
        else:    
            self.kodi.Input.ExecuteAction({"action": self.input_action})
                
        #play a file, can also be a stream or favorite with type media
        #check here for the path
        #http://192.168.178.101:8080/jsonrpc?request={ "jsonrpc": "2.0", "method": "Favourites.GetFavourites", "params": { "properties": ["window","path"] }, "id": 1 }
        self.kodi.Player.Open({"item":{"file": self.play_file}})            
           
            
        #open addon
        #check here to get a list with all addons and addonid
        #http://192.168.178.101:8080/jsonrpc?request={ "jsonrpc": "2.0", "method": "Addons.GetAddons","params":{}, "id": "1"}             
        self.kodi.Addons.ExecuteAddon({"addonid": self.open_addon})
                
        #scan video library
        if self.scan_video_lib is True:
            self.kodi.VideoLibrary.Scan()

        #scan audio library
        if self.scan_audio_lib is True:
            self.kodi.AudioLibrary.Scan()
                
        #values: smallbackward, bigbackward, smallforward, bigforward
        self.kodi.Player.Seek({"playerid":1,"value": self.skip_video})
            
        #exit kodi
        if self.kodi_exit is True:
            self.kodi.Application.Quit()       
            
        if self.set_volume is not None:
            self.kodi.Application.SetVolume({"volume":self.set_volume})
            
        if self.mute is not None:   
            self.kodi.Application.SetMute({"mute":self.mute})
        
        if self.show_context is True:
            self.kodi.Input.ContextMenu()
        
        if self.show_osd is True:
            self.kodi.Input.ShowOSD()

   
        


        


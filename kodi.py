# -*- coding: utf-8 -*-
import logging
import threading

from kalliope.core.NeuronModule import NeuronModule
from kodijson import PLAYER_VIDEO
from kodijson import Kodi as Kodi_Control
from kalliope import Utils


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
        self.check_movie_in_database  = kwargs.get('check_movie_in_database', None)
        
        # Resume TV-Show
        self.resume_tvshow = kwargs.get('resume_tvshow', None)

        # Search for TV-Show
        self.start_tvshow = kwargs.get('start_tvshow', None)
        self.tvshow_season = kwargs.get('season', None)
        self.tvshow_episode = kwargs.get('episode', None)
        self.open_season_dir = kwargs.get('open_season_dir', False)

        self.what_is_running = kwargs.get('what_is_running', False)
        
        if self._is_parameters_ok():
            if self.kodi_login is not None:
                self.kodi = Kodi_Control("http://" + str(self.kodi_ip) + ":" + str(self.kodi_port) + "/jsonrpc", self.kodi_login, self.kodi_password)
            else:
                self.kodi= Kodi_Control("http://" + str(self.kodi_ip) + ":" + str(self.kodi_port) + "/jsonrpc")
          
            kodi_thread = KodiThread(kodi_ip=self.kodi_ip, 
                                                        kodi_port=self.kodi_port, kodi_login=self.kodi_login, 
                                                        kodi_password=self.kodi_password, gui_window=self.gui_window, 
                                                        show_video_path=self.show_video_path, show_music_path=self.show_music_path, 
                                                        input_action=self.input_action, repeat_action=self.repeat_action, 
                                                        play_file=self.play_file, open_addon=self.open_addon, 
                                                        scan_video_lib=self.scan_video_lib, scan_audio_lib=self.scan_audio_lib, 
                                                        skip_video=self.skip_video, kodi_exit=self.kodi_exit, 
                                                        set_volume=self.set_volume, show_context=self.show_context, 
                                                        show_osd=self.show_osd, mute=self.mute)   
            kodi_thread.start()

            def search_and_play_movie(self):  
            
                def say_movie_not_found(self, search_movie):
                    """
                    Say movie_not_found
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
                    Search for the movie details
                    """
                    movies = self.kodi.VideoLibrary.GetMovies()['result']['movies']
                    movie_details = []
                    for m in movies:   
                        if self.search in m['label'].lower():
                            movie_details.append(m)            
                            logger.debug("Info: Found movie: %s" % movie_details)
                            self.found_movie = True
                    return movie_details
            
                def id_search(movie_details):
                    """
                    Search for the movie ID
                    """
                    movie_id = []
                    for id_search in movie_details:
                        movie_id.append((id_search)['movieid'])
                        logger.debug("Info: Found movie ID: %s" % movie_id)
                    return movie_id           
            
                def label_search(movie_details):
                    """
                    Search the label
                    """
                    label = []
                    for label_search in movie_details:
                        label.append((label_search)['label'])
                        logger.debug("Info: Found label: %s" %  (", ".join(label)))
                    return label
           
                def play_movie(self, movie_id, resume=True):
                    return self.kodi.Player.Open({"item": {"movieid": (movie_id[0])}, "options": {"resume": resume}})     
                  
                def check_movie(self, movie_details):
                    """
                    Check the movie_details with kodis database
                    """
                    label = label_search(movie_details)
                    label_form = (", ".join(label))

                    if len(movie_details) is 1:
                        movie_id = id_search(movie_details) 
                        play_movie(self, movie_id) 
                        logger.debug("Info: Found movie, start: %s" % label_form)
                        self.finish = True
                 
                    if len(movie_details) > 1:
                        logger.debug("Info: Multiple movies found with: %s" % label_form)
                        say_labels(self, label)
                        self.get_audio_from_stt(callback=self.callback)
                        logger.debug("Info: callback received: %s" % self.search_movie) 


                    if len(movie_details) is 0:
                        logger.debug("Info: Movie not found")   
                        say_movie_not_found(self, self.search_movie)    
                        self.get_audio_from_stt(callback=self.callback)
                        logger.debug("Info: callback received: %s" % self.search_movie)     

                if self.reask is True:
                    while self.finish is False:
                        if self.search_movie in self.abort_orders:
                                logger.debug("Info: Abort by user")
                                break
                        
                        if self.search_movie is not None and self.search_movie is not '':
                            logger.debug("Info: Search for: %s" % self.search_movie)
                            self.search = (self.search_movie).lower()
                            movie_details = search_for_movie(self, self.search)            
                            check_movie(self, movie_details)
                            
                            if self.finish is True:
                                play_movie(self, movie_details)
                                break    
                                
                        else:
                            logger.debug("Info: search_movie is None")
                            self.search_movie = None
                            say_movie_not_found(self, self.search_movie)
                            self.get_audio_from_stt(callback=self.callback)    

                else:
                    if self.search_movie is not None and self.search_movie is not '':
                        logger.debug("Info: Check movie: %s" % self.search_movie)
                        self.search = (self.search_movie).lower()
                        movie_details = search_for_movie(self, self.search)
                       
                        if self.found_movie is True:
                            label = label_search(movie_details)
                            label_form = (", ".join(label))
                            movie_id = id_search(movie_details) 
                            play_movie(self, movie_id) 
                            logger.debug("Info: Found movie play: %s" % label_form) 
                                
                        else:
                            logger.debug("Info: Movie not found")
                    else:
                        logger.debug("Info: Movie is none.")                

            def check_movie_in_database(self):
                
                def say_movie_found(self, label):
                    if self.check_movie_in_database is not None:
                        label = label_search(movie_details)
                        label_form = (", ".join(label))
                        
                        self.message = {
                            "movie_found": label_form}
                        self.say(self.message)
                    else:
                        self.message = {
                            "movie_found": " "}
                        self.say(self.message)

                def say_found_movie_labels(self, label):
                    label = label_search(movie_details)
                    label_form = (", ".join(label))
                    
                    self.message = {
                        "say_found_movie_labels": label_form}
                    self.say(self.message)

                def say_no_movie_found(self, check_movie_in_database):
                    if self.check_movie_in_database is not None: 
                        self.message = {
                            "say_no_movie_found": self.check_movie_in_database}
                        self.say(self.message)
                    else:
                        self.message = {
                            "say_no_movie_found": " "}
                        self.say(self.message)
                
                def search_for_movie_details(self, search):
                    """
                    Search the movie in the Kodi database
                    """
                    movies = self.kodi.VideoLibrary.GetMovies()['result']['movies']
                    movie_details = []
                    for m in movies:   
                        if self.search in m['label'].lower():
                            movie_details.append(m)            
                            logger.debug("Info: Found movie: %s" % movie_details)
                            self.found_movie = True
                    return movie_details
               
                def label_search(movie_details):
                    """
                    Search the label
                    """
                    label = []
                    for label_search in movie_details:
                        label.append((label_search)['label'])
                        logger.debug("Info: Found label: %s" %  (", ".join(label)))
                    return label
               
                def check_movie_exist(self, movie_details): 

                    label = label_search(movie_details)
                    label_form = (", ".join(label))
                    
                    if len(movie_details) is 1:    
                        logger.debug("Info: Movie exist: %s" % label_form)
                        say_movie_found(self, label)

                    if len(movie_details) > 1:
                        logger.debug("Info: Multiple movies found with: %s" % label_form)
                        say_found_movie_labels(self, label)
                            
                    if len(movie_details) is 0:
                        logger.debug("Info: Movie does not exist")   
                        say_no_movie_found(self, self.check_movie_in_database)


                if self.check_movie_in_database is not None and self.check_movie_in_database is not '':
                    logger.debug("Info: Check movie: %s" % self.check_movie_in_database)
                    self.search = (self.check_movie_in_database).lower()
                    movie_details = search_for_movie_details(self, self.search)   
                    check_movie_exist(self, movie_details)
                else:
                    logger.debug("Info: Movie is None")
                    self.check_movie_in_database = None
                    say_no_movie_found(self, self.check_movie_in_database)
                    
            def search_my_tvshow(self):
                """
                Search, start TV-Show and resume a specific TV-Show
                """
                
                def get_next_unwatched_episode(self):
                    data = self.kodi.VideoLibrary.GetEpisodes({"limits":{"end":1},"tvshowid": int(self.tvshow_id[0]), 
                                                                                "filter":{"field":"lastplayed", "operator":"greaterthan", "value":"0"}, 
                                                                                "properties":["showtitle",  "title", "season", "episode", "lastplayed", "resume"], 
                                                                                "sort":{"method":"lastplayed", "order":"descending"}})
                    if 'episodes' in data['result']:
                        episode = data['result']['episodes'][0]
                        if episode['resume']['position'] > 0.0:
                            self.episode_id = episode['episodeid']
                            self.resume = True
                        else:    
                            episode= episode['episodeid']             
                            self.episode_id = (episode + 1)
                            self.resume = False

                def get_specific_episode(self):
                    data = self.kodi.VideoLibrary.GetEpisodes({"tvshowid": int(self.tvshow_id[0]), 
                                                                                "season": int(self.tvshow_season), 
                                                                                "properties": ["season", "episode"]})
                    if 'episodes' in data['result']:
                        self.episode_id = None
                        for episode_data in data['result']['episodes']:  
                            if int(episode_data['episode']) == int(self.tvshow_episode):
                                self.episode_id = episode_data['episodeid']

                def search_for_tvshow(self):
                    data = self.kodi.VideoLibrary.GetTVShows()['result']['tvshows']
                    self.tvshow_id = []
                    self.multiple_labels = []
                    self.single_label = []
                    self.found_tvshow_id = False
                    self.found_muliple_ids = False
                    for m in data:
                        if self.search_tvshow in m['label'].lower():
                            self.tvshow_id.append((m)['tvshowid']) 
                            self.found_tvshow_id = True
                            self.single_label.append((m)['label'])  
                            if len(self.tvshow_id) > 1:
                                self.found_muliple_ids = True
                                self.multiple_labels.append((m)['label']) 

                def get_episode_details(self):
                    if self.episode_id:
                        data = self.kodi.VideoLibrary.GetEpisodeDetails({"episodeid": int(self.episode_id), "properties": 
                                                                                                                    ["showtitle", "title", "season", 
                                                                                                                    "episode", "lastplayed", "resume"]})
                        if 'episodedetails' in data['result']:
                            self.episode_details = data['result']['episodedetails']

                    if self.tvshow_id:
                        data = self.kodi.VideoLibrary.GetTVShowDetails({"tvshowid": self.tvshow_id[0], "properties": 
                                                                                                ["title", "genre", "year", "rating", "plot", 
                                                                                                "playcount", "episode", "lastplayed",  "season", 
                                                                                                "watchedepisodes", "runtime"]})            
                        if 'tvshowdetails' in data['result']:
                            self.tvshow_details = data['result']['tvshowdetails']
                    
                def check_season_episode_exist(self):
                    data = self.kodi.VideoLibrary.GetTVShowDetails({"tvshowid": self.tvshow_id[0], "properties": ["season"]})    
                    season = data['result']['tvshowdetails']
                    if self.tvshow_season <= season['season']:   
                        self.season_exist = True
                        data = self.kodi.VideoLibrary.GetEpisodes({"tvshowid": int(self.tvshow_id[0]), 
                                                                                    "season": int(self.tvshow_season), 
                                                                                    "properties": ["season", "episode"]})                                                                        
                        if self.tvshow_episode <= len(data['result']['episodes']):  
                            self.episode_exist = True   
                
                def play_episode(self):
                    if self.open_season_dir is True:
                        self.kodi.GUI.ActivateWindow({"window":"videos","parameters":["videodb://2/2/" + str(self.tvshow_id[0]) + "/" + str(self.episode_details['season'])]})
                    self.kodi.Player.Open({"item": {"episodeid": self.episode_id}, "options": {"resume": self.resume}})
                    
                self.resume = False    
                self.season_exist = False
                self.episode_exist = False
                self.stop_search = False
                self.episode_id = None
                
                if self.start_tvshow is not None:
                    if self.tvshow_episode is not None:
                        try:
                            self.tvshow_episode = int(self.tvshow_episode)
                        except ValueError:
                            Utils.print_info("Kodi: tvshow_episode needs to be integer")
                            self.stop_search = True

                    if self.tvshow_season is not None:
                        try:
                            self.tvshow_season = int(self.tvshow_season)
                        except ValueError:
                            Utils.print_info("Kodi: tvshow_season needs to be integer")
                            self.stop_search = True
                    
                    if self.stop_search is False:
                        self.search_tvshow = (self.start_tvshow).lower()
                        search_for_tvshow(self)
                        if self.found_tvshow_id is True:
                            if self.found_muliple_ids is False:          
                                check_season_episode_exist(self)
                                if self.season_exist is True:
                                    if self.episode_exist is True:            
                                        get_specific_episode(self)
                                        get_episode_details(self) 
                                        Utils.print_info("Kodi: Play " + self.episode_details['showtitle'] + " - " + self.episode_details['title'])
                                        play_episode(self)
                                    else:
                                        Utils.print_info("Kodi: " + ' '.join(self.single_label) + " season " + str(self.tvshow_season) + " episode " + str(self.tvshow_episode) +  " was not found")
                                else:
                                    Utils.print_info("Kodi: " + ' '.join(self.single_label) + " season " + str(self.tvshow_season) + " was not found")
                            else:
                                Utils.print_info("Kodi: Found multiple TV-Shows " + ', '.join(self.multiple_labels))
                        else:
                            Utils.print_info("Kodi: The TV-Show " + self.start_tvshow + " was not found")
                                
                if self.resume_tvshow is not None and self.resume_tvshow is not '':
                    self.search_tvshow = (self.resume_tvshow).lower()            
                    search_for_tvshow(self)
                    if self.found_tvshow_id is True:
                        if self.found_muliple_ids is False:     
                            get_next_unwatched_episode(self)
                            if self.episode_id:
                                get_episode_details(self)
                                Utils.print_info(("Kodi: Play and resume " + self.episode_details['showtitle'] + " - " + self.episode_details['title']))
                                play_episode(self)
                            else:
                                Utils.print_info("Kodi: There is nothing to resume for " + ' '.join(self.single_label))
                        else:
                            Utils.print_info("Kodi: Found multiple TV-Shows " + ', '.join(self.multiple_labels))       
                    else:
                        Utils.print_info("Kodi: The TV-Show " + self.search_tvshow + " was not found" )       
                
            def what_is_running(self):
            
                def say_what_is_running(self):
                    self.say(self.message)
                                    
                def get_player_id(self, playertype=['audio', 'video', 'picture']):
                  data = self.kodi.Player.GetActivePlayers()
                  result = data.get("result", [])
                  if len(result) > 0:
                    for result in result:
                      if result.get("type") in playertype:
                        return result.get("playerid")
                  return None

                def get_playing_item(self):
                    playerid = get_player_id(self)
                    if playerid is not None:
                        data = self.kodi.Player.GetItem({"playerid":playerid, "properties":
                                                        ["title", "album", "artist", "season", 
                                                        "episode", "showtitle", "tvshowid", "description"]})
                        return data['result']['item']
                    return None    

                result = get_playing_item(self)

                if result is not None:
                    if result['type'] == 'episode':
                        if result['showtitle']:
                            self.message = {
                                "say_show_title": result['showtitle']}
                            say_what_is_running(self)

                        if result['title']:
                            self.message = {
                                "say_episode_title": result['title']}
                            say_what_is_running(self)
                    
                    elif result['type'] == 'song' or result['type'] == 'musicvideo':
                      if result['title']:
                        self.message = {
                            "say_song_title": result['title']}
                        say_what_is_running(self)
                        
                        if result['artist']:
                            self.message = {
                                "say_song_artist": result['artist']}
                            say_what_is_running(self)
                        
                        if result['album']:
                            self.message = {
                                "say_song_album": result['album']}
                            say_what_is_running(self)  
                          
                    elif result['type'] == 'movie':
                      if result['title']:
                        self.message = {
                            "say_movie_title": result['title']}
                        say_what_is_running(self)
                else:
                    self.message = {
                        "say_no_media_infos_found": " " 
                        }
                    say_what_is_running(self)
                        
            if self.check_movie_in_database is not None:            
                check_movie_in_database(self)
            
            if self.search_movie is not None:
                self.finish = False
                self.found_movie = False
                search_and_play_movie(self)
            
            if self.resume_tvshow is not None:
                search_my_tvshow(self) 

            if self.start_tvshow is not None and self.start_tvshow is not '':
                search_my_tvshow(self)
             
            if self.what_is_running is True:
                what_is_running(self)
                
    def callback(self, audio): 
        """
        Our callback to ask again
        """
        self.search_movie = audio
        return self.search_movie
    
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
        if self.gui_window is not None:
            self.kodi.GUI.ActivateWindow(window= self.gui_window)
            
        #open a path or the Kodi lib
        #check here for the database paths
        #http://kodi.wiki/view/Opening_Windows_and_Dialogs
        if self.show_video_path is not None:
            self.kodi.GUI.ActivateWindow({"window":"videos","parameters": [self.show_video_path]})
        if self.show_music_path is not None:
            self.kodi.GUI.ActivateWindow({"window":"music","parameters": [self.show_music_path]})
            
        #control Kodi with repeat the action for x times
      
        if self.repeat_action is not None and self.repeat_action is not None:
            for _ in " "*int(self.repeat_action): self.kodi.Input.ExecuteAction({"action": self.input_action})
        
        if self.input_action is not None and self.repeat_action is None:
            self.kodi.Input.ExecuteAction({"action": self.input_action})

            
        #play a file, can also be a stream or favorite with type media
        #check here for the path
        #http://192.168.178.101:8080/jsonrpc?request={ "jsonrpc": "2.0", "method": "Favourites.GetFavourites", "params": { "properties": ["window","path"] }, "id": 1 }
        if self.play_file is not None:
            self.kodi.Player.Open({"item":{"file": self.play_file}})            
           
            
        #open addon
        #check here to get a list with all addons and addonid
        #http://192.168.178.101:8080/jsonrpc?request={ "jsonrpc": "2.0", "method": "Addons.GetAddons","params":{}, "id": "1"}             
        if self.open_addon is not None:
            self.kodi.Addons.ExecuteAddon({"addonid": self.open_addon})
                
        #scan video library
        if self.scan_video_lib is True:
            self.kodi.VideoLibrary.Scan()

        #scan audio library
        if self.scan_audio_lib is True:
            self.kodi.AudioLibrary.Scan()
                
        #values: smallbackward, bigbackward, smallforward, bigforward
        if self.skip_video is not None:
            self.kodi.Player.Seek({"playerid":1,"value": self.skip_video})
            
        #exit kodi
        if self.kodi_exit is True:
            self.kodi.Application.Quit()       
            
        if self.set_volume is not None:
            try: 
                self.kodi.Application.SetVolume({"volume":(int(self.set_volume))})
            except ValueError:
                logger.debug("Kodi set_volume needs to be integer. You tried: %s" % self.set_volume)
            
        if self.mute is not None:   
            self.kodi.Application.SetMute({"mute":self.mute})
        
        if self.show_context is True:
            self.kodi.Input.ContextMenu()
        
        if self.show_osd is True:
            self.kodi.Input.ShowOSD()

   
        


        


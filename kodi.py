# -*- coding: utf-8 -*-
import logging
import random
import re
import sys  
import datetime
import requests
from time import sleep
from kalliope.core.NeuronModule import NeuronModule, MissingParameterException
from kodijson import Kodi as codi
from kalliope import Utils
from fuzzywuzzy import fuzz, process


logging.basicConfig()
logger = logging.getLogger("kalliope")
reload(sys)  
sys.setdefaultencoding('utf8')

class Kodi(NeuronModule):
    def __init__(self, **kwargs):
        super(Kodi, self).__init__(**kwargs)
        # Basic configuration
        self.host = kwargs.get('host', 'Localhost')
        self.port = kwargs.get('port', 80)
        self.login = kwargs.get('login', None)
        self.password = kwargs.get('password', None)
        self.cutoff = kwargs.get('cutoff', 70)
        
        # Notification 
        self.show_notification = kwargs.get('show_notification', False)
        self.notifi_title = kwargs.get('notifi_title', 'Kalliope')
        self.notifi_displaytime = kwargs.get('notifi_displaytime', 5000)
        
        # Basic actions
        self.basic_action = kwargs.get('basic_action', None)
        self.scan_video_lib = kwargs.get('scan_video_lib', False)
        self.scan_music_lib = kwargs.get('scan_music_lib', False)
        self.send_text = kwargs.get('send_text', None)
        self.play_file = kwargs.get('play_file', None)
        
        # Open Windows
        self.gui_window = kwargs.get('show_window', None)
        self.video_path = kwargs.get('show_video_path', None)
        self.music_path = kwargs.get('show_music_path', None)
        self.program_path = kwargs.get('show_program_path', None)
        self.addon_path = kwargs.get('show_addon_path', None)
        self.pvr_path = kwargs.get('show_pvr_path', None)
                
        # Seeking
        self.seek_backward = kwargs.get('seek_backward', None)
        self.seek_forward = kwargs.get('seek_forward', None)
        self.seek_unit = kwargs.get('seek_unit', 'seconds')
        
        # Movies
        self.movie = kwargs.get('movie', None)
        self.random_movie = kwargs.get('random_movie', False)
        self.movie_genre = kwargs.get('movie_genre', None)
        self.movie_trailer = kwargs.get('movie_trailer', None)
        
        # TV-Shows
        self.tvshow = kwargs.get('tvshow', None)
        self.season = kwargs.get('season', None)
        self.episode = kwargs.get('episode', None)
        self.tvshow_option = kwargs.get('tvshow_option', None)
        self.open_season_dir = kwargs.get('open_season_dir', True)
        
        # Live TV
        self.channel = kwargs.get('channel', None)
        self.radio_channel = kwargs.get('radio_channel', None) 
        
        # Music
        self.artist = kwargs.get('artist', None)
        self.genre = kwargs.get('genre', None)
        self.album = kwargs.get('album', None)
        self.song = kwargs.get('song', None)
        self.artist_latest_album = kwargs.get('artist_latest_album', None)
        self.continue_with_artist = kwargs.get('continue_with_artist', False)
        
        # What is running
        self.what_is_running = kwargs.get('what_is_running', False)

        # Continue on second kodi
        self.continue_on_second_host = kwargs.get('continue_on_second_host', None)
        self.second_host_port = kwargs.get('second_host_port', 8080)
        self.second_host_login = kwargs.get('second_host_login', None)
        self.second_host_passwort = kwargs.get('second_host_passwort', None)
        
        # Execute and search for favorites
        self.favorite = kwargs.get('favorite', None)
        self.search_in_favorite = kwargs.get('search_in_favorite', None)
        self.add_to_playlist = kwargs.get('add_to_playlist', False)

        # Open Addon
        self.open_addon = kwargs.get('open_addon', None)
        
        # check if parameters have been provided
        if self._is_parameters_ok():     
            host_is_available = True
            
            if self.login:
                self.kodi = codi("http://" + str(self.host) + ":" + str(self.port) + "/jsonrpc", self.login, self.password)
            else:
                self.kodi= codi("http://" + str(self.host) + ":" + str(self.port) + "/jsonrpc")
            try:
                self.kodi.Player.GetActivePlayers()
            except requests.exceptions.RequestException:
                host_is_available = False

            if host_is_available:    
            # Handle basic action
                
                if self.basic_action:
                    self.ExecuteAction(self.basic_action)
                if self.play_file:
                    self.PlayerOpen(self.play_file)
                if self.scan_video_lib:
                    self.kodi.VideoLibrary.Scan()
                if self.scan_music_lib:
                    self.kodi.AudioLibrary.Scan()
                if self.send_text:
                    self.kodi.Input.SendText({"done": False, "text": self.send_text})
                if self.seek_backward:
                    self.SeekBackward()
                if self.seek_forward:
                    self.SeekForward()
                if self.gui_window or self.video_path or self.music_path or self.program_path or self.addon_path or self.pvr_path:
                    self.ActivateWindow()
 
                # Handle movies
                if self.movie:
                    self.WatchMovie()
                if self.random_movie:
                    self.WatchRandomMovie()
                if self.movie_trailer:
                    self.WatchMovieTrailer()

                # Handle TV-Shows        
                if self.tvshow_option or self.tvshow:
                    self.watch_a_tvshow()
                
                # Handle Live TV
                if self.channel and not self.continue_on_second_host and not self.what_is_running:
                    self.WatchLiveTv()
                if self.radio_channel:
                    self.ListenPvrRadio()
                
                # Handle Music
                if self.artist or self.song or self.album or self.genre or self.artist_latest_album:
                    self.ListenToMusic()

                # What is running
                if self.what_is_running:
                    self.WhatIsRunning()
                    
                # Continue on another instance
                if self.continue_on_second_host:
                    self.ContinueMediaOnSecondKodi()
                    
                # Search and execute favorites    
                if self.favorite:
                    self.Executefavorite()
                    
                # Open Addon
                if self.open_addon:
                    self.OpenAddon()
                
            else:
                self.PrintDebug("Kodi host %s is not reachable" % self.host)
  
    """ 
    Utils    
    """          
    def PrintInfos(self, line):     
        line.encode("utf-8")
        Utils.print_info("[ Kodi ] %s" % line)
        if self.show_notification:
            self.KodiNotification(line)
    
    def PrintDebug(self, line):
        line.encode("utf-8")
        logger.debug("[ Kodi debug ] %s " % line)

    def KodiNotification(self, notfication_to_send):
        return self.kodi.GUI.ShowNotification({"title": self.notifi_title, "message": notfication_to_send, "displaytime": self.notifi_displaytime})
    
    def SayWhatIsRunning(self, line):
        self.say(line)  
        
    def MatchSearch(self, to_search, results, lookingFor='label', limit=10):
        located = []
        to_search = to_search.lower()      
        self.PrintDebug('Trying to match: ' + to_search)
        for result in results:
            result_lower = result[lookingFor].lower()
            if result_lower == to_search:
                self.PrintDebug('Simple match on direct comparison')
                located.append(result)
                continue 
        if not located:
            self.PrintDebug('Simple match failed, trying fuzzy match')
            self.PrintDebug('Processing ' + str(len(results)) + ' items')
            fuzzy_results = []
            matches = process.extractBests(to_search, [d[lookingFor] for d in results], limit=limit, scorer=fuzz.UQRatio, score_cutoff=self.cutoff)
            if len(matches) > 0:
                self.PrintDebug('Best score ' + str(matches[0][1])+"%")
                fuzzy_results += matches
                if len(fuzzy_results) > 0:
                    winners = sorted(fuzzy_results, key=lambda x: x[1], reverse=True)
                    self.PrintDebug('BEST MATCH: '+ winners[0][0] + " " + str(winners[0][1]) +"%")
                    for winner in winners:
                        located.append((item for item in results if item[lookingFor] == winner[0]).next())
            else:
                self.PrintDebug('Nothing found for ' + to_search)
        return located[:limit]
        
    def GetPlayerID(self, playertype=['picture', 'audio', 'video']):
        data = self.kodi.Player.GetActivePlayers()
        result = data.get("result", [])
        if len(result) > 0:
            for curitem in result:
                if curitem.get("type") in playertype:
                    return curitem.get("playerid")
        return None
    
    def GetPlayingItem(self):
        playerid = self.GetPlayerID()
        if playerid is not None:
            data = self.kodi.Player.GetItem({"playerid":playerid, "properties":
                                            ["title", "album", "artist", "season", 
                                            "episode", "showtitle", "tvshowid", "description", "file"]})
            return data['result']['item']
        return None    

    def GetActivePlayProperties(self):
        playerid = self.GetPlayerID()
        if playerid:
            data = self.kodi.Player.GetProperties({"playerid":playerid, "properties":["currentaudiostream", "currentsubtitle", "canshuffle", "shuffled", "canrepeat", "repeat", "canzoom", "canrotate", "canmove"]})
            return data['result']   

    def GetTimeInSeconds(self, seconds):
        my_time = 0
        if self.seek_unit == "seconds":
            my_time = seconds
        if self.seek_unit == "minutes":
            my_time = seconds * 60
        if self.seek_unit == "hours":
            my_time = seconds * 3600     
        return my_time
        
    """
    Basic actions
    """    
    def SeekForward(self):
        to_seek = self.GetTimeInSeconds(self.seek_forward)
        self.PrintInfos("Seeking " + to_seek + " seconds forward")
        to_seek = int(to_seek)
        self.PlayerSeek(to_seek)

    def SeekBackward(self):
        to_seek = self.GetTimeInSeconds(self.seek_backward)
        self.PrintInfos("Seeking " + to_seek +  " seconds backward")
        to_seek = int(to_seek)
        self.PlayerSeek(-to_seek)
    
    def PlayerSeek(self, seconds):
        playerid = self.GetPlayerID()

        if playerid:
          return self.kodi.Player.Seek({"playerid": playerid, "value": {"seconds": seconds}})        

    def PlayerStop(self):
        playerid = self.GetPlayerID()
        if playerid is not None:
            return self.kodi.Player.Stop({"playerid":playerid})
      
    def ExecuteAction(self, action):
        self.PrintInfos('Execute ' + action)
        return self.kodi.Input.ExecuteAction({"action": action})
    
    
    def PlayerOpen(self, file):
        self.PrintInfos('Playing ' + file)
        return self.kodi.Player.Open({"item":{"file": file}})
    
   
    def ActivateWindow(self):
        if self.gui_window:
            return self.kodi.GUI.ActivateWindow({"window": self.gui_window})
        if self.video_path:
            return self.kodi.GUI.ActivateWindow({"window":"videos", "parameters": [self.video_path]})   
        if self.music_path:
            return self.kodi.GUI.ActivateWindow({"window":"music", "parameters": [self.music_path]})   
        if self.program_path:
            return self.kodi.GUI.ActivateWindow({"window":"programs", "parameters": [self.program_path]})   
        if self.addon_path:
            return self.kodi.GUI.ActivateWindow({"window":"addonbrowser", "parameters": [self.addon_path]})   
        if self.pvr_path:
            return self.kodi.GUI.ActivateWindow({"window":"pvr", "parameters": [self.pvr_path]})   

        
    """
    Start Movie
    """ 
    
    def GetUnwatchedMovies(self):
        data = self.kodi.VideoLibrary.GetMovies({"limits":{"start":0,"end":0}, 
                                           "sort":{"method": "dateadded", "order": "descending"},
                                           "filter":{"operator": "lessthan", "field": "playcount", "value": "1"}, 
                                           "properties":["title", "playcount", "dateadded"]})
        located = []
        if 'movies' in data['result']:
            for d in data['result']['movies']:
                located.append({'title': d['title'], 'movieid': d['movieid'], 'label': d['label'], 
                                'dateadded': datetime.datetime.strptime(d['dateadded'], "%Y-%m-%d %H:%M:%S")})
        return located	

    def GetUnwatchedMoviesByGenre(self, genre):
        data = self.kodi.VideoLibrary.GetMovies({"limits":{"start":0,"end":0}, 
                                           "sort":{"method": "dateadded", "order": "descending"},
                                           "filter":{"operator": "lessthan", "field": "playcount", "value": "1",
                                           "field": "genre", "operator": "contains", "value": genre},
                                           "properties":["title", "playcount", "dateadded"]})
        
        located = []
        if 'movies' in data['result']:
            for d in data['result']['movies']:
                located.append({'title': d['title'], 'movieid': d['movieid'], 'label': d['label'],
                                'dateadded': datetime.datetime.strptime(d['dateadded'], "%Y-%m-%d %H:%M:%S")})
        return located
        
    def GetMovieDetails(self, movie_id):
        data = self.kodi.VideoLibrary.GetMovieDetails({"movieid": movie_id, "properties":["resume", "trailer"]})
        return data['result']['moviedetails']

    def GetMovies(self):
        return self.kodi.VideoLibrary.GetMovies()

    def GetVideoGenres(self, genretype='movie'):
        return self.kodi.VideoLibrary.GetGenres({"type": genretype})

    def GetMoviesByGenre(self, genre):
        return self.kodi.scan_video_libbrary.GetMovies({"sort":{"genre": genre}})
        
    def FindVideoGenre(self, genre, genretype='movie'):
        self.PrintDebug('Searching for: ' + genre)
        located = []
        genres = self.GetVideoGenres(genretype)
        if 'result' in genres and 'genres' in genres['result']:
            ll = self.MatchSearch(genre, genres['result']['genres'])
            if ll:
                located = [(item['genreid'], item['label']) for item in ll]
            return located

    def FindMovie(self, to_search):
        self.PrintDebug('Searching for: ' + to_search)
        located = []
        movies = self.GetMovies()
        if 'result' in movies and 'movies' in movies['result']:
            ll = self.MatchSearch(to_search, movies['result']['movies'])
            if ll:
                located = [(item['movieid'], item['label']) for item in ll]
            return located

    def PlayFile(self, path):
        return self.kodi.Player.Open({"item": {"file": path}})

    def PlayMovie(self, movie_id, resume=True):
        return self.kodi.Player.Open({"item": {"movieid": movie_id}, "options": {"resume": resume}})
        
    def WatchMovie(self):
        movie = self.FindMovie(self.movie)
        if len(movie) > 0:
            self.PlayMovie(movie[0][0])
            movie_details = self.GetMovieDetails(movie[0][0])
            if movie_details['resume']['position'] > 0:
                self.PrintInfos('Resume with ' + (movie[0][1]))
            else:
                self.PrintInfos('Start to play ' + (movie[0][1]))
        else:
            self.PrintInfos('Could not find movie ' + self.movie)
            self.say({'notfound' : self.movie})
                    
    def WatchRandomMovie(self):
        movies_array = []
        genre = None
        if self.movie_genre:
            genre = self.FindVideoGenre(self.movie_genre)
            movies_array = self.GetUnwatchedMoviesByGenre(genre[0][1])
        else:
            movies_array = self.GetUnwatchedMovies()
        if not movies_array:
            if genre:
                movies = self.GetMoviesByGenre(genre[0][1])
            else:
                movies = self.GetMovies()
            if 'result' in movies and 'movies' in movies['result']:
                movies_array = movies['result']['movies']
        if movies_array:
            random_movie = random.choice(movies_array)
            if genre:
                self.PrintInfos('Start random movie of genre ' + genre[0][1])
                self.PrintInfos('Start to play ' + random_movie['label'])
            else:
                self.PrintInfos('Start to play ' + random_movie['label'])
            
            self.PlayMovie(random_movie['movieid'], False)
        else:
            self.PrintInfos('Could not find any movies')

    def WatchMovieTrailer(self):
        movie = self.FindMovie(self.movie_trailer)
        if movie:
            movie_id = movie[0][0]
            if movie_id:
                movie_details = self.GetMovieDetails(movie_id)
                if 'trailer' in movie_details and movie_details['trailer']:
                    self.kodi.Player.Open({"item": {"file": movie_details['trailer']}})

                    self.PrintInfos('Start to play trailer for ' + movie_details['label'])
                else:
                    self.PrintInfos('Could not find a trailer for ' + self.movie_trailer)
        else:
            self.PrintInfos('Could not find trailer for ' + self.movie_trailer)
            self.say({'notfound' : self.movie_trailer})

    """
    Start TV-Show
    Resume TV-Show
    Start a random episode from a TV-Show or random episode from a season
    """
    def OpenSeasonDir(self, showid, season):
       return self.kodi.GUI.ActivateWindow({"window":"videos","parameters":["videodb://tvshows/titles/" + str(showid) + "/" + str(season)]})
        
    
    def GetEpisodeDetails(self, ep_id):
        data = self.kodi.VideoLibrary.GetEpisodeDetails({"episodeid": int(ep_id), "properties":["showtitle", "season", "episode", "resume", "tvshowid"]})
        return data['result']['episodedetails']
            
    def GetSpecificEpisode(self, show_id, season, episode):
        data = self.kodi.VideoLibrary.GetEpisodes({"tvshowid": int(show_id), "season": int(season), "properties": ["season", "episode"]})

        if 'episodes' in data['result']:
          correct_id = None
          for episode_data in data['result']['episodes']:
            if int(episode_data['episode']) == int(episode):
              correct_id = episode_data['episodeid']
              break

          return correct_id
        else:
          return None

    def GetShows(self):
        return self.kodi.VideoLibrary.GetTVShows()
    
    def GetLastWatchedShow(self):
        data = self.kodi.VideoLibrary.GetEpisodes({"limits":{"start":0,"end":1},
                                            "filter":{"field": "lastplayed", "operator": "isnot", "value": "0"}, 
                                            "properties":["tvshowid", "showtitle"],
                                            "sort":{"method":"lastplayed", "order":"descending"}})  
        infos = []
        if 'episodes' in data['result']:  
            a = data['result']['episodes']
            infos.append([a[0]['tvshowid'],a[0]['showtitle']])
        return infos  
        
    def GetEpisodesFromShow(self, show_id):
        return self.kodi.VideoLibrary.GetEpisodes({"tvshowid": int(show_id)})

    def GetSeasonsFromShow(self, show_id, season):
        return self.kodi.VideoLibrary.GetEpisodes({"tvshowid": int(show_id), "season": int(season)})

    def GetNextUnwatchedEpisode(self, show_id):
        data = self.kodi.VideoLibrary.GetEpisodes({"limits":{"start":0,"end":1}, 
                                              "tvshowid": int(show_id), 
                                              "filter":{"operator": "lessthan", "field": "playcount", "value": "1"}, 
                                              "properties":["playcount"]})    
        if 'episodes' in data['result']:
            episode = data['result']['episodes'][0]
            return episode['episodeid'] 
        else:
            return None

    def GetLastWatchedEpisode(self, show_id):
        data = self.kodi.VideoLibrary.GetEpisodes({"limits":{"end":1},"tvshowid": int(show_id), 
                                                "filter":{"field":"lastplayed", "operator":"greaterthan", "value":"0"}, 
                                                "properties":["episode", "resume", "season"], 
                                                "sort":{"method":"lastplayed", "order":"descending"}})
        
        if 'episodes' in data['result']:
            episode = data['result']['episodes'][0]
            if episode['resume']['position'] > 0.0:
                episode_id = episode['episodeid']
                return episode_id
            else:
                episode_season = episode['season']
                episode_number = episode['episode']
                episode_id = self.GetSpecificEpisode(show_id, episode_season, episode_number + 1)
                if episode_id is not None:
                    check = self.GetEpisodeDetails(episode_id)
                    if show_id == check['tvshowid']:
                        return episode_id
                    else:
                        return None
                else:
                    return None

    def GetFirstEpisode(self, show_id, season=None):
        if season:
            data = self.kodi.VideoLibrary.GetEpisodes({"limits":{"end":1}, "tvshowid": int(show_id), "season": int(season)})  
        else:
            data = self.kodi.VideoLibrary.GetEpisodes({"limits":{"end":1}, "tvshowid": int(show_id)})
        
        if 'episodes' in data['result']:
            episode = data['result']['episodes'][0]
            return episode['episodeid']
        else:
            return None

    def GetNewestEpisodeFromShow(self, show_id):
        data = self.kodi.VideoLibrary.GetEpisodes({"limits":{"end":1}, "tvshowid": int(show_id),
                                                "filter":{"field":"lastplayed", "operator":"greaterthan", "value":"0"},
                                                "properties":["playcount", "episode", "season"],
                                                "sort":{"method": "dateadded", "order": "descending"}})
        if 'episodes' in data['result']:
            episode = data['result']['episodes'][0]
            episode_season = episode['season']
            episode_number = episode['episode']
            episode_id = self.GetSpecificEpisode(show_id, episode_season, episode_number + 1)
            if episode_id is not None:
                check = self.GetEpisodeDetails(episode_id)
                if show_id == check['tvshowid']:
                    return episode_id
                else:
                    return None
            else:
                return None
        else:
            return None
            
    def FindTvShow(self, tvshow):
        self.PrintDebug('Searching for: ' + tvshow)
        located = []
        shows = self.GetShows()
        if 'result' in shows and 'tvshows' in shows['result']:
            ll = self.MatchSearch(tvshow, shows['result']['tvshows'])
            if ll:
                located = [(item['tvshowid'], item['label']) for item in ll]
            return located


    def PlayEpisode(self, ep_id, resume=True):
        return self.kodi.Player.Open({"item": {"episodeid": ep_id}, "options": {"resume": resume}})
            
    def watch_a_tvshow(self):
        '''
        resume_unwatched_show:       Continue to watch the next unwatched marked episode of the given show
        resume_last_watched_show:    Continue to watch the last episode or next episode of the given show
        random_episode:              Random episode of the given show
        newest_episode:              Plays the newest unwatched episode of the given show
        continue_last_show:          Continue the last played show
        '''
        episode_id = None
        if self.tvshow:
            show = self.FindTvShow(self.tvshow)

            if len(show) > 0:
                if self.tvshow_option:
                    if self.tvshow_option == "resume_unwatched_show":
                        episode_id = self.GetNextUnwatchedEpisode(show[0][0])
                        if not episode_id:
                            print_not_found = ('There are no unwatched marked episodes for ' + show[0][1])
                            say_not_found = ({'NothingToResume' : show[0][1]})
                    
                    if self.tvshow_option == "resume_last_watched_show":
                        episode_id = self.GetLastWatchedEpisode(show[0][0])
                        if not episode_id:
                            print_not_found = ('There are no last watched episodes for ' + show[0][1])
                            say_not_found = ({'NothingToResume' : show[0][1]})
                            
                    if self.tvshow_option == "random_episode":
                        if self.season:
                            episodes_result = self.GetSeasonsFromShow(show[0][0], self.season)
                        else:
                            episodes_result = self.GetEpisodesFromShow(show[0][0])
                        episodes_array = []
                        for episode in episodes_result['result']['episodes']:
                            episodes_array.append(episode['episodeid'])
                        episode_id = random.choice(episodes_array)
                        
                    if self.tvshow_option == "newest_episode":
                        episode_id = self.GetNewestEpisodeFromShow(show[0][0])
                        if not episode_id:
                            print_not_found = ('There are no new unwatched episodes for ' + show[0][1])
                            say_not_found = ({'NothingToResume' : show[0][1]})
                        

                else:
                    if self.season and self.episode: 
                        episode_id = self.GetSpecificEpisode(show[0][0], self.season, self.episode)
                        if not episode_id:
                            print_not_found = ('Could not find Season ' + str(self.season) + ' episode ' + str(self.episode))
                
                    elif self.season and not self.episode:
                        episode_id = self.GetFirstEpisode(show[0][0], self.season)      
                    else:
                        episode_id = self.GetFirstEpisode(show[0][0])   

            else:
                print_not_found = ('Could not find ' + self.tvshow)
                say_not_found = ({'notfound' : self.tvshow}) 
        
        elif self.tvshow_option == "continue_last_show":
            show = self.GetLastWatchedShow()
            if len(show) > 0:
                episode_id = self.GetLastWatchedEpisode(show[0][0])
                if not episode_id:
                    episode_id = self.GetNextUnwatchedEpisode(show[0][0])
                    if not episode_id:  
                        print_not_found = ('There is no tvshow to continue')
            else:   
                print_not_found = ('There is no tvshow to continue')
        else:
            print_not_found = ('There is no tvshow to continue')
            say_not_found = ({'notfound' : ' '}) 
        
        if episode_id:
            episode_details = self.GetEpisodeDetails(episode_id)             
            if self.tvshow_option == "random_episode":
                self.PrintInfos('Play random episode for ' + episode_details['showtitle'] +  ' start with episode ' + episode_details['label'])
            elif self.tvshow_option == "continue_last_show":
                self.PrintInfos(print_info)
                self.PrintInfos('Continue to play ' + episode_details['showtitle'] + ' - ' + episode_details['label'])
            else:
                if episode_details['resume']['position'] > 0:
                    self.PrintInfos('Resume ' + episode_details['showtitle'] + ' - ' + episode_details['label'])
                else:
                    self.PrintInfos('Start to play ' + episode_details['showtitle'] +  ' - ' + episode_details['label'])
            
            if self.open_season_dir:
                self.OpenSeasonDir(show[0][0], episode_details['season'])
                
            self.PlayEpisode(episode_id)    

        else:
            self.PrintInfos('There is nothing to play')
            self.say(say_not_found)
           
    """        
    Live TV       
    """        
            
    def PlayChannel(self, ch_id):
        return self.kodi.Player.Open({"item": {"channelid": ch_id}})
        
    def GetTvChannels(self):
        return self.kodi.PVR.GetChannels({"channelgroupid": "alltv"})    
    
    def GetRadioChannels(self):
        return self.kodi.PVR.GetChannels({"channelgroupid": "allradio"})    

    def GetBroadcasts(self, ch_id):
        return self.kodi.PVR.GetBroadcasts({"channelid": ch_id,
                                   "properties": ["isactive", "title"]})      
        
    def FindTvChannel(self, to_search):
        self.PrintDebug('Searching for show ' + to_search)
        located = []
        channels = self.GetTvChannels()

        if 'result' in channels and 'channels' in channels['result']:
            ll = self.MatchSearch(to_search, channels['result']['channels'])
            if ll:
                located = [(item['channelid'], item['label']) for item in ll]
        return located        
    
    def WatchLiveTv(self):
        if self.channel:
            channel = self.FindTvChannel(self.channel)
            if len(channel) > 0:
                self.PrintInfos('Open Channel: ' + channel[0][1])
                self.PlayChannel(channel[0][0])
            else:
                self.PrintInfos('Could not found ' + self.channel)
                self.say({'notfound' : self.channel})
    
    def FindRadioChannel(self, to_search):
        self.PrintDebug('Searching for show ' + to_search)
        located = []
        channels = self.GetRadioChannels()

        if 'result' in channels and 'channels' in channels['result']:
            ll = self.MatchSearch(to_search, channels['result']['channels'])
            if ll:
                located = [(item['channelid'], item['label']) for item in ll]
        return located        
    
    def ListenPvrRadio(self):
        if self.radio_channel:
            channel = self.FindRadioChannel(self.radio_channel)
            if len(channel) > 0:
                self.PrintInfos('Play channel  ' + channel[0][1])
                self.PlayChannel(channel[0][0])
            else:
                self.PrintInfos('Could not find ' + self.radio_channel)
                self.say({'notfound' : self.radio_channel})
                
    """
    Start Music
    Start Genre
    Start a random music
    """
    

    def GetAudioPlaylistItems(self):
        return self.kodi.Playlist.GetItems({"playlistid": 0})
        
    def ClearAudioPlaylist(self):
        return self.kodi.Playlist.Clear({"playlistid": 0})

    def GetArtistAlbums(self, artist_id):
        return self.kodi.AudioLibrary.GetAlbums(filters={"artistid": int(artist_id)})
        
    def GetAlbums(self):
        return self.kodi.AudioLibrary.GetAlbums()
        
    def GetAlbumSongs(self, album_id):
        return self.GetSongs(filters={"albumid": int(album_id)})

    def GetMusicGenres(self):
        return self.kodi.AudioLibrary.GetGenres
        
    def GetArtistSongs(self, artist_id):
        return self.GetSongs(filters={"artistid": int(artist_id)})   

    def GetSongs(self, filters=None):
        if filters:
            return self.kodi.AudioLibrary.GetSongs({"filter":filters, "limits":{"start":0,"end":100}, "sort":{"method": "rating", "order": "ascending"}})
        else:
            return self.kodi.AudioLibrary.GetSongs({"limits":{"start":0,"end":100}, "sort":{"method": "rating", "order": "descending"}})

    def GetMusicArtists(self, filters=None):
        return self.kodi.AudioLibrary.GetArtists({"albumartistsonly": False},)

    def GetMusicGenres(self):
        return self.kodi.AudioLibrary.GetGenres()

    def GetSongsByGenre(self, genre):
        return self.GetSongs(filters={"field": "genre", "operator": "is", "value": genre})

    def GetNewestAlbumFromArtist(self, artist_id):
        data = self.kodi.AudioLibrary.GetAlbums({"limits":{"start":0,"end":1}, 
                                                "filter":{"artistid": int(artist_id)}, 
                                                "sort":{"method": "year", "order": "descending"}})
        if 'albums' in data['result']:
            album = data['result']['albums'][0]
            return album['albumid']
        else:
            return None
    
    def GetAlbumDetails(self, album_id):
        data = self.kodi.AudioLibrary.GetAlbumDetails({"albumid": int(album_id), "properties":["artist"]})
        return data['result']['albumdetails']
    
    def AddSongToPlaylist(self, song_id):
        return self.kodi.Playlist.Add({"playlistid": 0, "item": {"songid": int(song_id)}})

    def AddSongsToPlaylist(self, song_ids, shuffle=False):
        songs_array = []
        if shuffle:
            random.shuffle(song_ids)
        songs_array = [dict(songid=song_id) for song_id in song_ids]
        
        for a in [songs_array[x:x+2000] for x in range(0, len(songs_array), 2000)]:
            len_items = len(a)
            self.PrintDebug('Adding ' + str(len_items) + ' items to the queue...')
            res = self.kodi.Playlist.Add({"playlistid": 0, "item": a})
        return res

    def StartAudioPlaylist(self, playlist_file=None):
        if playlist_file is not None and playlist_file != '':
            return self.kodi.Player.Open({"item": {"file": playlist_file}})
        else:
            return self.kodi.Player.Open({"item": {"playlistid": 0}})

    def AddAlbumToPlaylist(self, album_id, shuffle=False):
        songs_result = self.GetAlbumSongs(album_id)
        songs = songs_result['result']['songs']
        songs_array = []
        for song in songs:
            songs_array.append(song['songid'])

        return self.AddSongsToPlaylist(songs_array, shuffle)

    def FindSong(self, to_search, artist_id=None, album_id=None):
        self.PrintDebug('Searching for ' + to_search)

        located = []
        if album_id:
            songs = self.GetAlbumSongs(album_id)
        elif artist_id:
            songs = self.GetArtistSongs(artist_id)
        else:
            songs = self.GetSongs()
        if 'result' in songs and 'songs' in songs['result']:
            ll = self.MatchSearch(to_search, songs['result']['songs'])
            if len(ll) > 0:
                located = [(item['songid'], item['label']) for item in ll]

        return located    

    def FindMusicGenre(self, to_search):
        self.PrintDebug('Searching for ' + to_search)

        located = []
        genres = self.GetMusicGenres()
        if 'result' in genres and 'genres' in genres['result']:
            ll = self.MatchSearch(to_search, genres['result']['genres'])
            if len(ll) > 0:
                located = [(item['genreid'], item['label']) for item in ll]

        return located

    def FindArtist(self, to_search):
        self.PrintDebug('Searching for ' + to_search)
        
        located = []
        artists = self.GetMusicArtists()
        if 'result' in artists and 'artists' in artists['result']:
            ll = self.MatchSearch(to_search, artists['result']['artists'], 'artist')
            if len(ll) > 0:
                located = [(item['artistid'], item['label']) for item in ll]

        return located

    def FindAlbum(self, to_search, artist_id=None):
        self.PrintDebug('Searching for album ' + to_search)

        located = []
        albums = self.GetAlbums()
        if 'result' in albums and 'albums' in albums['result']:
            albums_list = albums['result']['albums']
            ll = self.MatchSearch(to_search, albums['result']['albums'])
            if len(ll) > 0:
                located = [(item['albumid'], item['label']) for item in ll]

        return located

    def ListenToMusic(self, shuffle=False):
        artist = None
        songs_array = None
        if self.artist and not self.song and not self.album:
            artist = self.FindArtist(self.artist)
            if len(artist) > 0:            
                songs_result = self.GetArtistSongs(artist[0][0])    
                if 'songs' in songs_result['result']:
                    songs = songs_result['result']['songs']
                    songs_array = []
                    for song in songs:
                        songs_array.append(song['songid'])
                    
                    self.PrintInfos('Adding ' + str(len(songs_array)) + ' songs of ' + artist[0][1] + ' to playlist')
                    self.PlayerStop()
                    self.ClearAudioPlaylist() 
                    self.AddSongsToPlaylist(songs_array)
                    self.StartAudioPlaylist()
            else: 
                self.PrintInfos('No songs found for ' + self.artist)
                self.say({'notfound' : self.artist})

        elif self.song:
            if artist:
                single_song = self.FindSong(self.song, artist[0][0])
                if self.continue_with_artist:
                    songs_result = self.GetArtistSongs(artist[0][0])    
                    if 'songs' in songs_result['result']:
                        songs = songs_result['result']['songs']
                        songs_array = []
                        for song in songs:
                            songs_array.append(song['songid'])
            else:
                single_song = self.FindSong(self.song) 

            if len(single_song) > 0:
                self.PrintInfos('Playing song '+ single_song[0][1])
                self.PlayerStop()
                self.ClearAudioPlaylist()
                if songs_array:
                    self.AddSongToPlaylist(single_song[0][0])
                    self.PrintInfos('Contiune with artist is True')
                    self.AddSongsToPlaylist(songs_array)
                else:
                    self.AddSongToPlaylist(single_song[0][0])
                self.StartAudioPlaylist()
            else:
                self.PrintInfos('Could not find song ' + self.song)
                self.say({'notfound' : self.song})

        elif self.album:
            if artist:
                album = self.FindAlbum(self.album, artist[0][0])  
            else:
                album = self.FindAlbum(self.album)            
            if len(album) > 0:
                album_artist = self.GetAlbumDetails(album[0][0])['artist']                
                self.PrintInfos('Play ' + ''.join(album_artist) + ' - ' + album[0][1])
                self.PlayerStop()
                self.ClearAudioPlaylist() 
                self.AddAlbumToPlaylist(album[0][0], shuffle)
                self.StartAudioPlaylist()
            
            else: 
                self.PrintInfos('Could not find album ' + self.album)
                self.say({'notfound' : self.album})
                
        elif self.genre:
            genre = self.FindMusicGenre(self.genre)
            if len(genre) > 0:
                songs_result = self.GetSongsByGenre(genre[0][1])
                if 'songs' in songs_result['result']:
                    songs = songs_result['result']['songs']
                    songs_array = []
                    for song in songs:
                        songs_array.append(song['songid'])
                    
                    self.PrintInfos('Adding ' + str(len(songs_array)) + ' songs of the genre ' + genre[0][1] + ' to playlist')
                    self.PlayerStop()
                    self.ClearAudioPlaylist() 
                    self.AddSongsToPlaylist(songs_array, True)
                    self.StartAudioPlaylist()
            else: 
                self.PrintInfos('Could not find genre ' + self.genre)
                self.say({'notfound' : self.genre})

        elif self.artist_latest_album:
            artist = self.FindArtist(self.artist_latest_album)
            if artist:
                album_id = self.GetNewestAlbumFromArtist(artist[0][0])
                if album_id:
                    album_label = self.GetAlbumDetails(album_id)['label']
                    self.PrintInfos('Play ' + artist[0][1] + ' - ' + album_label)
                    self.PlayerStop()
                    self.ClearAudioPlaylist()
                    self.AddAlbumToPlaylist(album_id)
                    self.StartAudioPlaylist()
            else: 
                self.PrintInfos('Could not find latest album of  ' + self.artist_latest_album)
                self.say({'notfound' : self.artist_latest_album})

    """
    What is running
    """

    def WhatIsRunning(self):     
        '''
        current_on_tvchannel
        next_on_tvchannel
        next_on_current_tvchannel
        current
        '''
        if self.what_is_running == "current_on_tvchannel":
            if self.channel:
                ch_id = self.FindTvChannel(self.channel)
                if len(ch_id) > 0:
                    all_bc = self.GetBroadcasts(ch_id[0][0])
                    current = []
                    next = []
                    bc = all_bc['result']['broadcasts']
                    for x,y in enumerate(bc):
                        if y['isactive'] == True:
                            current.append(y)
                            next.append([bc[x+1]])

                    self.PrintInfos('Currently on ' + ch_id[0][1] + ' - ' + current[0]['title'])
                    self.say({"say_pvr_title_now" : current[0]['title'],
                              "say_pvr_channel" : ch_id[0][1]})
                else:
                    self.PrintInfos('Could not find channel ' + self.channel)
                    self.say({"say_channel_not_found" : self.channel}) 
            else:
                self.PrintInfos('There are no TV channels')         
        
        elif self.what_is_running == "next_on_tvchannel":
            if self.channel:
                ch_id = self.FindTvChannel(self.channel)
                if len(ch_id) > 0:
                    all_bc = self.GetBroadcasts(ch_id[0][0])
                    current = []
                    next = []
                    bc = all_bc['result']['broadcasts']
                    for x,y in enumerate(bc):
                        if y['isactive'] == True:
                            current.append(y)
                            next.append([bc[x+1]])

                    self.PrintInfos('Next on ' + ch_id[0][1] + ' - ' + next[0][0]['title'])
                    self.say({"say_pvr_title_next" : next[0][0]['title'],
                              "say_pvr_channel" : ch_id[0][1]})  

                else:
                    self.PrintInfos('Could not find Channel ' + self.channel)
                    self.say({"say_channel_not_found" : self.channel}) 
            else:
                self.PrintInfos('There are no TV channels')        
                               
        elif self.what_is_running == "next_on_current_tvchannel":    
            result = self.GetPlayingItem()
            if result['type'] == 'channel':
                ch_id = self.FindTvChannel(result['label'])
                all_bc = self.GetBroadcasts(ch_id[0][0])
                next = []
                bc = all_bc['result']['broadcasts']
                
                for x,y in enumerate(bc):
                    if y['isactive'] == True:
                        next.append([bc[x+1]])

                self.PrintInfos('Next on ' + ch_id[0][1] + ' - ' + next[0][0]['title'])
                self.say({"say_current_next" : next[0][0]['title']}) 
        
        elif self.what_is_running == "current":
            result = self.GetPlayingItem()
            if result:
                if result['type'] == 'episode':
                    if result['showtitle']:
                        result2print = result['showtitle']
                        self.PrintInfos('Currently playing show ' + result2print)
                        self.say({"say_show_title": result2print})

                    if result['title']:
                        result2print = result['title']
                        self.PrintInfos('Currently playing episode ' + result2print)
                        self.say({"say_episode_title": result2print})
                
                elif result['type'] == 'song' or result['type'] == 'musicvideo':
                    if result['title']:
                        result2print = result['title']
                        self.PrintInfos('Currently playing song ' + str(result2print))
                        self.say({"say_song_title": result2print})
                    
                    if result['artist']:
                        result2print = ', '.join(result['artist'])
                        self.PrintInfos('Currently playing artist ' + result2print)
                        self.say({"say_song_artist": result2print})
                    
                    if result['album']:
                        result2print = result['album']
                        self.PrintInfos('Currently playing album ' + result2print)
                        self.say({"say_song_album": result2print})

                elif result['type'] == 'movie':
                    if result['title']:
                        result2print = result['title']
                        self.PrintInfos('Currently playing movie ' + result2print)
                        self.say({"say_movie_title": result2print})
                
                elif result['type'] == 'unknown':
                    if result['title']:
                        result2print = result['title']
                    elif result['label']:
                        result2print = result['label']
                    if result2print:
                        self.PrintInfos('Currently playing ' + result2print)
                        self.say({"say_unknown_title": result2print})
                    else:
                        self.PrintInfos('Could not find anything')
                        self.say({"say_no_media_infos_found": " " })
                    
                elif result['type'] == 'channel':
                    if result['title']:
                        result2print = result['title']
                        self.PrintInfos('Currently playing channel ' + result2print)
                        self.say({"say_pvr_title": result2print})                
                
                elif result['type'] == 'file':
                    if result['title']:
                        result2print = result['title']
                        self.PrintInfos('Currently playing file ' + result2print)
                        self.say({"say_file_title": result2print})
                        
            else:
                self.PrintInfos('Could not find anything')
                self.say({"say_no_media_infos_found": " " })
    
    
    """
    Resume media on second Kodi
    """
    def ContinueMediaOnSecondKodi(self):
        host_is_available = True
        types = ['episode', 'movie', 'channel', 'unknown']
        
        if self.continue_on_second_host:
            second_kodi = codi("http://" + str(self.continue_on_second_host) + ":" + str(self.second_host_port) + "/jsonrpc", self.second_host_login, self.second_host_passwort)
        else:
            second_kodi = codi("http://" + str(self.continue_on_second_host) + ":" + str(self.second_host_port) + "/jsonrpc")
        try:
            second_kodi.Player.GetActivePlayers()
        except requests.exceptions.RequestException:
            host_is_available = False
       
        if host_is_available:
            result = self.GetPlayingItem()
            if result:
                self.kodi.Input.ExecuteAction({"action": "stop"})
                sleep(1)
                if result['type'] in types:
                    if result['type'] == 'episode':
                        self.PrintInfos("Continue TV Show " + result['showtitle'] + " on " + self.continue_on_second_host)
                        second_kodi.Player.Open({"item": {"episodeid": result['id']}, "options": {"resume": True}})
                        
                    elif result['type'] == 'movie':
                        self.PrintInfos("Continue movie " + result['label'] + " on " + self.continue_on_second_host)
                        second_kodi.Player.Open({"item": {"movieid": result['id']}, "options": {"resume": True}})
                        
                    elif result['type'] == 'channel':
                        self.PrintInfos("Continue channel " + result['label'] + " on " + self.continue_on_second_host)
                        second_kodi.Player.Open({"item": {"channelid": result['id']}})
                        
                    elif result['type'] == 'unknown':
                        self.PrintInfos("Continue file " + result['label'] + " on " + self.continue_on_second_host)
                        second_kodi.Player.Open({"item": {"file": result['file']}})
                    
                    elif result['type'] == 'song':
                        self.PrintInfos("Continue song " + result['label'] + " on " + self.continue_on_second_host)
                        second_kodi.Player.Open({"item": {"file": result['file']}})
                else:
                    self.PrintInfos("Unidentified type, can not process")
            else:
                 self.PrintInfos("There is nothing playing on host")
        else:
            self.PrintInfos("Please set the IP of the second KODI")
    
    """
    Search and execute favorites
    """
    def FindFavorite(self, to_search):
        located = []
        favorites = self.GetFavorites()
        if 'result' in favorites and 'favourites' in favorites['result']:
            ll = self.MatchSearch(to_search, favorites['result']['favourites'], 'title')
            if ll:
                if ll[0]['type'] == "window":
                    located = [(item['type'], item['windowparameter'], item['title']) for item in ll]
                if ll[0]['type'] == "media":
                    located = [(item['type'], item['path'], item['title']) for item in ll]
                    
        return located    


    def GetFavorites(self):
        return self.kodi.Favourites.GetFavourites({'properties':['path', 'windowparameter']})    
        

    def Executefavorite(self):
        located = []
        favorite = self.FindFavorite(self.favorite)
        file_array = []
        
        if favorite:
            if self.search_in_favorite:
                if favorite[0][0] == 'window':            
                    files = self.kodi.Files.GetDirectory({"directory":favorite[0][1]})
                    if 'result' in files and 'files' in files['result']:
                        ll = self.MatchSearch(self.search_in_favorite, files['result']['files'], 'label')
                        if ll:
                            located = [(item['filetype'], item['file'], item['label']) for item in ll]
                            if located[0][0] == 'file':
                                if self.add_to_playlist:
                                    for file in files['result']['files']:
                                        if file['filetype'] == 'file':
                                            file_array.append(file['file'])
                                            
                                    self.kodi.Playlist.Clear({"playlistid": 1})
                                    self.kodi.Playlist.Add({"playlistid": 1, "item": {"file": located[0][1]}})
                                    for file in file_array:
                                        self.kodi.Playlist.Add({"playlistid": 1, "item": {"file": file}})
                                    self.PrintInfos('Adding ' + str(len(file_array)) + ' files of ' + favorite[0][2] + ' to playlist')
                                    self.PlayerStop()
                                    self.PrintInfos("Start to play " + located[0][2])
                                    self.kodi.Player.Open({"item": {"playlistid": 1}})
                                    
                                else:
                                    self.kodi.Player.Open({"item": {"file": located[0][1]}})
                                    self.PrintInfos("Start to play " + located[0][2])

                            if located[0][0] == 'directory':
                                self.kodi.GUI.ActivateWindow({"window":"videos","parameters": [located[0][1]]})
                                self.PrintInfos("Opening " + located[0][2])
                        else:
                            self.PrintInfos("Could not find " + self.search_in_favorite)
                            self.say({'notfound' : self.search_in_favorite})
                else:
                    self.PrintInfos("Favorite need to be a directory")

            else:
                if favorite[0][0] == 'media':
                    self.kodi.Player.Open({"item": {"file": favorite[0][1]}, "options": {"resume": True}})
                    self.PrintInfos("Start to play " + favorite[0][2])
                if favorite[0][0] == 'window':
                    self.kodi.GUI.ActivateWindow({"window":"videos","parameters": [favorite[0][1]]})
                    self.PrintInfos("Opening  " + favorite[0][2])
        else:
            self.PrintInfos("Could not find favorite " + self.favorite)
            self.say({'notfound' : self.favorite})

    """
    Find and open addon
    """
    def GetAddons(self, content):
        if content:
            return self.kodi.Addons.GetAddons({"content": content, 'properties':["name"]})
        else:
            return self.kodi.Addons.GetAddons({'properties':["name"]})

    def FindAddon(self, to_search):
        located = []
        for content in ['video', 'audio', 'image', 'executable']:
            addons = self.GetAddons(content)
            if 'result' in addons and 'addons' in addons['result']:
                ll = self.MatchSearch(to_search, addons['result']['addons'], 'name')
                if ll:
                    located = [(item['addonid'], item['name']) for item in ll]

        return located
        
    def OpenAddon(self): 
        addon = self.FindAddon(self.open_addon)
        if addon:
            self.kodi.GUI.ActivateWindow({"window": "home"})
            self.kodi.Addons.ExecuteAddon({"addonid": addon[0][0]})
            self.PrintInfos('Execute addon ' + addon[0][1])
        else:
            PrintInfos('Could not find addon ' + self.addon)


    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException
        """
        if self.login is not None and self.password is None:
            raise MissingParameterException("You musst set a password")
        return True

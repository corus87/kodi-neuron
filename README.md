# Kodi neuron
## Control Kodi with Kalliope using the json api



## Installation
```bash
kalliope install --git-url https://github.com/corus87/kodi-neuron
```

## Options
| parameter               | default   | choices       | comments                                                            |
|-------------------------|-----------|---------------|---------------------------------------------------------------------|
|                         |           |               |                                                                     |
| **BASICS :**            |           |               |                                                                     |
| host	                  | localhost |               |                                                                     |           
| port	                  | 8080      | integer       |                                                                     |                    
| login	                  | None      | string        |                                                                     |          
| password                | None      | string        |                                                                     |    
| cutoff                  | 70        | 1 - 100       | Percentage of matching the item your are looking for                |          
| show_notifaction        | True      | True/False    | Shows a notification in Kodi about the given action                 |
| notifi_title            | Kalliope  | string        | The title of the notification                                       |
| notifi_display_time     | 5000      | integer       | The display time of the notification in mili seconds                |
| scan_video_lib          | False     | True/False    | Scan video database                                                 |
| scan_music_lib          | False     | True/False    | Scan music database                                                 |
| send_text               |           | string        | If a text field is open in Kodi, you can send a text to it          |
| play_file               |           | string        | You can play every media file, even from a plugin, you need only the path |
| basic_action            |           | [Kodi DOCS](https://kodi.wiki/view/JSON-RPC_API/v8#Input.Action) | Check the KODI API Docs for Input.Action |
| player_goto		  | None      | string	      | Skip a track in the playlist, options are `next`, `previous` and `specific` |
| show_window             |           | [Kodi DOCS](https://kodi.wiki/view/JSON-RPC_API/v8#GUI.Window) | Opens a specific window in Kodi |
| video_path              |           | [Kodi DOCS](https://kodi.wiki/view/Opening_Windows_and_Dialogs) | Opens a specific video path, can also be a non library path |
| music_path              |           | [Kodi DOCS](https://kodi.wiki/view/Opening_Windows_and_Dialogs) | Opens a specific music path, can also be a non library path |
| program_path            |           | [Kodi DOCS](https://kodi.wiki/view/Opening_Windows_and_Dialogs) | Opens a specific program path 
| addon_path              |           | [Kodi DOCS](https://kodi.wiki/view/Opening_Windows_and_Dialogs) | Opens a specific addon path 
| pvr_path                |           | [Kodi DOCS](https://kodi.wiki/view/Opening_Windows_and_Dialogs) | Opens a specific pvr path |
| seek_backward           |           | integer       | Seek backwards by a given time                                      |  
| seek_forward            |           | integer       | Seek forwards by a given time                                       |
| seek_unit               | seconds   | string        | Set one of the following units: seconds, minutes, hours             |
|                         |           |               |                                                                     |
| **MOVIES :**            |           |               |                                                                     |
| movie                   |           | string        | Play a movie from your library                                      |
| random_movie            |           |               | Play a random movie from your library                               |
| movie_genre             |           | string        | Play a movie by a given genre                                       |
| movie_trailer           |           | string        | Play a trailer from movie in your library                           |
|                         |           |               |                                                                     |
| **TVSHOWS :**           |           |               |                                                                     |
| tvshow                  |           | string        | Without tvshow_option parameter, it starts the first episode        |
| tvshow_option           |           | resume_unwatched_show | Continue to watch the next unwatched marked episode of the given show |
|                         |           | resume_last_watched_show | Continue to watch the last episode or next episode of the given show |
|                         |           | random_episode | Random episode of the given show |
|                         |           | newest_episode | Plays the newest unwatched episode of the given show |
|                         |           | continue_last_show | Continue the last played show |                             
| season                  |           | integer       | Play the first episode of the given season and tvshow               |
| episode                 |           | integer       | Play a specific episode of the given tvshow                         |
| open_season_dir         | True      | True/False    | When starting an episode, the current season will open              |
|                         |           |               |                                                                     |
| **PVR :**               |           |               |                                                                     |
| channel                 |           | string        | Start a PVR channel                                                 |
| radio_channel           |           | string        | Start a PVR radio channel                                           |
|                         |           |               |                                                                     |
| **MUSIC :**             |           |               |                                                                     |
| artist                  |           | string        | Play music of the given artist                                      |
| genre                   |           | string        | Play music of the given genre                                       |
| album                   |           | string        | Play the given album                                                |
| song                    |           | string        | Play a single song, can be combine with artist e.g play without me from Eminem |
| continue_with_artist    | False     | True/false    | If true and you want to start a single song with the given artist, Kalliope will continue with the artist |
| artist_latest_album     |           | string        | Play the latest album of the given artist                           |
|                         |           |               |                                                                     |
| **WHATS RUNNING :**     |           |               |                                                                     |
| what_is_running         |           | current_on_tvchannel | Ask what is running on the given channel - needs the channel parameter |                                                                                                      
|                         |           | next_on_tvchannel | Ask what is running next on the given channel - needs the channel parameter |
|                         |           | next_on_current_tvchannel | Ask what is running next on your current watching channel |
|                         |           | current                   | Ask what is currently running |   
|                         |           | rating                    | Ask what is the rating of the current show/movie |   
|                         |           |               |                                                                     |
| **MISSCELLANEOUS :**    |           |               |                                                                     |
| continue_on_second_host |           | integer       | Set here the IP of your second Kodi, to continue the currently running media on a second machine |
| second_host_port        | 8080      | integer       | Set here the port of your second Kodi                                |        
| second_host_login       |           | string        | Set here the login of your second Kodi                               |        
| second_host_passwort    |           | string        | Set here the password of your second Kodi                            |
| favorite                |           | string        | This can be a window or a media type                                 |
| search_in_favorite      |           | string        | If your favorite is a directory, you can search in there and execute a media or window type |
| add_to_playlist         | False     | True/False    | If True your favorite directory (in my case radio stations) will added to the playlist so you can easy skip to the next item |
| open_addon              |           | string        | Open the given addon                                                 |                            
| check_movie_in_database |           | string        | Check if a movie is in your database |
| check_runtime  	  |           | True/False    | Ask how many minutes/hours of the current show/movie remains |
| search_youtube          |           | string        | If Youtube addon is installed, you can search on youtube and it will start play the first search result |
| set_volume_to           |           | string/int    | Set volume between 0-100, it doesn't need to be a clean integer, it will remove everything from the string except the integers |
| get_volume		  | False     | True/False    | Get the current Volume |


## Return values for global
| Name                     | Description                                        |
|--------------------------|----------------------------------------------------|
| notfound                 | If not found the asked parameter will return       |


## Return values for what_is_running = current
| Name                     | Description                                        |
|--------------------------|----------------------------------------------------|
| say_show_title           | Returns the running show title                     |
| say_episode_title        | Returns the running episode title                  |
| say_song_title           | Returns the running song title                     |
| say_song_artist          | Returns the running artist name                    |
| say_song_album           | Returns the running album title                    |
| say_movie_title          | Returns the current running movie title            |            
| say_unknown_title        | Returns the title of unknown type                  |                
| say_pvr_title            | Returns the running PVR title                      |
| say_file_title           | Returns the running file title                     |
| say_no_media_infos_found | Returns an empty string                            |

## Return values for what_is_running = current_on_tvchannel
| Name                     | Description                                        |
|--------------------------|----------------------------------------------------|
| say_pvr_title_now        | Returns the show title of the given channel        |
| say_pvr_channel          | Returns the channel you asked for                  |
| say_channel_not_found    | Returns the asked channel if not found             |
| imdb_rating		   | Returns the imdb rating                            |
| no_rating                | Returns None if no rating is found                 |


## Return values for what_is_running = next_on_tvchannel
| Name                     | Description                                        |
|--------------------------|----------------------------------------------------|
| say_pvr_title_next       | Returns the next show title of the given channel   |
| say_pvr_channel          | Returns the next channel                           |
| say_channel_not_found    | Returns the asked channel if not found             |


## Return values for what_is_running = next_on_current_tvchannel
| Name                     | Description                                        |
|--------------------------|----------------------------------------------------|
| say_current_next         | returns the next show title on the current channel |

## Return values for check_runtime
| Name			   | Descripton                                         |
|--------------------------|----------------------------------------------------|
| runtime                  | Returns True if a show/movie is runnning           |
| hours                    | Returns the remaining hours                        |
| minutes                  | Returns the remaining minutes                      |

## Return values for check_movie_in_database
| Name			   | Descripton                                         |
|--------------------------|----------------------------------------------------|
| movie_found              | Returns a single found movie                       |
| say_found_movie_labels   | Returns all movies which are found                 |
| say_no_movie_found       | Returns the ask movie, if not found                |
  
## Return values for get_volume
| Name			   | Descripton						|
|--------------------------|----------------------------------------------------|
| current_volume	   | Returns the current volume				|
| muted			   | Returns the current mute status --> true or false  |

## Synapses example
```
  - name: "kodi-play-pause"
    signals:
      - order: "Pause kodi"        
    neurons:
      - kodi:
          basic_action: "pause"
          
  - name: "kodi-show-subs"
    signals:
      - order: "show subtitle"       
    neurons:
      - kodi:
          basic_action: "showsubtitles"    
  
  - name: "kodi-seek-back-sec"
    signals:
      - order: "go {{ time }} seconds back"
    neurons:
      - kodi:
          seek_backward: "{{ time }}" 
          
  - name: "kodi-seek-for-min"
    signals:
      - order: "go forward {{ time }} minutes"
    neurons:
      - kodi:
          seek_forward: "{{ time }}"
          seek_unit: "minutes"
          
  - name: "kodi-send-text"
    signals:
      - order: "send text {{ text_to_send }}"
    neurons:
      - kodi:
          send_text: "{{ text_to_send }}"  

  - name: "kodi-to-watch"
    signals:
      - order: "show downloads"
    neurons:
      - kodi:
          show_video_path: "smb://192.168.2.1/NAS/downloads/"
        
  - name: "kodi-filme"
    signals:
      - order: "Show movies"
    neurons:
      - kodi:
          show_video_path: "videodb://movies/titles" 
          
  - name: "kodi-epg"
    signals:
      - order: "Show tv guide"
    neurons:
      - kodi:
          show_window: "tvguide"  

  - name: "kodi-youtube-iss-live"
    signals:
      - order: "show me the earth"
    neurons:
      - kodi:
          basic_action: "stop"
          play_file: "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=RtU_mdL2vBM" 
          
  - name: "kodi-start-movie"
    signals:
      - order: "start movie {{ query }}"
    neurons:
      - kodi:
          movie: "{{ query }}"
          say_template: "{{ notfound }} was not found"
          
  - name: "kodi-resume-lastwatched-tvshow"
    signals:
      - order: "resume {{ tvshow }}"
    neurons:
      - kodi:
          tvshow: "{{ tvshow }}"
          tvshow_option: "resume_last_watched_show"
          say_template: "{{ notfound }} was not found"

  - name: "kodi-resume-last-show"
    signals:
      - order: "resume my last show"
    neurons:
      - kodi:
          tvshow_option: "continue_last_show"
          say_template: "{{ notfound }} was not found"
          

  - name: "kodi-play-artist"
    signals:
      - order: "play music from {{ artist }}"
    neurons:  
      - kodi:
          artist: "{{ artist }}"
          say_template: "{{ notfound }} was not found"
          
  - name: "kodi-play-genre"
    signals:
      - order: "play something of {{ genre }} "
    neurons:  
      - kodi:
          genre: "{{ genre }}"
          say_template: "{{ notfound }} was not found"
          
  - name: "kodi-play-song-artist"
    signals:
      - order: "play from {{ artist }} the song {{ song }}"
    neurons:  
      - kodi:
          song: "{{ song }}"
          artist: "{{ artist }}"
          continue_with_artist: True
          say_template: "{{ notfound }} was not found"

  - name: "kodi-play-song"
    signals:
      - order: "play song {{ song }}"
    neurons:  
      - kodi:
          song: "{{ song }}"
          say_template: "{{ notfound }} was not found"
      
  - name: "kodi-play-radio"
    signals:
      - order: "play radio station {{ channel }}"
    neurons:
      - kodi:
          favorite: "my stations"
          search_in_favorite: "{{ channel }}"
          add_to_playlist: True  
          say_template: "{{ notfound }} was not found"
          
  - name: "kodi-pvr-now"
    signals:
      - order: "what is running on {{ channel }}"
    neurons:
      - kodi:
          what_is_running: "current_on_tvchannel"
          channel: "{{ channel }}"
          file_template: "templates/kodi.j2"
        
  - name: "kodi-whats-running"
    signals:
      - order: "whats currently running"
    neurons:
      - kodi:
          what_is_running: "current"
          file_template: "templates/kodi.j2"

  - name: "kodi-whats-the-rating"
    signals:
      - order: "whats the rating"
    neurons:
      - kodi:
          what_is_running: "imdb_rating"
          file_template: "templates/kodi.j2"
	  
  - name: "kodi-continue-on-second-kodi"
    signals:
      - order: "Continue my show in the sleeping room"
    neurons:
      - kodi:
          continue_on_second_host: 192.168.2.22
	  
  - name: "kodi-search-youtube"
    signals:
      - order: "search on youtube for {{ query }}"
    neurons:
      - kodi:
          host: 192.168.2.22
          search_youtube: "{{ query }}"
          say_template: 
            - "I'm sorry I could not find anything about {{ notfound }} on youtube"
 
 - name: "kodi-check-movie"
    signals:
      - order: "Do I have the movie {{ query }}"
    neurons:
      - kodi:
          host: 192.168.2.22
          check_movie_in_database: "{{ query }}"
          file_template: "templates/kodi.j2"
	  
  - name: "kodi-set-volume"
    signals:
      - order: "Set volume to {{ volume }}"
    neurons:
      - kodi:
          host: 192.168.2.22
          set_volume_to: "{{ volume }}"
```

## Example file template
          
```
{% if say_show_title %} 
	Currently running {{ say_show_title }}

{% elif say_episode_title %}
    with episode {{ say_episode_title }}	

{% elif say_song_title %}
    Currently running {{ say_song_title }}	

{% elif say_song_artist %}
    Artist is {{ say_song_artist }}	

{% elif say_song_album %}
    Currently running album {{ say_song_album }}	

{% elif say_movie_title %}
    Currently running movie {{ say_movie_title }}

{% elif say_no_media_infos_found %}
    I could not find any informations {{ say_no_media_infos_found }}

{% elif say_unknown_title %}
    Currently running {{ say_unknown_title }}    

{% elif notfound %}    
    {{ notfound }} was not found.

{% elif NothingToResume %}    
    Could not find anything to resume for {{ NothingToResume }}

{% elif say_current_next %}    
    Next running {{ say_current_next }}

{% elif say_pvr_title %}    
    Currently running {{ say_pvr_title }}

{% elif say_file_title %}    
    Currently running {{ say_file_title }}
    
{% elif say_pvr_title_now %}    
    Currently running on {{ say_pvr_channel }}, {{ say_pvr_title_now }}

{% elif say_pvr_title_next %}    
    Next on {{ say_pvr_channel }}, {{ say_pvr_title_next }}   

{% elif say_channel_not_found %}    
    I could not find channel {{ say_channel_not_found }} 
    
{% elif imdb_rating %} 
    The rating is {{ imdb_rating }}

{% elif no_rating %}
    There is no rating
    
{% elif movie_found %}    
    Yes you have the movie {{ movie_found }} . 

{% elif say_found_movie_labels %}    
    I found the following movies: {{ say_found_movie_labels }} 

{% elif say_no_movie_found %}    
    I could not find the movie {{ say_no_movie_found }}.   
    
{% endif %}
              
```

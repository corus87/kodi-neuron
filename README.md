# Kodi neuron
## Control Kodi with Kalliope using the json api



## Installation
```bash
kalliope install --git-url https://github.com/corus87/kodi-neuron
```
## Options

| parameter        | required | default   | choices | comments |
|------------------|----------|-----------|---------|----------|
| kodi_ip          | no       | localhost |         |          |
| kodi_port        | no       | 8080      |         |          |
| kodi_login       | no       |           |         |          |
| kodi_password    | no       |           |         |          |
| gui_window       | no       |           | home, programs, pictures, settings, music, videos, tvchannels  | Open a certain Window, check http://kodi.wiki/view/JSON-RPC_API/v6#GUI.Window for more window names.|
| show_video_path  | no       |           | nfs://192.168.178.100/NAS/to watch\, videodb://movies/titles/  |Open a certain path, check http://kodi.wiki/view/Opening_Windows_and_Dialogs for database paths.|
| show_music_path  | no       |           | musicdb://songs/, musicdb://artists/ |   |
| input_action     | no       |           | left, right, up, down, select, back, menu, pause, stop | Perform an action, check http://kodi.wiki/view/JSON-RPC_API/v6#Input.Action for actions.|
| repeat_action    | no       |           | 2, 3, 7 | Repeats an action for x-times. |
| play_file        | no       |           |         | play a file, stream or favorite, check notes below to get the path of a favorite |
| open_addon       | no       |           |         | open a certain addon, ckeck notes below to get the addonid |
| scan_video_lib   | no       | false     |         | Scan the video library |
| scan_music_lib   | no       | false     |         | Scan the music library (perform the command a second time to cancel the scan) |
| skip_video       | no       |           | smallbackward, bigbackward, smallforward, bigforward |Default for a small step = 30 seconds, for big step = 10 minutes. |
| set_volume       | no       |           | integer |           |
| set_mute         | no       | false     |         |           |
| show_osd         | no       | false     |         |           |
| show_context     | no       | false     |         |           |
| search_movie     | no       |           |         |           |
| reask            | no       | false     |         |If true, Kalliope will ask you again if the movie was not found or there are multiple movies with similar name. |
| abort_orders     | yes      |           | list or string      | Is required if reask is True. |
| start_tvshow     | no       |           |         |           |
| season           | yes      |           | Integer | Is required if start_tvshow. |
| episode          | yes      |           | Integer | Is required if start_tvshow. |
| resume_tvshow    | no       |           |         | Resume a TV-Show.                      |
| open_season_dir  | no       | false     |         | If true and start_tvshow or resume_tvshow is used, it will open the current season folder of the TV-Show. | 
| what_is_running  | no       |           |         | You need a file template to use it. |


## Synapses example

```yml
  - name: "kodi-play-pause"
    signals:
      - order: "pause Kodi"    
      - order: "continue Kodi"      
    neurons:
      - kodi:
          input_action: "pause"
  
  - name: "kodi-stop"
    signals:
      - order: "stop Kodi"      
    neurons:
      - kodi:
          input_action: "stop" 

  - name: "kodi-movies"
    signals:
      - order: "open up movies"
    neurons:
      - kodi:
          show_video_path: videodb://movies/titles/ 

  - name: "kodi-music"
    signals:
      - order: "open up music"
    neurons:
      - kodi:
          show_video_path: musicdb://artists/ 
          
   - name: "kodi-home"
    signals:
      - order: "open up home"
    neurons:
      - kodi:
          gui_window: "home" 

    - name: "kodi-go-down"
    signals:
      - order: "go {{ query }} down"
    neurons:
      - kodi:
          input_action: "down"
          repeat_action: "{{query}}"

  - name: "kodi-select"
    signals:
      - order: "select"
    neurons:
      - kodi:
          input_action: "select"       

  - name: "kodi-radio"
    signals:
      - order: "start deepfm"
    neurons:
      - kodi:
          play_file: "plugin://plugin.audio.tuneinradio/?logo=http%3A%2F%2Fcdn-radiotime-logos.tunein.com%2Fs54426q.png&id=s54426&name=DeepFM+%28Niederlande%29&path=tune"       
  - name: "kodi-start-movie-without-reask"
    signals:
      - order: "start movie {{ query }}"
    neurons:
      - kodi:
          search_movie: "{{ query }}"
          say_template: "{{ movie_not_found }} was not found"     
   
  - name: "kodi-start-movie"
    signals:
      - order: "start movie {{ query }}"
    neurons:
      - kodi:
          search_movie: "{{ query }}"
          abort_orders:
            - "abort"
            - "stop asking"
          reask: True
          file_template: "templates/kodi.j2"        
  
  - name: "kodi-start-show"
    signals:
      - order: "start tvshow {{ start_tvshow }} season {{ season }} episode {{ episode }}"
    neurons:
      - kodi:
          start_tvshow: "{{ start_tvshow }}"
          season: "{{ season }}"
          episode: "{{ episode }}"
          open_season_dir: True        
  
  - name: "kodi-resume-tvshow"
    signals:
      - order: "continue tvshow {{ query }}"
    neurons:
      - kodi:
          resume_tvshow: "{{ query }}"
          open_season_dir: True

          
  - name: "kodi-whats-running"
    signals:
      - order: "what is currently running"
    neurons:
      - kodi:
          what_is_running: True
          file_template: "templates/kodi.j2" 
          
file_template:
    {% if say_labels%} 
        The following movies were found {{ say_labels}}, please define more precisely.
    
    {% elif movie_not_found %} 
        {{ movie_not_found }} were not found in database, please try again.
    
    {% elif movie_found %} 
        Yes, {{ movie_found }} was found.   

    {% elif say_found_movie_labels %} 
        The following movies were found: {{ say_found_movie_labels }}.      

    {% elif say_no_movie_found %} 
        {{ say_no_movie_found }} was not found.     

    {% elif say_show_title %} 
        The show title is: {{ say_show_title }}

    {% elif say_episode_title %}
        The episode title is: {{ say_episode_title }}	

    {% elif say_song_title %}
        Its running: {{ say_song_title }}	

    {% elif say_song_artist %}
        Artist is: {{ say_song_artist }}	

    {% elif say_song_album %}
        Album: {{ say_song_album }} is running

    {% elif say_movie_title %}
        You are watching: {{ say_movie_title }}

    {% elif say_no_media_infos_found %}
        No information were found {{ say_no_media_infos_found }}

    {% endif %}      
```

## Notes
To get a list with your addons and id use the json api:
- http://192.168.178.101:8080/jsonrpc?request={ "jsonrpc": "2.0", "method": "Addons.GetAddons","params":{}, "id": "1"}

To get a list with your favorites and path use:
- http://192.168.178.101:8080/jsonrpc?request={ "jsonrpc": "2.0", "method": "Favourites.GetFavourites", "params": { "properties": ["window","path"] }, "id": 1 }

If you have set reask to false, you need to be precisely with your movie name otherwise Kalliope will start the first movie what matches the name in the database.

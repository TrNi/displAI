import requests
import os
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import vlc
import time
import webbrowser
def action(actype, acargs):
    if actype=="weather":
        owm_api_key = os.getenv("OWM_API_KEY")
        baseurl = "https://api.openweathermap.org/data/2.5/forecast?"
        if not "city" in list(acargs.keys()):
            print(f"Call to weather API without a city name given. Args: {acargs}")
            return None
        city = acargs["city"]
        fullurl = f"{baseurl}q={city}&appid={owm_api_key}&units=imperial"
        apires = requests.get(fullurl)
        wthr = apires.json()
        with open("dump.json","w+") as f:
            f.write(json.dumps(wthr, indent=4))
        if wthr['cod']=='404':
            print(f"This city {city} is not found in weather API.")
            return None
        wthr = wthr['list'][2]
        weather = wthr['weather'][0]['description']
        temp = f"{wthr['main']['temp']:0.1f}"
        feels_like =  f"{wthr['main']['feels_like']:0.1f}"
        humidity = f"{wthr['main']['humidity']:0.0f} %"
        wind_speed = f"{wthr['wind']['speed']:0.0f}"
        op = ["weather in next 3 hours:",weather, "temperature", temp, "feels like:", feels_like, "humidity", humidity, "wind speed", wind_speed]

        if 'rain' in wthr:
            rain = f"{wthr['rain']['3h']:0.1f}"
            op.append("rain for next 3 hrs (mm)");  op.append(rain)
        return(op)

    elif actype=="news":
        params = {'country': acargs["country"] if "country" in acargs else "us",
                  'apiKey': os.getenv("NEWS_API_KEY"),
                  'pageSize': 10 #number of headlines
                  }
        baseurl = 'https://newsapi.org/v2/top-headlines?'

        apires= requests.get(baseurl, params=params)
        news = apires.json()
        if news['status'] != 'ok':
            print(f"Error retrieving news: {news['message']}")
            return None

        headlines = [article['title'] for article in news['articles']]
        dscr = [article['description'] for article in news['articles']]
        urls = [article['url'] for article in news['articles']]

        for i in range(len(headlines)):
            print(headlines[i])
            print(dscr[i])
            print(urls[i])
        return [headlines,dscr,urls]

    elif actype=="music":
        redirect_uri = "https://google.com/"
        scope = "streaming" #"user-library-read"
        oauth_object = spotipy.SpotifyOAuth(client_id=os.getenv("SPOT_CLIENT_ID"), client_secret=os.getenv("SPOT_CLIENT_SECRET"),redirect_uri= redirect_uri, scope=scope )
        token_dict = oauth_object.get_access_token()
        token = token_dict['access_token']
        #spotifyObject = spotipy.Spotify(auth=token)
        sp = spotipy.Spotify(auth=token)
        user_name = sp.current_user()
        print(json.dumps(user_name, sort_keys=True, indent=4))


        #spot_cred_manager = SpotifyClientCredentials()
        #sp = spotipy.Spotify(client_credentials_manager=spot_cred_manager)
        results = sp.search(q=f"track:{acargs['track']}", type='track', limit=10)
        track_uri = results['tracks']['items'][0]['uri']
        track_info = sp.track(track_uri)
        print(list(track_info.keys()))
        stream_url = track_info['preview_url']#list(track_info['external_urls'].values())[0]#track_info['preview_url']#list(track_info['external_urls'].values())[0]
        print(stream_url)#['preview_url']
        print(list(track_info['external_urls'].values()))
        Instance = vlc.Instance('--no-xlib')
        player = Instance.media_player_new()
        Media = Instance.media_new(stream_url)#stream_url)
        #Media.get_mrl()
        player.set_media(Media)
        player.play()
        player.audio_set_volume(100)
        time.sleep(3)
        duration = player.get_length() / 1000
        print(duration)
        time.sleep(duration)

        while True:
            state = player.get_state()
            if state == vlc.State.Ended:
                player.release()
                Media.release()
                break
    else:
        print(f"This action {actype} is not supported yet.")
        return None



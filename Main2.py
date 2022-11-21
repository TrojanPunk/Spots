import sys
import spotipy
import threading
import pyttsx3 as tts
from speech_recognition import Microphone, Recognizer, UnknownValueError
from spotipy.oauth2 import SpotifyOAuth

import Spots as sf

# Set variables from setup.txt
clientID = 'Your Spotify Client ID'
clientSecret = 'Your Spotify Client Secret ID'
deviceName = 'The device you want to play on'
redirectUri = 'http://example.com'
scope = 'playlist-read-private user-modify-playback-state user-read-currently-playing user-read-playback-state'
username = 'Your Spotify Username'

# Connecting to the Spotify account
auth_manager = SpotifyOAuth(
    client_id = clientID,
    client_secret=clientSecret,
    redirect_uri=redirectUri,
    scope=scope,
    username=username)
spotify = spotipy.Spotify(auth_manager=auth_manager)

# Selecting device to play from
devices = spotify.devices()
deviceID = None
for d in devices['devices']:
    d['name'] = d['name'].replace('’', '\'')
    if d['name'] == deviceName:
        deviceID = d['id']
        break

# Setup microphone and speech recognizer
class Assistant:
    def speak(self, toSpeak):
        self.speaker.say = toSpeak
        self.speaker.runAndWait()

    def __init__(self):
        self.r = Recognizer()
        self.speaker = tts.init()
        voices = self.speaker.getProperty('voices')
        self.speaker.setProperty('voice', voices[1].id)
        self.speaker.setProperty('rate', 150)
        print("hello")

        threading.Thread(target = self.runAssistant).start()

    def runAssistant(self):
        while True:
            print("entered")
            try:
                with Microphone() as source:
                    self.r.adjust_for_ambient_noise(source=source, duration=0.2)
                    audio = self.r.listen(source=source)

                    text = self.r.recognize_google(audio_data=audio).lower()

                    if "hello" in text:
                        print("listening")
                        audio = self.r.listen(source)
                        text = self.r.recognize_google(audio_data=audio).lower()
                        name = text.split()
                        if text == "stop":
                            self.speak("bye")
                            sys.exit(0)

                        elif "play" in text:
                            self.speak("playing" + " ".join(name[1 : ]))
                            print("Playing", " ".join(name[1 : ]))
                            uri = sf.get_track_uri(spotify, " ".join(name[1 : ]))
                            sf.play_track(spotify, deviceID, uri)

                        elif "play" and "album" in text:
                            self.speak("playing the album" + " ".join(name[2 : ]))
                            print("Playing the album", " ".join(name[2 : ]))
                            uri = sf.get_track_uri(spotify, " ".join(name[2 : ]))
                            sf.play_track(spotify, deviceID, uri)

                        elif "play" and "artist" in text:
                            self.speak("playing songs by" + " ".join(name[2 : ]))
                            print("Playing songs by", text[2 : ])
                            uri = sf.get_track_uri(spotify, " ".join(name[2 : ]))
                            sf.play_track(spotify, deviceID, uri)

                        else:
                            self.speak("sorry, i did not understand that one.")
            except sf.InvalidSearchError:
                self.speak("try again.")
                print('InvalidSearchError. Try Again')

if __name__ == '__main__':
    obj = Assistant()

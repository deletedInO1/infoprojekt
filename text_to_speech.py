# Import the required module for text
# to speech conversion
from gtts import gTTS
import vlc

language = 'en'

def speech(text):
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save("audio.mp3")
    player = vlc.MediaPlayer("./audio.mp3")
    player.play()
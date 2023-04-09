import speech_recognition as sr
import gtts
from playsound import playsound
import os

# Define the keywords to detect
keywords = ["hello", "world", "python"]
sphinx_kw = [('hello',1), ('world',1), ('python',1)]
# Initialize the speech recognizer
r = sr.Recognizer()

# Use the default microphone as the audio source
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source, phrase_time_limit=5)

try:
    # Use the Google Web Speech API to transcribe the audio
    text = r.recognize_whisper(audio,model='tiny.en')

    # Check if any of the keywords are in the transcribed text
    for keyword in keywords:
        if keyword in text:
            print("Keyword detected:", keyword)
            break
    else:
        print()
        print(f"No keywords detected, you said {text} .")

    tts = gtts.gTTS(text)
    pathpath = os.path.join(os.path.dirname(__file__), "yourtext.mp3")
    tts.save(pathpath)
    playsound(pathpath)

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

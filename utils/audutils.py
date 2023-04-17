import speech_recognition as srlib
import gtts
from pydub import AudioSegment
from pydub.playback import play
import os

sr = srlib.Recognizer()
def parser_wo_detect(raud):
    try:
        rtxt = sr.recognize_whisper(raud, model='tiny.en')
    except srlib.UnknownValueError:
        print("Could not understand audio, please say again.")

    except srlib.RequestError as e:
        print("Could not request audio transcription ")
    return rtxt

def parser_w_detect(raud, keywords):
    try:
        rtxt = sr.recognize_whisper(raud, model='tiny.en')
        kw_det = False
        for kw in keywords:
            if kw.casefold() in rtxt.casefold():
                kw_det = True  # keyword detected.
                rcmd = rtxt.casefold().strip(kw.casefold())  # received command
                print(f"Keyword detected:{kw}, processing:{rcmd}")
                break
        if kw_det:
            return kw_det,rtxt,rcmd
        else:
            return False,rtxt,None

    except srlib.UnknownValueError:
        print("Could not understand audio, please say again.")

    except srlib.RequestError as e:
        print("Could not request audio transcription ")


def playaud(txt, path=''):
    aud = gtts.gTTS(txt)
    audpath = os.path.join(os.path.dirname(__file__), 'tempaud.mp3' if path == '' else path)
    aud.save(audpath)
    play(AudioSegment.from_file(audpath, format="mp3"))
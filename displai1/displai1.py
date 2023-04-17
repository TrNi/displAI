import speech_recognition as srlib
import os
import OAIWrapper
from openai import Image as im
import cv2
import gtts
from pydub import AudioSegment
from pydub.playback import play
from utils.imgutils import strtoimg

ow = OAIWrapper.OAIWrapper()
sr = srlib.Recognizer()
mic = srlib.Microphone()
with mic as src:
    sr.adjust_for_ambient_noise(src)


keywords = ["Hey","Hello","Hi"]

while True:
    with srlib.Microphone() as source: #default microphone
        print("Say something!")
        raud = sr.listen(source, phrase_time_limit=8) # received audio

    try:
        rtxt = sr.recognize_whisper(raud, model='tiny.en') #Whisper API for audio transcription.
        kw_det = False
        for kw in keywords:
            if kw.casefold() in rtxt.casefold():
                kw_det = True #keyword detected.
                rcmd = rtxt.casefold().strip(kw.casefold()) #received command
                print(f"Keyword detected:{kw}, processing:{rcmd}")
                break
        if kw_det:
            #image prompt using chatgpt:
            gptprm = f"A person is suggesting or requesting a creative image. Understand the gist of the next sentence"+\
            f"and give a realistic, one-line visual description of the scene fitting for it in less than twenty words. {rcmd}"

            imgprm = f"A photo of {ow.chat_completion(gptprm)}"
            imgprmplus = f"Image prompt: "+imgprm
            imgprmplus = imgprmplus.replace('"','').replace("'",'')
            print(imgprmplus)
            imgprmaud = gtts.gTTS(imgprmplus)
            audpath = os.path.join(os.path.relpath("imgprompt.mp3"))
            imgprmaud.save(audpath);play(AudioSegment.from_file(audpath, format="mp3"))
            vres = im.create(prompt=imgprm, n=2, size="512x512", response_format="b64_json")

            for id, imdict in enumerate(vres["data"]):
                imdata= strtoimg(imdict["b64_json"])
                cv2.imshow(f'im{id}', imdata)
                cv2.moveWindow(f'im{id}',id*512+5, id*0*128+1)
                cv2.setWindowProperty(f'im{id}', cv2.WND_PROP_TOPMOST, 1)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    except srlib.UnknownValueError:
        print("Could not understand audio, please say again.")

    except srlib.RequestError as e:
        print("Could not request audio transcription ")

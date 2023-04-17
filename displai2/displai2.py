"""
This file is Displai V2: do multi-threading and parallel processing.
Listen, detect keyword, get intelligent prompt, show two images.
"""
import speech_recognition as srlib
import os
from utils import OAIWrapper
from openai import Image as im
import cv2
import gtts
from pydub import AudioSegment
from pydub.playback import play
from utils.imgutils import strtoimg
from multiprocessing import Process, cpu_count, Queue as Q

from utils.audutils import *
import re
ow = OAIWrapper.OAIWrapper()
sr = srlib.Recognizer()
mic = srlib.Microphone()
with mic as src:
    sr.adjust_for_ambient_noise(src)

cnt = cpu_count()
print(f"Parallel processing on up to {cnt} CPU cores.")
keywords = ["Hey","Hello","Hi"]
cnvr = None
nametry=0
botname = "Jolly"
usrname = None
linecnt = 0
def converse(q):
    cnvr, nametry, botname, usrname = q.get()

    while True:
        if cnvr is None and nametry==0:
            gptprm = f"You are conversing with a user and your name is {botname}. Introduce yourself as an intelligent chat bot and request the user to provide their name."
            gptres = ow.chat_completion(gptprm)
            nametry +=1
        elif nametry==1:
            gptprm = f"You are conversing with a user, your name is {botname}. Understand the past conversation given here and provide a one-word answer to the next question.Past conversation: {cnvr}. Question: spell the user's name if they provided, otherwise, answer 'no'."
            gptres = ow.chat_completion(gptprm)
            if any(item in gptres for item in ["no","nope","0"]):
                nametry+=1
            else:
                nametry=-1
                usrname = str(gptres) #just to create a copy.
        elif nametry>=1:
            gptres =  'hi, I will call you John, hope that is okay.'
            usrname='John'
            nametry=-1
        else:
            gptprm=f"You are an intelligent chatbot named {botname}, conversing with a user named {usrname}. Understand the past conversation and generate your next one-line response in less than 20 words. Past conversation: {cnvr}"
            gptres = ow.chat_completion(gptprm)
        gptres = gptres.strip("Jolly:").strip("Jolly").strip("jolly")
        playaud(gptres)
        cnvr = "" if cnvr is None else cnvr
        cnvr = cnvr + f'\n Jolly: {gptres}'

        with srlib.Microphone() as source:  # default microphone
            raud = sr.listen(source, phrase_time_limit=8)  # received audio

        txt = parser_wo_detect(raud)
        cnvr = cnvr + f'\n {"" if usrname is None else usrname}: {txt}'
        q.put((cnvr, nametry, botname, usrname))
        #cnvr, nametry, botname, usrname, linecnt = q.get()


def disp_occ(q): #display occasionally, based on conversation.
    cnvr, nametry, botname, usrname = q.get()
    lastcnt = 0 if cnvr is None else cnvr.count('\n')
    while True:
        cnvr, nametry, botname, usrname= q.get()
        if cnvr is not None:
            linecnt = cnvr.count('\n')
            if linecnt>lastcnt+8:
                lastcnt = linecnt
                ls = list(m.start() for m in re.finditer('\n', cnvr))
                startid = ls[-5]+1
                gptprm = f"Two humans named {botname} and {usrname} are conversing. Understand the gist of this conversation " + \
                         f"and give a realistic, one-line visual description of the scene fitting for the topic of conversation in less than twenty words. Conversation: {cnvr[startid:]}"

                imgprm = f"A photo of {ow.chat_completion(gptprm)}"
                imgprmplus = f"Image prompt: " + imgprm
                imgprmplus = imgprmplus.replace('"', '').replace("'", '')
                print(imgprmplus)
                #playaud(imgprm,"imgprompt.mp3")
                vres = im.create(prompt=imgprm, n=2, size="512x512", response_format="b64_json")

                for id, imdict in enumerate(vres["data"]):
                    imdata = strtoimg(imdict["b64_json"])
                    cv2.imshow(f'im{id}', imdata)
                    cv2.moveWindow(f'im{id}', id * 512 + 5, id * 0 * 128 + 1)
                    cv2.setWindowProperty(f'im{id}', cv2.WND_PROP_TOPMOST, 1)
                cv2.waitKey(0)
                cv2.destroyAllWindows()



if __name__=='__main__':
    q = Q()
    q.put((cnvr,nametry,botname,usrname))
    pr1 = Process(target=converse, args=(q,))
    pr2 = Process(target=disp_occ, args=(q,))
    pr1.start()
    pr2.start()
    pr1.join()
    pr2.join()
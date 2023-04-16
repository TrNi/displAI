import speech_recognition as sr
import gtts
from playsound import playsound
import os
import OAIWrapper

ow = OAIWrapper.OAIWrapper()
kw_ph = ["Hey Bob", "Hello Bob", "H"]

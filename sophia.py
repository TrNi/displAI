from gifviewer import GifViewer
from chatbot import ChatBot

import speech_recognition as sr
import gtts
from playsound import playsound

def log(msg):
    print(msg)

def say(msg):
    tts = gtts.gTTS(msg, lang="en")
    tts.save("hello.mp3")
    playsound("hello.mp3")

def main():
    gif_window = GifViewer()
    sophia_bot = ChatBot("sophia")

    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)
    #r.pause_threshold = 0.7
    #r.operation_timeout = 0.5
    r.dynamic_energy_threshold = True

    while True:
        try:
            if sophia_bot.is_awake():
                gif_window.change_state("awake")
            else:
                gif_window.change_state("sleep")

            log("Listening...")
            with mic as source:
                audio = r.listen(source, timeout=10)

            gif_window.change_state("thinking")

            log("Starting trancription")
            user_text = r.recognize_whisper(audio, model = "tiny.en")
            log(f"Recognized: {user_text}")

            if (user_text and
                (("sophia" in user_text.lower() or
                  "sofia" in user_text.lower()) and
                  user_text.strip(" ") != "you" and
                  user_text != "Thanks for watching!") or sophia_bot.is_awake()):

                    sophia_bot.add_user_msg("vanderson", user_text)

                    chatgpt_text = sophia_bot.get_and_save_bot_next_msg()

                    gif_window.change_state("saying")
                    log(f"Saying: {chatgpt_text}")
                    say(chatgpt_text)

        except Exception as e:
            print(f"Failed: {e}")

if __name__ == "__main__":
    main()

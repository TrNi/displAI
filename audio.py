import audioop
import pyaudio
import speech_recognition as sr
import gtts
from playsound import playsound
import OAIWrapper

oai = OAIWrapper.OAIWrapper()

def callback(recognizer, audio):
    try:
        print("Starting transcription...")
        text = recognizer.recognize_whisper(audio, model = "small.en")
        print(f"Recognized: {text}")

        chatgpt_result = oai.chat_completion("Pretend being a very cool dude, use a lot of slangs and short anwsers for this in portuguese: " + text)

        if text:
            tts = gtts.gTTS(chatgpt_result)
            tts.save("hello.mp3")
            playsound("hello.mp3")

    except sr.UnknownValueError:
        print("Speach Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

def main():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)

    while True:
        print("Listening...")
        with mic as source:
            audio = r.listen(source, phrase_time_limit=5)
        callback(r, audio)

if __name__ == "__main__":
    main()

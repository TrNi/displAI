import speech_recognition as sr
import gtts
from playsound import playsound
from utils import OAIWrapper
import openai
from threading import Thread
import time
import tkinter as tk
from PIL import Image, ImageTk
import threading

class GifViewer(threading.Thread):
    def __init__(self, gif_files):
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        self.tk = tk.Tk()

        self.gif_files = gif_files
        self.current_gif = 0

        width = self.tk.winfo_screenwidth()
        height= self.tk.winfo_screenheight()
        self.tk.title("GIF Viewer")
        self.tk.geometry("%dx%d" % (width, height))
        self.tk.attributes('-fullscreen', True)
        self.tk.configure(background='black')

        self.tk.label = tk.Label(self.tk)
        self.tk.label.pack(padx=10, pady=10)

        self.load_gif()
        self.tk.mainloop()

    def load_gif(self):
        self.gif = Image.open(self.gif_files[self.current_gif])
        self.show()

    def show(self):
        try:
            frame = ImageTk.PhotoImage(self.gif)
            self.tk.label.config(image=frame, borderwidth=0)
            self.tk.label.image = frame
            self.gif.seek(self.gif.tell() + 1)
        except EOFError:
            self.gif.seek(0)
        except Exception:
            return

        self.tk.after(100, self.show)

    def show_gif(self, position):
        self.current_gif = position % len(self.gif_files)
        self.load_gif()

    def next_gif(self):
        self.current_gif = (self.current_gif + 1) % len(self.gif_files)
        self.load_gif()

    def prev_gif(self):
        self.current_gif = (self.current_gif - 1) % len(self.gif_files)
        self.load_gif()

gif_files = ["gifs/listening.gif", "gifs/transcripting.gif", "gifs/thinking.gif", "gifs/speaking.gif", "gifs/starting.gif"]

oai = OAIWrapper.OAIWrapper()

user_name = "vanderson"

history_embeddings = []
history = []
conversation = []

def get_embedding(msg):
    resp = openai.Embedding.create(
        input=msg,
        engine="text-similarity-davinci-001")

def similarity(emb1, emb2):
    return np.dot(emb1, emb2)

def process():
    global conversation
    while True:
        time.sleep(1)
        for i in range(len(conversation)):
            if i > 5:
                print("Starting processing conversation:")
                old_conversation = conversation[i:len(conversation)]
                history += old_conversation
                history_embeddings += [get_embedding(msg) for msg in old_conversation]
                conversation = conversation[0:i]
                break

def get_context(msg):
    similarities = []
    msg_emb = get_embedding(msg)
    for emb, msg in zip(history_embeddings, history):
        similarities += [(similarity(emb, msg), msg)]
    similarities.sort()
    context = []
    for sim, msg in reversed(similarities):
        context += [msg]
        if len(context) > 3:
            break
    return context

def callback(recognizer, audio):
    global conversation, user_name, oai
    try:
        print("History: ")
        print(history)
        print("Current: ")
        print(conversation)
        print("Starting transcription...")
        app.show_gif(4)
        user_text = recognizer.recognize_whisper(audio, model = "small.en")
        print(f"Recognized: {user_text}")

        if user_text and ("sophia" in user_text.lower() or "sofia" in user_text.lower()):
            app.show_gif(2)
            user_text = user_text.strip()
            conversation += [user_name + ": " + user_text.strip("hey sophia")]
            context = get_context(user_text.strip("hey sophia"))
            print("Context: ")
            print(context)

            prompt = "Pretend being a very smart girl, be very friendly and give short anwsers to generate the next line from Sophia to " + user_name + " for this conversation: \n" + '\n'.join(context) + '\n'.join(conversation)
            print(prompt)
            chatgpt_text = oai.chat_completion(prompt = prompt)
            chatgpt_text = chatgpt_text.strip("sophia:").strip("Sophia:")

            conversation += ["sophia: " + chatgpt_text]

            app.show_gif(3)
            tts = gtts.gTTS(chatgpt_text)
            tts.save("hello.mp3")
            playsound("hello.mp3")

    except sr.UnknownValueError:
        print("Speach Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

app = GifViewer(gif_files)

def main():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)

    processThread = Thread(target=process)
    processThread.start()

    while True:
        app.show_gif(0)
        print("Listening...")
        with mic as source:
            audio = r.listen(source, timeout=5)
        print("Listened")
        callback(r, audio)

if __name__ == "__main__":
    main()

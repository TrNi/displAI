import tkinter as tk
from multiprocessing import Process, Value
import threading
from enum import Enum
from PIL import Image, ImageTk

class GifViewer(threading.Thread):
    gif_files = ["gifs/listening.gif", "gifs/transcripting.gif", "gifs/thinking.gif", "gifs/speaking.gif", "gifs/starting.gif"]

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        self.tk = tk.Tk()

        self.current_gif = 0

        width = self.tk.winfo_screenwidth()
        height= self.tk.winfo_screenheight()
        self.tk.title("GIF Viewer")
        self.tk.geometry("%dx%d" % (width, height))
        self.tk.attributes('-fullscreen', True)
        self.tk.configure(background='black')

        self.tk.label = tk.Label(self.tk)
        self.tk.label.pack(padx=400, pady=400)

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

    def change_state(self, state):
        if   state == "sleep":
            self.show_gif(2)
        elif state == "awake":
            self.show_gif(0)
        elif state == "thinking":
            self.show_gif(4)
        elif state == "saying":
            self.show_gif(3)

    def show_gif(self, position):
        self.current_gif = position % len(self.gif_files)
        self.load_gif()

    def next_gif(self):
        self.current_gif = (self.current_gif + 1) % len(self.gif_files)
        self.load_gif()

    def prev_gif(self):
        self.current_gif = (self.current_gif - 1) % len(self.gif_files)
        self.load_gif()



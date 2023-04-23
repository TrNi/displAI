from gifviewer import GifViewer
from chatbot import ChatBot
from utils.audutils import AudioHelper

def log(msg):
    print(msg)

def main():
    audio_interface = AudioHelper()
    sophia_bot = ChatBot("sophia")
    karen_bot = ChatBot("karen")

    sophia_bot.add_user_msg("karen", "Hello Sophia! Can you interview me?")

    while True:
        try:
            sophia_text = sophia_bot.get_and_save_bot_next_msg()
            audio_interface.say(sophia_text)
            karen_bot.add_user_msg("sophia", sophia_text)
            karen_text = karen_bot.get_and_save_bot_next_msg()
            audio_interface.say(karen_text)
            sophia_bot.add_user_msg("karen", karen_text)

        except Exception as e:
            log(f"Failed: {e}")

if __name__ == "__main__":
    main()

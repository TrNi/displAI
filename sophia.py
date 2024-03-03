from lib.viewer import Viewer
from lib.chatbot import ChatBot
from lib.audutils import AudioHelper
import threading
import cv2

def log(msg):
    print(msg)


def is_valid_msg(msg):
    return msg and msg.strip() != "you" and msg != "Thanks for watching!"


def has_keyword_sophia(msg):
    return "sophia" in msg.lower() or "sofia" in msg.lower()


def update_image(sophia_bot, gif_window):
    image = sophia_bot.gen_image_from_conversation()
    cv2.imwrite("image.png", image)
    gif_window.show_image("image.png")


def main():
    gif_window = Viewer()
    audio_interface = AudioHelper()
    sophia_bot = ChatBot("sophia")
    gif_window.change_state("thinking")
    i = 0
    while True:
        try:

            # if sophia_bot.is_awake():
            #     gif_window.change_state("awake")
            # else:
            #     gif_window.change_state("sleep")

            log("Listening...")
            audio = audio_interface.listen()

            # gif_window.change_state("thinking")

            log("Starting trancription")

            user_text = audio_interface.transcript(audio)

            log(f"Recognized: {user_text}")

            if is_valid_msg(user_text):
                if has_keyword_sophia(user_text) or sophia_bot.is_awake():

                    sophia_bot.add_user_msg("user", user_text)

                    chatgpt_text = sophia_bot.get_and_save_bot_next_msg()

                    #if i % 2 == 0:
                    #log("Generating new image")
                    threading.Thread(
                       target=update_image, args=(
                       sophia_bot, gif_window,)).start()

                    # gif_window.change_state("saying")
                    log(f"Saying: {chatgpt_text}")

                    audio_interface.say(chatgpt_text)
            i += 1

        except Exception as e:
            log(f"Failed: {e}")


if __name__ == "__main__":
    main()

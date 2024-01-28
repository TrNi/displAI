from lib.imgutils import strtoimg
from lib.OAIWrapper import OAIWrapper
import openai
import time
from openai import Image as im
import numpy as np


class ConversationDB:
    history_embeddings = []
    history = []

    def _get_embedding(self, msg):
        resp = openai.Embedding.create(
            input=msg,
            engine="text-embedding-ada-002")#"text-similarity-davinci-001")
        return resp['data'][0]['embedding']

    def _similarity(self, emb1, emb2):
        return np.dot(emb1, emb2)

    def add_to_history(self, conversation):
        self.history += conversation
        self.history_embeddings += [self._get_embedding(msg)
                                    for msg in conversation]

    def get_similar_msgs(self, msg, number_of_msgs):
        similarities = []
        msg_emb = self._get_embedding(msg.split(":")[1:])
        for emb, msg in zip(self.history_embeddings, self.history):
            similarities += [(self._similarity(emb, msg_emb), msg)]
        similarities.sort()
        context = []
        for sim, msg in reversed(similarities):
            context += [msg]
            if len(context) > number_of_msgs:
                break
        return context


class ChatBot:
    def __init__(self, bot_name, history_file=None):
        self.oai = OAIWrapper()
        self.bot_name = bot_name
        self.historyDB = ConversationDB()
        self.conversation = []
        self.bot_last_awake = 0

    # display occasionally, based on conversation.
    def gen_image_from_conversation(self):
        if len(self.conversation) > 0:
            cnvr = '\n'.join(self.conversation)
            gptprm = f"Understand the gist of this conversation " + \
                     f"and give a realistic, one-line visual description of the scene fitting for the topic of conversation in less than twenty words. The description should be about the topic of conversation and should not include people. Conversation: {cnvr}"
            imgprm = f"A photo of {self.oai.chat_completion(gptprm)}"
            imgprmplus = f"Image prompt: " + imgprm
            imgprmplus = imgprmplus.replace('"', '').replace("'", '')
            vres = im.create(
                prompt=imgprm,
                n=1,
                size="256x256",
                response_format="b64_json")
            return strtoimg(vres["data"][0]["b64_json"])

    def _awake(self):
        self.bot_last_awake = time.time()

    def is_awake(self):
        current_time = time.time()
        if current_time - self.bot_last_awake < 60:
            return True
        return False

    def _update_history(self):
        if len(self.conversation) > 10:
            self.conversation_to_save = self.conversation[:10]
            self.conversation = self.conversation[10:]
            self.historyDB.add_to_history(self.conversation_to_save)

    def add_user_msg(self, user_name, user_text):
        if user_text:
            user_text = user_text.strip()
            self.conversation += [user_name + ": " +
                                  user_text.strip(self.bot_name + ':')]
            self._awake()

    def get_and_save_bot_next_msg(self, context_window=10):
        context = self.historyDB.get_similar_msgs(
            self.conversation[-1], context_window)
        full_conversation = '\n'.join(context) + '\n'.join(self.conversation)
        prompt = f"""You are {self.bot_name}, a bot chat that speaks English. Create the next line/awnser that follows for this conversation: {full_conversation}"""
        chatgpt_text = self.oai.chat_completion(
            prompt=prompt).lower().strip(
            self.bot_name + ":").split('\n')[0]
        self.conversation += [self.bot_name + ": " + chatgpt_text]
        self._awake()
        self._update_history()
        return chatgpt_text

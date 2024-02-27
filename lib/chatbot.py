from lib.imgutils import strtoimg
from lib.OAIWrapper import OAIWrapper
import openai
import time
from openai import Image as im
import numpy as np
from actions.action import action

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
                     f"and give an artistic, real-life, one-line visual description of a fitting scene for the topic of conversation in less than twenty words. The description should capture the gist of the conversation and should not include people identities or letters. Here is the conversation: {cnvr}"
            imgprm = f"An image for this scene: {self.oai.chat_completion(gptprm)}"
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
            #print(f"user text: {user_text}")
            self.conversation += [user_name + ": " +
                                  user_text.replace(self.bot_name + ":", "")]
            print(f"conversation:{self.conversation}")
            self._awake()

    def get_and_save_bot_next_msg(self, context_window=10):
        context = self.historyDB.get_similar_msgs(self.conversation[-1], context_window)
        full_conversation = '\n'.join(context) + '\n'.join(self.conversation)
        action_conv='\n'.join(self.conversation[-3:])#last three lines of bidir. conv.
        print(f"Full conversation:{full_conversation}")
        prompt = f"You are a chatbot named {self.bot_name} conversing with a user and here is the latest conversation: {action_conv}. " \
                 f"Understand the conversation and generate one single-digit response from {0,1,2,3}." \
                 f"If user asked for weather, return 1. Elseif user asked for music, return 2. " \
                 f"Elseif user asked for news, return 3. Else return 0.Your response can only contain a single digit character, either 0 or 1 or 2 or 3. " \
                 f"You must not respond with any extra characters for the system to function without breaking."

        gptresp1 = self.oai.chat_completion(prompt=prompt).lower().replace(self.bot_name + ":", "").split('\n')[0]
        print(f"First response: {gptresp1}")
        actid=0
        actdict= {'1':'weather', '2': 'music', '3':'news'}
        if '1' in gptresp1:
            actid=1
            prompt2 = f"You are a chatbot named {self.bot_name} conversing with a user and here is the conversation: {action_conv}. "\
            "Choose and respond with only one response based on the following If-Else algorithm." \
            f"If the user did not provide city name for weather information, ask for it."\
            f"Else your response can only contain one Python3 list with this format:"\
            f"[weather, <insert the city name here without comma>]" \
            f"You must not respond with any extra characters for the system to function without breaking."
            
        elif '2' in gptresp1:
            actid = 2
            prompt2 = f"You are a chatbot named {self.bot_name} conversing with a user and here is the conversation: {action_conv}. " \
                      "Choose and respond with only one response based on the following If-Else algorithm." \
                      f"If the user did not provide some search terms for music to play, ask for it." \
                      f"Else your response can only contain one Python3 list with this format:" \
                      f"[music, <insert the search terms here without comma>]"
            
        elif '3' in gptresp1:
            actid = 3
            prompt2 = f"You are a chatbot named {self.bot_name} conversing with a user and here is the conversation: {action_conv}. " \
                      "Choose and respond with only one response based on the following If-Else algorithm." \
                      f"If the user did not provide country name for news to find, ask for it." \
                      f"Else your response can only contain one Python3 list with this format:" \
                      f"[news, <insert the country name here without comma>]"
        
        else:
            prompt2 = f"You are a chatbot named {self.bot_name} conversing with a user and here is the conversation: {full_conversation}. " \
                      "Generate the next compact line of response in this conversation."
            
            
        gptresp2 = self.oai.chat_completion(prompt=prompt2).strip().replace(self.bot_name + ":", "").split('\n')[0]
        if actid in [1,2,3]:
            gptresp2 = gptresp2.replace("'", "").replace('"', "")
            id1 = gptresp2.find("[")
            id2 = gptresp2.find(",",id1)
            id3 = gptresp2.find("]",id2)
            
            if id1!=-1 and id2!=-1 and id3!=-1:
                act = [actdict[str(actid)],gptresp2[id2+1:id3]]
                act[1] = act[1].strip()
                print(f"List: {act}", gptresp2, id1,id2,id3)
                if len(act)>1:
                    if actid==1:
                        wthr = action(act[0], act[1])
                        gptresp2 = self.oai.chat_completion(prompt=f"Make one weather sentence from this weather report, like a radio weatherman: {wthr}.")
                    elif actid==3:
                        if act[1].lower() in ['usa', 'america', 'united states', 'united states of america']:
                            act[1] = 'us'
                        newsevents = action(act[0], act[1])
                        gptresp2 = self.oai.chat_completion(
                            prompt=f"Make a compact summary report from this  list of news events, like a radio news anchor: {newsevents}.")
                    elif actid==2:
                        playedmusic = action(act[0], act[1])
                        gptresp2 = f'Played {act[1]}.'
                
        self.conversation += [self.bot_name + ": " + gptresp2]
        self._update_history()
        self._awake()
        return gptresp2

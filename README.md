# DisplAI

DisplAI is an interactive, multimedia chatbot that leverages OpenAI's GPT, DALL-E, Whisper, and GTTS to create an engaging and immersive user experience. The chatbot listens to user input, transcribes it, generates appropriate responses, and creates images to visually represent the conversation. This repository contains the source code and an example script for implementing and using the DisplAI chatbot.

## Project Idea

The main goal of this project is to create an intelligent and interactive chatbot that combines multiple AI technologies to deliver a unique and engaging user experience. By integrating GPT for natural language understanding, DALL-E for image generation, Whisper for speech recognition, and GTTS for text-to-speech capabilities, the chatbot provides an immersive experience for users to interact with the AI in a seamless manner.

## Library

The DisplAI library consists of several modules:

    lib.viewer: This module provides the Viewer class for displaying images and animations based on the current state of the chatbot (e.g., awake, asleep, thinking, or speaking).
    lib.chatbot: This module contains the ChatBot class, which manages the chatbot's core functionalities such as handling conversation history, generating responses using GPT, and creating images using DALL-E.
    lib.audutils: This module includes the AudioHelper class, which handles audio input and output using Whisper for speech recognition and GTTS for text-to-speech.
    lib.imgutils: This module provides utility functions for working with images, such as converting images from strings to image objects.
    lib.OAIWrapper: This module contains the OAIWrapper class, which wraps the OpenAI API for GPT, DALL-E, and Whisper.

## Example

To use DisplAI in your own projects, simply import the necessary modules and classes from the library, and create instances of the Viewer, ChatBot, and AudioHelper classes. Then, use the provided methods to interact with the chatbot and manage the conversation.

For example:

'''
python

from lib.viewer import Viewer
from lib.chatbot import ChatBot
from lib.audutils import AudioHelper

viewer = Viewer()
chatbot = ChatBot("sophia")
audio_helper = AudioHelper()
'''

Once you have instantiated these classes, you can use their methods to handle user input, generate chatbot responses, and display images based on the conversation.

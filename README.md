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

```
from lib.viewer import Viewer
from lib.chatbot import ChatBot
from lib.audutils import AudioHelper

viewer = Viewer()
chatbot = ChatBot("sophia")
audio_helper = AudioHelper()
```

Once you have instantiated these classes, you can use their methods to handle user input, generate chatbot responses, and display images based on the conversation.

## Getting Started
### Prerequisites

To use DisplAI, you will need the following dependencies:

```
    Python 3.7 or newer
    OpenAI Python library
    GTTS (Google Text-to-Speech)
    DALL-E
    Whisper
    SpeechRecognition
    Pydub
    Pillow (PIL)
    Tkinter
    Numpy
    OpenCV (cv2)
```

### Installation

To install the required dependencies, run the following command:

```
pip install openai gtts DALL-E Whisper speechrecognition pydub Pillow tkinter numpy opencv-python
```

### Setup

To use DisplAI, you will need to set up API keys for the OpenAI API (GPT, DALL-E, and Whisper). Follow the instructions on the OpenAI API documentation to obtain your API key.

Once you have your API key, add it to your environment variables:

```
export OPENAI_API_KEY="your_api_key_here"
```

## Documentation
### Viewer Class

The Viewer class is responsible for displaying images and animations on the screen based on the chatbot's current state. It is a subclass of threading.Thread and can be used as follows:

```
viewer = Viewer()
viewer.change_state("awake")  # or "sleep", "thinking", or "saying"
viewer.show_image("path/to/image.png")
```

### ChatBot Class

The ChatBot class manages the chatbot's core functionalities, such as handling conversation history, generating responses using GPT, and creating images using DALL-E. Here are some of its methods:

    gen_image_from_conversation(): Generates an image based on the current conversation using DALL-E.
    is_awake(): Checks if the chatbot is currently awake (has been active within the last 60 seconds).
    add_user_msg(user_name, user_text): Adds a user message to the conversation and updates the chatbot's awake status.
    get_and_save_bot_next_msg(context_window=10): Generates and saves the chatbot's next message based on the conversation history and context.

### AudioHelper Class

The AudioHelper class handles audio input and output using Whisper for speech recognition and GTTS for text-to-speech. Some of its methods include:

    listen(): Listens for user input and returns an audio object.
    transcript(audio): Transcribes the given audio object using Whisper's speech recognition.
    say(text, lang="en", accent="us", path=''): Converts the given text to speech using GTTS and plays the resulting audio.

## Contributing

We welcome contributions to the DisplAI project! If you would like to contribute, please follow these steps:

    Fork the repository.
    Create a new branch for your feature or bugfix.
    Commit your changes to the new branch.
    Submit a pull request for your branch.

Please make sure to follow the project's coding style and guidelines, and include tests and documentation for any new features or changes.
## License

DisplAI is released under the MIT License. See the LICENSE file for more information.

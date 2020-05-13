import speech_recognition as sr
import os
import sys
import re
import json

sys.path.insert(0, "utils")

from utils.speech_2_text import Speech2Text
import pyttsx3
from topics.search import *
from topics.music import *
from helper import remove_word_from_command

gs = GoogleSearch()
basic_search = DefaultSearch()
spotify = Spotify()

import logging

logger = logging.getLogger(__name__)
logger.setLevel("INFO")
logging.basicConfig(level=logging.INFO)

def search_category(command):
    sub_command = remove_word_from_command("search", command)
    if "google" in sub_command:
        gs.search_engine(command)
    else:
        basic_search.search_engine(command)


def voiceResponse(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[7].id)
    engine.setProperty("rate", 225)
    engine.say(audio)
    engine.runAndWait()


def assistant(command):

    command = command["transcription"]
    if "search" in command:
        updated_command = remove_word_from_command("search", command)
        search_category(updated_command)
    
    elif "add to playlist" in command:
        spotify.add_track_to_master_playlist()

    elif "play" in command:
        updated_command = remove_word_from_command("play", command)
        spotify.play_song(updated_command)


voiceResponse(
    "Hi User, I am Jazzzzz. What's up?"
)

# loop to continue executing multiple commands
while True:
    listener = Speech2Text()
    assistant(listener.listen())

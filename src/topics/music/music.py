import logging
import sys
from abc import ABC, abstractmethod


class Music(ABC):
    @abstractmethod
    def play_song(self, query):
        raise NotImplementedError

import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")
from nltk.tokenize import word_tokenize

nltk.download("punkt")

cached_stopwords = stopwords.words("english")
cached_exceptions = [f"{word} google" for word in cached_stopwords]
cached_exceptions += [f"google {word}" for word in cached_stopwords]


def remove_word_from_command(word, command):
    answer = command.replace(word, "")
    return answer


def parse_google_command(command):
    answer = command
    for word in cached_exceptions:
        answer = answer.replace(word, "")
    return answer


def remove_stopwords(text):
    text_tokens = word_tokenize(text)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]

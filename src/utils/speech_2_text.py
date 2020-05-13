import json
import speech_recognition as sr


class Speech2Text(object):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self):
        with self.microphone as source:
            print("I'm listening ...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source)

        # set up the response object
        response = {"success": True, "error": None, "transcription": None}

        try:
            response["transcription"] = self.recognizer.recognize_google(audio).lower()
            print(json.dumps(response, indent=4))

        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
            print(json.dumps(response, indent=4))
            response = self.listen()

        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"
            print(json.dumps(response, indent=4))
            response = self.listen()

        return response

import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self, lang="pl-PL"):
        self.lang = lang
        self.recognizer = sr.Recognizer()

    def recognize(self):
        with sr.Microphone() as source:
            print("Say something...")
            audio = self.recognizer.listen(source)
        try:
            text = self.recognizer.recognize_google(audio, language=self.lang)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
        return None

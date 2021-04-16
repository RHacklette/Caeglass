 import speech_recognition as sr
import os
from pocketsphinx import LiveSpeech, get_model_path
from sendtext import Sendtext

class SpeechToText:
    def __init__(self):
        self.s = Sendtext()
        self.s.start()

    def detectWords(self, audiofilepath):
        r = sr.Recognizer()

        try:
            wavfile = sr.AudioFile(audiofilepath)
        except:
            print("Erreur de lecture de WAV")

        with wavfile as source:
            audio = r.record(source)
            try:
                res = r.recognize_google(audio, language='fr_FR')
            except:
                res = "..."

            #os.remove(audiofilepath)
            try:
                print(res)
                self.s.send(res)
            except:
                print("Erreur lors de l'affichage")

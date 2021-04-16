#!/usr/bin/env python3

import pyaudio
import wave
import os
import math
import time
from grove.adc import ADC
from pydub import AudioSegment
from testscontant import SpeechToText
from grove.helper import SlotHelper
pin = 0
seconds = 8
#filename = "output.wav"
__all__ = ['GroveSoundSensor']

#Record settings
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
stt = SpeechToText()
#p = pyaudio.PyAudio()

class GroveSoundSensor(object):
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def sound(self):
        value = self.adc.read(self.channel)
        return value

def Recording(filename):
    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

def Slicing(file):

        song = AudioSegment.from_wav(file)

        # pydub does things in milliseconds
        first = song[:4050]
        last = song[-4050:]
        first.export('first.wav', format="wav")
        last.export('last.wav', format="wav")
        print('first')
        stt.detectWords('/root/audio/first.wav')
        print('last')
        stt.detectWords('/root/audio/last.wav')

Grove = GroveSoundSensor

def main():
        count=0
        sensor = GroveSoundSensor(pin)
        while(True):
                filename = "/root/audio/output"+str(count)+".wav"
                print('Record')
                Recording(filename)
                print('Slice')
                Slicing(filename)
                os.remove(filename)
                count+=1%100

if __name__ == "__main__":
    main()

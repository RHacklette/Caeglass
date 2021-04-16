#!/usr/bin/env python3

import pyaudio
import wave
import os
import math
import time
import threading

from grove.adc import ADC
from pydub import AudioSegment
from testscontant import SpeechToText
from grove.helper import SlotHelper

pin = 0
seconds = 10
#filename = "output.wav"
__all__ = ['GroveSoundSensor']

#Record settings
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second

class GroveSoundSensor(object):
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def sound(self):
        value = self.adc.read(self.channel)
        return value

class Recorder(threading.Thread):
        def __init__(self):
                self.p = pyaudio.PyAudio()  # Create an interface to PortAudio
                self.stream = self.p.open(format=sample_format,
                         channels=channels,
                         rate=fs,
                         frames_per_buffer=chunk,
                         input=True)
                self.frames = []
                threading.Thread.__init__(self)
                self.pat = False

        def run(self):
                while self.pat:
                         data = self.stream.read(chunk)
                         frames.append(data)

        def recording(self):
                self.pat=True
                #begin=time.time()
                print('Recording')
                # Store data in chunks
                #for i in range(0, int(fs / chunk * seconds)):
                #data = self.stream.read(chunk)
                #self.frames.append(data)
                self.start()

        def stopRecording(self,filename):
                # Stop and close the stream
                #stream.stop_stream()
                #stream.close()
                # Terminate the PortAudio interface
                #p.terminate()
                print('Finished recording')
                self.pat=False
                # Save the recorded data as a WAV file
                wf = wave.open(filename, 'wb')
                wf.setnchannels(channels)
                wf.setsampwidth(self.p.get_sample_size(sample_format))
                wf.setframerate(fs)
                wf.writeframes(b''.join(self.frames))
                wf.close()

def slicing(file):
    song = AudioSegment.from_wav(file)

    # pydub does things in milliseconds
    first_5_seconds = song[:5100]
    last_5_seconds = song[-5100:]
    first_5_seconds.export('first_5_seconds.wav', format="wav")
    last_5_seconds.export('last_5_seconds.wav', format="wav")

    print('first_5_sec')
    detectWords('/root/audio/first_5_seconds.wav')

    print('last_5_sec')
    detectWords('/root/audio/last_5_seconds.wav')


def main():
        count=0
        c=0
        threshold_value=550
        limit = 4
        recordingbool = False
        sensor = GroveSoundSensor(pin)
        Record = Recorder()
        while(True):
                filename = "/home/pi/Music/output"+str(count)+".wav"
                print('Start value: {0}'.format(sensor.sound))
                if sensor.sound < threshold_value:
                        c += 1
                if sensor.sound > threshold_value:
                        c = 0
                        if not recordingbool:
                                recordingbool =  True
                                print("Je lance le record")
                                #Record.start()
                        else:
                                print("recording")
                if c >= limit:
                        if recordingbool:
                                print("Stop Recording")
                                recordingbool = False
                                Record.stopRecording(filename)

                                #print('Slice')
                                #slicing(filename)
                                #os.remove(filename)
                print('Final value: {0}'.format(sensor.sound))
                print(c)
                time.sleep(.5)
                count+=1%100

if __name__ == "__main__":
        main()

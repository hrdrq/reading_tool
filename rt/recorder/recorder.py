# -*- coding: utf-8 -*-

from threading import Thread

from pyaudio import PyAudio

CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100

class Recorder:

    def __init__(self):
        self._recorder = PyAudio()
        self.recording = False
        self.playing = False

    def record(self):
        if self.playing:
            return
        thread = Thread(target=self.start)
        thread.start()

    def start(self):
        self.recording = True
        self.stream = self._recorder.open(format=self._recorder.get_format_from_width(WIDTH),
                                            channels=CHANNELS,
                                            rate=RATE,
                                            input=True,
                                            output=True,
                                            frames_per_buffer=CHUNK)
        self.buffer = []
        while self.recording:
            data = self.stream.read(CHUNK)  #read audio stream
            self.buffer.append(data)
        self.play()

    def stop(self):
        self.recording = False

    def play(self):
        self.playing = True
        for data in self.buffer:
            self.stream.write(data, CHUNK)  #play back audio stream
        self.stream.stop_stream()
        self.stream.close()
        self.playing = False

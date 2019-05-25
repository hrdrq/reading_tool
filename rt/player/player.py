# -*- coding: utf-8 -*-

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

class Player(QMediaPlayer):

    def __init__(self, path):
        super().__init__()
        sound = QMediaContent(QUrl.fromLocalFile(path))
        self.setMedia(sound)

    def play(self, start, end):
        self.setPosition(start)
        super().play()

        while self.position() <= end:
            continue
        self.stop()

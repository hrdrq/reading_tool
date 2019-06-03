# -*- coding: utf-8 -*-

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

from rt.config import get_path

class Player(QMediaPlayer):

    def __init__(self, path):
        super().__init__()
        if path:
            sound = QMediaContent(QUrl.fromLocalFile(get_path(path)))
            self.setMedia(sound)

    def play(self, start=None, end=None, path=None):
        if path:
            sound = QMediaContent(QUrl.fromLocalFile(get_path(path)))
            self.setMedia(sound)
            super().play()
        else:
            self.setPosition(start)
            super().play()

            while self.position() <= end:
                continue
            self.stop()

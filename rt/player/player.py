# -*- coding: utf-8 -*-

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtCore import QUrl

from rt.config import get_path

class Player(QMediaPlayer):

    def __init__(self, path):
        super().__init__()
        if path:
            sound = QMediaContent(QUrl.fromLocalFile(get_path(path)))
            self.setMedia(sound)
        else:
            play_list = QMediaPlaylist()
            play_list.setPlaybackMode(QMediaPlaylist.Sequential)
            self.setPlaylist(play_list)
            self.play_list = play_list

    def play(self, start=None, end=None, files=None):
        if files:
            self.play_list.clear()
            for file in files:
                self.play_list.addMedia(QMediaContent(QUrl.fromLocalFile(get_path(file))))
            super().play()
        else:
            self.setPosition(start)
            super().play()

            while self.position() <= end:
                continue
            self.stop()

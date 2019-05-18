# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

class Play(QPushButton):

    def __init__(self, parent, start, end):
        super().__init__(">", parent)
        self.start = start
        self.end = end
        self.clicked.connect(self.do)
        self.player = QMediaPlayer(self)
        sound = QMediaContent(QUrl.fromLocalFile("/Users/ericsun/Downloads/20190428.mp3"))
        self.player.setMedia(sound)
        self.player.setVolume(50)

    def do(self):
        print('do', self.start, self.end)
        self.player.play()
        print('end')

class Sentence(QWidget):

    def __init__(self, sentence):
        super().__init__()
        self.layout = QGridLayout()
        self.play = Play(self, sentence['start'], sentence['end'])
        self.text = QLabel(sentence['text'], self)
        self.text.move(50, 0)
        # text.setText()

        # self.layout.addWidget(button, 0, 0)
        # self.layout.addWidget(text, 0, 1)
        # self.setLayout(self.layout)

class Paragraph(QWidget):

    def __init__(self, paragraph):
        super().__init__()
        self.layout = QVBoxLayout()
        self.sentences = []
        for _sentence in paragraph:
            sentence = Sentence(_sentence)
            self.sentences.append(sentence)
            self.layout.addWidget(sentence)
        self.setLayout(self.layout)

class View(QWidget):

    def __init__(self, rt, article):
        super().__init__()
        self.rt = rt
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.set_article(article)

    def set_article(self, article):
        # if not hasattr(self, 'layout'):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        self.paragraphs = []
        for _paragraph in article:
            paragraph = Paragraph(_paragraph)
            self.paragraphs.append(paragraph)
            self.layout.addWidget(paragraph)

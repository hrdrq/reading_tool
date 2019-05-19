# -*- coding: utf-8 -*-

from itertools import chain

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton

from rt.player import Player

class PlayButton(QPushButton):

    def __init__(self, parent, start, end):
        super().__init__(">", parent)
        self.parent = parent
        self.start = start
        self.end = end
        self.clicked.connect(self.play)

    def play(self):
        player = self.parent.parent.parent.player
        player.play(self.start, self.end)

class Sentence(QWidget):

    def __init__(self, parent, sentence):
        super().__init__()
        self.parent = parent
        self.layout = QGridLayout()
        self.play_button = PlayButton(self, sentence['start'], sentence['end'])
        self.text = QLabel(sentence['text'], self)
        # self.text.setWordWrap(True)
        self.text.move(50, 0)

    def set_bold(self, to_set):
        font = self.text.font()
        font.setBold(to_set)
        self.text.setFont(font)

    def focus(self):
        self.set_bold(True)

    def unfocus(self):
        self.set_bold(False)

    def play(self):
        self.play_button.play()

class Paragraph(QWidget):

    def __init__(self, parent, paragraph):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout()
        self.sentences = []
        for _sentence in paragraph:
            sentence = Sentence(self, _sentence)
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
        self.sentence_index = 0
        self.focus_sentence()

    def set_article(self, article):
        self.player = Player(article['audio'])
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        self.paragraphs = []
        for _paragraph in article['article']:
            paragraph = Paragraph(self, _paragraph)
            self.paragraphs.append(paragraph)
            self.layout.addWidget(paragraph)

    def focus_sentence(self):
        self.sentences[self.sentence_index].focus()

    def to_next_sentence(self):
        sentences = self.sentences
        if self.sentence_index == len(sentences) - 1:
            return
        sentences[self.sentence_index].unfocus()
        self.sentence_index += 1
        sentences[self.sentence_index].focus()

    def to_prev_sentence(self):
        if self.sentence_index == 0:
            return
        sentences = self.sentences
        sentences[self.sentence_index].unfocus()
        self.sentence_index -= 1
        sentences[self.sentence_index].focus()

    def play_sentence(self):
        self.sentences[self.sentence_index].play()

    @property
    def sentences(self):
        return list(chain(*[p.sentences for p in self.paragraphs]))

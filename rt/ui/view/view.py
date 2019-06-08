# -*- coding: utf-8 -*-

from itertools import chain

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QScrollArea
from PyQt5.Qt import QRect

from rt.player import Player
from rt.ui.edit import Edit

class PlayButton(QPushButton):

    def __init__(self, parent, start, end, audio):
        super().__init__(">", parent)
        self.parent = parent
        self.start = start
        self.end = end
        self.audio = audio
        self.clicked.connect(self.play)

    def play(self):
        player = self.parent.parent.parent.player
        if self.audio:
            player.play(files=[self.audio])
        else:
            player.play(start=self.start, end=self.end)

class Sentence(QWidget):

    def __init__(self, parent, sentence):
        super().__init__()
        self.parent = parent
        # self.layout = QGridLayout()
        self.play_button = PlayButton(self, sentence.get('start'), sentence.get('end'), sentence.get('audio'))
        self.text = QLabel(sentence['text'], self)
        # self.text.setWordWrap(True)
        self.text.move(50, 0)
        self.setFixedHeight(20)

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
        self.layout = QVBoxLayout(self)
        self.sentences = []
        for _sentence in paragraph:
            sentence = Sentence(self, _sentence)
            self.sentences.append(sentence)
            self.layout.addWidget(sentence)

    def play(self):
        player = self.parent.player
        sentences = self.sentences
        if sentences[0].play_button.start:
            player.play(start=sentences[0].play_button.start, end=sentences[-1].play_button.end)
        else:
            player.play(files=[sentence.play_button.audio for sentence in sentences])

class ToolBar(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.edit_button = QPushButton('Edit', self)
        self.setFixedHeight(25)
        self.edit_button.clicked.connect(self.show_edit)

    def show_edit(self):
        self.edit = Edit(self.parent.article, self.parent.file)
        self.edit.resize(800, 800)
        self.edit.show()

class View(QWidget):

    def __init__(self, rt, article, file):
        super().__init__()
        self.rt = rt
        self.base_layout = QVBoxLayout(self)
        self.tool_bar = ToolBar(self)
        self.scroll = QScrollArea(self)
        self.base_layout.addWidget(self.tool_bar)
        self.base_layout.addWidget(self.scroll)
        # self.scroll.resize(600, 450)
        self.base = QWidget()
        self.layout = QVBoxLayout(self.base)
        self.scroll.setWidget(self.base)
        self.scroll.setWidgetResizable(True)
        # self.scroll.move(0, 50)
        # self.setFixedHeight(400)
        self.article = article
        self.file = file
        self.set_article(article, file)
        self.sentence_index = 0
        self.focus_sentence()

    def set_article(self, article, file):
        self.article = article
        self.file = file
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

    def select_sentence(self, direction):
        sentences = self.sentences
        if (direction == 'prev' and self.sentence_index == 0) or \
            (direction == 'next' and self.sentence_index == len(sentences) - 1):
            return
        try:
            sentences[self.sentence_index].unfocus()
            self.sentence_index += (1 if direction == 'next' else -1)
        except:
            self.sentence_index = 0
        sentence = sentences[self.sentence_index]
        sentence.focus()
        if sentence.visibleRegion().boundingRect().height() != sentence.height():
            scroll_bar = self.scroll.verticalScrollBar()
            scroll_bar.setValue(scroll_bar.value() + (100 if direction == 'next' else -100))

    def to_next_sentence(self):
        self.select_sentence('next')

    def to_prev_sentence(self):
        self.select_sentence('prev')

    def to_first_sentence(self):
        sentences = self.sentences
        try:
            sentences[self.sentence_index].unfocus()
        except:
            pass
        self.sentence_index = 0
        sentences[0].focus()
        self.scroll.verticalScrollBar().setValue(0)

    def to_last_sentence(self):
        sentences = self.sentences
        try:
            sentences[self.sentence_index].unfocus()
        except:
            pass
        self.sentence_index = len(sentences) - 1
        sentences[self.sentence_index].focus()
        scroll_bar = self.scroll.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

    def play_sentence(self):
        self.sentences[self.sentence_index].play()

    def play_paragraph(self):
        self.sentences[self.sentence_index].parent.play()

    @property
    def sentences(self):
        return list(chain(*[p.sentences for p in self.paragraphs]))

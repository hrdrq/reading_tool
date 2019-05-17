# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

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

class Sentence(QWidget):

    def __init__(self, sentence):
        super().__init__()
        self.layout = QHBoxLayout()
        text = QLabel()
        text.setText(sentence['text'])
        button = QPushButton(">")
        self.layout.addWidget(button)
        self.layout.addWidget(text)
        self.setLayout(self.layout)

class View(QWidget):

    def __init__(self, article):
        super().__init__()
        self.layout = QVBoxLayout()
        self.paragraphs = []
        for _paragraph in article:
            paragraph = Paragraph(_paragraph)
            self.paragraphs.append(paragraph)
            self.layout.addWidget(paragraph)

        self.setLayout(self.layout)

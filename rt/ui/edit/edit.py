# -*- coding: utf-8 -*-

import json

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel, QLineEdit
from PyQt5.Qt import QStyleOption, QPainter, QStyle

class ToolBar(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QHBoxLayout(self)
        self.add_sentence_button = QPushButton('Add Sentence', self)
        self.add_paragraph_button = QPushButton('Add Paragraph', self)
        self.save_button = QPushButton('Save', self)
        self.add_sentence_button.setFixedWidth(140)
        self.add_paragraph_button.setFixedWidth(140)
        self.save_button.setFixedWidth(80)
        self.add_paragraph_button.move(150, 0)
        self.save_button.move(300, 0)
        self.setFixedHeight(25)
        # self.edit_button.clicked.connect(self.show_edit)

class Sentence(QWidget):

    def __init__(self, parent, sentence):
        super().__init__()
        self.parent = parent
        self.sentence = sentence
        self.text = QLineEdit(sentence['text'], self)
        self.text.resize(800, 25)
        self.start = QLineEdit(str(sentence['start'] or ''), self)
        self.end = QLineEdit(str(sentence['end'] or ''), self)
        start_label = QLabel('Start', self)
        end_label = QLabel('End', self)
        start_label.move(0, 30)
        self.start.move(40, 30)
        end_label.move(180, 30)
        self.end.move(210, 30)
        self.setFixedHeight(70)

        self.text.editingFinished.connect(lambda: self.update('text'))
        self.start.editingFinished.connect(lambda: self.update('start'))
        self.end.editingFinished.connect(lambda: self.update('end'))

    def update(self, attr):
        value = getattr(self, attr).text()
        self.sentence[attr] = value if attr == 'text' else int(value or 0)

class Paragraph(QWidget):

    def __init__(self, parent, paragraph):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.setObjectName('Paragraph')
        self.setStyleSheet('#Paragraph{border:2px solid black;}')
        self.sentences = []
        for _sentence in paragraph:
            sentence = Sentence(self, _sentence)
            self.sentences.append(sentence)
            self.layout.addWidget(sentence)

    # setStyleSheetを使うため、override必要がある
    # https://wiki.qt.io/How_to_Change_the_Background_Color_of_QWidget
    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)


class Edit(QWidget):

    def __init__(self, article, file):
        super().__init__()
        self.article = article
        self.file = file
        self.base_layout = QVBoxLayout(self)
        self.tool_bar = ToolBar(self)
        self.scroll = QScrollArea(self)
        self.base_layout.addWidget(self.tool_bar)
        self.base_layout.addWidget(self.scroll)
        self.base = QWidget()
        self.layout = QVBoxLayout(self.base)
        self.scroll.setWidget(self.base)
        self.scroll.setWidgetResizable(True)

        self.tool_bar.save_button.clicked.connect(self.save)
        self.tool_bar.add_paragraph_button.clicked.connect(self.add_paragraph)
        self.load()

    def add_paragraph(self):
        raw_paragraph = [dict(text='', start=0, end=0)]
        self.article['article'].append(raw_paragraph)
        paragraph = Paragraph(self, raw_paragraph)
        self.paragraphs.append(paragraph)
        self.layout.addWidget(paragraph)

    def save(self):
        # print(self.file)
        with open(self.file, 'w') as f:
            json.dump(self.article, f, indent=2, ensure_ascii=False)

    def load(self):
        self.paragraphs = []
        for _paragraph in self.article['article']:
            paragraph = Paragraph(self, _paragraph)
            self.paragraphs.append(paragraph)
            self.layout.addWidget(paragraph)

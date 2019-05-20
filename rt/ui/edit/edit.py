# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel, QLineEdit

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
        self.text = QLineEdit(sentence['text'], self)
        self.text.resize(800, 25)
        self.start = QLineEdit(str(sentence['start']), self)
        self.end = QLineEdit(str(sentence['end']), self)
        start_label = QLabel('Start', self)
        end_label = QLabel('End', self)
        start_label.move(0, 30)
        self.start.move(40, 30)
        end_label.move(180, 30)
        self.end.move(210, 30)
        self.setFixedHeight(70)

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


class Edit(QWidget):

    def __init__(self, article):
        super().__init__()
        self.article = article
        self.base_layout = QVBoxLayout(self)
        self.tool_bar = ToolBar(self)
        self.scroll = QScrollArea(self)
        self.base_layout.addWidget(self.tool_bar)
        self.base_layout.addWidget(self.scroll)
        self.base = QWidget()
        self.layout = QVBoxLayout(self.base)
        self.scroll.setWidget(self.base)
        self.scroll.setWidgetResizable(True)

        self.paragraphs = []
        for _paragraph in article['article']:
            paragraph = Paragraph(self, _paragraph)
            self.paragraphs.append(paragraph)
            self.layout.addWidget(paragraph)

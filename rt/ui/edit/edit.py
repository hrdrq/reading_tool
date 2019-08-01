# -*- coding: utf-8 -*-

import json

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
                            QScrollArea, QLabel, QLineEdit, QFileDialog, QSpinBox
from PyQt5.Qt import QStyleOption, QPainter, QStyle

from rt.ui.audio import Audio
from rt.config import get_path, root
from rt.shortcut import Shortcut

class ToolBar(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QHBoxLayout(self)
        self.add_sentence_button = QPushButton('Add Sentence', self)
        self.add_paragraph_button = QPushButton('Add Paragraph', self)
        self.save_button = QPushButton('Save', self)
        if parent.article['audio'] != False:
            self.file_text = QLineEdit(parent.article['audio'], self)
            self.file_text.setFixedWidth(280)
            self.file_select = QPushButton('Select', self)
            self.file_select.clicked.connect(self.show_file_dialog)
            self.file_text.move(380, 0)
            self.file_select.move(660, 0)
        self.add_sentence_button.setFixedWidth(140)
        self.add_paragraph_button.setFixedWidth(140)
        self.save_button.setFixedWidth(80)
        self.add_paragraph_button.move(150, 0)
        self.save_button.move(300, 0)
        self.setFixedHeight(25)

    def show_file_dialog(self):
        self.file_dialog = QFileDialog()
        self.file_dialog.fileSelected.connect(self.set_file)
        self.file_dialog.show()

    def set_file(self, file_name):
        file_name = file_name.replace(root(), '')
        self.file_text.setText(file_name)
        self.parent.article['audio'] = file_name

class Sentence(QWidget):

    def __init__(self, parent, sentence):
        super().__init__()
        self.parent = parent
        self.sentence = sentence
        self.text = QLineEdit(sentence['text'], self)
        self.text.resize(800, 25)
        self.text.editingFinished.connect(lambda: self.update('text'))
        self.text.mousePressEvent = self.mousePressEvent
        self.remove_button = QPushButton('Remove', self)
        self.remove_button.move(0, 30)
        self.play_button = QPushButton('Play', self)
        self.play_button.move(80, 30)
        self.play_button.clicked.connect(self.play)
        if 'start' in sentence:
            # self.start = QLineEdit(str(sentence['start'] or ''), self)
            # self.end = QLineEdit(str(sentence['end'] or ''), self)
            for time_edit in ('start', 'end'):
                setattr(self, time_edit, QSpinBox(self))
                edit = getattr(self, time_edit)
                edit.setMaximum(99999999)
                edit.setSingleStep(100)
                if sentence[time_edit]:
                    edit.setValue(sentence[time_edit])
            self.start.valueChanged.connect(lambda: self.valueChanged('start'))
            self.end.valueChanged.connect(lambda: self.valueChanged('end'))
            # self.start = QSpinBox(self)
            # if sentence['start']:
            #     print("sentence['start']", sentence['start'], type(sentence['start']))
            #     self.start.setValue(sentence['start'])
            # self.end = QSpinBox(self)
            # if sentence['end']:
            #     self.end.setValue(sentence['end'])
            start_label = QLabel('Start', self)
            end_label = QLabel('End', self)
            self.set_button = QPushButton('Set', self)
            start_label.move(155, 30)
            self.start.move(190, 30)
            end_label.move(320, 30)
            self.end.move(350, 30)
            self.set_button.move(490, 30)
            self.start.editingFinished.connect(lambda: self.update('start'))
            self.end.editingFinished.connect(lambda: self.update('end'))
            # self.start.mousePressEvent = self.mousePressEvent
            # self.end.mousePressEvent = self.mousePressEvent
            self.set_button.clicked.connect(self.set_start_end)
        self.setFixedHeight(70)
        self.remove_button.clicked.connect(lambda: self.parent.parent.remove_sentence(self))

    def play(self):
        self.parent.parent.audio.player.play(self.sentence['start'], self.sentence['end'])

    def set_start_end(self):
        audio = self.parent.parent.audio
        start, end = audio.start_end
        self.sentence['start'] = start
        self.sentence['end'] = end
        self.start.setValue(str(start))
        self.end.setValue(str(end))

    def update(self, attr):
        value = getattr(self, attr).text()
        if attr == 'text':
            self.sentence[attr] = value
        else:
            try:
                self.sentence[attr] = int(value)
            except:
                self.sentence[attr] = 0

    def mousePressEvent(self, _=None):
        # self.parent.mousePressEvent()
        self.parent.parent.update_sentence_focusing(self.parent, self)

    def valueChanged(self, attr):
        self.mousePressEvent()
        self.update(attr)

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
        self.remove_button = QPushButton('Remove Paragraph', self)
        self.layout.addWidget(self.remove_button)

        self.remove_button.clicked.connect(lambda: self.parent.remove_paragraph(self))

    def mousePressEvent(self, _):
        self.parent.update_paragraph_focusing(self)

    # setStyleSheetを使うため、override必要がある
    # https://wiki.qt.io/How_to_Change_the_Background_Color_of_QWidget
    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

    def add_sentence(self, raw_sentence):
        sentence = Sentence(self, raw_sentence)
        self.sentences.append(sentence)
        self.layout.addWidget(sentence)


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
        try:
            self.audio = Audio(self, article['audio'])
            self.base_layout.addWidget(self.audio)
        except:
            pass
        self.base = QWidget()
        self.layout = QVBoxLayout(self.base)
        self.scroll.setWidget(self.base)
        self.scroll.setWidgetResizable(True)

        self.tool_bar.save_button.clicked.connect(self.save)
        self.tool_bar.add_paragraph_button.clicked.connect(self.add_paragraph)
        self.tool_bar.add_sentence_button.clicked.connect(self.add_sentence)
        self.shortcut = Shortcut(self)
        self.shortcut.alt_z.activated.connect(self.play_focusing_sentence)
        self.load()

    @staticmethod
    def create_raw_sentence():
        return dict(text='', start=0, end=0)

    def add_paragraph(self):
        raw_paragraph = [self.create_raw_sentence()]
        self.article['article'].append(raw_paragraph)
        paragraph = Paragraph(self, raw_paragraph)
        self.paragraphs.append(paragraph)
        self.layout.addWidget(paragraph)

    def add_sentence(self):
        raw_sentence = self.create_raw_sentence()
        self.article['article'][self.paragraph_focusing].append(raw_sentence)
        self.paragraphs[self.paragraph_focusing].add_sentence(raw_sentence)

    def remove_sentence(self, sentence):
        for p_index in range(len(self.paragraphs)):
            for s_index in range(len(self.paragraphs[p_index].sentences)):
                if self.paragraphs[p_index].sentences[s_index] == sentence:
                    self.paragraphs[p_index].layout.removeWidget(sentence)
                    del self.paragraphs[p_index].sentences[s_index]
                    del self.article['article'][p_index][s_index]
                    return

    def remove_paragraph(self, paragraph):
        for p_index in range(len(self.paragraphs)):
            if self.paragraphs[p_index] == paragraph:
                self.layout.removeWidget(paragraph)
                del self.paragraphs[p_index]
                del self.article['article'][p_index]
                return

    def save(self):
        # print(self.file)
        with open(get_path(self.file), 'w') as f:
            json.dump(self.article, f, indent=2, ensure_ascii=False)

    def load(self):
        self.paragraphs = []
        for _paragraph in self.article['article']:
            paragraph = Paragraph(self, _paragraph)
            self.paragraphs.append(paragraph)
            self.layout.addWidget(paragraph)
        self.paragraph_focusing = 0
        self.sentence_focusing = 0

    def update_paragraph_focusing(self, paragraph):
        for index, p in enumerate(self.paragraphs):
            if p == paragraph:
                self.paragraph_focusing = index
                break

    def update_sentence_focusing(self, paragraph, sentence):
        for p_index, p in enumerate(self.paragraphs):
            if p == paragraph:
                self.paragraph_focusing = p_index
                for s_index, s in enumerate(p.sentences):
                    if s == sentence:
                        self.sentence_focusing = s_index
                        break
                break

    def play_focusing_sentence(self):
        # print('play_focusing_sentence')
        self.paragraphs[self.paragraph_focusing].sentences[self.sentence_focusing].play()

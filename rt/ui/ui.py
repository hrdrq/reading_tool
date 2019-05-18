# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

from rt.base import Base
from rt.ui.list import List
from rt.ui.view import View
from rt.shortcut import Shortcut
from rt.recorder import Recorder

class Ui(QMainWindow):

    def __init__(self, rt):
        super().__init__()
        self.rt = rt
        self.title = "Reading Tool"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480


        self.shortcut = Shortcut(self)
        self.recorder = Recorder()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        article_list = self.rt.article.list()
        self.list = List(self.rt, article_list)
        self.view = View(self.rt, self.rt.article.item(article_list[0]['id']))
        self.central_widget = QWidget()
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.list, 2)
        self.layout.addWidget(self.view, 5)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.shortcut.up.activated.connect(self.view.to_prev_sentence)
        self.shortcut.down.activated.connect(self.view.to_next_sentence)
        self.shortcut.z.activated.connect(self.view.play_sentence)

    def start_record(self):
        self.recorder.record()

    def stop_record(self):
        self.recorder.stop()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.start_record()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.stop_record()

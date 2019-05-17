# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel

from rt.base import Base
from rt.ui.list import List
from rt.ui.view import View

class Ui(QMainWindow):

    def __init__(self, rt):
        super().__init__()
        self.rt = rt
        self.title = "Reading Tool"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480



        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        article_list = self.rt.article.list()
        self.list = List(article_list)
        self.view = View(self.rt.article.item(article_list[0]['id']))
        self.central_widget = QWidget()
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.list, 2)
        self.layout.addWidget(self.view, 5)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

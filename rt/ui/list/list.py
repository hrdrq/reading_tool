# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QListWidget

class List(QListWidget):

    def __init__(self, article_list):
        super().__init__()
        for article in article_list:
            self.addItem(article['title'])

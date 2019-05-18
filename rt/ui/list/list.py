# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QListWidget, QListWidgetItem

class Item(QListWidgetItem):

    def __init__(self, title, id):
        super().__init__()
        self.setText(title)
        self.id = id

class List(QListWidget):

    def __init__(self, rt, article_list):
        super().__init__()
        self.rt = rt
        for article in article_list:
            item = Item(article['title'], article['id'])
            self.addItem(item)
        self.itemClicked.connect(self.select)

    def select(self, item):
        article = self.rt.article.item(item.id)
        self.rt.ui.view.set_article(article)

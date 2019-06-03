# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, \
                            QPushButton, QHBoxLayout, QLineEdit, QInputDialog

class Item(QTreeWidgetItem):

    def __init__(self, title, id=None, children=None):
        super().__init__()
        self.setText(0, title)
        if id:
            self.id = id
        elif children:
            for child in children:
                child = Item(child['title'], child['id'])
                self.addChild(child)

class ToolBar(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QHBoxLayout(self)
        self.add_button = QPushButton('Add', self)
        self.edit_button = QPushButton('Edit', self)
        self.remove_button = QPushButton('Remove', self)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.edit_button)
        self.layout.addWidget(self.remove_button)
        self.setFixedHeight(40)

        self.add_button.clicked.connect(self.show_dialog)

    def show_dialog(self):
        text, okPressed = QInputDialog.getText(self, "", "Title:", QLineEdit.Normal, "")
        if okPressed and text != '':
            self.parent.add(text)


class List(QWidget):

    def __init__(self, rt, article_list):
        super().__init__()
        self.rt = rt
        self.layout = QVBoxLayout(self)
        self.tool_bar = ToolBar(self)
        self.list_widget = QTreeWidget()
        self.article_list = article_list
        for article in article_list:
            if 'id' in article:
                item = Item(article['title'], id=article['id'])
            elif 'children' in article:
                item = Item(article['title'], children=article['children'])
            self.list_widget.addTopLevelItem(item)
        self.list_widget.itemClicked.connect(self.select)
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.tool_bar)

    def select(self, item):
        if not hasattr(item, 'id'):
            return
        self.rt.ui.view.set_article(*self.rt.article.item(item.id))

    def add(self, title):
        id, self.article_list = self.rt.article.add(title)
        item = Item(title, id=id)
        self.list_widget.addTopLevelItem(item)

    def edit(self):
        pass

    def remove(self):
        pass

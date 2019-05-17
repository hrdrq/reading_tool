# -*- coding: utf-8 -*-

from rt.base import Base
from rt.ui import Ui
from rt.article import Article

class Rt(Base):

    def __init__(self):
        self.article = Article()
        self.ui = Ui(self)

    def show(self):
        self.ui.show()

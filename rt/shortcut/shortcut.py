# -*- coding: utf-8 -*-

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

class Shortcut:

    def __init__(self, ui):
        self.up = QShortcut(QKeySequence("Up"), ui)
        self.down = QShortcut(QKeySequence("Down"), ui)
        self.slash = QShortcut(QKeySequence("/"), ui)
        self.dot = QShortcut(QKeySequence("."), ui)
        self.e = QShortcut(QKeySequence("E"), ui)

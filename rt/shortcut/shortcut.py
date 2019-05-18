# -*- coding: utf-8 -*-

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

class Shortcut:

    def __init__(self, ui):
        self.up = QShortcut(QKeySequence("Up"), ui)
        self.down = QShortcut(QKeySequence("Down"), ui)
        self.z = QShortcut(QKeySequence("Z"), ui)

# -*- coding: utf-8 -*-

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

class Shortcut:

    def __init__(self, ui):
        self.up = QShortcut(QKeySequence("Up"), ui)
        self.down = QShortcut(QKeySequence("Down"), ui)
        self.ctrl_up = QShortcut(QKeySequence("Ctrl+Up"), ui)
        self.ctrl_down = QShortcut(QKeySequence("Ctrl+Down"), ui)
        self.slash = QShortcut(QKeySequence("/"), ui)
        self.dot = QShortcut(QKeySequence("."), ui)
        self.e = QShortcut(QKeySequence("E"), ui)
        self.alt_z = QShortcut(QKeySequence("Alt+Z"), ui)
        self.underline = QShortcut(QKeySequence("_"), ui)

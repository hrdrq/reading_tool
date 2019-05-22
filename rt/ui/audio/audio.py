# -*- coding: utf-8 -*-

import json

from PyQt5.QtWidgets import QWidget, QScrollArea
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Audio(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.scroll = QScrollArea(self)
        fig, ax = plt.subplots(1)
        DPI = fig.get_dpi()
        fig.set_size_inches(2400.0/float(DPI),190.0/float(DPI))
        self.figure_canvas = FigureCanvas(fig)
        self.figure_canvas.setParent(parent)
        self.scroll.setWidget(self.figure_canvas)
        self.scroll.setFixedHeight(200)
        self.scroll.setFixedWidth(750)
        self.setFixedHeight(200)

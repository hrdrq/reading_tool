# -*- coding: utf-8 -*-

import json
from threading import Thread

from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from pydub import AudioSegment
import numpy as np

from rt.player import Player
from rt.config import get_path

class Audio(QWidget):

    def __init__(self, parent, path):
        super().__init__()
        self.parent = parent
        # self.scroll = QScrollArea(self)
        self.fig, self.ax = plt.subplots(1)
        DPI = self.fig.get_dpi()
        # self.fig.set_size_inches(7200.0/float(DPI),190.0/float(DPI))
        self.figure_canvas = FigureCanvas(self.fig)
        self.figure_canvas.setParent(self)
        # self.scroll.setWidget(self.figure_canvas)
        # self.scroll.setFixedHeight(200)
        # self.scroll.setFixedWidth(750)
        layout = QVBoxLayout(self)
        layout.addWidget(self.figure_canvas)
        # self.setFixedWidth(750)
        self.setFixedHeight(300)
        sound = AudioSegment.from_file(get_path(path), "mp3")
        data = np.array(sound.get_array_of_samples())
        data = data[::sound.channels]
        self.data = data[::int(sound.frame_rate / 100)]
        self.offset = 0
        self.ax.plot(range(self.offset, self.offset + 2000), self.data[self.offset:self.offset + 2000])
        self.ax.get_yaxis().set_visible(False)
        self.start = None
        self.end = None
        self.fill = None
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)

        self.player = Player(path)

    def on_scroll(self, event):
        if event.button == 'down' and self.offset < len(self.data) - 50:
            self.offset += 50
        elif event.button == 'up' and self.offset > 50:
            self.offset -= 50
        else:
            return
        self.fill = None
        self.ax.clear()
        plot_data = self.data[self.offset:self.offset + 2000]
        self.ax.plot(range(self.offset, self.offset + len(plot_data)), plot_data)
        self.fig.canvas.draw()

    def on_press(self, event):
        self.start = int(event.xdata)

    def on_release(self, event):
        self.end = int(event.xdata)
        if not self.fill:
            self.fill = self.ax.axvspan(self.start, self.end, alpha=0.5, color='yellow')
        else:
            x0, x1 = self.start, self.end
            _ndarray = self.fill.get_xy()
            _ndarray[:, 0] = [x0, x0, x1, x1, x0]
            self.fill.set_xy(_ndarray)
        self.fig.canvas.draw()
        thread = Thread(target=lambda:self.player.play((self.start - 1) * 10, (self.end + 1) * 10))
        thread.start()

    @property
    def start_end(self):
        return (self.start - 1) * 10, (self.end + 1) * 10

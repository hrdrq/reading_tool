from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')

if __name__ == '__main__':

    app = QApplication(sys.argv)
    widget = QWidget()
    widget.resize(400, 300)
    fig, ax = plt.subplots(1)
    fig.set_size_inches(30, 1)
    figure_canvas = FigureCanvas(fig)
    scroll = QScrollArea(widget)
    scroll.setWidget(figure_canvas)
    widget.show()

    sys.exit(app.exec_())

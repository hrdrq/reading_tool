# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication

from rt import Rt
from rt.article import Article

if __name__ == '__main__':
    app = QApplication(sys.argv)
    rt = Rt()
    rt.show()
    sys.exit(app.exec_())

    # a = Article()
    # print(a.list())

    # a = Article()
    # print(a.item('123'))

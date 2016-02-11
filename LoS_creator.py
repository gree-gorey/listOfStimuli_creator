# -*- coding:utf-8 -*-

import sys
from PyQt4.QtGui import *

__author__ = 'Gree-gorey'


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(500, 700)
        self.center()
        self.setWindowTitle(u'LoS creator 0.1')


        # check
        cb = QCheckBox(u'Инструментальный', self)
        cb.move(20, 50)

        def go():
            print cb.checkState(), button_group.checkedId()

        # Add a button
        btn = QPushButton(u'Рассчитать', self)
        btn.setToolTip(u'Нажмите, чтобы составить листы')
        btn.clicked.connect(go)
        btn.resize(btn.sizeHint())
        btn.move(380, 640)

        # text
        list1_label = QLabel(u'Лист 1', self)
        list1_label.move(110, 20)
        list2_label = QLabel(u'Лист 2', self)
        list2_label.move(320, 20)

        # radio
        button_group = QButtonGroup()

        button1 = QRadioButton(u'раз', self)
        button1.move(20, 70)
        button2 = QRadioButton(u'два', self)
        button2.move(20, 90)
        button3 = QRadioButton(u'три', self)
        button3.move(20, 110)

        button_group.addButton(button1, 1)
        button_group.addButton(button2, 2)
        button_group.addButton(button3, 3)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

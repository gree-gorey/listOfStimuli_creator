# -*- coding:utf-8 -*-

import sys
# from PyQt4.QtGui import *
from PyQt4.Qt import *

__author__ = 'Gree-gorey'


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        # self.resize(500, 500)
        self.center()
        self.setWindowTitle(u'LoS creator 0.1')

        # задаем шрифты
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        pos_font = QFont()
        pos_font.setBold(True)
        pos_font.setPointSize(18)

        # создаем главный грид
        main_layout = QGridLayout()

        ############
        # ЛИСТ 1
        ############

        groupBox = QGroupBox()
        vbox = QVBoxLayout()

        # выбор части речи
        verbs = QRadioButton(u'Глаголы')
        verbs.setFont(pos_font)
        nouns = QRadioButton(u'Существительные')
        nouns.setFont(pos_font)
        list_1_pos = QButtonGroup()
        list_1_pos.addButton(verbs, 1)
        list_1_pos.addButton(nouns, 2)
        label_list1 = QLabel(u'Лист 1\n')
        label_list1.setAlignment(Qt.AlignHCenter)
        label_list1.setFont(title_font)
        vbox.addWidget(label_list1)

        # раздел ГЛАГОЛЫ
        vbox.addWidget(verbs)

        # уточняем кол-во аргументов
        vbox.addWidget(QLabel(u'Уточните количество аргументов'))
        arguments_list1 = QComboBox()
        arguments_list1.addItem(u'любые')
        arguments_list1.addItem(u'только один аргумент')
        arguments_list1.addItem(u'только два аргумента')
        vbox.addWidget(arguments_list1)

        # учточняем возвратность
        vbox.addWidget(QLabel(u'Уточните возвратность'))
        reflexivity_list1 = QComboBox()
        reflexivity_list1.addItem(u'любые')
        reflexivity_list1.addItem(u'только возвратные')
        reflexivity_list1.addItem(u'только невозвратные')
        vbox.addWidget(reflexivity_list1)

        # учточняем инструментальность
        vbox.addWidget(QLabel(u'Уточните инструментальность'))
        instrumentality_list1 = QComboBox()
        instrumentality_list1.addItem(u'любые')
        instrumentality_list1.addItem(u'только инструментальные')
        instrumentality_list1.addItem(u'только неинструментальные')
        vbox.addWidget(instrumentality_list1)

        # учточняем именную соотнесенность
        vbox.addWidget(QLabel(u'Уточните именную соотнесенность'))
        relation_list1 = QComboBox()
        relation_list1.addItem(u'любые')
        relation_list1.addItem(u'только соотнесенные')
        relation_list1.addItem(u'только несоотнесенные')
        vbox.addWidget(relation_list1)

        # dummy label
        vbox.addWidget(QLabel(u''))

        # раздел СУЩЕСТВИТЕЛЬНЫЕ
        vbox.addWidget(nouns)

        # учточняем часть
        vbox.addWidget(QLabel(u'Уточните часть'))
        part_list1 = QComboBox()
        part_list1.addItem(u'любые')
        part_list1.addItem(u'только из первой части')
        part_list1.addItem(u'только из второй части')
        vbox.addWidget(part_list1)

        # завершаем ЛИСТ 1
        groupBox.setLayout(vbox)

        ############
        # ЛИСТ 2
        ############

        groupBox2 = QGroupBox()
        vbox = QVBoxLayout()

        # выбор части речи
        verbs = QRadioButton(u'Глаголы')
        verbs.setFont(pos_font)
        nouns = QRadioButton(u'Существительные')
        nouns.setFont(pos_font)
        list_2_pos = QButtonGroup()
        list_2_pos.addButton(verbs, 1)
        list_2_pos.addButton(nouns, 2)
        label_list2 = QLabel(u'Лист 2\n')
        label_list2.setAlignment(Qt.AlignHCenter)
        label_list2.setFont(title_font)
        vbox.addWidget(label_list2)

        # раздел ГЛАГОЛЫ
        vbox.addWidget(verbs)

        # уточняем кол-во аргументов
        vbox.addWidget(QLabel(u'Уточните количество аргументов'))
        arguments_list1 = QComboBox()
        arguments_list1.addItem(u'любые')
        arguments_list1.addItem(u'только один аргумент')
        arguments_list1.addItem(u'только два аргумента')
        vbox.addWidget(arguments_list1)

        # учточняем возвратность
        vbox.addWidget(QLabel(u'Уточните возвратность'))
        reflexivity_list1 = QComboBox()
        reflexivity_list1.addItem(u'любые')
        reflexivity_list1.addItem(u'только возвратные')
        reflexivity_list1.addItem(u'только невозвратные')
        vbox.addWidget(reflexivity_list1)

        # учточняем инструментальность
        vbox.addWidget(QLabel(u'Уточните инструментальность'))
        instrumentality_list1 = QComboBox()
        instrumentality_list1.addItem(u'любые')
        instrumentality_list1.addItem(u'только инструментальные')
        instrumentality_list1.addItem(u'только неинструментальные')
        vbox.addWidget(instrumentality_list1)

        # учточняем именную соотнесенность
        vbox.addWidget(QLabel(u'Уточните именную соотнесенность'))
        relation_list1 = QComboBox()
        relation_list1.addItem(u'любые')
        relation_list1.addItem(u'только соотнесенные')
        relation_list1.addItem(u'только несоотнесенные')
        vbox.addWidget(relation_list1)

        # dummy label
        vbox.addWidget(QLabel(u''))

        # раздел СУЩЕСТВИТЕЛЬНЫЕ
        vbox.addWidget(nouns)

        # учточняем часть
        vbox.addWidget(QLabel(u'Уточните часть'))
        part_list1 = QComboBox()
        part_list1.addItem(u'любые')
        part_list1.addItem(u'только из первой части')
        part_list1.addItem(u'только из второй части')
        vbox.addWidget(part_list1)

        # завершаем ЛИСТ 2
        groupBox2.setLayout(vbox)


        def go():
            self.close()
            # print arguments_list1.currentIndex()
            # pass
            # print cb.checkState(), button_group.checkedId()





        # Add a button
        btn = QPushButton(u'Далее >')
        btn.setToolTip(u'Нажмите, чтобы составить листы')
        btn.clicked.connect(go)
        btn.resize(btn.sizeHint())

        main_layout.addWidget(groupBox, 1, 1)
        main_layout.addWidget(groupBox2, 1, 2)
        main_layout.addWidget(btn, 2, 2)

        # завершаем окно
        self.setLayout(main_layout)
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

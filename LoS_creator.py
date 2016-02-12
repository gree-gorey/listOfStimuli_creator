# -*- coding:utf-8 -*-

import sys
from PyQt4.Qt import *

__author__ = 'Gree-gorey'


class About(QWidget):
    def __init__(self, parent=None):
        super(About, self).__init__(parent)
        self.initUI()

    def go(self):
        self.parent().close()

    def initUI(self):
        main_layout = QGridLayout()
        message = QLabel(u'LoS creator version 0.1\n'
                         u'author: gree-gorey\n'
                         u'repository: https://github.com/gree-gorey/listOfStimuli_creator')

        # Add a button
        btn = QPushButton(u'OK')
        btn.clicked.connect(self.go)
        btn.resize(btn.sizeHint())

        main_layout.addWidget(message, 1, 1, 1, 3)
        main_layout.addWidget(btn, 2, 3, 1, 1)

        self.setLayout(main_layout)


class WaitWidget(QWidget):
    def __init__(self, parent=None):
        super(WaitWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        main_layout = QGridLayout()
        message = QLabel(u'\nПожалуйста, подождите.\n'
                         u'Листы создаются...')
        message.setAlignment(Qt.AlignHCenter)
        main_layout.addWidget(message, 1, 1)
        self.setLayout(main_layout)


class StatWidget(QWidget):
    def __init__(self, parent=None):
        super(StatWidget, self).__init__(parent)
        self.initUI()

    def go(self):
        wait = MainWindow(self.parent().parent().parent())
        wait.setCentralWidget(WaitWidget())
        wait.move(600, 350)
        wait.show()
        self.parent().close()

    def initUI(self):
        self.resize(100, 100)

        # создаем главный грид
        main_layout = QGridLayout()

        ############
        # ЛИСТ 1
        ############

        groupBox = QGroupBox()
        vbox = QVBoxLayout()

        # пишем предварительную оценку
        vbox.addWidget(QLabel(u'Параметры установлены.\n\n'
                              u'Для формирования листов с заданными параметрами\n'
                              u'Для Листа №1 - из 234 слов\n'
                              u'Для Листа №2 - из 243 слов\n'))

        # выбираем размер листа
        vbox.addWidget(QLabel(u'Выберите размер листа'))
        self.field = QLineEdit()
        vbox.addWidget(self.field)

        # уточняем кол-во аргументов
        vbox.addWidget(QLabel(u'Выберите статичтический тест'))
        arguments_list1 = QComboBox()
        arguments_list1.addItem(u'Student\'s t-test')
        arguments_list1.addItem(u'Welch\'s t-test')
        arguments_list1.addItem(u'Manna-Whitney U test')
        vbox.addWidget(arguments_list1)

        # завершаем ЛИСТ 1
        groupBox.setLayout(vbox)

        # Add a button
        btn = QPushButton(u'Создать листы')
        btn.setToolTip(u'Нажмите, чтобы начать генерирование')
        btn.clicked.connect(self.go)
        # btn.resize(btn.sizeHint())

        # добавляем виджеты в грид
        main_layout.addWidget(groupBox, 1, 1)
        # main_layout.setColumnStretch(0, 2)
        main_layout.addWidget(btn, 2, 1)

        # завершаем создание окна и высвечиваем
        self.setLayout(main_layout)


class TwoListsWidget(QWidget):
    def __init__(self, parent=None):
        super(TwoListsWidget, self).__init__(parent)
        self.initUI()

    def go(self):
        new = MainWindow(self.parent().parent())
        new.setCentralWidget(StatWidget())
        new.move(600, 100)
        new.show()
        self.parent().close()

        # next = NextWidget(self.parent())
        # self.close()
        # next.parent().setCentralWidget(next)

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

        # добавляем выбор для различающихся
        groupBox3 = QGroupBox()
        vbox = QVBoxLayout()

        # выбор части речи
        differ = QRadioButton(u'Листы не должны отличаться')
        no_differ = QRadioButton(u'Листы должны отличаться на параметр:')
        differ_radio = QButtonGroup()
        differ_radio.addButton(differ, 1)
        differ_radio.addButton(no_differ, 2)

        vbox.addWidget(differ)
        vbox.addWidget(no_differ)

        # выбор дифф парамтра
        diff_parameter = QComboBox()
        diff_parameter.addItem(u'-- не задан --')
        diff_parameter.addItem(u'частотность')
        diff_parameter.addItem(u'длина')
        vbox.addWidget(diff_parameter)

        # выбор высоких значений
        higher = QComboBox()
        higher.addItem(u'-- не задан --')
        higher.addItem(u'Высокие значения у Листа №1')
        higher.addItem(u'Высокие значения у Листа №2')
        vbox.addWidget(higher)

        groupBox3.setLayout(vbox)

        # Add a button
        btn = QPushButton(u'Далее >')
        btn.setToolTip(u'Нажмите, чтобы составить листы')
        btn.clicked.connect(self.go)
        # btn.resize(btn.sizeHint())

        # добавляем виджеты в грид
        main_layout.addWidget(groupBox, 1, 1, 1, 2)
        main_layout.addWidget(groupBox2, 1, 3, 1, 2)
        main_layout.addWidget(groupBox3, 2, 2, 1, 2)
        # main_layout.setColumnStretch(0, 2)
        main_layout.addWidget(btn, 3, 2, 1, 2)

        # завершаем создание окна и высвечиваем
        self.setLayout(main_layout)
        # self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def go(self):
        self.close()

    def initUI(self):
        # self.resize(500, 500)
        # self.center()
        self.move(300, 350)
        self.setWindowTitle(u'LoS creator 0.1')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class StartWidget(QWidget):
    def __init__(self, parent=None):
        super(StartWidget, self).__init__(parent)
        self.initUI()

    def start(self):
        new = MainWindow(self.parent())
        new.setCentralWidget(TwoListsWidget())
        new.move(600, 100)
        new.show()
        # TwoListsWindow(self)
        # print arguments_list1.currentIndex()
        # print cb.checkState(), button_group.checkedId()

    def exit_f(self):
        self.parent().close()

    def about(self):
        about = MainWindow(self.parent())
        about.setCentralWidget(About())
        about.move(600, 350)
        about.setWindowTitle(u'About')
        about.show()

    def initUI(self):
        self.center()
        self.setWindowTitle(u'LoS creator 0.1')

        # создаем главный грид
        main_layout = QGridLayout()

        # создаем поле кнопок
        groupBox = QGroupBox()
        hbox = QHBoxLayout()

        # Add a button
        start_btn = QPushButton(u'Создать ...')
        start_btn.setToolTip(u'Нажмите, чтобы начать создавать листы')
        start_btn.clicked.connect(self.start)
        # btn.resize(btn.sizeHint())


        # Add a button
        exit_btn = QPushButton(u'Выход')
        exit_btn.setToolTip(u'Нажмите, чтобы завершить работу')
        exit_btn.clicked.connect(self.exit_f)
        # btn.resize(btn.sizeHint())

        # Add a button
        about_btn = QPushButton(u'О программе ...')
        # about_btn.setToolTip(u'Нажмите, чтобы составить листы')
        about_btn.clicked.connect(self.about)
        # btn.resize(btn.sizeHint())

        # Приветствие
        gr = QLabel(u'Это альфа-версия программы LoS creator\n'
                    u'Возможны баги')

        hbox.addWidget(start_btn)
        hbox.addWidget(exit_btn)
        hbox.addWidget(about_btn)
        groupBox.setLayout(hbox)

        # добавляем виджеты в грид
        main_layout.addWidget(gr, 1, 1)
        main_layout.addWidget(groupBox, 2, 1)

        # завершаем создание окна и высвечиваем
        self.setLayout(main_layout)
        # self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


# def main():
#     app = QApplication(sys.argv)
#     # StartWindow()
#     TwoListsWindow()
#     # SetDiffer()
#     sys.exit(app.exec_())

if __name__ == '__main__':
    # main()

    app = QApplication(sys.argv)
    app.setApplicationName(u'LoS')

    main = MainWindow()
    main.setCentralWidget(StartWidget(main))
    main.show()

    sys.exit(app.exec_())

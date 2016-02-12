# -*- coding:utf-8 -*-

import sys
import pickle
from face import List, Parameters
# from structures import Store
from PyQt4.Qt import *

__author__ = 'Gree-gorey'


class Success(QWidget):
    def __init__(self, parent=None):
        super(Success, self).__init__(parent)
        self.initUI()

    def go(self):
        self.parent().close()

    def initUI(self):
        main_layout = QGridLayout()
        message = QLabel(u'Создание листов завершено.'
                         u'<br>Результаты сохранены в архив <b>results.zip</b>'
                         u'<br>в папке с программой')
        message.setOpenExternalLinks(True)

        # Add a button
        btn = QPushButton(u'OK')
        btn.clicked.connect(self.go)
        btn.resize(btn.sizeHint())

        main_layout.addWidget(message, 1, 1, 1, 3)
        main_layout.addWidget(btn, 2, 3, 1, 1)

        self.setLayout(main_layout)


class About(QWidget):
    def __init__(self, parent=None):
        super(About, self).__init__(parent)
        self.initUI()

    def go(self):
        self.parent().close()

    def initUI(self):
        main_layout = QGridLayout()
        message = QLabel(u'<b>LoS creator</b> version 0.1<br>'
                         u'Author: gree-gorey<br>'
                         u'<a href=\"https://github.com/gree-gorey/listOfStimuli_creator\">Repository</a>\n')
        message.setOpenExternalLinks(True)

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
        message = QLabel(u'<br>Пожалуйста, подождите.'
                         u'<br>Листы создаются...')
        message.setAlignment(Qt.AlignHCenter)
        main_layout.addWidget(message, 1, 1)
        self.setLayout(main_layout)


class StatWidget(QWidget):
    def __init__(self, parent=None):
        super(StatWidget, self).__init__(parent)
        self.initUI()

    def go(self):
        wait = MainWindow(self.parent().parent())
        wait.setCentralWidget(WaitWidget())
        wait.move(600, 350)
        wait.show()

        success = MainWindow(self.parent().parent())
        success.setCentralWidget(Success())
        success.move(600, 350)
        success.show()

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
        # add parameters
        print self.list_1_pos.checkedId()
        print self.arguments_list1.currentIndex()
        print self.reflexivity_list1.currentIndex()
        print self.instrumentality_list1.currentIndex()
        print self.relation_list1.currentIndex()
        print self.part_list1.currentIndex()

        # добавляем параметры первого листа
        self.parent().parent().parameters.first_list = List()
        self.parent().parent().parameters.first_list.pos = self.list_1_pos.checkedId()

        if self.parent().parent().parameters.first_list.pos == 1:
            self.parent().parent().parameters.first_list.arguments = self.arguments_list1.currentIndex()
            self.parent().parent().parameters.first_list.reflexivity = self.reflexivity_list1.currentIndex()
            self.parent().parent().parameters.first_list.instrumentality = self.instrumentality_list1.currentIndex()
            self.parent().parent().parameters.first_list.relation = self.relation_list1.currentIndex()
        elif self.parent().parent().parameters.first_list.pos == 2:
            self.parent().parent().parameters.first_list.part = self.part_list1.currentIndex()

        self.parent().parent().parameters.first_list.get_vector()

        print self.list_2_pos.checkedId()
        print self.arguments_list2.currentIndex()
        print self.reflexivity_list2.currentIndex()
        print self.instrumentality_list2.currentIndex()
        print self.relation_list2.currentIndex()
        print self.part_list2.currentIndex()

        # добавляем параметры второго листа
        self.parent().parent().parameters.second_list = List()
        self.parent().parent().parameters.second_list.pos = self.list_2_pos.checkedId()

        if self.parent().parent().parameters.second_list.pos == 1:
            self.parent().parent().parameters.second_list.arguments = self.arguments_list2.currentIndex()
            self.parent().parent().parameters.second_list.reflexivity = self.reflexivity_list2.currentIndex()
            self.parent().parent().parameters.second_list.instrumentality = self.instrumentality_list2.currentIndex()
            self.parent().parent().parameters.second_list.relation = self.relation_list2.currentIndex()
        elif self.parent().parent().parameters.second_list.pos == 2:
            self.parent().parent().parameters.second_list.part = self.part_list2.currentIndex()

        self.parent().parent().parameters.second_list.get_vector()

        self.parent().parent().store.first_list = \
            self.parent().parent().store.create_list_from_to_choose(self.parent().parent().parameters.first_list)
        self.parent().parent().store.second_list = \
            self.parent().parent().store.create_list_from_to_choose(self.parent().parent().parameters.second_list)

        new = MainWindow(self.parent().parent())
        new.setCentralWidget(StatWidget())
        new.move(600, 350)
        new.show()
        self.parent().close()

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
        self.list_1_pos = QButtonGroup()
        self.list_1_pos.addButton(verbs, 1)
        self.list_1_pos.addButton(nouns, 2)
        label_list1 = QLabel(u'Лист 1\n')
        label_list1.setAlignment(Qt.AlignHCenter)
        label_list1.setFont(title_font)
        vbox.addWidget(label_list1)

        # раздел ГЛАГОЛЫ
        vbox.addWidget(verbs)

        # уточняем кол-во аргументов
        vbox.addWidget(QLabel(u'Уточните количество аргументов'))
        self.arguments_list1 = QComboBox()
        self.arguments_list1.addItem(u'любые')
        self.arguments_list1.addItem(u'только один аргумент')
        self.arguments_list1.addItem(u'только два аргумента')
        vbox.addWidget(self.arguments_list1)

        # учточняем возвратность
        vbox.addWidget(QLabel(u'Уточните возвратность'))
        self.reflexivity_list1 = QComboBox()
        self.reflexivity_list1.addItem(u'любые')
        self.reflexivity_list1.addItem(u'только возвратные')
        self.reflexivity_list1.addItem(u'только невозвратные')
        vbox.addWidget(self.reflexivity_list1)

        # учточняем инструментальность
        vbox.addWidget(QLabel(u'Уточните инструментальность'))
        self.instrumentality_list1 = QComboBox()
        self.instrumentality_list1.addItem(u'любые')
        self.instrumentality_list1.addItem(u'только инструментальные')
        self.instrumentality_list1.addItem(u'только неинструментальные')
        vbox.addWidget(self.instrumentality_list1)

        # учточняем именную соотнесенность
        vbox.addWidget(QLabel(u'Уточните именную соотнесенность'))
        self.relation_list1 = QComboBox()
        self.relation_list1.addItem(u'любые')
        self.relation_list1.addItem(u'только соотнесенные')
        self.relation_list1.addItem(u'только несоотнесенные')
        vbox.addWidget(self.relation_list1)

        # dummy label
        vbox.addWidget(QLabel(u''))

        # раздел СУЩЕСТВИТЕЛЬНЫЕ
        vbox.addWidget(nouns)

        # учточняем часть
        vbox.addWidget(QLabel(u'Уточните часть'))
        self.part_list1 = QComboBox()
        self.part_list1.addItem(u'любые')
        self.part_list1.addItem(u'только из первой части')
        self.part_list1.addItem(u'только из второй части')
        vbox.addWidget(self.part_list1)

        # завершаем ЛИСТ 1
        groupBox.setLayout(vbox)

        ############
        # ЛИСТ 2
        ############

        groupBox2 = QGroupBox()
        vbox = QVBoxLayout()

        # выбор части речи
        verbs2 = QRadioButton(u'Глаголы')
        verbs2.setFont(pos_font)
        nouns2 = QRadioButton(u'Существительные')
        nouns2.setFont(pos_font)
        self.list_2_pos = QButtonGroup()
        self.list_2_pos.addButton(verbs2, 1)
        self.list_2_pos.addButton(nouns2, 2)
        label_list2 = QLabel(u'Лист 2\n')
        label_list2.setAlignment(Qt.AlignHCenter)
        label_list2.setFont(title_font)
        vbox.addWidget(label_list2)

        # раздел ГЛАГОЛЫ
        vbox.addWidget(verbs2)

        # уточняем кол-во аргументов
        vbox.addWidget(QLabel(u'Уточните количество аргументов'))
        self.arguments_list2 = QComboBox()
        self.arguments_list2.addItem(u'любые')
        self.arguments_list2.addItem(u'только один аргумент')
        self.arguments_list2.addItem(u'только два аргумента')
        vbox.addWidget(self.arguments_list2)

        # учточняем возвратность
        vbox.addWidget(QLabel(u'Уточните возвратность'))
        self.reflexivity_list2 = QComboBox()
        self.reflexivity_list2.addItem(u'любые')
        self.reflexivity_list2.addItem(u'только возвратные')
        self.reflexivity_list2.addItem(u'только невозвратные')
        vbox.addWidget(self.reflexivity_list2)

        # учточняем инструментальность
        vbox.addWidget(QLabel(u'Уточните инструментальность'))
        self.instrumentality_list2 = QComboBox()
        self.instrumentality_list2.addItem(u'любые')
        self.instrumentality_list2.addItem(u'только инструментальные')
        self.instrumentality_list2.addItem(u'только неинструментальные')
        vbox.addWidget(self.instrumentality_list2)

        # учточняем именную соотнесенность
        vbox.addWidget(QLabel(u'Уточните именную соотнесенность'))
        self.relation_list2 = QComboBox()
        self.relation_list2.addItem(u'любые')
        self.relation_list2.addItem(u'только соотнесенные')
        self.relation_list2.addItem(u'только несоотнесенные')
        vbox.addWidget(self.relation_list2)

        # dummy label
        vbox.addWidget(QLabel(u''))

        # раздел СУЩЕСТВИТЕЛЬНЫЕ
        vbox.addWidget(nouns2)

        # учточняем часть
        vbox.addWidget(QLabel(u'Уточните часть'))
        self.part_list2 = QComboBox()
        self.part_list2.addItem(u'любые')
        self.part_list2.addItem(u'только из первой части')
        self.part_list2.addItem(u'только из второй части')
        vbox.addWidget(self.part_list2)

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
        self.parent().parameters = Parameters()
        with open(u'store.p', u'r') as f:
            self.parent().store = pickle.load(f)

        new = MainWindow(self.parent())
        new.setCentralWidget(TwoListsWidget())
        new.move(600, 100)
        new.show()

    def exit_f(self):
        self.parent().close()

    def about(self):
        about = MainWindow(self.parent())
        about.setCentralWidget(About())
        about.move(600, 350)
        about.setWindowTitle(u'About')
        about.show()

    def initUI(self):
        # создаем главный грид
        main_layout = QGridLayout()

        # создаем поле кнопок
        groupBox = QGroupBox()
        hbox = QHBoxLayout()

        # Add a button
        start_btn = QPushButton(u'Создать ...')
        start_btn.setToolTip(u'Нажмите, чтобы начать создавать листы')
        start_btn.clicked.connect(self.start)

        # Add a button
        exit_btn = QPushButton(u'Выход')
        exit_btn.setToolTip(u'Нажмите, чтобы завершить работу')
        exit_btn.clicked.connect(self.exit_f)

        # Add a button
        about_btn = QPushButton(u'О программе ...')
        about_btn.clicked.connect(self.about)

        # Приветствие
        gr = QLabel(u'Это альфа-версия программы <b>LoS creator</b><br>'
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

    def connect_creator(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName(u'LoS')

    main = MainWindow()
    main.setCentralWidget(StartWidget(main))
    main.show()

    sys.exit(app.exec_())

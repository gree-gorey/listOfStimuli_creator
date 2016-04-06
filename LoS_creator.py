# -*- coding:utf-8 -*-

import time
import sys
import pickle
from structures import List, Parameters
from PyQt4.Qt import *

__author__ = 'gree-gorey'


class Success(QWidget):
    def __init__(self, parent=None):
        super(Success, self).__init__(parent)
        self.time = 0
        self.initUI()

    def go(self):
        self.parent().close()

    def initUI(self):
        main_layout = QGridLayout()
        message = QLabel(u'Создание листов завершено.<br>'
                         u'<br>Результаты сохранены в архив <b>results.zip</b>'
                         u'<br>в папке с программой<br>'
                         u'<br>Время работы: ' + str(round(self.parent().time, 2)) + u' с')
        message.setOpenExternalLinks(True)

        # Add a button
        btn = QPushButton(u'OK')
        btn.clicked.connect(self.go)
        btn.resize(btn.sizeHint())

        main_layout.addWidget(message, 1, 1, 1, 3)
        main_layout.addWidget(btn, 2, 3, 1, 1)

        self.setLayout(main_layout)


class Fail(QWidget):
    def __init__(self, parent=None):
        super(Fail, self).__init__(parent)
        self.time = 0
        self.initUI()

    def go(self):
        self.parent().close()

    def initUI(self):
        main_layout = QGridLayout()
        message = QLabel(u'Лимит времени работы программы превышен.<br>'
                         u'Невозможно создать листы с заданными параметрами.<br>'
                         u'<br>Попробуйте изменить параметры и попробовать снова.')
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
        message = QLabel(u'<b>LoS creator</b> version 0.2<br>'
                         u'Author: gree-gorey<br>'
                         u'<a href=\"https://github.com/gree-gorey/losc\">Go to repository</a>\n')
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

    def go(self):
        self.parent().parent().store.setup_parameters(self.parent().parent().parameters)

        # добавим отсчет времени
        self.parent().parent().store.time_begin = time.time()

        # собственно генерация листов
        self.parent().parent().store.generate()

        if self.parent().parent().store.success:

            # подсчет окончательной статы
            self.parent().parent().store.final_statistics()

            # для печати результатов
            self.parent().parent().store.print_results()

            # создаем файлы и пакуем в архив
            self.parent().parent().store.create_zip()


class StatWidget(QWidget):
    def __init__(self, parent=None):
        super(StatWidget, self).__init__(parent)
        self.initUI()

    def go(self):
        # print self.length.text()
        # print self.statistics.currentIndex()

        self.parent().parent().parameters.statistics = self.statistics.currentIndex()
        self.parent().parent().parameters.freq = self.freq.currentIndex()
        self.parent().parent().parameters.length = int(self.length.text())

        self.parent().close()

        t1 = time.time()

        wait = MainWindow(self.parent().parent())
        wait_widget = WaitWidget(wait)
        wait.setCentralWidget(wait_widget)
        wait.move(600, 350)
        wait.show()

        wait_widget.go()
        wait.close()

        # считаем время
        t2 = time.time()
        self.time = t2 - t1

        if self.parent().parent().store.success:

            success = MainWindow(self.parent().parent())
            widget_success = Success(self)
            success.setCentralWidget(widget_success)
            success.move(600, 350)
            success.show()

        else:

            fail = MainWindow(self.parent().parent())
            widget_fail = Fail(self)
            fail.setCentralWidget(widget_fail)
            fail.move(600, 350)
            fail.show()


    def initUI(self):
        # создаем главный грид
        main_layout = QGridLayout()

        groupBox = QGroupBox()
        vbox = QVBoxLayout()

        # print self.parent().parent()

        # пишем предварительную оценку
        vbox.addWidget(QLabel(u'Параметры установлены.<br>'
                              u'<br>Для формирования листов с заданными параметрами осталось:'
                              u'<br>Для Листа №1 - ' + str(len(self.parent().parent().store.first_list)) + u' слов'
                              u'<br>Для Листа №2 - ' + str(len(self.parent().parent().store.second_list)) + u' слов<br>'))

        # выбираем размер листа
        vbox.addWidget(QLabel(u'Выберите размер листа'))
        self.length = QLineEdit()
        vbox.addWidget(self.length)

        # уточняем кол-во аргументов
        vbox.addWidget(QLabel(u'Выберите статистический тест'))
        self.statistics = QComboBox()
        self.statistics.addItem(u'-- не выбрано --')
        self.statistics.addItem(u'Student\'s t-test')
        self.statistics.addItem(u'Welch\'s t-test')
        self.statistics.addItem(u'Manna-Whitney U test')
        vbox.addWidget(self.statistics)

        # уточняем частотность
        vbox.addWidget(QLabel(u'Преобразование частотности слов'))
        self.freq = QComboBox()
        self.freq.addItem(u'не требуется (по умолчанию)')
        self.freq.addItem(u'использовать логарифмическое преобразование')
        vbox.addWidget(self.freq)

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
        # print self.list_1_pos.checkedId()
        # print self.arguments_list1.currentIndex()
        # print self.reflexivity_list1.currentIndex()
        # print self.instrumentality_list1.currentIndex()
        # print self.relation_list1.currentIndex()
        # print self.part_list1.currentIndex()

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

        # print self.list_2_pos.checkedId()
        # print self.arguments_list2.currentIndex()
        # print self.reflexivity_list2.currentIndex()
        # print self.instrumentality_list2.currentIndex()
        # print self.relation_list2.currentIndex()
        # print self.part_list2.currentIndex()

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

        # создаем в сторе предварительные листы
        self.parent().parent().store.first_list = \
            self.parent().parent().store.create_list_from_to_choose(self.parent().parent().parameters.first_list)
        self.parent().parent().store.second_list = \
            self.parent().parent().store.create_list_from_to_choose(self.parent().parent().parameters.second_list)

        self.parent().parent().store.normalize()

        # проверяем, должны ли различаться
        if self.differ_radio.checkedId() == 1:
            self.parent().parent().store.differ = self.diff_parameter.currentIndex()
            self.parent().parent().store.which_higher = self.higher.currentIndex()
            self.parent().parent().store.differentiate()

        # создаем вектор одинаковых
        self.parent().parent().parameters.get_same(self.parent().parent().store)

        # print self.differ_radio.checkedId()
        # print self.diff_parameter.currentIndex()
        # print self.higher.currentIndex()
        # print self.parent().parent().parameters.same

        self.parent().parent().store.split()

        stat = MainWindow(self.parent().parent())
        stat.setCentralWidget(StatWidget(stat))
        stat.move(600, 350)
        stat.show()
        self.parent().close()

        # print self.parent().parent()
        # print self.parent().parent()

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
        no_differ = QRadioButton(u'Листы не должны отличаться')
        differ = QRadioButton(u'Листы должны отличаться на параметр:')
        self.differ_radio = QButtonGroup()
        self.differ_radio.addButton(no_differ, 0)
        self.differ_radio.addButton(differ, 1)

        vbox.addWidget(no_differ)
        vbox.addWidget(differ)

        # выбор дифф парамтра
        self.diff_parameter = QComboBox()
        self.diff_parameter.addItem(u'-- не задан --')
        self.diff_parameter.addItem(u'Устойчивость номинации')
        self.diff_parameter.addItem(u'Субъективная сложность')
        self.diff_parameter.addItem(u'Знакомство с объектом')
        self.diff_parameter.addItem(u'Возраст усвоения')
        self.diff_parameter.addItem(u'Представимость')
        self.diff_parameter.addItem(u'Схожесть образа с рисунком')
        self.diff_parameter.addItem(u'Частотность')
        self.diff_parameter.addItem(u'Длина в слогах')
        self.diff_parameter.addItem(u'Длина в фонемах')
        vbox.addWidget(self.diff_parameter)

        # выбор высоких значений
        self.higher = QComboBox()
        self.higher.addItem(u'-- не задан --')
        self.higher.addItem(u'Высокие значения у Листа №1')
        self.higher.addItem(u'Высокие значения у Листа №2')
        vbox.addWidget(self.higher)

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

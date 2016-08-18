# -*- coding:utf-8 -*-

import time
import json
import pickle
import codecs
from parameters import Parameters
from store import Store

__author__ = 'gree-gorey'

store = Store()


def set_parameters():
    global store

    # загружаем базу данных в переменную
    with open(u'data/store.p', u'r') as f:
        store = pickle.load(f)

    store.parameters = Parameters()

    with codecs.open(u'lists_parameters.json', u'r', u'utf-8') as f:
        parameters_from_client = json.load(f)

    # создаем в сторе предварительные листы
    store.first_list = store.create_list_from_to_choose(parameters_from_client['list1'])
    store.second_list = store.create_list_from_to_choose(parameters_from_client['list2'])

    # создаем хэши-счетчики равновесия для тех параметров, которые выбрал пользователь
    store.first_list_equality_counter = store.create_equality_counter(parameters_from_client['list1'])
    store.second_list_equality_counter = store.create_equality_counter(parameters_from_client['list2'])

    # нормализуем все к шкале от 0 до 1
    store.normalize()
    # print store.first_list[0].normalized_features

    # проверяем, должны ли различаться и если да, то различаем
    if parameters_from_client['differ_feature'] != 'question':
        store.key_for_differ_feature = parameters_from_client['differ_feature']
        store.which_higher = parameters_from_client['which_is_higher']
        store.differentiate()
    # print len(store.first_list)
    # print store.second_list[0].name

    # устанавливаем отличающийся параметр
    store.parameters.differ = parameters_from_client['differ_feature']

    # устанавливаем bonferroni
    store.parameters.bonferroni = parameters_from_client['bonferroni']

    # создаем вектор одинаковых
    store.parameters.same = parameters_from_client['same_features']

    # если листы оказались одинаковыми, нужно рандомно разделить их
    store.split()


def create():

    with codecs.open(u'stat_parameters.json', u'r', u'utf-8') as f:
        parameters_from_client = json.load(f)

    store.parameters.length = int(parameters_from_client['length'])
    store.parameters.statistics = parameters_from_client['statistics']
    store.parameters.frequency = parameters_from_client['frequency']
    # print parameters.length

    # устанавливаем параметры
    store.setup_parameters()

    # добавим отсчет времени
    store.time_begin = time.time()

    # собственно генерация листов
    store.generate()

    print store.first_list_equality_counter

    if store.success:
        # создаем файлы и пакуем в архив
        store.create_zip()


if __name__ == '__main__':
    set_parameters()

    create()


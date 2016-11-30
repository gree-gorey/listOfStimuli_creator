# -*- coding:utf-8 -*-

import os
import time
import json
import flask
# import pickle
import codecs
from random import shuffle
import webbrowser
import threading
from store import Store
from parameters import Parameters

__author__ = 'gree-gorey'


path = os.path.dirname(os.path.realpath(__file__))


def get_version():
    with open(path + "/version.py", "rt") as f:
        return f.readline().split("=")[1].strip(' "\n')


version = get_version()


# Initialize the Flask application
app = flask.Flask(__name__)


store = Store()


@app.route('/')
def index():
    return flask.render_template('index.html', version=version)


@app.route('/parameters')
def parameters():
    return flask.render_template('parameters.html', version=version)


@app.route('/statistics')
def statistics():
    return flask.render_template('statistics.html',
                                 version=version,
                                 max=store.get_max_list_length())


@app.route('/_read_data_file', methods=['GET', 'POST'])
def read_data_file():
    global store

    store.__init__()

    result = dict()

    # считываем табличку с данными
    try:
        store.read_data(path)
        result['success'] = 'success'
    except ValueError as error:
        result['success'] = 'failure'
        result['error'] = str(error)
        # print error

    return flask.jsonify(result=result)


@app.route('/_get_features', methods=['GET', 'POST'])
def get_features():

    result = {
        'categorical_features_list': store.categorical_features_list,
        'categorical_features': store.categorical_features,
        'numeric_features': store.numeric_features_range
    }

    return flask.jsonify(result=result)


@app.route('/_get_features_for_statistics_page', methods=['GET', 'POST'])
def get_features_for_statistics_page():
    # print store.lists
    result = {
        'lens': [
            len(store.lists['list_1']),
            len(store.lists['list_2']) if 'list_2' in store.lists else None,
            len(store.lists['list_3']) if 'list_3' in store.lists else None
        ],
        'n': store.lists_number
    }

    # print result

    return flask.jsonify(result=result)


@app.route('/_set_parameters', methods=['GET', 'POST'])
def set_parameters():
    store.parameters = Parameters()

    parameters_from_client = flask.request.json
    # print parameters_from_client['list1']['features']['reflexivity']

    # print parameters_from_client

    with codecs.open(u'lists_parameters.json', u'w', u'utf-8') as w:
        json.dump(parameters_from_client, w, ensure_ascii=False, indent=2)

    if int(parameters_from_client['n']) == 1:
        # указываем количество листов
        store.lists_number = 1
        # просто фильтруем только те слова, которые в границах заданных пользователем
        store.lists['list_1'] = store.create_list_from_to_choose(parameters_from_client['list1'])

        # создаем хэши-счетчики равновесия для тех параметров, которые выбрал пользователь
        store.list_equality_counter['list_1'] = store.create_equality_counter(parameters_from_client['list1'])

        # перемешиваем лист
        shuffle(store.lists['list_1'])

        if len(store.lists['list_1']) == 0:
            result = 'failure'
            return flask.jsonify(result=result)
        else:
            result = 'success'
            return flask.jsonify(result=result)

    elif int(parameters_from_client['n']) == 2:
        # создаем в сторе предварительные листы
        store.lists['list_1'] = store.create_list_from_to_choose(parameters_from_client['list1'])
        store.lists['list_2'] = store.create_list_from_to_choose(parameters_from_client['list2'])

        if len(store.lists['list_1']) == 0 or len(store.lists['list_2']) == 0:
            result = 'failure'
            return flask.jsonify(result=result)

        # создаем хэши-счетчики равновесия для тех параметров, которые выбрал пользователь
        store.list_equality_counter['list_1'] = store.create_equality_counter(parameters_from_client['list1'])
        store.list_equality_counter['list_2'] = store.create_equality_counter(parameters_from_client['list2'])

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

        result = 'success'

        return flask.jsonify(result=result)


@app.route('/_create', methods=['GET', 'POST'])
def create():
    result = {'feedback': 'failure'}

    parameters_from_client = flask.request.json

    with codecs.open(u'stat_parameters.json', u'w', u'utf-8') as w:
        json.dump(parameters_from_client, w, ensure_ascii=False, indent=2)

    # time.sleep(2)

    if store.lists_number == 1:
        store.parameters.length = int(parameters_from_client['length'])

        # собственно генерация листа
        store.generate_one()

        if store.success:
            result['feedback'] = 'success'

            # создаем файлы и пакуем в архив
            store.create_zip()

        return flask.jsonify(result=result)

    else:

        store.parameters.length = int(parameters_from_client['length'])
        store.parameters.statistics = parameters_from_client['statistics']

        # устанавливаем параметры
        store.setup_parameters()

        # добавим отсчет времени
        store.time_begin = time.time()

        # собственно генерация листов
        store.generate()

        # print store.first_list_equality_counter

        if store.success:
            result['feedback'] = 'success'

            # создаем файлы и пакуем в архив
            store.create_zip()

        return flask.jsonify(result=result)


if __name__ == '__main__':
    url = 'http://127.0.0.1:5000'

    threading.Timer(1.25, lambda: webbrowser.open(url)).start()

    app.run(
        # host="0.0.0.0",
        # port=int("80"),
        debug=True,
        threaded=True
    )


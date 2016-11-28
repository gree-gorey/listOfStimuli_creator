# -*- coding:utf-8 -*-

import os
# import math
import time
import random
import codecs
import zipfile
from os.path import basename
from scipy import stats
import numpy as np
from parameters import Parameters
from word import Word

__author__ = 'gree-gorey'


class Store:
    def __init__(self):
        self.words = list()
        self.lists_number = 2
        self.min = dict()
        self.max = dict()
        self.lists = dict()  # словарь, ключ -- 'list_1', значение -- массив с исходными векторами (=словами)
        self.list_outputs = dict()  # словарь, ключ -- 'list_1', значение -- массив с отобранными векторами (=словами)
        self.minimum = None
        self.length = 0
        self.number_of_same = 0
        self.allow = True
        self.same = list()
        self.statistics = None
        self.key_for_differ_feature = ''
        self.which_higher = None
        self.p_values = list()
        self.time_begin = None
        self.success = True
        self.list_equality_counter = dict()  # словарь, ключ -- 'list_1', значение -- хэш-счетчик равновесия для данного листа
        self.should_append = dict()  # словарь, ключ -- 'list_1', значение -- хэш
        self.numeric_features = list()
        self.numeric_features_range = dict()  # словарь, ключ -- имя колич переменной, значение -- словарь из min и max
        self.categorical_features = dict()
        self.categorical_features_list = list()
        self.distance_for_the_list = dict()
        self.word_to_pop_from_the_list = dict()
        self.list_mean = dict()
        self.len_of_numeric = 0
        self.len_of_categorical = 0
        self.parameters = Parameters()

    def read_dummy_data_and_setup(self):
        path = os.path.dirname(os.path.realpath(__file__))

        self.read_data(path, '/data/test.tsv')

        self.lists['list_1'] = list()
        self.lists['list_2'] = list()
        self.list_outputs['list_1'] = list()
        self.list_outputs['list_2'] = list()

        self.list_equality_counter['list_1'] = {}
        self.list_equality_counter['list_2'] = {}

        for word in self.words[:6:]:
            self.lists['list_1'].append(word)

        for word in self.words[6::]:
            self.lists['list_2'].append(word)

    def get_max_list_length(self):
        return min([len(self.lists[list_name]) for list_name in self.lists])

    def read_data(self, path, file_name='/data/data.tsv'):
        with codecs.open(path + file_name, 'r', 'utf-8') as f:
            lines = f.readlines()

        features_list = lines[0].rstrip().split('\t')[1::]

        types = lines[1].rstrip().split('\t')[1::]

        features_dict = dict(zip(features_list, types))

        for feature in features_list:
            if features_dict[feature] == 'categorical':
                self.categorical_features[feature] = list()
                self.categorical_features_list.append(feature)
            else:
                self.numeric_features.append(feature)

        self.len_of_numeric = len(self.numeric_features)
        self.len_of_categorical = len(self.categorical_features)

        first_word_line = lines[2]
        columns = first_word_line.rstrip().split('\t')
        for feature, value in zip(features_list, columns[1::]):
            if features_dict[feature] == 'int':
                self.numeric_features_range[feature] = {
                    'min': float(value),
                    'max': float(value)
                }
            elif features_dict[feature] == 'float':
                self.numeric_features_range[feature] = {
                    'min': float(value),
                    'max': float(value)
                }

        for line in lines[2::]:
            self.words.append(Word())

            columns = line.rstrip().split('\t')
            self.words[-1].name = columns[0]

            for feature, value in zip(features_list, columns[1::]):
                if features_dict[feature] == 'int':
                    self.words[-1].features[feature] = float(value)
                    if self.words[-1].features[feature] < self.numeric_features_range[feature]['min']:
                        self.numeric_features_range[feature]['min'] = self.words[-1].features[feature]
                    if self.words[-1].features[feature] > self.numeric_features_range[feature]['max']:
                        self.numeric_features_range[feature]['max'] = self.words[-1].features[feature]
                elif features_dict[feature] == 'float':
                    self.words[-1].features[feature] = float(value)
                    if self.words[-1].features[feature] < self.numeric_features_range[feature]['min']:
                        self.numeric_features_range[feature]['min'] = self.words[-1].features[feature]
                    if self.words[-1].features[feature] > self.numeric_features_range[feature]['max']:
                        self.numeric_features_range[feature]['max'] = self.words[-1].features[feature]
                else:
                    if value != 'NR':
                        self.words[-1].features[feature] = value
                        if value not in self.categorical_features[feature]:
                            self.categorical_features[feature].append(value)
                    else:
                        self.words[-1].features[feature] = None

        for feature in self.categorical_features:
            self.categorical_features[feature] = sorted(self.categorical_features[feature])

    def reset_counters(self):
        for feature, parameters in self.list_equality_counter['list_1'].iteritems():
            for parameter, value in parameters.iteritems():
                parameters[parameter] = 0
        for feature, parameters in self.list_equality_counter['list_2'].iteritems():
            for parameter, value in parameters.iteritems():
                parameters[parameter] = 0

        # print '\n#####\nCounters were reset'
        # print self.first_list_equality_counter

    def generate_one(self):
        self.list_outputs['list_1'] = list()
        while len(self.list_outputs['list_1']) < self.parameters.length:
            # print 'foo'
            self.check_words_for_allowance('list_1')
            # break
            for i, word in enumerate(self.lists['list_1']):
                if word.allowed:
                    # print 'foo'
                    self.list_outputs['list_1'].append(word)
                    del self.lists['list_1'][i]
                    if len(self.list_outputs['list_1']) == self.parameters.length:
                        break

    def generate(self):
        for n in range(1, self.lists_number+1):
            self.list_outputs['list_{}'.format(n)] = list()

        # print 'x'

        while self.sharp():
            # print self.length
            # print 'foo'
            # print self.allow, self.less()

            # Сбрасываем счетчики для 50/50
            self.reset_counters()

            # считаем сколько времени прошло и убиваем
            time_current = time.time()
            if time_current - self.time_begin > 30:
                self.success = False
                break

            # сбрасывем листы и аутпут, добавляем в аутпут по одному случайному слову
            self.add_first()
            # print 'reset'

            self.allow = True

            # print self.same

            # пока длина аутпута не превышает требуемой
            while self.allow and self.less():
                #
                # print len(self.list_outputs['list_1'])
                # print self.same
                # print self.list_outputs['list_1'][0].normalized_features
                # print [word.normalized_features['H'] for word in self.list_outputs['list_1']]
                # print [word.normalized_features['H'] for word in self.list_outputs['list_2']]

                # print 'egg'
                time_current = time.time()
                if time_current - self.time_begin > 20:
                    self.success = False
                    break

                # начинаем добавлять слова с ближайшими векторами
                self.add_closest()
                # как только размер листа больше 5, начинаем проверять
                if len(self.list_outputs['list_1']) > 5:
                    # print 'foo'
                    self.test_and_fix()

            # break

    def create_equality_counter(self, list_parameters_from_client):
        # создаем пустой счетчик
        equality_counter = dict()

        # обходим список категориальных
        for feature in self.categorical_features:
            # если у кого-то значение 50/50
            if list_parameters_from_client[feature]['value'] == 'half':
                # print feature

                # создаем для данного параметра ячейку с двумя значениями, равными нулю
                equality_counter[feature] = {
                    self.categorical_features[feature][0]: 0,
                    self.categorical_features[feature][1]: 0
                }

        return equality_counter

    def find_min_max(self, word_list):
        for word in word_list:
            for key in word.features:
                if type(word.features[key]) in [float, int]:
                    if word.features[key] < self.min[key]:
                        self.min[key] = word.features[key]
                    if word.features[key] > self.max[key]:
                        self.max[key] = word.features[key]

    def normalize(self):
        # копируем фичи первого слова, чтобы было с чего начать сравнивать
        self.min = self.lists['list_1'][0].features.copy()
        self.max = self.lists['list_1'][0].features.copy()

        # находим минимум и максимум для всех фич в листах
        self.find_min_max(self.lists['list_1'])
        self.find_min_max(self.lists['list_2'])

        # print self.max, self.min

        # нормализуем
        for list_name in self.lists:
            for word in self.lists[list_name]:
                word.normalized_features = word.features.copy()
                for key in word.features:
                    if type(word.features[key]) in [float, int]:
                        word.normalized_features[key] = (word.features[key] - self.min[key]) / (self.max[key] - self.min[key])

    def create_zip(self):
        path = os.path.dirname(os.path.realpath(__file__))

        # print self.list_outputs

        for list_key in self.list_outputs:
            if self.list_outputs[list_key]:
                # print self.list_outputs[list_key]
                list_head = 'name\t' + '\t'.join(self.list_outputs[list_key][0].features.keys()) + '\r\n'
                with codecs.open(path + '/static/output/{}.tsv'.format(list_key), 'w', 'utf-8') as w:
                    w.write(list_head)
                    for word in self.list_outputs[list_key]:
                        for key in word.features:
                            if word.features[key] is None:
                                word.features[key] = 'NR'

                        w.write(word.name + u'\t' + u'\t'.join([str(word.features[key]) for key in word.features]) + u'\r\n')

        table = self.create_final_table()

        with codecs.open(path + '/static/output/statistics.tsv', u'w', u'utf-8') as w:
            w.write(table)

        z = zipfile.ZipFile(path + '/static/output/results.zip', u'w')

        for list_key in self.list_outputs:
            z.write(path + '/static/output/{}.tsv'.format(list_key), basename(path + '/static/output/{}.tsv'.format(list_key)))
        z.write(path + '/static/output/statistics.tsv', basename(path + '/static/output/statistics.tsv'))

        for list_key in self.list_outputs:
            os.remove(path + '/static/output/{}.tsv'.format(list_key))
        os.remove(path + '/static/output/statistics.tsv')

    def create_table_per_list(self, list_output, list_name):
        table_per_list = ''

        list_features = dict()

        for feature in self.numeric_features:
            list_features[feature] = [word.features[feature] for word in list_output]

        means = [str(np.mean(list_features[feature])) for feature in self.numeric_features]

        list1_mean = list_name + '\tmean\t' + '\t'.join(means) + '\t' + '\t'.join(['NR'] * self.len_of_categorical) + '\r\n'
        table_per_list += list1_mean

        # print self.numeric_features
        # print list_features[u'PercNA']
        # print list_features[u'H']

        mins = [str(np.min(list_features[feature])) for feature in self.numeric_features]

        list1_min = '\tmin\t' + '\t'.join(mins) + '\t' + '\t'.join(['NR'] * self.len_of_categorical) + '\r\n'
        table_per_list += list1_min

        maxes = [str(np.max(list_features[feature])) for feature in self.numeric_features]

        list1_max = '\tmax\t' + '\t'.join(maxes) + '\t' + '\t'.join(['NR'] * self.len_of_categorical) + '\r\n'
        table_per_list += list1_max

        sd = [str(np.std(list_features[feature], ddof=1)) for feature in self.numeric_features]

        list1_sd = '\tSD\t' + '\t'.join(sd) + '\t' + '\t'.join(['NR'] * self.len_of_categorical) + '\r\n'
        table_per_list += list1_sd

        ratios = list()

        for feature in self.categorical_features:
            # print '<< {} >>'.format(self.categorical_features[feature][0])
            # print self.categorical_features[feature]

            ratio = {
                self.categorical_features[feature][0]: 0,
                self.categorical_features[feature][1]: 0
            }

            for word in list_output:
                if word.features[feature] in self.categorical_features[feature]:
                    ratio[word.features[feature]] += 1
                else:
                    ratio = None
                    break

            ratios.append(ratio)

        ratio_string = ''
        for ratio in ratios:
            ratio_string += '\t'
            if ratio is None:
                ratio_string += 'NR'
            else:
                for key in ratio:
                    string = key + ': ' + str(ratio[key]) + '; '
                    ratio_string += string

        # print ratio_string

        list1_ratio = '\tratio\t' + '\t'.join(['NR'] * self.len_of_numeric) + ratio_string + '\r\n'
        table_per_list += list1_ratio

        shapiro = [str(stats.shapiro(list_features[feature])[1]) for feature in self.numeric_features]

        list1_shapiro = '\tShapiro, p-value\t' + '\t'.join(shapiro) + '\t' + '\t'.join(['NR'] * self.len_of_categorical) + '\r\n'
        table_per_list += list1_shapiro

        return table_per_list

    def return_test_results(self, arr1, arr2):
        test_name = ''
        p_value = 0
        t_value = 0
        levene = stats.levene(arr1, arr2)[1]
        if self.statistics == 'auto':
            # проверяем Левеном на равенство дисперсий. Если равны
            if levene > 0.05:
                # Шапир на нормальность выборок. Если нормальные
                if stats.shapiro(arr1)[1] > 0.05 and stats.shapiro(arr2)[1] > 0.05:
                    # p = Student
                    test_name = 'Student'
                    result = stats.ttest_ind(arr1, arr2)
                    t_value = result[0]
                    p_value = result[1]
                else:
                    # p = Mann
                    test_name = 'Mann'
                    if equal(arr1, arr2):
                        t_value = None
                        p_value = 1
                    else:
                        result = stats.mannwhitneyu(arr1, arr2, alternative='two-sided')
                        t_value = result[0]
                        p_value = result[1]
            else:
                test_name = 'Welch'
                result = stats.ttest_ind(arr1, arr2, False)
                t_value = result[0]
                p_value = result[1]

        elif self.statistics == 'student':
            test_name = 'Student'
            result = stats.ttest_ind(arr1, arr2)
            t_value = result[0]
            p_value = result[1]
        elif self.statistics == 'welch':
            test_name = 'Welch'
            result = stats.ttest_ind(arr1, arr2, False)
            t_value = result[0]
            p_value = result[1]
        elif self.statistics == 'mann':
            test_name = 'Mann'
            if equal(arr1, arr2):
                t_value = None
                p_value = 1
            else:
                result = stats.mannwhitneyu(arr1, arr2, alternative='two-sided')
                t_value = result[0]
                p_value = result[1]

        df = len(arr1) + len(arr2) - 2

        return [test_name, t_value, p_value, df, levene]

    def create_stat_table(self):
        stat_table = ''

        first_list_features = dict()
        for feature in self.numeric_features:
            first_list_features[feature] = [word.features[feature] for word in self.list_outputs['list_1']]

        second_list_features = dict()
        for feature in self.numeric_features:
            second_list_features[feature] = [word.features[feature] for word in self.list_outputs['list_2']]

        list_of_test_results = [self.return_test_results(first_list_features[feature], second_list_features[feature]) for feature in self.numeric_features]

        test_name = 'statistics\ttest name\t' + '\t'.join([result_list[0] for result_list in list_of_test_results])\
                    + '\t' + '\t'.join(['NR'] * self.len_of_categorical) + '\r\n'
        stat_table += test_name

        t_value = '\tstatistics value\t' + '\t'.join([str(result_list[1]) for result_list in list_of_test_results])\
                  + '\t' + '\t'.join(['NR'] * self.len_of_categorical) + '\r\n'
        stat_table += t_value

        p_value = '\tp-value\t' + '\t'.join([str(result_list[2]) for result_list in list_of_test_results]) \
                  + '\t' + '\t'.join(['NR'] * self.len_of_categorical) + '\r\n'
        stat_table += p_value

        df = '\tDF\t' + '\t'.join([str(result_list[3]) for result_list in list_of_test_results]) \
             + '\t' + '\t'.join(['NR'] * self.len_of_categorical) + '\r\n'
        stat_table += df

        levene = '\tLevene, p-value\t' + '\t'.join([str(result_list[4]) for result_list in list_of_test_results]) \
                 + '\t' + '\t'.join(['NR'] * self.len_of_categorical) + '\r\n'
        stat_table += levene

        return stat_table

    def create_final_table(self):
        table = ''
        header = '\t\t' + '\t'.join(self.numeric_features) + '\t' + '\t'.join(self.categorical_features) + '\r\n'
        table += header

        for n in xrange(1, self.lists_number+1):
            table += self.create_table_per_list(self.list_outputs['list_{}'.format(n)], 'list {}'.format(n))
            table += '\r\n'

        if self.lists_number > 1:
            table += self.create_stat_table()

        return table

    def set_should_append(self, list_equality_counter, list_name_key):
        self.should_append[list_name_key] = dict()

        # print list_equality_counter

        for feature in list_equality_counter:
            keys = list_equality_counter[feature].keys()

            # print keys

            if list_equality_counter[feature][keys[0]] < list_equality_counter[feature][keys[1]]:
                self.should_append[list_name_key][feature] = keys[0]
            elif list_equality_counter[feature][keys[0]] > list_equality_counter[feature][keys[1]]:
                self.should_append[list_name_key][feature] = keys[1]

    def check_words_for_allowance(self, list_name_key):
        # оставляем только неравные параметры, остальные неважны в этой итерации
        self.set_should_append(self.list_equality_counter[list_name_key], list_name_key)

        # print self.should_append

        if self.should_append[list_name_key]:
            for word in self.lists[list_name_key]:
                for feature in self.should_append[list_name_key]:
                    if word.features[feature] != self.should_append[list_name_key][feature]:
                        word.allowed = False
        else:
            # print list_name_key
            # print self.lists[list_name_key]
            for word in self.lists[list_name_key]:
                word.allowed = True
                # print 'foo'

    def add_features_into_counter(self, word, list_name_key):
        for feature in self.list_equality_counter[list_name_key]:
            # если значение этого параметра есть среди значений в счетчике, то плюс 1
            if word.features[feature] in self.list_equality_counter[list_name_key][feature]:
                # print word.features[feature]
                self.list_equality_counter[list_name_key][feature][word.features[feature]] += 1

    def remove_features_from_counter(self, word, list_name_key):
        for feature in self.list_equality_counter[list_name_key]:
            # если значение этого параметра есть среди значений в счетчике, то минус 1
            if word.features[feature] in self.list_equality_counter[list_name_key][feature]:
                # print word.features[feature]
                self.list_equality_counter[list_name_key][feature][word.features[feature]] -= 1

    def add_closest(self):
        ##########
        # LIST 1 #
        ##########

        self.check_words_for_allowance('list_1')

        # вектор расстояния до другого листа
        self.distance_for_the_list['list_1'] = list()
        for i in xrange(self.number_of_same):
            # длина этого массива равна длине массива одинаковых фич
            # значения -- это среднее значение фичи по всем словам второго листа
            self.distance_for_the_list['list_1'].append(mean([word.same[i] for word in self.list_outputs['list_2']]))

        index = 0
        for i, word in enumerate(self.lists['list_1']):
            if word.allowed:
                index = i
                break

        # задираем максимальо минимум (максимальное значение это длина массива одинаковых фич,
        # т.к. все они максимум по 1
        minimum = self.number_of_same
        # обходим первый лист и ищем слово с ближайшим вектором
        for i in xrange(len(self.lists['list_1'])):
            if self.lists['list_1'][i].allowed:
                # считаем расстояние (Эвклидово??) от текущего слова до "среднего" вектора второго листа
                from_distance = sum([abs(self.lists['list_1'][i].same[j] - self.distance_for_the_list['list_1'][j]) for j in xrange(self.number_of_same)])
                # находим среди всех минимум и запоминаем индекс
                if from_distance < minimum:
                    minimum = from_distance
                    index = i

        word = self.lists['list_1'][index]

        # добавляем найденное слово в аутпут и удаляем из листа
        self.list_outputs['list_1'].append(word)

        # прибавляем параметры добавленного слова в счетчик
        self.add_features_into_counter(word, 'list_1')

        del self.lists['list_1'][index]

        # print '\nAdd closest'
        # print 'Should append: ', self.should_append_first
        # print 'Arguments feature of added word: {}'.format(word.features['arguments'])
        # print 'Counter: ', self.first_list_equality_counter

        ##########
        # LIST 2 #
        ##########

        self.check_words_for_allowance('list_2')

        index = 0
        for i, word in enumerate(self.lists['list_2']):
            if word.allowed:
                index = i
                break

        # повторяем те же действия для второго листа
        self.distance_for_the_list['list_2'] = list()
        for i in xrange(self.number_of_same):
            self.distance_for_the_list['list_2'].append(mean([word.same[i] for word in self.list_outputs['list_1']]))
        minimum = self.number_of_same + 1
        for i in xrange(len(self.lists['list_2'])):
            if self.lists['list_2'][i].allowed:
                from_distance = sum([abs(self.lists['list_2'][i].same[j] - self.distance_for_the_list['list_2'][j]) for j in xrange(self.number_of_same)])
                if from_distance < minimum:
                    minimum = from_distance
                    index = i

        word = self.lists['list_2'][index]

        # добавляем найденное слово в аутпут и удаляем из листа
        self.list_outputs['list_2'].append(word)

        # прибавляем параметры добавленного слова в счетчик
        self.add_features_into_counter(word, 'list_2')

        del self.lists['list_2'][index]

    def compensate(self, feature_name):
        # print 777

        # находим имя листа с более высоким и более низким средним
        lowest_mean_list_name = 'list_1' if self.list_mean['list_1'] <= self.list_mean['list_2'] else 'list_2'
        highest_mean_list_name = 'list_1' if self.list_mean['list_1'] > self.list_mean['list_2'] else 'list_2'

        # print
        # print 'means before compensation:'
        # print '1st mean: {}'.format(self.list_mean['list_1'])
        # print '2nd mean: {}'.format(self.list_mean['list_2'])
        # print lowest_mean_list_name, highest_mean_list_name

        self.check_words_for_allowance(lowest_mean_list_name)

        # обходим лист
        min_value = 1
        word_index_for_highest_mean_list_to_add = 0
        for j, word in enumerate(self.lists[highest_mean_list_name]):
            if word.allowed:
                if word.normalized_features[feature_name] < min_value:
                    min_value = word.normalized_features[feature_name]
                    word_index_for_highest_mean_list_to_add = j

        # print
        # print min_value
        #
        # print [word.normalized_features[feature_name] for word in self.list_outputs[highest_mean_list_name]]

        self.check_words_for_allowance(highest_mean_list_name)

        max_value = 0
        word_index_for_lowest_mean_list_to_add = 0
        for j, word in enumerate(self.lists[lowest_mean_list_name]):
            # print j
            if word.allowed:
                if word.normalized_features[feature_name] > max_value:
                    max_value = word.normalized_features[feature_name]
                    word_index_for_lowest_mean_list_to_add = j

        word_to_lowest = self.lists[lowest_mean_list_name][word_index_for_lowest_mean_list_to_add]
        self.list_outputs[lowest_mean_list_name].append(word_to_lowest)
        # прибавляем параметры добавленного слова в счетчик
        self.add_features_into_counter(word_to_lowest, lowest_mean_list_name)
        del self.lists[lowest_mean_list_name][word_index_for_lowest_mean_list_to_add]

        # print len(self.lists[highest_mean_list_name])

        # print self.list_mean['list_1']

        # print '\nCompensate'
        # print 'Should append: ', self.should_append_first
        # print 'Arguments feature of added word: {}'.format(word.features['arguments'])
        # print 'Counter: ', self.first_list_equality_counter

        # print len(self.lists[highest_mean_list_name])
        # print word_index_for_highest_mean_list_to_add

        word_to_highest = self.lists[highest_mean_list_name][word_index_for_highest_mean_list_to_add]
        self.list_outputs[highest_mean_list_name].append(word_to_highest)
        # прибавляем параметры добавленного слова в счетчик
        self.add_features_into_counter(word_to_highest, highest_mean_list_name)
        del self.lists[highest_mean_list_name][word_index_for_highest_mean_list_to_add]

        # print [word.normalized_features[feature_name] for word in self.list_outputs[highest_mean_list_name]]

    def test_and_fix(self):
        for feature_name in self.same:
            # print feature_name
            p_value_same = self.test([word.normalized_features[feature_name] for word in self.list_outputs['list_1']],
                                     [word.normalized_features[feature_name] for word in self.list_outputs['list_2']])

            # print p_value_same

            # if p_value_same < 0.2:
            if p_value_same < self.parameters.alpha * 4:
                # print 888
                # while p_value_same < 0.06:
                # print 'before compensation:'
                # print feature_name, p_value_same

                # если листы достигли нужной пользователю длины
                if self.equal():
                    # print 888

                    # возвращаем по одному слову из аутпута в общий лист
                    self.word_to_pop_from_the_list['list_1'] = self.list_outputs['list_1'].pop(random.randint(0, len(self.list_outputs['list_1'])-1))
                    self.word_to_pop_from_the_list['list_2'] = self.list_outputs['list_2'].pop(random.randint(0, len(self.list_outputs['list_2'])-1))

                    self.remove_features_from_counter(self.word_to_pop_from_the_list['list_1'], 'list_1')
                    self.remove_features_from_counter(self.word_to_pop_from_the_list['list_2'], 'list_2')

                    self.lists['list_1'].append(self.word_to_pop_from_the_list['list_1'])
                    self.lists['list_2'].append(self.word_to_pop_from_the_list['list_2'])

                # по всем словам в аутпуте считаем среднее параметра i
                self.list_mean['list_1'] = mean([word.normalized_features[feature_name] for word in self.list_outputs['list_1']])
                self.list_mean['list_2'] = mean([word.normalized_features[feature_name] for word in self.list_outputs['list_2']])

                # print self.list_mean

                self.compensate(feature_name)

                p_value_same = self.test(
                    [word.normalized_features[feature_name] for word in self.list_outputs['list_1']],
                    [word.normalized_features[feature_name] for word in self.list_outputs['list_2']])

                # print '\nafter compensation:'
                # print feature_name, p_value_same
                # print

            p_value_same = self.test([word.normalized_features[feature_name] for word in self.list_outputs['list_1']],
                                     [word.normalized_features[feature_name] for word in self.list_outputs['list_2']])

            # if p_value_same < 0.15:
            if p_value_same < self.parameters.alpha * 3:
                # print 'Not allowed because of: {}'.format(feature_name)
                # print
                self.allow = False

    def high_low(self, high, low):
        high_sorted = sorted(high, reverse=True)
        low_sorted = sorted(low, reverse=False)
        stop = min(len(high_sorted), len(low_sorted))
        high_stop = high_sorted[0]
        low_stop = low_sorted[0]
        i = 0
        high = []
        low = []
        while high_stop > low_stop and stop > i:
            high.append(high_sorted[i])
            low.append(low_sorted[i])
            high_stop = high_sorted[i]
            low_stop = low_sorted[i]
            i += 1
        return high, low

    def differentiate(self):
        for word in self.lists['list_1']:
            word.value_of_differ_feature = word.normalized_features[self.key_for_differ_feature]
        for word in self.lists['list_2']:
            word.value_of_differ_feature = word.normalized_features[self.key_for_differ_feature]
        if self.which_higher == 'first':
            self.lists['list_1'], self.lists['list_2'] = self.high_low(self.lists['list_1'], self.lists['list_2'])
        elif self.which_higher == 'second':
            self.lists['list_2'], self.lists['list_1'] = self.high_low(self.lists['list_2'], self.lists['list_1'])

    def create_list_from_to_choose(self, parameters_for_one_list):
        filtered_list = []
        for word in self.words:
            if is_match(word, parameters_for_one_list):
                # print word.features["pos"]
                filtered_list.append(word)
                # print

        return filtered_list

    def split(self):
        if self.lists['list_1'] == self.lists['list_2']:
            new = []
            new += self.lists['list_1']
            random.shuffle(new)
            self.lists['list_1'] = []
            self.lists['list_1'] += new[:len(new)/2]
            self.lists['list_2'] = []
            self.lists['list_2'] += new[len(new)/2:]

    def setup_parameters(self):
        if self.parameters.bonferroni != 'off':
            self.parameters.calculate_alpha()

        self.same = self.parameters.same
        self.number_of_same = len(self.same)
        self.length = self.parameters.length
        self.statistics = self.parameters.statistics
        for list_name_key in self.lists:
            for word in self.lists[list_name_key]:
                # это массив из значений фич, которые не должны отличаться
                word.same = [word.normalized_features[key] for key in self.same]

    def add_first(self):
        self.lists['list_1'] += self.list_outputs['list_1']
        self.lists['list_2'] += self.list_outputs['list_2']

        self.list_outputs['list_1'] = list()
        self.list_outputs['list_2'] = list()

        # вытаскиваем случайное слово из листа
        index = random.randint(0, len(self.lists['list_1'])-1)

        word = self.lists['list_1'][index]

        # прибавляем параметры добавленного слова в счетчик
        for feature in self.list_equality_counter['list_1']:
            # если значение этого параметра есть среди значений в счетчике, то плюс 1
            if word.features[feature] in self.list_equality_counter['list_1'][feature]:
                self.list_equality_counter['list_1'][feature][word.features[feature]] += 1

        self.list_outputs['list_1'].append(word)
        del self.lists['list_1'][index]

        # вытаскиваем случайное слово из листа
        index = random.randint(0, len(self.lists['list_2'])-1)

        word = self.lists['list_2'][index]

        # прибавляем параметры добавленного слова в счетчик
        for feature in self.list_equality_counter['list_2']:
            # если значение этого параметра есть среди значений в счетчике, то плюс 1
            if word.features[feature] in self.list_equality_counter['list_2'][feature]:
                self.list_equality_counter['list_2'][feature][word.features[feature]] += 1

        self.list_outputs['list_2'].append(word)
        del self.lists['list_2'][index]

    def sharp(self):
        return len(self.list_outputs['list_1']) != self.length

    def less(self):
        return len(self.list_outputs['list_1']) < self.length

    def equal(self):
        return len(self.list_outputs['list_1']) == self.length

    def test(self, arr1, arr2):
        p_value = 0
        if self.statistics == 'auto':
            # проверяем Левеном на равенство дисперсий. Если равны
            if stats.levene(arr1, arr2)[1] > 0.05:
                # Шапир на нормальность выборок. Если нормальные
                if stats.shapiro(arr1)[1] > 0.05 and stats.shapiro(arr2)[1] > 0.05:
                    # p = Student
                    p_value = stats.ttest_ind(arr1, arr2)[1]
                else:
                    # p = Mann
                    if equal(arr1, arr2):
                        p_value = 1
                    else:
                        p_value = stats.mannwhitneyu(arr1, arr2, alternative='two-sided')[1]
            else:
                p_value = stats.ttest_ind(arr1, arr2, False)[1]

        elif self.statistics == 'student':
            p_value = stats.ttest_ind(arr1, arr2)[1]
        elif self.statistics == 'welch':
            p_value = stats.ttest_ind(arr1, arr2, False)[1]
        elif self.statistics == 'mann':
            if equal(arr1, arr2):
                p_value = 1
            else:
                p_value = stats.mannwhitneyu(arr1, arr2, alternative='two-sided')[1]
        return p_value


def equal(arr1, arr2):
    ref = arr1[0]
    for el in arr1[2:] + arr2:
        if el != ref:
            return False
    return True


def mean(arr):
    # vector_without_none = []
    # for value in arr:
    #     if value is not None:
    #         vector_without_none.append(value)
    return sum(arr)/len(arr) if len(arr) > 0 else None


def is_match(database_word, client_word_parameters):
    for feature in client_word_parameters:

        # Берем только те, которые нам важны
        if client_word_parameters[feature]['matters']:

            # если это категориальная фича, просто сравниваем значение
            if client_word_parameters[feature]['categorical']:
                if client_word_parameters[feature]['value'] != database_word.features[feature]:
                    return False

            # если это континуальная фича, то должна попадать в диапазон
            else:
                # print client_word_parameters['features'][feature]['value']
                # print database_word.features[feature]
                # print float(client_word_parameters['features'][feature]['value'][0]) <= database_word.features[feature] <= float(client_word_parameters['features'][feature]['value'][1])

                if not client_word_parameters[feature]['value'][0]:
                    client_word_parameters[feature]['value'][0] = -float('inf')
                if not client_word_parameters[feature]['value'][1]:
                    client_word_parameters[feature]['value'][1] = float('inf')

                if not float(client_word_parameters[feature]['value'][0]) <= database_word.features[feature] <= float(client_word_parameters[feature]['value'][1]):
                    return False
    return True

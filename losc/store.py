# -*- coding:utf-8 -*-

import os
import math
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
        self.min = dict()
        self.max = dict()
        self.first_list = list()
        self.second_list = list()
        self.first_list_output = list()
        self.second_list_output = list()
        self.minimum = None
        self.length = 0
        self.frequency = 'off'
        self.number_of_same = 0
        self.allow = True
        self.same = list()
        self.statistics = None
        self.key_for_differ_feature = ''
        self.which_higher = None
        self.p_values = list()
        self.time_begin = None
        self.success = True
        self.first_list_equality_counter = dict()
        self.second_list_equality_counter = dict()
        self.should_append_first = dict()
        self.should_append_second = dict()
        self.numeric_features = list()
        self.categorical_features = dict()
        self.categorical_features_list = list()
        self.len_of_numeric = 0
        self.len_of_categorical = 0
        self.parameters = Parameters()

    def read_data(self):
        with codecs.open('./data/map.tsv', 'r', 'utf-8') as f:
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

        for line in lines[2::]:
            self.words.append(Word())

            columns = line.rstrip().split('\t')
            self.words[-1].name = columns[0]

            for feature, value in zip(features_list, columns[1::]):
                if features_dict[feature] == 'int':
                    self.words[-1].features[feature] = int(value)
                elif features_dict[feature] == 'float':
                    self.words[-1].features[feature] = float(value)
                else:
                    self.words[-1].features[feature] = value
                    if value != 'None':
                        if value not in self.categorical_features[feature]:
                            self.categorical_features[feature].append(value)

        for feature in self.categorical_features:
            self.categorical_features[feature] = sorted(self.categorical_features[feature])

    def reset_counters(self):
        for feature, parameters in self.first_list_equality_counter.iteritems():
            for parameter, value in parameters.iteritems():
                parameters[parameter] = 0
        for feature, parameters in self.second_list_equality_counter.iteritems():
            for parameter, value in parameters.iteritems():
                parameters[parameter] = 0

        # print '\n#####\nCounters were reset'
        # print self.first_list_equality_counter

    def generate(self):
        while self.sharp():

            # Сбрасываем счетчики для 50/50
            self.reset_counters()

            # считаем сколько времени прошло и убиваем
            time_current = time.time()
            if time_current - self.time_begin > 30:
                self.success = False
                break

            # сбрасывем листы и аутпут, добавляем в аутпут по одному случайному слову
            self.add_first()

            self.allow = True

            # пока длина аутпута не превышает требуемой
            while self.allow and self.less():
                time_current = time.time()
                if time_current - self.time_begin > 20:
                    self.success = False
                    break

                # начинаем добавлять слова с ближайшими векторами
                self.add_closest()
                # как только размер листа больше 5, начинаем проверять
                if len(self.first_list_output) > 5:
                    self.test_and_fix()

    def create_equality_counter(self, list_parameters_from_client):
        # создаем пустой счетчик
        equality_counter = dict()

        # обходим список категориальных
        for feature in self.categorical_features:
            # если у кого-то значение 50/50
            if list_parameters_from_client[feature]['value'] == 'half':
                # создаем для данного параметра ячейку с двумя значениями, равными нулю
                equality_counter[feature] = {
                    self.categorical_features[feature][0]: 0,
                    self.categorical_features[feature][1]: 0
                }

        return equality_counter

    def find_min_max(self, word_list):
        for word in word_list:
            for key in word.features:
                if type(word.features[key]) == float:
                    if word.features[key] < self.min[key]:
                        self.min[key] = word.features[key]
                    if word.features[key] > self.max[key]:
                        self.max[key] = word.features[key]

    def normalize(self):
        # копируем фичи первого слова, чтобы было с чего начать сравнивать
        self.min = self.first_list[0].features.copy()
        self.max = self.first_list[0].features.copy()

        # находим минимум и максимум для всех фич в листах
        self.find_min_max(self.first_list)
        self.find_min_max(self.second_list)

        # нормализуем
        for word in self.first_list:
            word.normalized_features = word.features.copy()
            for key in word.features:
                if type(word.features[key]) == float:
                    word.normalized_features[key] = (word.features[key] - self.min[key]) / (self.max[key] - self.min[key])
        for word in self.second_list:
            word.normalized_features = word.features.copy()
            for key in word.features:
                if type(word.features[key]) == float:
                    word.normalized_features[key] = (word.features[key] - self.min[key]) / (self.max[key] - self.min[key])

    def create_zip(self):
        path = os.path.dirname(os.path.realpath(__file__))

        first_list_head = 'name\t' + '\t'.join(self.first_list_output[0].features.keys()) + '\r\n'
        with codecs.open(path + '/static/output/list_1.tsv', u'w', u'utf-8') as w:
            w.write(first_list_head)
            for word in self.first_list_output:
                w.write(word.name + u'\t' + u'\t'.join([str(word.features[key]) for key in word.features]) + u'\r\n')

        second_list_head = 'name\t' + '\t'.join(self.first_list_output[0].features.keys()) + '\r\n'
        with codecs.open(path + '/static/output/list_2.tsv', u'w', u'utf-8') as w:
            w.write(second_list_head)
            for word in self.second_list_output:
                w.write(word.name + u'\t' + u'\t'.join([str(word.features[key]) for key in word.features]) + u'\r\n')

        table = self.create_final_table()

        with codecs.open(path + '/static/output/statistics.tsv', u'w', u'utf-8') as w:
            w.write(table)

        z = zipfile.ZipFile(path + '/static/output/results.zip', u'w')
        z.write(path + '/static/output/list_1.tsv', basename(path + '/static/output/list_1.tsv'))
        z.write(path + '/static/output/list_2.tsv', basename(path + '/static/output/list_2.tsv'))
        z.write(path + '/static/output/statistics.tsv', basename(path + '/static/output/statistics.tsv'))

        os.remove(path + '/static/output/list_1.tsv')
        os.remove(path + '/static/output/list_2.tsv')
        os.remove(path + '/static/output/statistics.tsv')

    def create_table_per_list(self, list_output, list_name):
        table_per_list = ''

        list_features = dict()

        for feature in self.numeric_features:
            list_features[feature] = [word.features[feature] for word in list_output]

        means = [str(np.mean(list_features[feature])) for feature in self.numeric_features]

        list1_mean = list_name + '\tmean\t' + '\t'.join(means) + '\t' + '\t'.join(['None'] * self.len_of_categorical) + '\r\n'
        table_per_list += list1_mean

        mins = [str(np.min(list_features[feature])) for feature in self.numeric_features]

        list1_min = '\tmin\t' + '\t'.join(mins) + '\t' + '\t'.join(['None'] * self.len_of_categorical) + '\r\n'
        table_per_list += list1_min

        maxes = [str(np.max(list_features[feature])) for feature in self.numeric_features]

        list1_max = '\tmax\t' + '\t'.join(maxes) + '\t' + '\t'.join(['None'] * self.len_of_categorical) + '\r\n'
        table_per_list += list1_max

        sd = [str(np.std(list_features[feature])) for feature in self.numeric_features]

        list1_sd = '\tSD\t' + '\t'.join(sd) + '\t' + '\t'.join(['None'] * self.len_of_categorical) + '\r\n'
        table_per_list += list1_sd

        ratios = list()

        for feature in self.categorical_features:
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
                ratio_string += 'None'
            else:
                for key in ratio:
                    string = key + ': ' + str(ratio[key]) + '; '
                    ratio_string += string

        print ratio_string

        list1_ratio = '\tratio\t' + '\t'.join(['None'] * self.len_of_numeric) + ratio_string + '\r\n'
        table_per_list += list1_ratio

        shapiro = [str(stats.shapiro(list_features[feature])[1]) for feature in self.numeric_features]

        list1_shapiro = '\tShapiro, p-value\t' + '\t'.join(shapiro) + '\t' + '\t'.join(['None'] * self.len_of_categorical) + '\r\n'
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
                        result = stats.mannwhitneyu(arr1, arr2)
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
                result = stats.mannwhitneyu(arr1, arr2)
                t_value = result[0]
                p_value = result[1]

        df = len(arr1) + len(arr2) - 2

        return [test_name, t_value, p_value, df, levene]

    def create_stat_table(self):
        stat_table = ''

        first_list_features = dict()
        for feature in self.numeric_features:
            first_list_features[feature] = [word.features[feature] for word in self.first_list_output]

        second_list_features = dict()
        for feature in self.numeric_features:
            second_list_features[feature] = [word.features[feature] for word in self.second_list_output]

        list_of_test_results = [self.return_test_results(first_list_features[feature], second_list_features[feature]) for feature in self.numeric_features]

        test_name = 'statistics\ttest name\t' + '\t'.join([result_list[0] for result_list in list_of_test_results])\
                    + '\t' + '\t'.join(['None'] * self.len_of_categorical) + '\r\n'
        stat_table += test_name

        t_value = '\tt-value\t' + '\t'.join([str(result_list[1]) for result_list in list_of_test_results])\
                  + '\t' + '\t'.join(['None'] * self.len_of_categorical) + '\r\n'
        stat_table += t_value

        p_value = '\tp-value\t' + '\t'.join([str(result_list[2]) for result_list in list_of_test_results]) \
                  + '\t' + '\t'.join(['None'] * self.len_of_categorical) + '\r\n'
        stat_table += p_value

        df = '\tDF\t' + '\t'.join([str(result_list[3]) for result_list in list_of_test_results]) \
             + '\t' + '\t'.join(['None'] * self.len_of_categorical) + '\r\n'
        stat_table += df

        levene = '\tLevene, p-value\t' + '\t'.join([str(result_list[4]) for result_list in list_of_test_results]) \
                 + '\t' + '\t'.join(['None'] * self.len_of_categorical) + '\r\n'
        stat_table += levene

        return stat_table

    def create_final_table(self):
        table = ''
        header = '\t\t' + '\t'.join(self.numeric_features) + '\t' + '\t'.join(self.categorical_features) + '\r\n'
        table += header

        table += self.create_table_per_list(self.first_list_output, 'list 1')
        table += '\r\n'
        table += self.create_table_per_list(self.second_list_output, 'list 2')
        table += '\r\n'

        table += self.create_stat_table()

        return table

    def set_should_append(self, list_equality_counter, list_name):
        if list_name == 'first':
            self.should_append_first = dict()
            for feature in list_equality_counter:
                keys = list_equality_counter[feature].keys()
                if list_equality_counter[feature][keys[0]] < list_equality_counter[feature][keys[1]]:
                    self.should_append_first[feature] = keys[0]
                elif list_equality_counter[feature][keys[0]] > list_equality_counter[feature][keys[1]]:
                    self.should_append_first[feature] = keys[1]
        else:
            self.should_append_second = dict()
            for feature in list_equality_counter:
                keys = list_equality_counter[feature].keys()
                if list_equality_counter[feature][keys[0]] < list_equality_counter[feature][keys[1]]:
                    self.should_append_second[feature] = keys[0]
                elif list_equality_counter[feature][keys[0]] > list_equality_counter[feature][keys[1]]:
                    self.should_append_second[feature] = keys[1]

    def check_words_for_allowance(self, list_name):
        if list_name == 'first':
            # оставляем только неравные параметры, остальные неважны в этой итерации
            self.set_should_append(self.first_list_equality_counter, 'first')

            if self.should_append_first:
                for word in self.first_list:
                    for feature in self.should_append_first:
                        if word.features[feature] != self.should_append_first[feature]:
                            word.allowed = False
            else:
                for word in self.first_list:
                    word.allowed = True

        else:
            # оставляем только неравные параметры, остальные неважны в этой итерации
            self.set_should_append(self.second_list_equality_counter, 'second')

            if self.should_append_second:
                for word in self.second_list:
                    for feature in self.should_append_second:
                        if word.features[feature] != self.should_append_second[feature]:
                            word.allowed = False
            else:
                for word in self.second_list:
                    word.allowed = True

    def add_features_into_counter(self, word, list_name):
        if list_name == 'first':
            for feature in self.first_list_equality_counter:
                # если значение этого параметра есть среди значений в счетчике, то плюс 1
                if word.features[feature] in self.first_list_equality_counter[feature]:
                    # print word.features[feature]
                    self.first_list_equality_counter[feature][word.features[feature]] += 1

        else:
            for feature in self.second_list_equality_counter:
                # если значение этого параметра есть среди значений в счетчике, то плюс 1
                if word.features[feature] in self.second_list_equality_counter[feature]:
                    self.second_list_equality_counter[feature][word.features[feature]] += 1

    def remove_features_from_counter(self, word, list_name):
        if list_name == 'first':
            for feature in self.first_list_equality_counter:
                # если значение этого параметра есть среди значений в счетчике, то минус 1
                if word.features[feature] in self.first_list_equality_counter[feature]:
                    # print word.features[feature]
                    self.first_list_equality_counter[feature][word.features[feature]] -= 1

        else:
            for feature in self.second_list_equality_counter:
                # если значение этого параметра есть среди значений в счетчике, то минус 1
                if word.features[feature] in self.second_list_equality_counter[feature]:
                    self.second_list_equality_counter[feature][word.features[feature]] -= 1

    def add_closest(self):
        ##########
        # LIST 1 #
        ##########

        self.check_words_for_allowance('first')

        # вектор расстояния до другого листа
        distance_for_first_list = []
        for i in xrange(self.number_of_same):
            # длина этого массива равна длине массива одинаковых фич
            # значения -- это среднее значение фичи по всем словам второго листа
            distance_for_first_list.append(mean([word.same[i] for word in self.second_list_output]))

        index = 0
        for i, word in enumerate(self.first_list):
            if word.allowed:
                index = i
                break

        # задираем максимальо минимум (максимальное значение это длина массива одинаковых фич,
        # т.к. все они максимум по 1
        minimum = self.number_of_same
        # обходим первый лист и ищем слово с ближайшим вектором
        for i in xrange(len(self.first_list)):
            if self.first_list[i].allowed:
                # считаем расстояние (Эвклидово??) от текущего слова до "среднего" вектора второго листа
                from_distance = sum([abs(self.first_list[i].same[j] - distance_for_first_list[j]) for j in xrange(self.number_of_same)])
                # находим среди всех минимум и запоминаем индекс
                if from_distance < minimum:
                    minimum = from_distance
                    index = i

        word = self.first_list[index]

        # добавляем найденное слово в аутпут и удаляем из листа
        self.first_list_output.append(word)

        # прибавляем параметры добавленного слова в счетчик
        self.add_features_into_counter(word, 'first')

        del self.first_list[index]

        # print '\nAdd closest'
        # print 'Should append: ', self.should_append_first
        # print 'Arguments feature of added word: {}'.format(word.features['arguments'])
        # print 'Counter: ', self.first_list_equality_counter

        ##########
        # LIST 2 #
        ##########

        self.check_words_for_allowance('second')

        index = 0
        for i, word in enumerate(self.second_list):
            if word.allowed:
                index = i
                break

        # повторяем те же действия для второго листа
        distance_for_second_list = []
        for i in xrange(self.number_of_same):
            distance_for_second_list.append(mean([word.same[i] for word in self.first_list_output]))
        minimum = self.number_of_same + 1
        for i in xrange(len(self.second_list)):
            if self.second_list[i].allowed:
                from_distance = sum([abs(self.second_list[i].same[j] - distance_for_second_list[j]) for j in xrange(self.number_of_same)])
                if from_distance < minimum:
                    minimum = from_distance
                    index = i

        word = self.second_list[index]

        # добавляем найденное слово в аутпут и удаляем из листа
        self.second_list_output.append(word)

        # прибавляем параметры добавленного слова в счетчик
        self.add_features_into_counter(word, 'second')

        del self.second_list[index]

    def compensate(self, first_list_mean, second_list_mean, i):
        # print 777

        # если это среднее больше в первом листе
        if first_list_mean > second_list_mean:
            self.check_words_for_allowance('first')

            lowest_from_rest = 1
            first_list_index = 0
            for j, word in enumerate(self.first_list):
                if word.allowed:
                    if word.normalized_features[i] < lowest_from_rest:
                        lowest_from_rest = word.normalized_features[i]
                        first_list_index = j

            self.check_words_for_allowance('second')

            highest_from_rest = 0
            second_list_index = 0
            for j, word in enumerate(self.second_list):
                if word.allowed:
                    if word.normalized_features[i] > highest_from_rest:
                        highest_from_rest = word.normalized_features[i]
                        second_list_index = j

        else:
            self.check_words_for_allowance('second')

            lowest_from_rest = 1
            second_list_index = 0
            for j, word in enumerate(self.second_list):
                if word.allowed:
                    if word.normalized_features[i] < lowest_from_rest:
                        lowest_from_rest = word.normalized_features[i]
                        second_list_index = j

            self.check_words_for_allowance('first')

            highest_from_rest = 0
            first_list_index = 0
            for j, word in enumerate(self.first_list):
                if word.allowed:
                    if word.normalized_features[i] > highest_from_rest:
                        highest_from_rest = word.normalized_features[i]
                        first_list_index = j

        word = self.first_list[first_list_index]
        self.first_list_output.append(word)
        # прибавляем параметры добавленного слова в счетчик
        self.add_features_into_counter(word, 'first')
        del self.first_list[first_list_index]

        # print '\nCompensate'
        # print 'Should append: ', self.should_append_first
        # print 'Arguments feature of added word: {}'.format(word.features['arguments'])
        # print 'Counter: ', self.first_list_equality_counter

        word = self.second_list[second_list_index]
        self.second_list_output.append(word)
        # прибавляем параметры добавленного слова в счетчик
        self.add_features_into_counter(word, 'second')
        del self.second_list[second_list_index]

    def test_and_fix(self):
        for i in self.same:
            p_value_same = self.test([word.normalized_features[i] for word in self.first_list_output],
                                     [word.normalized_features[i] for word in self.second_list_output])

            # if p_value_same < 0.2:
            if p_value_same < self.parameters.alpha * 4:
                # while p_value_same < 0.06:

                # если листы достигли нужной пользователю длины
                if self.equal():
                    # print 888

                    # возвращаем по одному слову из аутпута в общий лист
                    word_first_list_to_pop = self.first_list_output.pop(random.randint(0, len(self.first_list_output)-1))
                    word_second_list_to_pop = self.second_list_output.pop(random.randint(0, len(self.second_list_output)-1))

                    self.remove_features_from_counter(word_first_list_to_pop, 'first')
                    self.remove_features_from_counter(word_second_list_to_pop, 'second')

                    # print 'Features were removed. Arguments feature of removed word: {}'.format(word_first_list_to_pop.features['arguments'])
                    # print 'Counter: ', self.first_list_equality_counter

                    self.first_list.append(word_first_list_to_pop)
                    self.second_list.append(word_second_list_to_pop)

                # по всем словам в аутпуте считаем среднее параметра i
                first_list_mean = mean([word.normalized_features[i] for word in self.first_list_output])
                second_list_mean = mean([word.normalized_features[i] for word in self.second_list_output])

                self.compensate(first_list_mean, second_list_mean, i)

            p_value_same = self.test([word.normalized_features[i] for word in self.first_list_output],
                                     [word.normalized_features[i] for word in self.second_list_output])

            # if p_value_same < 0.15:
            if p_value_same < self.parameters.alpha * 3:
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
        for word in self.first_list:
            word.value_of_differ_feature = word.normalized_features[self.key_for_differ_feature]
        for word in self.second_list:
            word.value_of_differ_feature = word.normalized_features[self.key_for_differ_feature]
        if self.which_higher == 'first':
            self.first_list, self.second_list = self.high_low(self.first_list, self.second_list)
        elif self.which_higher == 'second':
            self.second_list, self.first_list = self.high_low(self.second_list, self.first_list)

    def create_list_from_to_choose(self, parameters_for_one_list):
        filtered_list = []
        for word in self.words:
            if is_match(word, parameters_for_one_list):
                filtered_list.append(word)

        return filtered_list

    def split(self):
        if self.first_list == self.second_list:
            new = []
            new += self.first_list
            random.shuffle(new)
            self.first_list = []
            self.first_list += new[:len(new)/2]
            self.second_list = []
            self.second_list += new[len(new)/2:]

    def setup_parameters(self):
        if self.parameters.bonferroni != 'off':
            self.parameters.calculate_alpha()

        self.same = self.parameters.same
        self.number_of_same = len(self.same)
        self.length = self.parameters.length
        self.statistics = self.parameters.statistics
        self.frequency = self.parameters.frequency
        for word in self.first_list:
            # это массив из значений фич, которые не должны отличаться
            word.same = [word.normalized_features[key] for key in self.same]
        for word in self.second_list:
            word.same = [word.normalized_features[key] for key in self.same]

        if self.frequency == 'on':
            self.change_frequency()

    def change_frequency(self):
        for word in self.first_list:
            word.features['frequency'] = word.log_freq
        for word in self.second_list:
            word.features['frequency'] = word.log_freq

    def add_first(self):
        self.first_list += self.first_list_output
        self.second_list += self.second_list_output

        self.first_list_output = []
        self.second_list_output = []

        # вытаскиваем случайное слово из листа
        index = random.randint(0, len(self.first_list)-1)

        word = self.first_list[index]

        # прибавляем параметры добавленного слова в счетчик
        for feature in self.first_list_equality_counter:
            # если значение этого параметра есть среди значений в счетчике, то плюс 1
            if word.features[feature] in self.first_list_equality_counter[feature]:
                self.first_list_equality_counter[feature][word.features[feature]] += 1

        self.first_list_output.append(word)
        del self.first_list[index]

        # вытаскиваем случайное слово из листа
        index = random.randint(0, len(self.second_list)-1)

        word = self.second_list[index]

        # прибавляем параметры добавленного слова в счетчик
        for feature in self.second_list_equality_counter:
            # если значение этого параметра есть среди значений в счетчике, то плюс 1
            if word.features[feature] in self.second_list_equality_counter[feature]:
                self.second_list_equality_counter[feature][word.features[feature]] += 1

        self.second_list_output.append(word)
        del self.second_list[index]

    def sharp(self):
        return len(self.first_list_output) != self.length

    def less(self):
        return len(self.first_list_output) < self.length

    def equal(self):
        return len(self.first_list_output) == self.length

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
                        p_value = stats.mannwhitneyu(arr1, arr2)[1]
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
                p_value = stats.mannwhitneyu(arr1, arr2)[1]
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

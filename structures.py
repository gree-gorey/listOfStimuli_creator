# -*- coding:utf-8 -*-

import os
import math
import time
import random
import codecs
import zipfile
from scipy import stats

__author__ = 'gree-gorey'


class Store:
    def __init__(self):
        self.min = dict()
        self.max = dict()
        self.first_list = []
        self.second_list = []
        self.nouns = []
        self.verbs = []
        self.first_list_output = []
        self.second_list_output = []
        self.minimum = None
        self.length = 0
        self.number_of_same = 0
        self.allow = True
        self.same = []
        self.statistics = None
        self.key_for_differ_feature = ''
        self.which_higher = None
        self.p_values = []
        self.time_begin = None
        self.success = True

    def generate(self):
        while self.sharp():
            # считаем сколько времени прошло и убиваем
            time_current = time.time()
            if time_current - self.time_begin > 10:
                self.success = False
                break

            self.add_first()

            # self.allow = [True in xrange(self.number_of_same)]
            self.allow = True

            # while sum(self.allow) == self.number_of_same and self.less():

            while self.allow and self.less():
                time_current = time.time()
                if time_current - self.time_begin > 10:
                    self.success = False
                    break

                self.add_closest()
                if len(self.first_list_output) > 5:
                    self.test_and_fix()

    def final_statistics(self):
        for i in xrange(9):
            p_value = self.test([word.features[i] for word in self.first_list_output],
                                [word.features[i] for word in self.second_list_output])

            self.p_values.append(p_value)

    def print_results(self):
        print '\n######################################\n'

        for p in self.p_values:
            print p

        print '\n######################################\n'

    def read_verbs(self, f):
        for line in f:
            line = line.rstrip(u'\n').replace(',', '.').split(u'\t')
            self.verbs.append(Word())

            self.verbs[-1].name = line[0] + '. ' + line[1] + ' (' + line[2] + ')'

            self.verbs[-1].features['name_agreement_percent'] = float(line[3])
            self.verbs[-1].features['name_agreement_abs'] = float(line[4])
            self.verbs[-1].features['subjective_complexity'] = float(line[5])
            self.verbs[-1].features['objective_complexity'] = None if '-' in line[6] else float(line[6])
            self.verbs[-1].features['familiarity'] = float(line[7])
            self.verbs[-1].features['age'] = float(line[8])
            self.verbs[-1].features['imageability'] = float(line[9])
            self.verbs[-1].features['image_agreement'] = float(line[10])
            self.verbs[-1].features['frequency'] = float(line[11])
            self.verbs[-1].features['syllables'] = float(line[12])
            self.verbs[-1].features['phonemes'] = float(line[13])
            self.verbs[-1].features['arguments'] = 'one' if '1' in line[14] else 'two'
            self.verbs[-1].features['reflexivity'] = 'on' if '+' in line[15] else 'off'
            self.verbs[-1].features['instrumentality'] = 'on' if '+' in line[16] else 'off'
            self.verbs[-1].features['relation'] = 'on' if '+' in line[16] else 'off'

            # логарифмируем частоту
            self.verbs[-1].log_freq = math.log(self.verbs[-1].features['frequency'] + 1, 10)

    def read_nouns(self, f):
        for line in f:
            line = line.rstrip(u'\n').replace(',', '.').split(u'\t')
            self.nouns.append(Word())

            self.nouns[-1].name = line[1]

            self.nouns[-1].features['part'] = line[0]
            self.nouns[-1].features['name_agreement_percent'] = float(line[2])
            self.nouns[-1].features['name_agreement_abs'] = float(line[3])
            self.nouns[-1].features['subjective_complexity'] = float(line[4])
            self.nouns[-1].features['objective_complexity'] = None if '-' in line[5] else float(line[5])
            self.nouns[-1].features['familiarity'] = float(line[6])
            self.nouns[-1].features['age'] = float(line[7])
            self.nouns[-1].features['imageability'] = float(line[8])
            self.nouns[-1].features['image_agreement'] = float(line[9])
            self.nouns[-1].features['frequency'] = float(line[10])
            self.nouns[-1].features['syllables'] = float(line[11])
            self.nouns[-1].features['phonemes'] = float(line[12])

            # логарифмируем частоту
            self.nouns[-1].log_freq = math.log(self.nouns[-1].features['frequency'] + 1, 10)

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
        head = u'Доминантная номинация\tУстойчивость номинации\tСубъективная сложность\tЗнакомство с объектом\t' \
               u'Возраст усвоения\tПредставимость\tСхожесть образа с рисунком\tЧастотность\tДлина в слогах\t' \
               u'Длина в фонемах\n'
        with codecs.open(u'list_1.csv', u'w', u'utf-8') as w:
            w.write(head)
            for word in self.first_list_output:
                w.write(word.name + u'\t' + u'\t'.join([str(f) for f in word.features]) + u'\n')

        with codecs.open(u'list_2.csv', u'w', u'utf-8') as w:
            w.write(head)
            for word in self.second_list_output:
                w.write(word.name + u'\t' + u'\t'.join([str(f) for f in word.features]) + u'\n')

        stat_head = u'Характеристика\tУстойчивость номинации\tСубъективная сложность\tЗнакомство с объектом\t' \
                    u'Возраст усвоения\tПредставимость\tСхожесть образа с рисунком\tЧастотность\tДлина в слогах\t' \
                    u'Длина в фонемах\n'

        with codecs.open(u'statistics.csv', u'w', u'utf-8') as w:
            w.write(stat_head)
            w.write(u'p-value\t' + u'\t'.join([str(p) for p in self.p_values]) + u'\n')

        z = zipfile.ZipFile(u'results.zip', u'w')
        z.write(u'list_1.csv')
        z.write(u'list_2.csv')
        z.write(u'statistics.csv')

        os.remove(u'list_1.csv')
        os.remove(u'list_2.csv')
        os.remove(u'statistics.csv')

    def test_and_fix(self):
        for i in self.same:
            p_value_same = self.test([word.normalized_features[i] for word in self.first_list_output],
                                     [word.normalized_features[i] for word in self.second_list_output])

            if p_value_same < 0.2:
                # while p_value_same < 0.06:
                if self.equal():
                    self.first_list.append(self.first_list_output.pop(random.randint(0, len(self.first_list_output)-1)))
                    self.second_list.append(self.second_list_output.pop(random.randint(0, len(self.second_list_output)-1)))

                first_list_mean = mean([word.normalized_features[i] for word in self.first_list_output])
                second_list_mean = mean([word.normalized_features[i] for word in self.second_list_output])

                if first_list_mean > second_list_mean:
                    hhh, lll = compensate(self.first_list, self.second_list, i)
                    self.first_list_output.append(self.first_list[hhh])
                    del self.first_list[hhh]
                    self.second_list_output.append(self.second_list[lll])
                    del self.second_list[lll]
                else:
                    hhh, lll = compensate(self.second_list, self.first_list, i)
                    self.first_list_output.append(self.first_list[lll])
                    del self.first_list[lll]
                    self.second_list_output.append(self.second_list[hhh])
                    del self.second_list[hhh]

            p_value_same = self.test([word.normalized_features[i] for word in self.first_list_output],
                                     [word.normalized_features[i] for word in self.second_list_output])

            if p_value_same < 0.15:
                self.allow = False

                # for k in self.same:
                #     p_value_same = self.test([word.normalized_features[k] for word in self.first_list_output],
                #                              [word.normalized_features[k] for word in self.second_list_output])
                #
                #     if p_value_same < 0.05:
                #         self.allow = False

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
        if parameters_for_one_list['pos'] == 'verb':
            parameters_for_one_list['features']['part']['matters'] = False

            for verb in self.verbs:
                if is_match(verb, parameters_for_one_list):
                    filtered_list.append(verb)

        elif parameters_for_one_list['pos'] == 'noun':
            parameters_for_one_list['features']['arguments']['matters'] = False
            parameters_for_one_list['features']['reflexivity']['matters'] = False
            parameters_for_one_list['features']['instrumentality']['matters'] = False
            parameters_for_one_list['features']['relation']['matters'] = False

            for noun in self.nouns:
                if is_match(noun, parameters_for_one_list):
                    filtered_list.append(noun)

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

    def setup_parameters(self, parameters):
        self.same = parameters.same
        self.number_of_same = len(self.same)
        self.length = parameters.length
        self.statistics = parameters.statistics
        self.freq = parameters.freq
        # print len(self.first_list[0].normalized_features), u'длина нормализованных фич'
        for word in self.first_list:
            word.same = [word.normalized_features[i] for i in self.same]
            # word.diff = word.normalized_features[different]
        for word in self.second_list:
            word.same = [word.normalized_features[i] for i in self.same]

        if self.freq == 1:
            self.change_frequency()

    def change_frequency(self):
        for word in self.first_list:
            word.features[6] = word.log_freq
        for word in self.second_list:
            word.features[6] = word.log_freq
        # print u'done freq'

    def add_first(self):
        self.first_list += self.first_list_output
        self.second_list += self.second_list_output

        self.first_list_output = []
        self.second_list_output = []

        index = random.randint(0, len(self.first_list)-1)
        self.first_list_output.append(self.first_list[index])
        del self.first_list[index]

        index = random.randint(0, len(self.second_list)-1)
        self.second_list_output.append(self.second_list[index])
        del self.second_list[index]

    def add_closest(self):
        distance_for_first_list = []
        for i in xrange(self.number_of_same):
            distance_for_first_list.append(mean([word.same[i] for word in self.second_list_output]))
        minimum = self.number_of_same
        index = 0
        for i in xrange(len(self.first_list)):
            from_distance = sum([abs(self.first_list[i].same[j] - distance_for_first_list[j]) for j in xrange(self.number_of_same)])
            if from_distance < minimum:
                minimum = from_distance
                index = i
        self.first_list_output.append(self.first_list[index])
        del self.first_list[index]

        distance_for_second_list = []
        for i in xrange(self.number_of_same):
            distance_for_second_list.append(mean([word.same[i] for word in self.first_list_output]))
        minimum = self.number_of_same
        index = 0
        for i in xrange(len(self.second_list)):
            from_distance = sum([abs(self.second_list[i].same[j] - distance_for_second_list[j]) for j in xrange(self.number_of_same)])
            if from_distance < minimum:
                minimum = from_distance
                index = i
        self.second_list_output.append(self.second_list[index])
        del self.second_list[index]

    def sharp(self):
        return len(self.first_list_output) != self.length

    def less(self):
        return len(self.first_list_output) < self.length

    def equal(self):
        return len(self.first_list_output) == self.length

    def test(self, arr1, arr2):
        if self.statistics == 1:
            p_value = stats.ttest_ind(arr1, arr2)[1]
        elif self.statistics == 2:
            p_value = stats.ttest_ind(arr1, arr2, False)[1]
        elif self.statistics == 3:
            if equal(arr1, arr2):
                p_value = 1
            else:
                p_value = stats.mannwhitneyu(arr1, arr2)[1]
        return p_value


class Word:
    def __init__(self):
        self.name = u''
        self.features = {
            'part': None,
            'arguments': None,
            'reflexivity': None,
            'instrumentality': None,
            'relation': None
        }
        self.normalized_features = dict()
        self.same = 0
        self.value_of_differ_feature = 0
        self.distance = 1
        self.vector = []
        self.log_freq = None

    def __gt__(self, other):
        return self.value_of_differ_feature > other.value_of_differ_feature

    def __lt__(self, other):
        return self.value_of_differ_feature < other.value_of_differ_feature

    def __eq__(self, other):
        return self.value_of_differ_feature == other.value_of_differ_feature


def equal(arr1, arr2):
    ref = arr1[0]
    for el in arr1[2:] + arr2:
        if el != ref:
            return False
    return True


def mean(arr):
    return sum(arr)/len(arr) if len(arr) > 0 else None


def compensate(higher, lower, i):
    lowest_from_rest = 1
    first_list_index = 0
    for j in xrange(len(higher)):
        if higher[j].normalized_features[i] < lowest_from_rest:
            lowest_from_rest = higher[j].normalized_features[i]
            first_list_index = j

    highest_from_rest = 0
    second_list_index = 0
    for j in xrange(len(lower)):
        if lower[j].normalized_features[i] > highest_from_rest:
            highest_from_rest = lower[j].normalized_features[i]
            second_list_index = j

    return first_list_index, second_list_index


def is_match(database_word, client_word_parameters):
    for feature in client_word_parameters['features']:

        # Берем только те, которые нам важны
        if client_word_parameters['features'][feature]['matters']:

            # если это категориальная фича, просто сравниваем значение
            if client_word_parameters['features'][feature]['categorical']:
                if client_word_parameters['features'][feature]['value'] != database_word.features[feature]:
                    return False

            # если это континуальная фича, то должна попадать в диапазон
            else:
                # print client_word_parameters['features'][feature]['value']
                # print database_word.features[feature]
                # print float(client_word_parameters['features'][feature]['value'][0]) <= database_word.features[feature] <= float(client_word_parameters['features'][feature]['value'][1])

                if not client_word_parameters['features'][feature]['value'][0]:
                    client_word_parameters['features'][feature]['value'][0] = -float('inf')
                if not client_word_parameters['features'][feature]['value'][1]:
                    client_word_parameters['features'][feature]['value'][1] = float('inf')

                if not float(client_word_parameters['features'][feature]['value'][0]) <= database_word.features[feature] <= float(client_word_parameters['features'][feature]['value'][1]):
                    return False
    return True

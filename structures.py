# -*- coding:utf-8 -*-

import random
import codecs
import zipfile
from scipy import stats

__author__ = 'Gree-gorey'


class Store:
    def __init__(self):
        self.min = []
        self.max = []
        self.first_list = []
        self.second_list = []
        self.nouns = []
        self.verbs = []
        self.first_list_output = []
        self.second_list_output = []
        self.minimum = None
        self.arr = []
        self.nouns_min = []
        self.nouns_max = []
        self.verbs_min = []
        self.verbs_max = []
        self.length = 0
        self.number_of_same = 0
        self.allow = True
        self.same = []

    def read_words(self, f, pos):
        j = 0
        for line in f:
            line = line.rstrip(u'\n').split(u'\t')
            self.arr.append(Word())
            self.arr[-1].name = line[0]
            self.arr[-1].features = [float(x) for x in line[1::]]
            if j == 0:
                self.min += self.arr[-1].features
                self.max += self.arr[-1].features
            for i in xrange(len(self.arr[-1].features)):
                if self.arr[-1].features[i] < self.min[i]:
                    self.min[i] = self.arr[-1].features[i]
                if self.arr[-1].features[i] > self.max[i]:
                    self.max[i] = self.arr[-1].features[i]
            j += 1
        if pos == u'noun':
            self.nouns += self.arr
            self.arr = []
            self.nouns_min = self.min
            self.nouns_max = self.max
        elif pos == u'verb':
            self.verbs += self.arr
            self.arr = []
            self.verbs_min = self.min
            self.verbs_max = self.max

    def normalize(self):
        for word in self.nouns:
            word.normalized_features += word.features
            for i in xrange(len(word.features)):
                word.normalized_features[i] = (word.features[i] - self.nouns_min[i]) / (self.nouns_max[i] - self.nouns_min[i])
        for word in self.verbs:
            word.normalized_features += word.features
            for i in xrange(len(word.features)):
                word.normalized_features[i] = (word.features[i] - self.verbs_min[i]) / (self.verbs_max[i] - self.verbs_min[i])

    def create_zip(self):
        with codecs.open(u'./data/list_1.csv', u'w', u'utf-8') as w:
            w.write(self.first_list_output)

        with codecs.open(u'./data/list_2.csv', u'w', u'utf-8') as w:
            w.write(self.second_list_output)

        z = zipfile.ZipFile(u'output.zip', u'w')
        z.write(u'./data/list_1.csv')
        z.write(u'./data/list_2.csv')

    def test_and_fix(self):
        for i in self.same:
            p_value_same = test([word.normalized_features[i] for word in self.first_list_output],
                                [word.normalized_features[i] for word in self.second_list_output])

            if p_value_same < 0.1:
                first_list_mean = mean([word.normalized_features[i] for word in self.first_list_output])
                second_list_mean = mean([word.normalized_features[i] for word in self.second_list_output])

                if self.sharp():
                    self.first_list.append(self.first_list_output.pop(random.randint(0, len(self.first_list_output)-1)))
                    self.second_list.append(self.second_list_output.pop(random.randint(0, len(self.second_list_output)-1)))

                if first_list_mean > second_list_mean:
                    hhh, lll = compensate(self.first_list, self.second_list, i)
                    self.first_list_output.append(self.first_list[hhh])
                    self.second_list_output.append(self.second_list[lll])
                else:
                    hhh, lll = compensate(self.second_list, self.first_list, i)
                    self.first_list_output.append(self.first_list[lll])
                    self.second_list_output.append(self.second_list[hhh])

                for k in self.same:
                    p_value_same = test([word.normalized_features[k] for word in self.first_list_output],
                                        [word.normalized_features[k] for word in self.second_list_output])

                    if p_value_same < 0.05:
                        self.allow = False

    def setup_parameters(self, same, length, different=None):
        self.same = same
        self.number_of_same = len(same)
        self.length = length
        if not different:
            self.first_list += self.nouns
            self.second_list += self.verbs
        for word in self.first_list:
            word.same = [word.normalized_features[i] for i in same]
            # noun.diff = noun.normalized_features[different]
        for word in self.second_list:
            word.same = [word.normalized_features[i] for i in same]

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


class Word:
    def __init__(self):
        self.name = u''
        self.features = []
        self.normalized_features = []
        self.same = 0
        self.diff = 0
        self.distance = 1

    def __gt__(self, other):
        return self.diff > other.diff

    def __lt__(self, other):
        return self.diff < other.diff

    def __eq__(self, other):
        return self.diff == other.diff


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


def test(arr1, arr2):
    # shapiro_first = stats.shapiro(arr1)[1]
    # shapiro_second = stats.shapiro(arr2)[1]
    # if shapiro_first < 0.05 or shapiro_second < 0.05:
    #     p_value = stats.mannwhitneyu(arr1, arr2)[1]
    # else:
    #     # levene = stats.levene(arr1, arr2)[1]
    #     # if levene < 0.05:
    #     #     p_value = stats.ttest_ind(arr1, arr2, False)[1]
    #     # else:
    p_value = stats.ttest_ind(arr1, arr2)[1]
    return p_value

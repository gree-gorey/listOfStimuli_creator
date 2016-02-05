# -*- coding:utf-8 -*-

import random
import time
import codecs
import pickle
import copy
from scipy import stats

__author__ = 'Gree-gorey'

t1 = time.time()


class Store:
    def __init__(self):
        self.words = []
        self.min = []
        self.max = []
        self.high = []
        self.low = []
        self.high_output = []
        self.low_output = []
        self.minimum = None


class Noun:
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
    hhh = 0
    for j in xrange(len(higher)):
        if higher[j].normalized_features[i] < lowest_from_rest:
            lowest_from_rest = higher[j].normalized_features[i]
            hhh = j

    highest_from_rest = 0
    lll = 0
    for j in xrange(len(lower)):
        if lower[j].normalized_features[i] > highest_from_rest:
            highest_from_rest = lower[j].normalized_features[i]
            lll = j

    return hhh, lll


newStore = Store()

with codecs.open(u'/home/gree-gorey/stimdb/nouns.csv', u'r', u'utf-8') as f:
    j = 0
    for line in f:
        line = line.rstrip(u'\n').split(u'\t')
        newStore.high.append(Noun())
        newStore.high[-1].name = line[0]
        newStore.high[-1].features = [float(x) for x in line[1::]]
        if j == 0:
            newStore.min = copy.deepcopy(newStore.high[-1].features)
            newStore.max = copy.deepcopy(newStore.high[-1].features)
        for i in xrange(len(newStore.high[-1].features)):
            if newStore.high[-1].features[i] < newStore.min[i]:
                newStore.min[i] = newStore.high[-1].features[i]
            if newStore.high[-1].features[i] > newStore.max[i]:
                newStore.max[i] = newStore.high[-1].features[i]
        j += 1

with codecs.open(u'/home/gree-gorey/stimdb/verbs.csv', u'r', u'utf-8') as f:
    j = 0
    for line in f:
        line = line.rstrip(u'\n').split(u'\t')
        newStore.low.append(Noun())
        newStore.low[-1].name = line[0]
        newStore.low[-1].features = [float(x) for x in line[1::]]
        if j == 0:
            newStore.min = copy.deepcopy(newStore.low[-1].features)
            newStore.max = copy.deepcopy(newStore.low[-1].features)
        for i in xrange(len(newStore.low[-1].features)):
            if newStore.low[-1].features[i] < newStore.min[i]:
                newStore.min[i] = newStore.low[-1].features[i]
            if newStore.low[-1].features[i] > newStore.max[i]:
                newStore.max[i] = newStore.low[-1].features[i]
        j += 1


parameters = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# parameters = [1, 2, 3, 4, 8, 9]
# different = 7
N = len(parameters)


for word in newStore.high:
    word.normalized_features = copy.deepcopy(word.features)
    for i in xrange(len(word.features)):
        word.normalized_features[i] = (word.features[i] - newStore.min[i]) / (newStore.max[i] - newStore.min[i])
    word.same = [word.normalized_features[i] for i in parameters]
    # noun.diff = noun.normalized_features[different]

for word in newStore.low:
    word.normalized_features = copy.deepcopy(word.features)
    for i in xrange(len(word.features)):
        word.normalized_features[i] = (word.features[i] - newStore.min[i]) / (newStore.max[i] - newStore.min[i])
    word.same = [word.normalized_features[i] for i in parameters]

# newStore.backup_low = copy.deepcopy(newStore.low)
# newStore.backup_high = copy.deepcopy(newStore.high)

while len(newStore.high_output) != 150:
    newStore.low += newStore.low_output
    newStore.high += newStore.high_output

    newStore.low_output = []
    newStore.high_output = []

    index = random.randint(0, len(newStore.low)-1)

    newStore.low_output.append(newStore.low[index])
    del newStore.low[index]

    index = random.randint(0, len(newStore.high)-1)

    newStore.high_output.append(newStore.high[index])
    del newStore.high[index]

    allow = True
    end = False
    p_value_diff = 0

    while allow and len(newStore.high_output) < 150:
        distance_for_low = []
        for i in xrange(N):
            distance_for_low.append(mean([word.same[i] for word in newStore.high_output]))

        minimum = N
        index = 0
        for i in xrange(len(newStore.low)):
            from_distance = sum([abs(newStore.low[i].same[j] - distance_for_low[j]) for j in xrange(N)])
            if from_distance < minimum:
                minimum = from_distance
                index = i

        newStore.low_output.append(newStore.low[index])
        del newStore.low[index]

        distance_for_high = []
        for i in xrange(N):
            distance_for_high.append(mean([word.same[i] for word in newStore.low_output]))

        minimum = N
        index = 0
        for i in xrange(len(newStore.high)):
            from_distance = sum([abs(newStore.high[i].same[j] - distance_for_high[j]) for j in xrange(N)])
            if from_distance < minimum:
                minimum = from_distance
                index = i

        newStore.high_output.append(newStore.high[index])
        del newStore.high[index]

        if len(newStore.high_output) > 15:
            # p_value_diff = stats.ttest_ind([noun.normalized_features[different] for noun in newStore.high_output],
            #                                [noun.normalized_features[different] for noun in newStore.low_output])[1]

            for i in parameters:
                p_value_same = stats.ttest_ind([word.normalized_features[i] for word in newStore.high_output],
                                               [word.normalized_features[i] for word in newStore.low_output])[1]

                # if p_value_same < 0.05:
                if p_value_same < 0.1:
                    high_mean = mean([word.normalized_features[i] for word in newStore.high_output])
                    low_mean = mean([word.normalized_features[i] for word in newStore.low_output])

                    if high_mean > low_mean:
                        hhh, lll = compensate(newStore.high, newStore.low, i)
                        newStore.high_output.append(newStore.high[hhh])
                        newStore.low_output.append(newStore.low[lll])
                    else:
                        hhh, lll = compensate(newStore.low, newStore.high, i)
                        newStore.high_output.append(newStore.high[lll])
                        newStore.low_output.append(newStore.low[hhh])

                    for k in parameters:
                        p_value_same = stats.ttest_ind([noun.normalized_features[k] for noun in newStore.high_output],
                                                       [noun.normalized_features[k] for noun in newStore.low_output])[1]

                        if p_value_same < 0.05:
                            end = True

        if end or p_value_diff > 0.05:
            allow = False

print len(newStore.high_output), len(newStore.low_output)

for i in xrange(6):
    print newStore.low_output[i].name

# w = codecs.open(u'/home/gree-gorey/stimdb/nouns.p', u'w', u'utf-8')
# pickle.dump(newStore, w)
# w.close()

# pickle.load(f)

for i in parameters:
    p_value_same = stats.ttest_ind([noun.normalized_features[i] for noun in newStore.high_output],
                                       [noun.normalized_features[i] for noun in newStore.low_output])[1]

    print p_value_same

print '\n######################################\n'

# with codecs.open(u'/home/gree-gorey/stimdb/high.csv', u'w', u'utf-8') as w:
#     for word in newStore.high_output:
#         w.write(word.name + u'\t' + u'\t'.join([str(f) for f in word.features]) + u'\n')
#
# with codecs.open(u'/home/gree-gorey/stimdb/low.csv', u'w', u'utf-8') as w:
#     for word in newStore.low_output:
#         w.write(word.name + u'\t' + u'\t'.join([str(f) for f in word.features]) + u'\n')

t2 = time.time()

print t2 - t1


# -*- coding:utf-8 -*-

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


newStore = Store()

#
# with codecs.open(u'/home/gree-gorey/stimdb/nouns.csv', u'r', u'utf-8') as f:
#     j = 0
#     for line in f:
#         line = line.rstrip(u'\n').split(u'\t')
#         newStore.words.append(Noun())
#         newStore.words[-1].name = line[0]
#         newStore.words[-1].features = [float(x) for x in line[1::]]
#         if j == 0:
#             newStore.min = copy.deepcopy(newStore.words[-1].features)
#             newStore.max = copy.deepcopy(newStore.words[-1].features)
#         for i in xrange(len(newStore.words[-1].features)):
#             if newStore.words[-1].features[i] < newStore.min[i]:
#                 newStore.min[i] = newStore.words[-1].features[i]
#             if newStore.words[-1].features[i] > newStore.max[i]:
#                 newStore.max[i] = newStore.words[-1].features[i]
#         j += 1

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


# newStore.low = copy.deepcopy(sorted(newStore.words)[:len(newStore.words)/2:])
# newStore.high = copy.deepcopy(sorted(newStore.words)[len(newStore.words)/2::])

# print mean([word.same[0] for word in newStore.low]), mean([word.same[0] for word in newStore.high])
# print mean([word.same[1] for word in newStore.low]), mean([word.same[1] for word in newStore.high])

distance = []
for i in xrange(N):
    distance.append((mean([word.same[i] for word in newStore.low]) + mean([word.same[i] for word in newStore.high])) / 2)

# print distance

minimum = N
index = 0
for i in xrange(len(newStore.low)):
    from_distance = sum([abs(newStore.low[i].same[j] - distance[j]) for j in xrange(N)])
    if from_distance < minimum:
        minimum = from_distance
        index = i

newStore.low_output.append(newStore.low[index])
del newStore.low[index]

# print newStore.low_output[0].same

minimum = N
index = 0
for i in xrange(len(newStore.high)):
    from_distance = sum([abs(newStore.high[i].same[j] - distance[j]) for j in xrange(N)])
    if from_distance < minimum:
        minimum = from_distance
        index = i

newStore.high_output.append(newStore.high[index])
del newStore.high[index]

# print newStore.high_output[0].same

allow = True
end = False
p_value_diff = 0

# while len(newStore.high_output) < 40:

while allow:
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
            p_value_same = stats.ttest_ind([noun.normalized_features[i] for noun in newStore.high_output],
                                           [noun.normalized_features[i] for noun in newStore.low_output])[1]

            if p_value_same < 0.05:
                end = True

    if end or p_value_diff > 0.05:
        allow = False

print len(newStore.high_output)

# w = codecs.open(u'/home/gree-gorey/stimdb/nouns.p', u'w', u'utf-8')
# pickle.dump(newStore, w)
# w.close()

# pickle.load(f)

# with codecs.open(u'/home/gree-gorey/stimdb/high.csv', u'w', u'utf-8') as w:
#     for word in newStore.high_output:
#         w.write(word.name + u'\t' + u'\t'.join([str(f) for f in word.features]) + u'\n')
#
# with codecs.open(u'/home/gree-gorey/stimdb/low.csv', u'w', u'utf-8') as w:
#     for word in newStore.low_output:
#         w.write(word.name + u'\t' + u'\t'.join([str(f) for f in word.features]) + u'\n')

t2 = time.time()

print t2 - t1


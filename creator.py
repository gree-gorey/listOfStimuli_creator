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


with codecs.open(u'/home/gree-gorey/stimdb/nouns.csv', u'r', u'utf-8') as f:
    newStore = Store()
    j = 0
    for line in f:
        line = line.rstrip(u'\n').split(u'\t')
        newStore.words.append(Noun())
        newStore.words[-1].name = line[0]
        newStore.words[-1].features = [float(x) for x in line[1::]]
        if j == 0:
            newStore.min = copy.deepcopy(newStore.words[-1].features)
            newStore.max = copy.deepcopy(newStore.words[-1].features)
        for i in xrange(len(newStore.words[-1].features)):
            if newStore.words[-1].features[i] < newStore.min[i]:
                newStore.min[i] = newStore.words[-1].features[i]
            if newStore.words[-1].features[i] > newStore.max[i]:
                newStore.max[i] = newStore.words[-1].features[i]
        j += 1

# for noun in sorted(newStore.words):
#     print noun.name, noun.age


def mean(arr):
    return sum(arr)/len(arr) if len(arr) > 0 else None

# print newStore.min, newStore.max

for noun in newStore.words:
    noun.normalized_features = copy.deepcopy(noun.features)
    for i in xrange(len(noun.features)):
        noun.normalized_features[i] = (noun.features[i] - newStore.min[i]) / (newStore.max[i] - newStore.min[i])
    # noun.same = (sum(x**2 for x in noun.features[7:8]))**1/2
    # noun.diff = (sum(x**2 for x in noun.features[:3]))**1/2
    noun.same = noun.normalized_features[9]
    noun.diff = noun.normalized_features[7]

newStore.low = copy.deepcopy(sorted(newStore.words)[:len(newStore.words)/2:])
newStore.high = copy.deepcopy(sorted(newStore.words)[len(newStore.words)/2::])

# print mean([word.same for word in newStore.low]), mean([word.same for word in newStore.high])

distance = (mean([word.same for word in newStore.low]) + mean([word.same for word in newStore.high])) / 2

minimum = 1
index = 0
for i in xrange(len(newStore.low)):
    if abs(newStore.low[i].same - distance) < minimum:
        minimum = abs(newStore.low[i].same - distance)
        index = i

newStore.low_output.append(newStore.low[index])
del newStore.low[index]

minimum = 1
index = 0
for i in xrange(len(newStore.high)):
    if abs(newStore.high[i].same - distance) < minimum:
        minimum = abs(newStore.high[i].same - distance)
        index = i

newStore.high_output.append(newStore.high[index])
del newStore.high[index]

while len(newStore.high_output) < 30:
    distance_for_low = mean([word.same for word in newStore.high_output])
    minimum = 1
    index = 0
    for i in xrange(len(newStore.low)):
        if abs(newStore.low[i].same - distance_for_low) < minimum:
            minimum = abs(newStore.low[i].same - distance_for_low)
            index = i
    newStore.low_output.append(newStore.low[index])
    del newStore.low[index]

    distance_for_high = mean([word.same for word in newStore.low_output])
    minimum = 1
    index = 0
    for i in xrange(len(newStore.high)):
        if abs(newStore.high[i].same - distance_for_high) < minimum:
            minimum = abs(newStore.high[i].same - distance_for_high)
            index = i
    newStore.high_output.append(newStore.high[index])
    del newStore.high[index]

# for high_noun in sorted(newStore.words, reverse=True):
#     if len(newStore.high) < 30:
#         newStore.high.append(high_noun)
#         for low_noun in sorted(newStore.words)[:len(newStore.words)/2:]:
#             length = (low_noun.diff**2 + high_noun.same**2)**1/2
#             if length < newStore.minimum.distance:
#                 newStore.minimum = copy.deepcopy(low_noun)
#         newStore.low.append(newStore.minimum)
#     else:
#         break

print mean([word.diff for word in newStore.low_output]), mean([word.diff for word in newStore.high_output])
print mean([word.same for word in newStore.low_output]), mean([word.same for word in newStore.high_output])

print u'\n##########################\n'

print stats.ttest_ind([noun.diff for noun in newStore.high_output], [noun.diff for noun in newStore.low_output])
print stats.ttest_ind([noun.same for noun in newStore.high_output], [noun.same for noun in newStore.low_output])

print u'\n##########################\n'

# w = codecs.open(u'/home/gree-gorey/stimdb/nouns.p', u'w', u'utf-8')
# pickle.dump(newStore, w)
# w.close()

# pickle.load(f)

with codecs.open(u'/home/gree-gorey/stimdb/high.csv', u'w', u'utf-8') as w:
    for word in newStore.high_output:
        w.write(word.name + u'\t' + u'\t'.join([str(f) for f in word.features]) + u'\n')

with codecs.open(u'/home/gree-gorey/stimdb/low.csv', u'w', u'utf-8') as w:
    for word in newStore.low_output:
        w.write(word.name + u'\t' + u'\t'.join([str(f) for f in word.features]) + u'\n')

t2 = time.time()

print t2 - t1


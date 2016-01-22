# -*- coding:utf-8 -*-

import time
import codecs
import pickle
import copy

__author__ = 'Gree-gorey'

t1 = time.time()


class Store:
    def __init__(self):
        self.words = []
        self.min = []
        self.max = []


class Noun:
    def __init__(self):
        self.name = u''
        self.features = []

    def __gt__(self, other):
        return self.features[1] > other.features[1]

    def __lt__(self, other):
        return self.features[1] < other.features[1]

    def __eq__(self, other):
        return self.features[1] == other.features[1]


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

print newStore.min, newStore.max

for noun in newStore.words:
    for i in xrange(len(noun.features)):
        noun.features[i] = (noun.features[i] - newStore.min[i]) / (newStore.max[i] - newStore.min[i])

for noun in newStore.words:
    if noun.features[4] == 0:
        print noun.features[4]

# w = codecs.open(u'/home/gree-gorey/stimdb/nouns.p', u'w', u'utf-8')
# pickle.dump(newStore, w)
# w.close()

# pickle.load(f)

t2 = time.time()

print t2 - t1

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
        self.minimum = None


class Noun:
    def __init__(self):
        self.name = u''
        self.features = []
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

# print newStore.min, newStore.max

for noun in newStore.words:
    for i in xrange(len(noun.features)):
        noun.features[i] = (noun.features[i] - newStore.min[i]) / (newStore.max[i] - newStore.min[i])
    noun.same = (sum(x**2 for x in noun.features[7:8]))**1/2
    noun.diff = (sum(x**2 for x in noun.features[:3]))**1/2

newStore.minimum = copy.deepcopy(newStore.words[0])

for high_noun in sorted(newStore.words, reverse=True):
    if len(newStore.high) < 30:
        newStore.high.append(high_noun)
        for low_noun in sorted(newStore.words)[:len(newStore.words)/2:]:
            length = (low_noun.diff**2 + high_noun.same**2)**1/2
            if length < newStore.minimum.distance:
                newStore.minimum = copy.deepcopy(low_noun)
        newStore.low.append(newStore.minimum)
    else:
        break

print sum([noun.diff for noun in newStore.high])/len(newStore.high)
print sum([noun.diff for noun in newStore.low])/len(newStore.low)
print sum([noun.same for noun in newStore.high])/len(newStore.high)
print sum([noun.same for noun in newStore.low])/len(newStore.low)

print u'\n##########################\n'

print stats.ttest_ind([noun.diff for noun in newStore.high], [noun.diff for noun in newStore.low])
print stats.ttest_ind([noun.same for noun in newStore.high], [noun.same for noun in newStore.low])

print u'\n##########################\n'

# w = codecs.open(u'/home/gree-gorey/stimdb/nouns.p', u'w', u'utf-8')
# pickle.dump(newStore, w)
# w.close()

# pickle.load(f)

t2 = time.time()

print t2 - t1

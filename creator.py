# -*- coding:utf-8 -*-

import time
import codecs
import pickle

__author__ = 'Gree-gorey'

t1 = time.time()


class Store:
    def __init__(self):
        self.words = []


class Noun:
    def __init__(self):
        self.name = u''
        self.stability = None
        self.complexity = None
        self.familiarity = None
        self.age = None
        self.representability = None
        self.similarity = None
        self.frequency = None
        self.syl_length = None
        self.ph_length = None

    def __gt__(self, other):
        return self.age > other.age

    def __lt__(self, other):
        return self.age < other.age

    def __eq__(self, other):
        return self.age == other.age


with codecs.open(u'/home/gree-gorey/stimdb/nouns.csv', u'r', u'utf-8') as f:
    newStore = Store()
    for line in f:
        line = line.rstrip(u'\n').split(u'\t')
        newStore.words.append(Noun())
        newStore.words[-1].name = line[0]
        newStore.words[-1].stability = line[1]
        newStore.words[-1].complexity = line[2]
        newStore.words[-1].familiarity = line[3]
        newStore.words[-1].age = float(line[4])
        newStore.words[-1].representability = line[5]
        newStore.words[-1].similarity = line[6]
        newStore.words[-1].frequency = line[7]
        newStore.words[-1].syl_length = line[8]
        newStore.words[-1].ph_length = line[9]

# for noun in sorted(newStore.words):
#     print noun.name, noun.age

w = codecs.open(u'/home/gree-gorey/stimdb/nouns.p', u'w', u'utf-8')
pickle.dump(newStore, w)
w.close()

# pickle.load(f)

t2 = time.time()

print t2 - t1

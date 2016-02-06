# -*- coding:utf-8 -*-

import codecs
import pickle
from structures import Store

__author__ = 'Gree-gorey'


newStore = Store()


with codecs.open(u'/home/gree-gorey/stimdb/nouns.csv', u'r', u'utf-8') as f:
    newStore.read_nouns(f)

with codecs.open(u'/home/gree-gorey/stimdb/verbs.csv', u'r', u'utf-8') as f:
    newStore.read_verbs(f)

with codecs.open(u'/home/gree-gorey/stimdb/store.p', u'w', u'utf-8') as w:
    pickle.dump(newStore, w)

# -*- coding:utf-8 -*-

import codecs
import pickle
from structures import Store

__author__ = 'gree-gorey'


def main():
    new_store = Store()

    with codecs.open(u'/home/gree-gorey/stimdb/nouns.csv', u'r', u'utf-8') as f:
        new_store.read_nouns(f)

    with codecs.open(u'/home/gree-gorey/stimdb/verbs.csv', u'r', u'utf-8') as f:
        new_store.read_verbs(f)

    with codecs.open(u'/home/gree-gorey/Py/losc/store.p', u'w', u'utf-8') as w:
        pickle.dump(new_store, w)

if __name__ == '__main__':
    main()

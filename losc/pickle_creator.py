# -*- coding:utf-8 -*-

import codecs
import pickle
from structures import Store

__author__ = 'gree-gorey'


def main():
    new_store = Store()

    with codecs.open('data/nouns.tsv', 'r', 'utf-8') as f:
        new_store.read_nouns(f)

    with codecs.open('data/verbs.tsv', 'r', 'utf-8') as f:
        new_store.read_verbs(f)

    with codecs.open('data/store.p', 'w', 'utf-8') as w:
        pickle.dump(new_store, w)

if __name__ == '__main__':
    main()

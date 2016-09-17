# -*- coding:utf-8 -*-

import codecs
from store import Store, Word

__author__ = 'gree-gorey'

store = Store()

with codecs.open('./data/map.tsv', 'r', 'utf-8') as f:
    lines = f.readlines()

features_list = lines[0].rstrip().split('\t')[1::]

types = lines[1].rstrip().split('\t')[1::]

features_dict = dict(zip(features_list, types))

for feature in features_list:
    if features_dict[feature] == 'categorical':
        store.categorical_features[feature] = set()
    else:
        store.numeric_features.append(feature)

store.len_of_numeric = len(store.numeric_features)
store.len_of_categorical = len(store.categorical_features)

for line in lines[2::]:
    store.words.append(Word())

    columns = line.rstrip().split('\t')
    store.words[-1].name = columns[0]

    for feature, value in zip(features_list, columns[1::]):
        if features_dict[feature] == 'int':
            store.words[-1].features[feature] = int(value)
        elif features_dict[feature] == 'float':
            store.words[-1].features[feature] = float(value)
        else:
            store.words[-1].features[feature] = value
            if value != 'None':
                store.categorical_features[feature].add(value)

# -*- coding:utf-8 -*-

import pickle


# # загружаем базу данных в переменную
# with open(u'data/store.p', u'r') as f:
#     store = pickle.load(f)
#
# print store.verbs[0].features

print type(0.1) == float


class Parameters:
    def __init__(self):
        self.first_list = None
        self.second_list = None
        self.length = 800
        self.differ = 0
        self.statistics = None
        self.same = []

    def get_same(self, store):
        for i in xrange(9):
            if i != store.differ - 1:
                self.same.append(i)


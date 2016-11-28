# -*- coding:utf-8 -*-


class Word:
    def __init__(self):
        self.name = u''
        self.features = dict()
        self.normalized_features = dict()
        self.same = []  # это массив из значений фич, которые не должны отличаться
        self.value_of_differ_feature = 0
        self.distance = 1
        self.vector = []
        self.log_freq = None
        self.allowed = True

    def __gt__(self, other):
        return self.value_of_differ_feature > other.value_of_differ_feature

    def __lt__(self, other):
        return self.value_of_differ_feature < other.value_of_differ_feature

    def __eq__(self, other):
        return self.value_of_differ_feature == other.value_of_differ_feature

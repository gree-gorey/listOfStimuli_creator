# -*- coding:utf-8 -*-


class Word:
    def __init__(self):
        self.name = u''
        self.features = {
            'part': None,
            'arguments': None,
            'reflexivity': None,
            'instrumentality': None,
            'relation': None
        }
        self.normalized_features = dict()
        # это массив из значений фич, которые не должны отличаться
        self.same = []
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

# -*- coding:utf-8 -*-


class Parameters:
    def __init__(self):
        self.same = []
        self.differ = ''
        self.length = 800
        self.statistics = None
        self.frequency = None
        self.alpha = 0.05
        self.number_of_comparisons = 0
        self.bonferroni = 'off'

    def calculate_alpha(self):
        if self.differ != 'question':
            self.number_of_comparisons = len(self.same) + 1
        else:
            self.number_of_comparisons = len(self.same)

        self.alpha /= self.number_of_comparisons

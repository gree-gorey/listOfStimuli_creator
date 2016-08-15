# -*- coding:utf-8 -*-

from scipy import stats

a = [0, 1, 2, 4]

b = [0, 1, 2, 8]

#
# p = stats.levene(a, b)[1]

p = stats.shapiro(b)[1]

print p




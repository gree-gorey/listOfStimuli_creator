# -*- coding:utf-8 -*-

try:
    print float('0,01')
except ValueError as x:
    print x

try:
    print int('0.01')
except ValueError as x:
    print x
# from scipy import stats
# import numpy as np
# import csv
#
# with open('/home/gree-gorey/Py/slg/slg/static/output/list_1.tsv', 'rb') as f:
#     cf = csv.DictReader(f, delimiter="\t")
#     arr1 = []
#     for row in cf:
#         arr1.append(float(row['H']))
#
# with open('/home/gree-gorey/Py/slg/slg/static/output/list_2.tsv', 'rb') as f:
#     cf = csv.DictReader(f, delimiter="\t")
#     arr2 = []
#     for row in cf:
#         arr2.append(float(row['H']))

# print np.std(arr1, ddof=1)
# print np.std(arr1)

# arr1 = range(15)
# arr2 = range(13)
#
# result = stats.mannwhitneyu(arr1, arr2, alternative='two-sided')

# levene = stats.levene(arr1, arr2, center='median', proportiontocut=0.05)
# print levene
#
# result = stats.ttest_ind(arr1, arr2, False)
# print result
# kruskalwallis = stats.mstats.kruskalwallis(arr1, arr2)
# print kruskalwallis

# # result = stats.wilcoxon(arr1, arr2)
#
# # result = stats.ranksums(arr1, arr2)
#
# t_value = result[0]
# p_value = result[1]
#
# print result
#
# print t_value, p_value




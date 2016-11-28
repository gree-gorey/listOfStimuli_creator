# -*- coding:utf-8 -*-

from slg.store import Store
from slg.store import mean

store = Store()

store.read_dummy_data_and_setup()

store.normalize()

store.list_outputs['list_1'] = store.lists['list_1'][:2:]
store.lists['list_1'] = store.lists['list_1'][2::]

store.list_outputs['list_2'] = store.lists['list_2'][4::]
store.lists['list_2'] = store.lists['list_2'][:4:]

print [word.normalized_features['first'] for word in store.lists['list_1']]
print [word.normalized_features['first'] for word in store.lists['list_2']]
print [word.normalized_features['first'] for word in store.list_outputs['list_1']]
print [word.normalized_features['first'] for word in store.list_outputs['list_2']]

store.list_mean['list_1'] = mean([word.normalized_features['first'] for word in store.list_outputs['list_1']])
store.list_mean['list_2'] = mean([word.normalized_features['first'] for word in store.list_outputs['list_2']])

print store.list_mean['list_1']
print store.list_mean['list_2']

store.compensate('first')

print [word.normalized_features['first'] for word in store.lists['list_1']]
print [word.normalized_features['first'] for word in store.lists['list_2']]
print [word.normalized_features['first'] for word in store.list_outputs['list_1']]
print [word.normalized_features['first'] for word in store.list_outputs['list_2']]

store.list_mean['list_1'] = mean([word.normalized_features['first'] for word in store.list_outputs['list_1']])
store.list_mean['list_2'] = mean([word.normalized_features['first'] for word in store.list_outputs['list_2']])

print store.list_mean['list_1']
print store.list_mean['list_2']

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




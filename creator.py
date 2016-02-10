# -*- coding:utf-8 -*-

import time
import pickle
from scipy import stats
from face import Parameters

__author__ = 'Gree-gorey'

t1 = time.time()

with open(u'/home/gree-gorey/stimdb/store.p', u'r') as f:
    newStore = pickle.load(f)

same = [0, 1, 2, 3, 4, 5, 6, 7, 8]
# same = [1, 2, 8, 9]
# different = 7
length = 100

p = Parameters()
p.get_parameters()

# newStore.setup_parameters(same, length, arg=2, part=2)
newStore.setup_parameters(p)


while newStore.sharp():
    newStore.add_first()

    p_value_diff = 0
    newStore.allow = True

    while newStore.allow and newStore.less():
        newStore.add_closest()
        if len(newStore.first_list_output) > 15:
            newStore.test_and_fix()


def test(arr1, arr2):
    # shapiro_first = stats.shapiro(arr1)[1]
    # shapiro_second = stats.shapiro(arr2)[1]
    # if shapiro_first < 0.05 or shapiro_second < 0.05:
    #     p_value = stats.mannwhitneyu(arr1, arr2)[1]
    # else:
    #     # levene = stats.levene(arr1, arr2)[1]
    #     # if levene < 0.05:
    #     #     p_value = stats.ttest_ind(arr1, arr2, False)[1]
    #     # else:
    p_value = stats.ttest_ind(arr1, arr2, False)[1]
    # p_value = stats.mannwhitneyu(arr1, arr2)[1]
    return p_value


print len(newStore.first_list_output), len(newStore.second_list_output)
print len(newStore.first_list), len(newStore.second_list)

print '\n######################################\n'

# p_value_diff = stats.ttest_ind([noun.normalized_features[different] for noun in newStore.first_list_output],
# [noun.normalized_features[different] for noun in newStore.second_list_output])[1]

# for i in xrange(6):
#     print newStore.second_list_output[i].name

for i in newStore.same:
    # p_value_same = stats.ttest_ind([word.normalized_features[i] for word in newStore.first_list_output],
    #                                [word.normalized_features[i] for word in newStore.second_list_output], False)[1]

    p_value_same = test([word.normalized_features[i] for word in newStore.first_list_output],
                        [word.normalized_features[i] for word in newStore.second_list_output])

    # p_mann = stats.mannwhitneyu([word.normalized_features[i] for word in newStore.first_list_output],
    #                             [word.normalized_features[i] for word in newStore.second_list_output])[1]

    # levene = stats.levene([word.normalized_features[i] for word in newStore.first_list_output],
    #                       [word.normalized_features[i] for word in newStore.second_list_output])[1]
    # print '\n##################\n'
    print p_value_same

    # print '\n###\n'
    # shapiro_first = stats.shapiro([word.normalized_features[i] for word in newStore.first_list_output])
    # shapiro_second = stats.shapiro([word.normalized_features[i] for word in newStore.second_list_output])
    # print shapiro_first, shapiro_second

print '\n######################################\n'

# with codecs.open(u'/home/gree-gorey/stimdb/first_list.csv', u'w', u'utf-8') as w:
#     for word in newStore.first_list_output:
#         w.write(word.name + u'\t' + u'\t'.join([str(f) for f in word.features]) + u'\n')
#
# with codecs.open(u'/home/gree-gorey/stimdb/second_list.csv', u'w', u'utf-8') as w:
#     for word in newStore.second_list_output:
#         w.write(word.name + u'\t' + u'\t'.join([str(f) for f in word.features]) + u'\n')

t2 = time.time()

print t2 - t1


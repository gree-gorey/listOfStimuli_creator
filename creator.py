# -*- coding:utf-8 -*-

import time
import pickle
from scipy import stats
from face import Parameters

__author__ = 'Gree-gorey'

with open(u'/home/gree-gorey/stimdb/store.p', u'r') as f:
    newStore = pickle.load(f)

p = Parameters()
p.get_parameters(newStore)

print p.first_list.vector, p.second_list.vector

newStore.setup_parameters(p)

t1 = time.time()


while newStore.sharp():
    newStore.add_first()

    p_value_diff = 0
    newStore.allow = True

    while newStore.allow and newStore.less():
        newStore.add_closest()
        if len(newStore.first_list_output) > 15:
            newStore.test_and_fix()


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

    p_value_same = newStore.test([word.normalized_features[i] for word in newStore.first_list_output],
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


# -*- coding:utf-8 -*-

import time
import pickle
from scipy import stats

__author__ = 'Gree-gorey'

t1 = time.time()


with open(u'/home/gree-gorey/stimdb/store.p', u'r') as f:
    newStore = pickle.load(f)

# same = [1, 2, 3, 4, 5, 6, 7, 8, 9]
same = [1, 2, 8, 9]
# different = 7
length = 50

newStore.setup_parameters(same, length)

while newStore.sharp():
    newStore.add_first()

    end = False
    p_value_diff = 0

    while newStore.allow and newStore.less():
        newStore.add_closest()
        if len(newStore.first_list_output) > 15:
            newStore.test_and_fix()

print len(newStore.first_list_output), len(newStore.second_list_output)

print '\n######################################\n'

# p_value_diff = stats.ttest_ind([noun.normalized_features[different] for noun in newStore.first_list_output],
# [noun.normalized_features[different] for noun in newStore.second_list_output])[1]

# for i in xrange(6):
#     print newStore.second_list_output[i].name

for i in newStore.same:
    p_value_same = stats.ttest_ind([noun.normalized_features[i] for noun in newStore.first_list_output],
                                       [noun.normalized_features[i] for noun in newStore.second_list_output])[1]

    print p_value_same

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


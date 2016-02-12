# -*- coding:utf-8 -*-

import time
import pickle

__author__ = 'Gree-gorey'


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

for i in xrange(9):
    p_value_same = newStore.test([word.normalized_features[i] for word in newStore.first_list_output],
                                 [word.normalized_features[i] for word in newStore.second_list_output])

    print p_value_same

print '\n######################################\n'

i = newStore.differ - 1
if i != 0:
    p_value_differ = newStore.test([word.normalized_features[i] for word in newStore.first_list_output],
                                   [word.normalized_features[i] for word in newStore.second_list_output])

print p_value_differ

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


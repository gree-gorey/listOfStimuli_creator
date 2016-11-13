# -*- coding:utf-8 -*-

import codecs

with codecs.open('./data/verbs.tsv', 'r', 'utf-8') as f:
    lines = f.readlines()

with codecs.open('./data/verbs_new.tsv', 'w', 'utf-8') as w:

    for line in lines:
        new_line = list()

        columns = line.rstrip().split('\t', 18)
        name = u'{}. {} ({})'.format(columns[0], columns[1], columns[2])
        new_line.append(name)

        new_line += columns[3::]

        w.write(u'\t'.join(new_line) + u'\n')




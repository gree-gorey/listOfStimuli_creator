# -*- coding:utf-8 -*-

__author__ = 'Gree-gorey'


class List:
    def __init__(self):
        self.pos = None
        self.part = None
        self.arguments = None
        self.reflexivity = None
        self.instrumentality = None
        self.relation = None


class Parameters:
    def __init__(self):
        self.first_list = None
        self.second_list = None
        self.length = None
        self.differ = None
        self.statistics = None

    def get_parameters(self):
        print u'Please, specify the parameters for the 1st list:'
        self.first_list = List()

        self.first_list.pos = input(u'\n1 - verbs\n2 - nouns\nChoose part of speech: ')

        if self.first_list.pos == 1:
            self.first_list.arguments = input(u'\n0 - irrelevant\n1 - one argument\n2 - two arguments\nChoose number of arguments: ')
            self.first_list.reflexivity = input(u'\n0 - irrelevant\n1 - reflexive\n2 - non-reflexive\nChoose reflexivity: ')
            self.first_list.instrumentality = input(u'\n0 - irrelevant\n1 - instrumental\n2 - non-instrumental\nChoose instrumentality: ')
            self.first_list.relation = input(u'\n0 - irrelevant\n1 - true \n2 - false\nChoose name relation: ')
        elif self.first_list.pos == 2:
            self.first_list.part = input(u'\n0 - irrelevant\n1 - first part \n2 - second part\nChoose the part: ')

        print u'\nPlease, specify the parameters for the 2st list:'
        self.second_list = List()

        self.second_list.pos = input(u'\n1 - verbs\n2 - nouns\nChoose part of speech: ')

        if self.second_list.pos == 1:
            self.second_list.arguments = input(u'\n0 - irrelevant\n1 - one argument\n2 - two arguments\nChoose number of arguments: ')
            self.second_list.reflexivity = input(u'\n0 - irrelevant\n1 - reflexive\n2 - non-reflexive\nChoose reflexivity: ')
            self.second_list.instrumentality = input(u'\n0 - irrelevant\n1 - instrumental\n2 - non-instrumental\nChoose instrumentality: ')
            self.second_list.relation = input(u'\n0 - irrelevant\n1 - true \n2 - false\nChoose name relation: ')
        elif self.second_list.pos == 2:
            self.second_list.part = input(u'\n0 - irrelevant\n1 - first part \n2 - second part\nChoose the part: ')

        self.length = input(u'\nSpecify the size of the lists (in words): ')

        self.differ = input(u'\n0 - the lists are not supposed to be different\n'
                                u'they should differ in:\n'
                                u'1 - Name agreement\n'
                                u'2 - Subjective visual complexity\n'
                                u'3 - Familiarity\n'
                                u'4 - Age of acquisition\n'
                                u'5 - Imageability\n'
                                u'6 - Image agreement\n'
                                u'7 - Frequency\n'
                                u'8 - Syllables length\n'
                                u'9 - Phonemes length\n'
                                u'Specify: ')

        self.statistics = input(u'\n1 - Student\'s t-test\n'
                                     u'2 - Welch\'s t-test\n'
                                     u'3 - Mann–Whitney U test\n'
                                     u'Specify statistics: ')


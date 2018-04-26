# -*- encoding: utf-8 -*-


class ContextNoMatch(Exception):
    def __init__(self):
        super(ContextNoMatch, self).__init__(u'There is no matching data!')


class MultipleContextMatch(Exception):
    def __init__(self):
        super(MultipleContextMatch, self).__init__(u'Multiple matches!')


class NoIndex(Exception):
    def __init__(self):
        super(NoIndex, self).__init__(u'No index!')


class NoMatchExTree(Exception):
    def __init__(self):
        super(NoMatchExTree, self).__init__(u'No match ex tree!')
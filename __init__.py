# -*- encoding: utf-8 -*-

from create_template_tree import CreateExtractTree
from extractors.template_maker import CustomTemplateMaker
from collections import OrderedDict


class TemplateDict(object):
    def __init__(self):
        self.dict = OrderedDict

    def __getitem__(self, item):
        pass

    def __setitem__(self, key, value):
        pass

    def add_element(self, field, value):
        pass

    def add_fragment(self, field, re_compile):
        pass


if __name__ == '__main__':
    test = TemplateDict()


# -*- encoding: utf-8 -*-

from extractors.template_maker import CustomTemplateMaker, CustomRecordExtractor
from errors import NoIndex
from scrapely.template import best_match
from scrapely.htmlpage import HtmlPage
from scrapely.extraction.pageparsing import parse_template
from scrapely.extraction import BasicTypeExtractor
from scrapely import InstanceBasedLearningExtractor
from find_context_index import full_div_context_index
from util.encode_tools import code_to_unicode
from copy import deepcopy


class CreateExtractTree(object):
    def __init__(self, url, body, data, best_match_field=None):
        """
        best_match 控制是否是模糊查询 ['test', 'test_2'], 默认为严格匹配
        :param url:
        :param body:
        :param data:
        :param best_match:
        """
        super(CreateExtractTree, self).__init__()
        self.url = url
        self.body = body
        self.data = data
        self.best_match_field = best_match_field
        self.template_htmlpage = None
        self.source_data = {'common': {'data': deepcopy(data)}}
        self.source_data['common'].update({'best_match_field': best_match_field})

    def get_htmlpage(self):
        self.body = code_to_unicode(self.body)
        return HtmlPage(url=self.url, body=self.body)

    def get_template_id(self):
        return self.get_htmlpage().page_id

    def get_template_make(self):
        if not self.template_htmlpage:
            self.htmlpage = self.get_htmlpage()
            self.token_dict = InstanceBasedLearningExtractor([(self.htmlpage, None)]).token_dict
            self.template_htmlpage = CustomTemplateMaker(self.htmlpage)
        for data_item in self.data.items():
            best_match_col = True
            if self.best_match_field and data_item[0] in self.best_match_field:
                best_match_col = False
            self.template_htmlpage.annotate(field=data_item[0], score_func=best_match(code_to_unicode(data_item[1])),
                                            best_match=best_match_col)

    def get_extract_tree(self):
        self.get_template_make()
        template = self.template_htmlpage.get_template()
        parse_tmp = parse_template(self.token_dict, template)
        basic_extractors = list(map(BasicTypeExtractor, parse_tmp.annotations))
        return CustomRecordExtractor.apply(parse_tmp, basic_extractors, self.htmlpage, self.source_data)[0]

    def add_div_parse(self, field, text_compile, diff=None, ele_type='div'):
        text_compile = text_compile.strip()
        try:
            self.source_data['chunk'].append({'field': field, 'text_compile': text_compile, 'diff': diff, 'ele_type': ele_type})
        except KeyError:
            self.source_data['chunk'] = [{'field': field, 'text_compile': text_compile, 'diff': diff, 'ele_type': ele_type}]
        if not self.template_htmlpage:
            self.htmlpage = self.get_htmlpage()
            self.token_dict = InstanceBasedLearningExtractor([(self.htmlpage, None)]).token_dict
            self.template_htmlpage = CustomTemplateMaker(self.htmlpage)
        index = full_div_context_index(self.htmlpage, text_compile=text_compile, diff=diff, ele_type=ele_type)
        if index is None:
            raise NoIndex
        self.template_htmlpage.add_annotate(field=field, indexes=[index])


class Field(dict):
    def __init__(self):
        super(Field, self).__init__()

    def __call__(self, *args, **kwargs):
        pass


class FormatDict(object):
    title = Field()
    data = Field()



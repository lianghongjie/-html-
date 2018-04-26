# -*- encoding: utf-8 -*-

from scrapely.htmlpage import HtmlPage
from scrapely import InstanceBasedLearningExtractor
from scrapely.extraction.pageparsing import parse_extraction_page
from util.encode_tools import code_to_unicode
from scrapely.extraction.pageparsing import parse_template
from scrapely.extraction.pageobjects import TokenDict
from errors import NoMatchExTree
import re


def output_clear_special_char(char_dict):
    """
    extract_tree_parse return data eg: {'dd': ['tt', 'ss'], 'ff': ['test']}
    自动解析特殊字符输出仍保留原有extract_tree_parse返回值的格式
    :param char dict:
    :return:
    """
    special_char_dict = {'&nbsp;': u' ', '&emsp;': u' ', '&ensp;': u' ', '&trade;': u'™',
                        '&copy;': u'©', '&reg;': u'®', '&quot;': u'\"', '&amp;': u'&', '&gt;': u'>', '&lt;': u'<'}

    def sub_char(m):
        special_char = m.group('special_char')
        return special_char_dict.get(special_char)

    for item in char_dict.items():
        char_dict[item[0]] = [re.sub('(?P<special_char>&\w+;)', sub_char, value) for value in item[1]]
    return char_dict


def extract_tree_parse(url, body, ex, comb=True):
    """
    comb 通过下划线连接相同的字段, 结果合并
    :param url: 
    :param body: 
    :param ex: 
    :param comb: 
    :return: 
    """
    body = code_to_unicode(body)
    htmlpage = HtmlPage(url=url, body=body)
    token_dict = InstanceBasedLearningExtractor([(htmlpage, None)]).token_dict
    extract_page = parse_extraction_page(token_dict, htmlpage)
    data_dict = ex.extract(extract_page)[0]
    if comb:
        sub_key = [data.split("_")[0] for data in data_dict.keys()]
        all_slim = set(filter(lambda x: sub_key.count(x) > 1, sub_key))
        for data in data_dict.keys():
            sub_key = data.split('_')[0]
            if sub_key in all_slim:
                try:
                    data_dict[sub_key].extend(data_dict[data])
                except KeyError:
                    data_dict[sub_key] = data_dict.get(data)
                data_dict.pop(data)
        return data_dict
    return ex.extract(extract_page)[0]


class CirculationParse(object):
    def __init__(self, ex_trees):
        """
        循环树解析,通过链接筛选不出的页面
        :param ex_trees list:
        """
        super(CirculationParse, self).__init__()
        assert isinstance(ex_trees, list)
        self._ex_trees = ex_trees

    def get_ex_trees(self):
        return self._ex_trees

    def extract(self, url, body, comb=True):
        htmlpage = HtmlPage(url=url, body=code_to_unicode(body))
        page_tokens = parse_template(TokenDict(), htmlpage).page_tokens
        match_ex_tree = None
        for ex_tree in self._ex_trees:
            if not cmp(list(ex_tree.template_tokens), list(page_tokens)):
                match_ex_tree = ex_tree
        if match_ex_tree is None: raise NoMatchExTree
        return extract_tree_parse(url=url, body=body, ex=match_ex_tree, comb=comb)


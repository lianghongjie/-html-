# -*- encoding: utf-8 -*-

from scrapely.template import TemplateMaker, best_match, FragmentNotFound
from scrapely.extraction.regionextract import RecordExtractor


class CustomTemplateMaker(TemplateMaker):
    def __init__(self, parent=None):
        super(CustomTemplateMaker, self).__init__(parent)

    def annotate(self, field, score_func, best_match=True):
        """Annotate a field."""
        indexes = self.select(score_func)
        if not indexes:
            raise FragmentNotFound("Fragment not found annotating %r (检查是否有特殊字符eg:&nbsp;或尝试best_match=False)" % field)
        if best_match:
            del indexes[1:]
        for i in indexes:
            self.annotate_fragment(i, field)

    def add_annotate(self, field, indexes):
        """

        :param field:
        :param indexes list:
        :return:
        """
        if not indexes:
            raise FragmentNotFound("Fragment not found annotating %r (检查是否有特殊字符,请进行转义eg:[.()*])" % field)
        if best_match:
            del indexes[1:]
        for i in indexes:
            self.annotate_fragment(i, field)


class CustomRecordExtractor(RecordExtractor):
    """
    绑定属性值
    source_data 结构
    {'title': 'test_title',
    'date': 'test_date',
    'chunk': [
    {'context': 'test_context'},
    {'p_chunk': '<p>_context'}
    ]}
    """
    def __init__(self, extractors, template_tokens, htmlpage, source_data):
        super(CustomRecordExtractor, self).__init__(extractors, template_tokens)
        self.htmlpage = htmlpage
        self.source_data = source_data

    @classmethod
    def apply(cls, template, extractors, htmlpage, source_data):
        return [cls(extractors, template.page_tokens, htmlpage, source_data)]


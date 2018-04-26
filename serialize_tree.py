# -*- encoding: utf-8 -*-
import json
import dill
import os
from util.encode_tools import code_to_unicode
from create_template_tree import CreateExtractTree


class SerializeTree(object):
    def __init__(self, exs):
        """
        Initialize an empty scraper.
        :param exs list
        """
        self._exs = exs if isinstance(exs, list) else [exs]

    @staticmethod
    def from_ex_file(file):
        """Initialize a scraper from a file previously stored by tofile()
        method.
        """
        with open(file, 'r') as fl:
            exs_message = dill.load(fl)
        return exs_message

    @staticmethod
    def from_source_file(url_body_dict, file):
        """ url_body_dict is {'http://test.com': 'body', 'http://test_2.com': 'body2'}"""
        with open(file, 'r') as fl:
            datas = json.load(fl)
            exs = []
            for data in datas:
                url = data.get('url')
                data_dict = data.get('data')
                ex_tree = CreateExtractTree(url=url, body=code_to_unicode(url_body_dict.get(url)),
                                            **(data_dict.get('common')))
                for chunk in data_dict.get('chunk'):
                    ex_tree.add_div_parse(**chunk)
                exs.append(ex_tree.get_extract_tree())
            return exs

    def tofile(self, path):
        """保存源数据和ex树"""
        json_path = os.path.join(path, 'source.json')
        ex_path = os.path.join(path, 'ex.tree')
        self.save_source(json_path)
        self.save_exs(ex_path)

    def save_source(self, file, **kwargs):
        """json 结构
        [{
        "url": "http://www.afinance.cn/insurance/hyzx/201803/2049022.html",
        "web": "weibo.com",
        "data": {
            "chunk": [{
                "field": "context",
                "ele_type": "div",
                "text_compile": "2018\u5e743\u670828\u65e5\u4e0a\u5348\uff0c\u4e0a\u6d77\u5e02\u7b2c\u4e00\u4e2d\u7ea7\u4eba\u6c11\u6cd5\u9662\u516c\u5f00\u5f00\u5ead\u5ba1\u7406\u4e0a\u6d77\u5e02\u4eba\u6c11\u68c0\u5bdf\u9662\u7b2c\u4e00\u5206\u9662\u63d0\u8d77\u516c\u8bc9\u7684\u5b89\u90a6$",
                "diff": null
            }],
            "common": {
                "best_match_field": null,
                "data": {
                    "tt": "\u5434\u5c0f\u6656\u5426\u8ba4\u8f6c\u79fb\u8d44\u91d1 \u79f0\u589e\u8d44\u6b3e\u662f\u771f\u5b9e\u7684\u81ea\u6709\u8d44\u91d1"
                }
            }
        },
        "template_id": "c7ab0e9a70d74cdfe946fed9a524aee0835b7157",
        "url_type": "001"
        }]
        """
        datas = []
        for ex_tree in self._exs:
            htmlpage = ex_tree.htmlpage
            datas.append(dict({'url': htmlpage.url,
                    'template_id': htmlpage.page_id,
                    'data': ex_tree.source_data}, **kwargs))
        with open(file, 'w') as fl:
            json.dump(datas, fl, indent=4)

    def save_exs(self, file, **kwargs):
        with open(file, 'w') as fl:
            dill.dump([dict({'template_id': ex.htmlpage.page_id, 'ex': ex}, **kwargs) for ex in self._exs], file=fl)


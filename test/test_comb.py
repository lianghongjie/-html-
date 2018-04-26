# -*- encoding: utf-8 -*-


from util.encode_tools import code_to_unicode
from create_template_tree import CreateExtractTree
import requests
headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }
url = 'https://www.analysys.cn'
body = requests.get(url=url, headers=headers).content
data = {

}
test = CreateExtractTree(url=url, body=code_to_unicode(body), data=data, best_match_field=['rr'])
# test.add_div_parse('context', '滬港通')
ex = test.get_extract_tree()
print ex
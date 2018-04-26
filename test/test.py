# -*- encoding: utf-8 -*-

from create_template_tree import CreateExtractTree
import requests
from scrapely.htmlpage import HtmlPage

headers = {
            "Cookie":
                "prov=cn010; city=010; weather_city=bj; region_ip=111.198.24.x; region_ver=1.2; userid=1523330065384_jblxca8959; UM_distinctid=162ad8c84f82db-0f9eb56a201821-3a76015a-1aeaa0-162ad8c84f9458; vjuids=-3b54fe109.162ae2213fe.0.4e31c99192779; __gads=ID=6f3d8bbf0d575a34:T=1523341269:S=ALNI_MZdIo4VoemQcJz5_XPE5uscNTOCbQ; games_source_375765101=4; games_source_316765743=3; vjlast=1523339892.1523439244.13; BAIDU_SSP_lcr=https://www.baidu.com/link?url=A-NqNkDB9c0Ztb2sjKmjNM87AuusZF-KsdhrP1x1qCVMz6K5C4dy_wWtoV0K6LD9&wd=&eqid=bb70142b000121e9000000025acf06d9; ifengRotator_AP299=0; bdshare_firstime=1523517357361; CNZZDATA1269613747=1575582443-1523513688-null%7C1523859342; ifengRotator_iis3=5; CNZZDATA1257375399=261690128-1523514973-http%253A%252F%252Fculture.ifeng.com%252F%7C1523860573; CNZZDATA1266101310=70189921-1523515450-http%253A%252F%252Fculture.ifeng.com%252F%7C1523861051; games_source_3962747416=10; ifengRotator_iis3_c=16; CNZZDATA1257652052=272132132-1523516671-http%253A%252F%252Fculture.ifeng.com%252F%7C1523862291; ifengRotator_AP2842=1",
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }
url = 'http://finance.ifeng.com/a/20180416/16098030_0.shtml'
body = requests.get(url=url, headers=headers).content.decode('utf-8')
htmlpage = HtmlPage(url=url, body=body)
test = CreateExtractTree(url=url, body=body, data={'title': u'买不起房，就多买两套？你总在误解真相！'})
test.add_div_parse('context', u'^来源：子木聊房（ID：zimuliaofang）作者：子木$')
ex = test.get_extract_tree()
# print dir(ex)
print ex

url = 'http://finance.ifeng.com/a/20180417/16105993_0.shtml'
body = requests.get(url=url).content
from parse_html import extract_tree_parse
print extract_tree_parse(url, body, ex)


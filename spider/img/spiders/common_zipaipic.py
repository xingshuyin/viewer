from hashlib import md5
import scrapy
import json
from ..tools import path, deal_path, parse_item, script_shot, script
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
from scrapy.http import HtmlResponse
from scrapy_splash.response import SplashTextResponse

rule = {
    'name': 'common_zipaipic',
    'start_urls': 'https://wv.sslkn.name/photos/',  # 开始页(逗号分隔)

    'page_min': 1,
    'page_max': 840,
    'page_shift': 'str(num)',

    'get_page': 'https://xn--cjs-zipaipiccom-6m3z988bh2ek30lissa.www-zipaipic.com/index_{}.html',  # 分页链接提取区域xpath(必填)
    'get_item': '//div[@class="items-list"]',  # 内容链接提取区域xpath(必填)
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
args = {'wait': 0.5, 'lua_source': script}
args_shot = {'wait': 0.5, 'lua_source': script_shot}


class common_zipaipicSpider(CrawlSpider):
    name = "zipaipic"
    seen = set()

    def __init__(self):
        self.rule = rule
        self.allowed_domains = rule.get('allowed_domains', '*')
        self.name = rule['name']
        self.start_urls = rule['start_urls'].split(",")
        self.rules = [
            Rule(LinkExtractor(allow=rule['re_item'], restrict_xpaths=[rule['get_item']]), process_request='item_request', follow=False),

        ]
        if not (self.rule['page_min'] and self.rule['page_max'] and self.rule['get_page'] and self.rule['page_shift']):
            self.rules.append(Rule(LinkExtractor(allow=rule['re_page'], restrict_xpaths=[
                              rule['get_page']]), process_request='page_request', follow=True),)
        self.data = []
        super().__init__()

    def start_requests(self):
        print('start_requests', self.rule)
        if self.rule['page_min'] and self.rule['page_max'] and self.rule['get_page'] and self.rule['page_shift']:
            for num in range(self.rule['page_min'], self.rule['page_max'] + 1):
                num = eval(self.rule['page_shift'])
                yield SplashRequest(self.rule['get_page'].format(num),
                                    self.get_item,
                                    endpoint='execute',
                                    args=args,
                                    dont_filter=True)
        else:
            print('start_urls', self.start_urls)
            for url in self.start_urls:
                yield SplashRequest(url,
                                    endpoint='execute',
                                    args=args,
                                    dont_filter=True)

    def get_item(self, response):
        items = response.xpath('//ul[@id="tiles"]/li/@onclick').getall()
        for i in items:
            url = "https://xn--cjs-zipaipiccom-6m3z988bh2ek30lissa.www-zipaipic.com/" + i.split("'")[1]
            yield SplashRequest(url=url,
                                callback=self.parse_item,
                                endpoint='execute',
                                args=args, dont_filter=True)

    def parse_item(self, response):
        imgs = response.xpath('//div[@class="artical-content"]//img/@src').getall()
        print(response.url, len(imgs))
        self.data.extend(imgs)

    @staticmethod
    def close(spider, reason):
        with open(f'{rule["name"]}.json', 'w') as f:
            f.write(json.dumps(spider.data))
        print('共有', len(spider.data), '个')
        closed = getattr(spider, "closed", None)
        if callable(closed):
            return closed(reason)

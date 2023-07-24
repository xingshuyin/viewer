from hashlib import md5
import scrapy
import json
import os
import time
from ..tools import path, deal_path, parse_item, script_shot, script
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
from scrapy.http import HtmlResponse
from scrapy_splash.response import SplashTextResponse

rule = {
    'name': 'taotuhome',
    'start_urls': 'https://taotuhome.com/category/dietutu/',  # 开始页(逗号分隔)

    'page_min': None,
    'page_max': None,
    'page_shift': None,

    'get_page': '//nav[@class="navigation pagination"]',  # 分页链接提取区域xpath(必填)
    'get_item': '//main[@id="main"]//article',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="single-content"]//img/@src',
    'get_item_page': '//div[@class="page-links"]',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}

args = {'wait': 2, 'lua_source': script}
args_shot = {'wait': 0.5, 'lua_source': script_shot}


class ItemPageSpider(CrawlSpider):
    name = "item_page"
    seen = set()

    def __init__(self):
        self.rule = rule
        self.allowed_domains = self.rule.get('allowed_domains', '*')
        self.name = self.rule['name']
        self.start_urls = self.rule['start_urls'].split(",")
        self.rules = [
            Rule(LinkExtractor(allow=self.rule['re_item'], restrict_xpaths=[self.rule['get_item']]), callback='parse_item', follow=False),

        ]
        if not (self.rule['page_min'] and self.rule['page_max'] and self.rule['get_page'] and self.rule['page_shift']):
            self.rules.append(Rule(LinkExtractor(allow=self.rule['re_page'], restrict_xpaths=[
                              self.rule['get_page']]), callback='_requests_to_follow', follow=True),)
        if self.rule['get_item_page']:
            self.rules.append(Rule(LinkExtractor(allow=self.rule['re_page'], restrict_xpaths=[
                self.rule['get_item_page']]), callback='parse_item', follow=True),)
        self.data = []
        self.start = 0
        super().__init__()

    def start_requests(self):
        if self.rule['page_min'] and self.rule['page_max'] and self.rule['get_page'] and self.rule['page_shift']:
            for num in range(self.rule['page_min'], self.rule['page_max'] + 1):
                num = eval(self.rule['page_shift'])
                yield SplashRequest(self.rule['get_page'].format(num),
                                    self._requests_to_follow,
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

    def _requests_to_follow(self, response):
        if not isinstance(response, SplashTextResponse):
            return

        for rule_index, rule in enumerate(self._rules):
            links = [
                lnk
                for lnk in rule.link_extractor.extract_links(response)
                if lnk not in self.seen
            ]
            if len(self.seen) >= 10000:
                self.seen = set()
            for link in rule.process_links(links):
                self.seen.add(link)
                request = self._build_request(rule_index, link)
                yield rule.process_request(request, response)

    def _build_request(self, rule_index, link):
        print(link.url)
        return SplashRequest(
            url=link.url,
            callback=self._callback,
            errback=self._errback,
            meta=dict(rule=rule_index, link_text=link.text),
            endpoint='execute',
            args=args,
            dont_filter=True)

    def parse_item(self, response):
        imgs = response.xpath('//div[@class="album"]//div[@class="img-holder"]//img/@src').getall()
        imgs = response.xpath(self.rule['get_img']).getall()
        print('item ', response.url, len(imgs))
        self.data.extend(imgs)
        if time.time() - self.start > 60:
            self.start = time.time()
            print('共有', len(self.data), '个')
            with open(f'D:/python/viewer/src/renderer/src/assets/json_source/{self.rule["name"]}.json', 'w') as f:
                f.write(json.dumps(self.data))
        for i in self._requests_to_follow(response):
            yield i

    @staticmethod
    def close(spider, reason):
        with open(f'D:/python/viewer/src/renderer/src/assets/json_source/{spider.rule["name"]}.json', 'w') as f:
            f.write(json.dumps(spider.data))
        print('共有', len(spider.data), '个')
        closed = getattr(spider, "closed", None)
        if callable(closed):
            return closed(reason)

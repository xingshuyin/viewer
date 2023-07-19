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
    'name': 'yuyu',
    'start_urls': 'https://www.yuyu456.com/picture/index/lianglirenqi.html',  # 开始页(逗号分隔)

    'page_min': None,
    'page_max': None,
    'page_shift': None,

    'get_page': '//div[id="page"]',  # 分页链接提取区域xpath(必填)
    'get_item': '//ul[@id="contWaterfall"]',  # 内容链接提取区域xpath(必填)
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
rule = {
    'name': '06se',
    'start_urls': 'https://www.06se.com/?orderby=rand',  # 开始页(逗号分隔)

    'page_min': 2,
    'page_max': 462,
    'page_shift': 'str(num)',

    'get_page': 'https://www.06se.com/page/{}?orderby=rand',  # 分页链接提取区域xpath(必填)
    'get_item': '//posts[@class="posts-item ajax-item card style3"]//div[@class="item-thumbnail"]',  # 内容链接提取区域xpath(必填)
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
args = {'wait': 0.5, 'lua_source': script}
args_shot = {'wait': 0.5, 'lua_source': script_shot}


class CommonSpider(CrawlSpider):
    name = "common"
    seen = set()

    def __init__(self):
        self.rule = rule
        self.allowed_domains = self.rule.get('allowed_domains', '*')
        self.name = self.rule['name']
        self.start_urls = self.rule['start_urls'].split(",")
        self.rules = [
            Rule(LinkExtractor(allow=self.rule['re_item'], restrict_xpaths=[self.rule['get_item']]), process_request='item_request', follow=False),

        ]
        if not (self.rule['page_min'] and self.rule['page_max'] and self.rule['get_page'] and self.rule['page_shift']):
            self.rules.append(Rule(LinkExtractor(allow=self.rule['re_page'], restrict_xpaths=[
                              self.rule['get_page']]), process_request='page_request', follow=True),)
        self.data = []
        super().__init__()

    def start_requests(self):
        print('start_requests', self.rule)
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

    def item_request(self, request, response):
        url_hash = md5(request.url.encode(encoding='UTF-8')).hexdigest()
        return SplashRequest(url=request.url,
                             callback=self.parse_item,
                             endpoint='execute',
                             args=args,
                             dont_filter=True)

    def page_request(self, request, response):
        print('page--- ', request.url)
        return SplashRequest(url=request.url,
                             callback=self._requests_to_follow,
                             endpoint='execute',
                             args=args, dont_filter=True)

    def _requests_to_follow(self, response):
        if not isinstance(response, SplashTextResponse):
            return

        for rule_index, rule in enumerate(self._rules):
            links = [
                lnk
                for lnk in rule.link_extractor.extract_links(response)
                if lnk not in self.seen
            ]
            for link in rule.process_links(links):
                self.seen.add(link)
                request = self._build_request(rule_index, link)
                yield rule.process_request(request, response)

    def _build_request(self, rule_index, link):
        return SplashRequest(
            url=link.url,
            callback=self._callback,
            errback=self._errback,
            meta=dict(rule=rule_index, link_text=link.text),
            endpoint='execute',
            args=args,
            dont_filter=True)

    def parse_item(self, response):
        imgs = response.xpath('//div[@class="article-content"]//img/@src').getall()
        print(response.url, len(imgs))
        self.data.extend(imgs)

    @staticmethod
    def close(spider, reason):
        with open(f'{spider.rule["name"]}.json', 'w') as f:
            f.write(json.dumps(spider.data))
        print('共有', len(spider.data), '个')
        closed = getattr(spider, "closed", None)
        if callable(closed):
            return closed(reason)

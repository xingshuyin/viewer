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
    'name': 'taotuhome_dietutu',
    'start_urls': 'https://taotuhome.com/category/dietutu/',  # 开始页(逗号分隔)
    'allowed_domains': 'taotuhome.com',
    'get_page': '//body',  # 分页链接提取区域xpath(必填)
    'get_item': '//body',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="single-content"]//img/@src',
    're_page': 'https://taotuhome.com/category/.*?',  # 分页链接正则(必填)
    're_item': 'https://taotuhome.com/\d+.html.*',  # 内容链接正则(必填)
}

rule = {
    'name': 'lingleis',
    'start_urls': 'http://lingleis.info/bdsvy/7/2.html',  # 开始页(逗号分隔)
    'allowed_domains': 'lingleis.info',
    'get_page': '//body',  # 分页链接提取区域xpath(必填)
    'get_item': '//body',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="titletablerow"]//img/@src',
    're_page': 'http://lingleis.info/bdsvy/7.*?.html',  # 分页链接正则(必填)
    're_item': '.*?acuz2/\d+.html',  # 内容链接正则(必填)
}
lingleis_mtsw = {
    'name': 'lingleis-mtsw',
    'start_urls': 'http://lingleis.info/bdsvy/9/2.html',  # 开始页(逗号分隔)
    'allowed_domains': 'lingleis.info',
    'get_page': '//body',  # 分页链接提取区域xpath(必填)
    'get_item': '//body',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="titletablerow"]//img/@src',
    're_page': 'http://lingleis.info/bdsvy/9.*?.html',  # 分页链接正则(必填)
    're_item': '.*?acuz2/\d+.html',  # 内容链接正则(必填)
}
lingleis_qcym = {
    'name': 'lingleis-qcym',
    'start_urls': 'http://lingleis.info/bdsvy/10/2.html',  # 开始页(逗号分隔)
    'allowed_domains': 'lingleis.info',
    'get_page': '//body',  # 分页链接提取区域xpath(必填)
    'get_item': '//body',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="titletablerow"]//img/@src',
    're_page': 'http://lingleis.info/bdsvy/10.*?.html',  # 分页链接正则(必填)
    're_item': '.*?acuz2/\d+.html',  # 内容链接正则(必填)
}
kdsomy = {
    'name': 'kdsomy',
    'start_urls': 'https://kdsomy.xyz/html/category/photo/list_7_1.html',  # 开始页(逗号分隔)
    'allowed_domains': 'kdsomy.xyz',
    'get_page': '//body',  # 分页链接提取区域xpath(必填)
    'get_item': '//body',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="bf_js"]//img/@src',
    're_page': 'https://kdsomy.xyz/html/category/photo/list.*?.html',  # 分页链接正则(必填)
    're_item': '.*?/html/\d+/',  # 内容链接正则(必填)
}
rule = {
    'name': 'mh3515-ai',
    'start_urls': 'https://mh3515.com/ai/list_1418_1.html',  # 开始页(逗号分隔)
    'allowed_domains': 'mh3515.com',
    'get_page': '//body',  # 分页链接提取区域xpath(必填)
    'get_item': '//body',  # 内容链接提取区域xpath(必填)
    'get_img': '//article[@id="contxt"]//img/@src',
    're_page': '.*?list.*?',  # 分页链接正则(必填)
    're_item': '.*?/ai/ai.*?',  # 内容链接正则(必填)
}
mh3515_sptu = {
    'name': 'mh3515-sptu',
    'start_urls': 'https://mh3515.com/sptu/',  # 开始页(逗号分隔)
    'allowed_domains': 'mh3515.com',
    'get_page': '//body',  # 分页链接提取区域xpath(必填)
    'get_item': '//body',  # 内容链接提取区域xpath(必填)
    'get_img': '//article[@id="contxt"]//img/@src',
    're_page': '.*?list.*?',  # 分页链接正则(必填)
    're_item': '.*?sptu/sp.*?',  # 内容链接正则(必填)
}
mh3515_mv = {
    'name': 'mh3515-mv',
    'start_urls': 'https://mh3515.com/mv/',  # 开始页(逗号分隔)
    'allowed_domains': 'mh3515.com',
    'get_page': '//body',  # 分页链接提取区域xpath(必填)
    'get_item': '//body',  # 内容链接提取区域xpath(必填)
    'get_img': '//article[@id="contxt"]//img/@src',
    're_page': '.*?list.*?',  # 分页链接正则(必填)
    're_item': '.*?/mv/xr.*?|.*?/mv/XR.*?',  # 内容链接正则(必填)
}
mh3515_mh = {
    'name': 'mh3515-mh',
    'start_urls': 'https://mh3515.com/mh/',  # 开始页(逗号分隔)
    'allowed_domains': 'mh3515.com',
    'get_page': '//body',  # 分页链接提取区域xpath(必填)
    'get_item': '//body',  # 内容链接提取区域xpath(必填)
    'get_img': '//article[@id="contxt"]//img/@src',
    're_page': '.*?list.*?',  # 分页链接正则(必填)
    're_item': '.*?/3d/.*?|.*?/mh/.*?',  # 内容链接正则(必填)
}
mh3515_qq = {
    'name': 'mh3515-qq',
    'start_urls': 'https://mh3515.com/qq/',  # 开始页(逗号分隔)
    'allowed_domains': 'mh3515.com',
    'get_page': '//body',  # 分页链接提取区域xpath(必填)
    'get_item': '//body',  # 内容链接提取区域xpath(必填)
    'get_img': '//article[@id="contxt"]//img/@src',
    're_page': '.*?list.*?',  # 分页链接正则(必填)
    're_item': '.*?/qq/.*?',  # 内容链接正则(必填)
}
mh3515_yh = {
    'name': 'mh3515-yh',
    'start_urls': 'https://mh3515.com/yh/',  # 开始页(逗号分隔)
    'allowed_domains': 'mh3515.com',
    'get_page': '//body',  # 分页链接提取区域xpath(必填)
    'get_item': '//body',  # 内容链接提取区域xpath(必填)
    'get_img': '//article[@id="contxt"]//img/@src',
    're_page': '.*?list.*?',  # 分页链接正则(必填)
    're_item': '.*?/yh/.*?',  # 内容链接正则(必填)
}
mh3515_jp = {
    'name': 'mh3515-jp',
    'start_urls': 'https://mh3515.com/jp/',  # 开始页(逗号分隔)
    'allowed_domains': 'mh3515.com',
    'get_page': '//body',  # 分页链接提取区域xpath(必填)
    'get_item': '//body',  # 内容链接提取区域xpath(必填)
    'get_img': '//article[@id="contxt"]//img/@src',
    're_page': '.*?list.*?',  # 分页链接正则(必填)
    're_item': '.*?/jp/.*?',  # 内容链接正则(必填)
}
mh3515_zz = {
    'name': 'mh3515-zz',
    'start_urls': 'https://mh3515.com/zz/',  # 开始页(逗号分隔)
    'allowed_domains': 'mh3515.com',
    'get_page': '//body',  # 分页链接提取区域xpath(必填)
    'get_item': '//body',  # 内容链接提取区域xpath(必填)
    'get_img': '//article[@id="contxt"]//img/@src',
    're_page': '.*?list.*?',  # 分页链接正则(必填)
    're_item': '.*?/zz/.*?',  # 内容链接正则(必填)
}
args = {'wait': 2, 'lua_source': script}
args_shot = {'wait': 0.5, 'lua_source': script_shot}


class FullSpider(CrawlSpider):
    name = "full"
    seen = set()
    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
        'DOWNLOAD_DELAY': 0
    }

    def __init__(self):
        self.rule = mh3515_zz
        self.allowed_domains = self.rule.get('allowed_domains', '*')
        self.name = self.rule['name']
        self.start_urls = self.rule['start_urls'].split(",")
        self.rules = [
            Rule(LinkExtractor(allow=self.rule['re_item'], restrict_xpaths=[self.rule['get_item']]),
                 callback='parse_item', process_request='process_item', follow=True),
            Rule(LinkExtractor(allow=self.rule['re_page'], restrict_xpaths=[self.rule['get_page']]),
                 callback='_requests_to_follow', process_request='process_page', follow=True)
        ]
        self.data = []
        self.start = 0
        super().__init__()

    def start_requests(self):
        print('start_urls', self.start_urls)
        for url in self.start_urls:
            yield SplashRequest(url,
                                endpoint='execute',
                                args=args,
                                dont_filter=True)

    def process_page(self, request, response):
        request.priority = 10
        return request

    def process_item(self, request, response):
        request.priority = 1
        return request

    def _requests_to_follow(self, response):
        if not isinstance(response, SplashTextResponse):
            return

        for rule_index, rule in enumerate(self._rules):
            links = [
                lnk
                for lnk in rule.link_extractor.extract_links(response)
                if lnk not in self.seen
            ]
            if rule_index == 1:
                time.sleep(1)
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
        if time.time() - self.start > 60 * 5:
            self.start = time.time()
            print('共有', len(self.data), '个')
            with open(f'D:/python/viewer/src/renderer/src/assets/json_source/{self.rule["name"]}.json', 'w') as f:
                f.write(json.dumps(self.data))

    @staticmethod
    def close(spider, reason):
        with open(f'D:/python/viewer/src/renderer/src/assets/json_source/{spider.rule["name"]}.json', 'w') as f:
            f.write(json.dumps(spider.data))
        print('共有', len(spider.data), '个')
        closed = getattr(spider, "closed", None)
        if callable(closed):
            return closed(reason)

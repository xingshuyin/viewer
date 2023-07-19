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
    'name': 'yuyu',
    'start_urls': 'https://www.yuyu456.com/picture/index/lianglirenqi.html',  # 开始页(逗号分隔)

    'page_min': None,
    'page_max': None,
    'page_shift': None,

    'get_page': '//div[id="page"]',  # 分页链接提取区域xpath(必填)
    'get_item': '//ul[@id="contWaterfall"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="images"]//img/@src',
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
    'get_img': '//div[@class="article-content"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
rule = {
    'name': 'sslkn',
    'start_urls': 'https://wv.sslkn.name/photos/',  # 开始页(逗号分隔)

    'page_min': 1,
    'page_max': 400,
    'page_shift': 'str(num)',

    'get_page': 'https://wv.sslkn.name/photos/{}/',  # 分页链接提取区域xpath(必填)
    'get_item': '//div[@class="items-list"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="album"]//div[@class="img-holder"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
luoli111_43 = {
    'name': 'luoli111_43',
    'start_urls': 'https://www.luoli111.top/index.php/vod/show/id/43.html',  # 开始页(逗号分隔)

    'page_min': None,
    'page_max': None,
    'page_shift': 'str(num)',

    'get_page': '//ul[@class="stui-page text-center clearfix"]',  # 分页链接提取区域xpath(必填)
    'get_item': '//ul[@class="stui-vodlist clearfix"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="stui-content clearfix video-info"]//img/@data-original',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
rule = {
    'name': 'luoli111_39',
    'start_urls': 'https://www.luoli111.top/index.php/vod/show/by/hits/id/39.html',  # 开始页(逗号分隔)

    'page_min': None,
    'page_max': None,
    'page_shift': 'str(num)',

    'get_page': '//ul[@class="stui-page text-center clearfix"]',  # 分页链接提取区域xpath(必填)
    'get_item': '//ul[@class="stui-vodlist clearfix"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="stui-content clearfix video-info"]//img/@data-original',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
luoli111_40 = {
    'name': 'luoli111_40',
    'start_urls': 'https://www.luoli111.top/index.php/vod/show/by/hits/id/40.html',  # 开始页(逗号分隔)

    'page_min': None,
    'page_max': None,
    'page_shift': 'str(num)',

    'get_page': '//ul[@class="stui-page text-center clearfix"]',  # 分页链接提取区域xpath(必填)
    'get_item': '//ul[@class="stui-vodlist clearfix"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="stui-content clearfix video-info"]//img/@data-original',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
luoli111_41 = {
    'name': 'luoli111_41',
    'start_urls': 'https://www.luoli111.top/index.php/vod/show/by/hits/id/41.html',  # 开始页(逗号分隔)

    'page_min': None,
    'page_max': None,
    'page_shift': 'str(num)',

    'get_page': '//ul[@class="stui-page text-center clearfix"]',  # 分页链接提取区域xpath(必填)
    'get_item': '//ul[@class="stui-vodlist clearfix"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="stui-content clearfix video-info"]//img/@data-original',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
luoli111_42 = {
    'name': 'luoli111_42',
    'start_urls': 'https://www.luoli111.top/index.php/vod/show/by/hits/id/42.html',  # 开始页(逗号分隔)

    'page_min': None,
    'page_max': None,
    'page_shift': 'str(num)',

    'get_page': '//ul[@class="stui-page text-center clearfix"]',  # 分页链接提取区域xpath(必填)
    'get_item': '//ul[@class="stui-vodlist clearfix"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="stui-content clearfix video-info"]//img/@data-original',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
mntu1 = {
    'name': 'mntu1',
    'start_urls': 'http://446m.com/index.php/mntu/1/',  # 开始页(逗号分隔)

    'page_min': None,
    'page_max': None,
    'page_shift': 'str(num)',

    'get_page': '//ol[@class="page-navigator"]',  # 分页链接提取区域xpath(必填)
    'get_item': '//div[@id="masonry"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="post-content"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
mntu2 = {
    'name': 'mntu2',
    'start_urls': 'http://446m.com/index.php/mntu/2/',  # 开始页(逗号分隔)

    'page_min': None,
    'page_max': None,
    'page_shift': 'str(num)',

    'get_page': '//ol[@class="page-navigator"]',  # 分页链接提取区域xpath(必填)
    'get_item': '//div[@id="masonry"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="post-content"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
mntu3 = {
    'name': 'mntu3',
    'start_urls': 'http://446m.com/index.php/mntu/3/',  # 开始页(逗号分隔)

    'page_min': None,
    'page_max': None,
    'page_shift': 'str(num)',

    'get_page': '//ol[@class="page-navigator"]',  # 分页链接提取区域xpath(必填)
    'get_item': '//div[@id="masonry"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="post-content"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
mntu4 = {
    'name': 'mntu4',
    'start_urls': 'http://446m.com/index.php/mntu/4/',  # 开始页(逗号分隔)

    'page_min': None,
    'page_max': None,
    'page_shift': 'str(num)',

    'get_page': '//ol[@class="page-navigator"]',  # 分页链接提取区域xpath(必填)
    'get_item': '//div[@id="masonry"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="post-content"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
mntu130 = {
    'name': 'mntu130',
    'start_urls': 'http://446m.com/index.php/mntu/130/',  # 开始页(逗号分隔)

    'page_min': None,
    'page_max': None,
    'page_shift': 'str(num)',

    'get_page': '//ol[@class="page-navigator"]',  # 分页链接提取区域xpath(必填)
    'get_item': '//div[@id="masonry"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="post-content"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
mntu137 = {
    'name': 'mntu137',
    'start_urls': 'http://446m.com/index.php/mntu/137/',  # 开始页(逗号分隔)

    'page_min': None,
    'page_max': None,
    'page_shift': 'str(num)',

    'get_page': '//ol[@class="page-navigator"]',  # 分页链接提取区域xpath(必填)
    'get_item': '//div[@id="masonry"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="post-content"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
mntu175 = {
    'name': 'mntu175',
    'start_urls': 'http://446m.com/index.php/mntu/175/',  # 开始页(逗号分隔)

    'page_min': None,
    'page_max': None,
    'page_shift': 'str(num)',

    'get_page': '//ol[@class="page-navigator"]',  # 分页链接提取区域xpath(必填)
    'get_item': '//div[@id="masonry"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="post-content"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
sslkn = {
    'name': 'sslkn',
    'start_urls': 'https://wv.sslkn.name/photos/',  # 开始页(逗号分隔)

    'page_min': None,
    'page_max': None,
    'page_shift': 'str(num)',

    'get_page': '//ul[@class="pagination-holder"]',  # 分页链接提取区域xpath(必填)
    'get_item': '//div[@class="item  "]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="swiper-wrapper list-albums-images"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
jiepai = {
    'name': 'jiepai',
    'start_urls': 'https://nongfu66.top/xiao77/cat/jiepai?page=1',  # 开始页(逗号分隔)

    'page_min': None,
    'page_max': None,
    'page_shift': 'str(num)',

    'get_page': '//ul[@class="pagination"]',  # 分页链接提取区域xpath(必填)
    'get_item': '//div[@class="container-fluid"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@id="adarea"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
xiao77 = {
    'name': 'xiao77',
    'start_urls': 'https://nongfu66.top/xiao77/cat/self',  # 开始页(逗号分隔)

    'page_min': None,
    'page_max': None,
    'page_shift': 'str(num)',

    'get_page': '//ul[@class="pagination"]',  # 分页链接提取区域xpath(必填)
    'get_item': '//div[@class="container-fluid"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@id="adarea"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
oumei = {
    'name': 'oumei',
    'start_urls': 'https://nongfu66.top/oumei',  # 开始页(逗号分隔)

    'page_min': None,
    'page_max': None,
    'page_shift': 'str(num)',

    'get_page': '//ul[@class="pagination"]',  # 分页链接提取区域xpath(必填)
    'get_item': '//div[@class="container-fluid"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@id="adarea"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}

cos = {
    'name': 'cos',
    'start_urls': r'http://www.jdcoser.net/archives/category/cos%E5%86%99%E7%9C%9F/%E7%BB%9D%E5%AF%B9%E9%A2%86%E5%9F%9F#/page/19',  # 开始页(逗号分隔)

    'page_min': 1,
    'page_max': 19,
    'page_shift': 'str(num)',

    'get_page': r'http://www.jdcoser.net/archives/category/cos%E5%86%99%E7%9C%9F/%E7%BB%9D%E5%AF%B9%E9%A2%86%E5%9F%9F#/page/{}',  # 分页链接提取区域xpath(必填)
    'get_item': '//div[@class="excerpts"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//article[@class="article-content"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
cybesx_cosplay = {
    'name': 'cybesx_cosplay',
    'start_urls': 'https://www.cybesx.com/cosplay/',  # 开始页(逗号分隔)

    'page_min': 2,
    'page_max': 470,
    'page_shift': 'str(num)',

    'get_page': 'https://www.cybesx.com/cosplay/page/{}/',  # 分页链接提取区域xpath(必填)
    'get_item': '//main[@id="main"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="entry-content"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
cybesx_siwa = {
    'name': 'cybesx_siwa',
    'start_urls': 'https://www.cybesx.com/siwa/',  # 开始页(逗号分隔)

    'page_min': 2,
    'page_max': 707,
    'page_shift': 'str(num)',

    'get_page': 'https://www.cybesx.com/cosplay/page/{}/',  # 分页链接提取区域xpath(必填)
    'get_item': '//main[@id="main"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="entry-content"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
cybesx_model = {
    'name': 'cybesx_model',
    'start_urls': 'https://www.cybesx.com/model/',  # 开始页(逗号分隔)

    'page_min': 2,
    'page_max': 323,
    'page_shift': 'str(num)',

    'get_page': 'https://www.cybesx.com/cosplay/page/{}/',  # 分页链接提取区域xpath(必填)
    'get_item': '//main[@id="main"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="entry-content"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
cybesx_goddess = {
    'name': 'cybesx_goddess',
    'start_urls': 'https://www.cybesx.com/goddess/',  # 开始页(逗号分隔)

    'page_min': 2,
    'page_max': 4,
    'page_shift': 'str(num)',

    'get_page': 'https://www.cybesx.com/cosplay/page/{}/',  # 分页链接提取区域xpath(必填)
    'get_item': '//main[@id="main"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="entry-content"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}

cybesx_selfiephoto = {
    'name': 'cybesx_selfiephoto',
    'start_urls': 'https://www.cybesx.com/selfiephoto/',  # 开始页(逗号分隔)

    'page_min': 2,
    'page_max': 20,
    'page_shift': 'str(num)',

    'get_page': 'https://www.cybesx.com/cosplay/page/{}/',  # 分页链接提取区域xpath(必填)
    'get_item': '//main[@id="main"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="entry-content"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
cybesx_streetphotography = {
    'name': 'cybesx_streetphotography',
    'start_urls': 'https://www.cybesx.com/streetphotography/',  # 开始页(逗号分隔)

    'page_min': 2,
    'page_max': 80,
    'page_shift': 'str(num)',

    'get_page': 'https://www.cybesx.com/cosplay/page/{}/',  # 分页链接提取区域xpath(必填)
    'get_item': '//main[@id="main"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="entry-content"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}


hot2333 = {
    'name': 'hot2333',
    'start_urls': '',  # 开始页(逗号分隔)

    'page_min': 1,
    'page_max': 22,
    'page_shift': 'str(num)',

    'get_page': 'https://hot2333.com/?paged={}',  # 分页链接提取区域xpath(必填)
    'get_item': '//div[@class="post-thumbnail"]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="entry-content"]//img/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
cosporn = {
    'name': 'cosporn',
    'start_urls': '',  # 开始页(逗号分隔)

    'page_min': 1,
    'page_max': 52,
    'page_shift': 'str(num)',

    'get_page': 'https://cosporn.online/page/{}/',  # 分页链接提取区域xpath(必填)
    'get_item': '//div[@class="entry-featured-media "]',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="entry-inner"]//img[@decoding="async"]/@src',
    're_page': '.*',  # 分页链接正则(必填)
    're_item': '.*',  # 内容链接正则(必填)
}
args = {'wait': 2, 'lua_source': script}
args_shot = {'wait': 0.5, 'lua_source': script_shot}


class Common_Spider(CrawlSpider):
    name = "common_"
    seen = set()

    def __init__(self):
        self.rule = cosporn
        self.allowed_domains = self.rule.get('allowed_domains', '*')
        self.name = self.rule['name']
        self.start_urls = self.rule['start_urls'].split(",")
        self.rules = [
            Rule(LinkExtractor(allow=self.rule['re_item'], restrict_xpaths=[self.rule['get_item']]), process_request='item_request', follow=False),

        ]
        if not (self.rule['page_min'] and self.rule['page_max'] and self.rule['get_page'] and self.rule['page_shift']):
            self.rules.append(Rule(LinkExtractor(allow=self.rule['re_page'], restrict_xpaths=[
                              self.rule['get_page']]), process_request='page_request', follow=True),)
        # if os.path.exists(self.rule["name"] + '.json'):
        #     self.data = json.load(open(self.rule["name"] + '.json', 'r'))
        # else:
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
            if len(self.seen) >= 10000:
                self.seen = set()
            print(rule)
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
        imgs = response.xpath('//div[@class="album"]//div[@class="img-holder"]//img/@src').getall()
        imgs = response.xpath(self.rule['get_img']).getall()
        print(response.url, len(imgs))
        self.data.extend(imgs)
        if time.time() - self.start > 100000:
            self.start = time.time()
            print('共有', len(self.data), '个')
            with open(f'D:/python/viewer/src/renderer/src/assets/json/{self.rule["name"]}.json', 'w') as f:
                f.write(json.dumps(self.data))

    @staticmethod
    def close(spider, reason):
        with open(f'D:/python/viewer/src/renderer/src/assets/json/{spider.rule["name"]}.json', 'w') as f:
            f.write(json.dumps(spider.data))
        print('共有', len(spider.data), '个')
        closed = getattr(spider, "closed", None)
        if callable(closed):
            return closed(reason)

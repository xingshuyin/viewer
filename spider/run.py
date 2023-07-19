from twisted.internet import reactor
import time
import pymysql
from scrapy.crawler import CrawlerRunner
from multiprocessing import Process
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from img.spiders.common import CommonSpider
from img.spiders.common_json import JsonSpider

spider_types = {
    1: '分页爬虫',
    2: 'json爬虫'
}

rule = [
    {
        'name': '河北科技大学就业信息网-招聘会',
        'allowed_domains': '*',  # 域名列表(逗号分隔)
        'start_urls': 'https://job.hebust.edu.cn/jobfair/index?domain=hebust',  # 开始页(逗号分隔)


        'type': 1,

        'page_min': None,  # 分页页数开头
        'page_max': None,  # 分页页数最大值 --- 优先使用分页页数正则而不是最大值
        'page_shift': None,


        # 上下两块选其一
        'get_page': '//ul[@class="page"]',  # 分页链接提取区域xpath(必填)
        'get_item': '//ul[@class="infoList jobfairList"]',  # 内容链接提取区域xpath(必填)
        're_page': '.*',  # 分页链接正则(必填)
        're_item': '.*',  # 内容链接正则(必填)

        'path_name': '//title/text()',  # 标题xpath(必填)
        'path_time': '//ul[@class="clearfix"]/li[4]/span/text()',  # 时间xpath(必填)
        'path_content': '//div[@class="aContent"]',  # 内容xpath(必填)
        'path_source': '//ul[@class="clearfix"]/li[6]/span/text()',  # 来源xpath(必填)
        'path_area': '//ul[@class="clearfix"]/li[3]//text()',  # 来源xpath(必填)
        're_time': None,  # 时间正则(选填)
        're_source': None,  # 来源正则(选填)
        're_area': None,  # 地址正则(选填)
        'enable': 0,  # 是否启用
    },
    {
        'name': '河北工程大学就业信息网-在线招聘',
        'allowed_domains': '*',  # 域名列表(逗号分隔)
        'start_urls': '',  # 开始页(逗号分隔)


        'type': 2,

        'page_min': None,  # 分页页数开头
        'page_max': None,  # 分页页数最大值 --- 优先使用分页页数正则而不是最大值
        'page_shift': 'str(num)',  # 分页页数转换


        # 上下两块选其一
        'get_page': 'https://hbgc.bysjy.com.cn/module/getonlines?start_page=1&count=15&start={}',  # 分页链接提取区域xpath(必填) | 分页链接格式化
        'get_item': """[i['link_type'] if i['link_type'] else f'https://hbgc.bysjy.com.cn/detail/online?id={i["recruitment_id"]}'  for i in res['data']] """,  # 内容链接提取区域xpath(必填): json分页的话获取json结果里所有item链接的列表, 返回的json数据变量是res
        're_page': '.*',  # 分页链接正则(必填)
        're_item': '.*',  # 内容链接正则(必填)

        'path_name': '//h1[@class="dh-tit"]/text()|//h1[@id="activity-name"]//text()',  # 标题xpath(必填)
        'path_time': '//span[@class="time"]//text()|//em[@id="publish_time"]//text()',  # 时间xpath(必填)
        'path_content': '//div[@class="details-content"]|//div[@id="js_content"]',  # 内容xpath(必填)
        'path_source': '//ul[@class="clearfix"]/li[6]/span/text()',  # 来源xpath(必填)
        'path_area': '//ul[@class="clearfix"]/li[3]//text()',  # 来源xpath(必填)
        're_time': None,  # 时间正则(选填)
        're_source': None,  # 来源正则(选填)
        're_area': None,  # 地址正则(选填)
        'enable': 1,  # 是否启用
    },
]


def main():
    start = time.time()
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    # cursor.execute('SELECT * FROM `spider`')
    # spiders = cursor.fetchall()
    # cursor.close()
    # db.close()
    for i in rule:
        if not i['enable']:
            continue
        print('运行- ', i['name'])
        if i['type'] == 1:
            runner.crawl(CommonSpider, rule=i)
        elif i['type'] == 2:
            runner.crawl(JsonSpider, rule=i)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished
    end = time.time()
    print('程序运行时间为: %s s' % (end - start))


if __name__ == '__main__':
    # db = pymysql.connect(
    #     host="localhost",
    #     port=3306,
    #     user='root',  #在这里输入用户名
    #     password='123456',  #在这里输入密码
    #     charset='utf8mb4',
    #     db='smart_edu')  #连接数据库
    # cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    main()

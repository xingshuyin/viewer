from hashlib import md5
import re
import base64
from PIL import Image
from io import BytesIO
'''
description: 获取链接几级父级目录
param {*} full_url 提取父级目录的链接
param {*} num 提取级别
return {string} 父级目录
'''


def root_path(full_url, num):
    r = full_url
    for _ in range(num):
        r = r[:r.rindex('/')]
    return r


'''
description: 获取链接完整路径
param {*} url
param {*} response
return {*}
'''


def path(url, response):
    full_url = response.url
    if '../' in url:
        f_path_count = url.count('../')
        root = root_path(full_url, f_path_count + 1)
        p = url.strip('../')
    elif './' in url:
        root = root_path(full_url, 1)
        p = url.strip('./')
    elif url.startswith('/'):
        t = [s.start() for s in re.finditer('/', response.url)]  # TODO: 查找返回索引
        root = response.url[:t[2]]  # 获取网站根目录
        p = url.strip('/')
    else:
        return url
    return root + '/' + p

    # if '../../../' in url:
    #     url = base4 + '/' + url.strip('../')
    # if '../../' in url:
    #     url = base3 + '/' + url.strip('../')
    # elif '../' in url:
    #     url = base2 + '/' + url.strip('../')
    # elif './' in url:
    #     url = base1 + '/' + url.strip('../')


def get_group(a, response, pre):
    # print(a.group(3))
    return pre + path(a.group(1), response) + '"'


'''
description: 处理所有图片链接转换为绝对路径
param {*} content
param {*} response
return {*}
'''


def deal_path(content, response):

    content = re.sub(r'src="(.*?)"', lambda x: get_group(x, response, 'src="'), content)
    content = re.sub(r'href="(.*?)"', lambda x: get_group(x, response, 'href="'), content)
    return content


def parse_item(self, response):
    # image = base64.b64decode(response.data['image'], altchars=None, validate=False)
    # image = Image.open(BytesIO(image))
    # image.save('shot.png')
    # image.show()

    name = ''.join(response.xpath(self.rule['path_name']).getall()).replace(
        '\n', '').strip()
    url = response.url
    url_hash = md5(response.url.encode(encoding='UTF-8')).hexdigest()
    hold_time = response.xpath(self.rule['path_time'])
    source = response.xpath(self.rule['path_source'])
    area = response.xpath(self.rule['path_area'])
    content = ''.join(response.xpath(self.rule['path_content']).getall())
    content = deal_path(content, response)  # 处理所有相对路径的链接
    content_source = deal_path(response.data['html'], response)
    content_image = response.data['image']
    content_text = ''.join(
        response.xpath(self.rule['path_content']).xpath(
            './/text()').getall())  # 处理所有相对路径的链接
    if self.rule['re_time']:
        hold_time = hold_time.re(self.rule['re_time'])
        if len(hold_time) > 0:
            hold_time = hold_time[0].replace('\n', '').strip()
        else:
            hold_time = None
    else:
        hold_time = ''.join(hold_time.getall())
    if self.rule['re_source']:
        source = source.re(self.rule['re_source'])  # 获取文章来源
        if len(source) > 0:
            source = source[0].replace('\n', '').strip()
        else:
            source = None
    else:
        source = ''.join(source.getall())
    if self.rule['re_area']:
        area = area.re(self.rule['re_area'])  # 获取文章来源
        if len(area) > 0:
            area = area[0].replace('\n', '').strip()
        else:
            area = None
    else:
        area = ''.join(area.getall())
    # with open('a.html','w', encoding='utf-8') as f:
    #     f.write(content_source)
    print(name, response.url, hold_time, source, area)


def parse_item_shot(self, response):
    # image = base64.b64decode(response.data['image'], altchars=None, validate=False)
    # image = Image.open(BytesIO(image))
    # image.save('shot.png')
    # image.show()

    name = ''.join(response.xpath(self.rule['path_name']).getall()).replace('\n', '').strip()
    url = response.url
    url_hash = md5(response.url.encode(encoding='UTF-8')).hexdigest()
    hold_time = response.xpath(self.rule['path_time'])
    source = response.xpath(self.rule['path_source'])
    area = response.xpath(self.rule['path_area'])
    content = ''.join(response.xpath(self.rule['path_content']).getall())
    content = deal_path(content, response)  # 处理所有相对路径的链接
    content_source = deal_path(response.data['html'], response)
    content_image = response.data['image']
    content_text = ''.join(response.xpath(self.rule['path_content']).xpath('.//text()').getall())  # 处理所有相对路径的链接
    if self.rule['re_time']:
        hold_time = hold_time.re(self.rule['re_time'])
        if len(hold_time) > 0:
            hold_time = hold_time[0].replace('\n', '').strip()
        else:
            hold_time = None
    else:
        hold_time = ''.join(hold_time.getall())
    if self.rule['re_source']:
        source = source.re(self.rule['re_source'])  # 获取文章来源
        if len(source) > 0:
            source = source[0].replace('\n', '').strip()
        else:
            source = None
    else:
        source = ''.join(source.getall())
    if self.rule['re_area']:
        area = area.re(self.rule['re_area'])  # 获取文章来源
        if len(area) > 0:
            area = area[0].replace('\n', '').strip()
        else:
            area = None
    else:
        area = ''.join(area.getall())
    # with open('a.html','w', encoding='utf-8') as f:
    #     f.write(content_source)
    print(name, response.url, hold_time, source, area)


# 网页源码标注关键词
def mark(html, words):
    html = re.sub('<meta.*?>', '', html)
    for i in words:
        html = re.sub(
            i,
            f'<strong style="background-color: yellow;color: black;font-size:150%;">{i}</strong>',
            html)
    return html


script = """
function main(splash, args)
    headers = {
        ["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    splash:set_custom_headers(headers)
    assert(splash:go(args.url))
    assert(splash:wait(1))
  return splash:html()
end
"""
script = """
function main(splash, args)
    assert(splash:go(args.url))
    assert(splash:wait(1))
  return splash:html()
end
"""

script_shot = """
function main(splash, args)
    headers = {
        ["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    splash:set_custom_headers(headers)
    splash.private_mode_enabled = false
    assert(splash:go(args.url))
    assert(splash:wait(1))
    splash:set_viewport_full()
    return {
        image = splash:png(),
        html = splash:html()
    }
end
"""

splash_args = {
    'wait': 0.5,
    'lua_source': script,
    'timeout': 90,
    'resource_timeout': 10
}
splash_args_shot = {
    'wait': 0.5,
    'lua_source': script_shot,
    'timeout': 90,
    'resource_timeout': 10
}

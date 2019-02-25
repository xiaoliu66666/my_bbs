"""
电影天堂的爬虫，爬取每部电影的部分信息
"""
from lxml import html
import requests
from exts import collections
from config import HEADERS, BASE_DOMAIN

etree = html.etree


def get_detail_urls(url):
    resp = requests.get(url, headers=HEADERS)
    text = resp.text
    html = etree.HTML(text)
    detail_urls = html.xpath("//table[@class='tbspan']//a/@href")
    detail_urls = map(lambda url: BASE_DOMAIN + url, detail_urls)
    return detail_urls


def parse_detail_page(url):
    movie = {}
    resp = requests.get(url, headers=HEADERS)
    text = resp.content.decode("gbk")
    html = etree.HTML(text)
    title = html.xpath("//div[@class='title_all']//font/text()")[0]
    movie["电影名"] = title

    zoom = html.xpath("//div[@id='Zoom']")[0]
    imgs = zoom.xpath(".//img/@src")
    cover = imgs[0]
    movie["封面"] = cover

    def parse_info(info, rule):
        return info.replace(rule, "").strip()

    infos = zoom.xpath(".//text()")
    # print('infos:', infos)
    for index, info in enumerate(infos):
        # print('index', index)
        # print('info before', info)
        if info.startswith("◎年　　代"):
            info = parse_info(info, "◎年　　代")
            movie["年代"] = info
        elif info.startswith("◎产　　地"):
            info = parse_info(info, "◎产　　地")
            movie["产地"] = info
        elif info.startswith("◎类　　别"):
            info = parse_info(info, "◎类　　别")
            movie["类别"] = info
        elif info.startswith("◎字　　幕"):
            info = parse_info(info, "◎字　　幕")
            movie["字幕"] = info
        elif info.startswith("豆瓣评分"):
            info = parse_info(info, "豆瓣评分")
            movie["豆瓣评分"] = info
        elif info.startswith("◎导　　演"):
            info = parse_info(info, "◎导　　演")
            movie["导演"] = info
        elif info.startswith("◎主　　演"):
            info = parse_info(info, "◎主　　演")
            actors = [info]
            for x in range(index + 1, len(infos)):
                actor = infos[x].strip()
                if actor.startswith("◎"):
                    break
                actors.append(actor)
            movie["演员"] = actors
        elif info.startswith("◎简　　介"):
            profile = ''
            for x in range(index + 1, len(infos)):
                # print('简介infos[x]', x, infos[x])
                profile += infos[x].strip()
                if infos[x].startswith("【下载地址】") or infos[x].startswith("◎"):
                    break
                movie["简介"] = profile

    download_url = html.xpath("//td[@bgcolor='#fdfddf']/a/@href")[0]
    movie["下载链接"] = download_url
    return movie


def spider():
    base_url = "http://www.dytt8.net/html/gndy/dyzz/list_23_{}.html"

    for i in range(1, 2):
        url = base_url.format(i)
        detail_urls = get_detail_urls(url)
        for detail_url in detail_urls:
            movie = parse_detail_page(detail_url)
            # print(movie)

            # 写入mongodb
            collections.insert_one(movie)


# if __name__ == '__main__':
#     spider()

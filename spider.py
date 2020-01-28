#!/usr/bin/python
# -*- coding: UTF-8 -*-
# baidupictures_spider

import requests
import re

method = "GET"
url = "https://image.baidu.com/search/acjson"

"""
rn: pics to load
pn: pics loaded
queryWord, word: pics keywords
"""
keywords = "赛博朋克"
payload = {
    "tn": "resultjson_com",
    "ipn": "rj",
    "ct": "201326592",
    "fp": "result",
    "queryWord": keywords,
    "cl": "2",
    "lm": "-1",
    "ie": "utf-8",
    "oe": "utf-8",
    "st": "-1",
    "ic": "0",
    "word": keywords,
    "face": "0",
    "istype": "2",
    "nc": "1",
    "pn": "0",
    "rn": "30"
        }

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36",
    "referer": "https://image.baidu.com"
}


def spider(method, url, payload, headers):
    """
    XHR request
    """
    response = requests.request(method, url, params=payload, headers=headers)
    return response


def decode_url(url):
    """
    decode encrypted urls of pictures
    """
    token = {'w': "a", 'k': "b", 'v': "c", '1': "d",
             'j': "e", 'u': "f", '2': "g", 'i': "h",
             't': "i", '3': "j", 'h': "k", 's': "l",
             '4': "m", 'g': "n", '5': "o", 'r': "p",
             'q': "q", '6': "r", 'f': "s", 'p': "t",
             '7': "u", 'e': "v", 'o': "w", '8': "1",
             'd': "2", 'n': "3", '9': "4", 'c': "5",
             'm': "6", '0': "7",
             'b': "8", 'l': "9", 'a': "0", '_z2C$q': ":",
             "_z&e3B": ".", 'AzdH3F': "/"}
    url = re.sub(r'(?P<matched>_z2C\$q|_z\&e3B|AzdH3F)', lambda matched: token.get(matched.group("matched")), url)
    return re.sub(r'(?P<matched>[0-9a-w])', lambda matched: token.get(matched.group("matched")), url)


def parser(pic_info):
    """
    parse pics info, extract urls
    """
    # transforms str to json to dict
    pic_urls = re.findall('"objURL":"(.+?)"', pic_info, re.S)
    for i in range(0, len(pic_urls)):
        pic_urls[i] = decode_url(pic_urls[i])
    return pic_urls


if __name__ == '__main__':
    text = spider(method, url, payload, headers).text
    pic_urls = parser(text)

    # download pics
    num = 0
    for pic_url in pic_urls:
        cate = pic_url.split(".")[-1]

        content = None
        try:
            content = requests.get(url=pic_url, timeout=5).content
        except requests.exceptions.ConnectTimeout:
            print("failed to connect", pic_url)
            continue
        except requests.exceptions.ReadTimeout:
            print("failed to read", pic_url)
            continue

        try:
            with open("{num}.{cate}".format(num=num, cate=cate), "wb+") as f:
                f.write(content)
        except FileNotFoundError:
            with open("{num}.png".format(num=num), "wb+") as f:
                f.write(content)
        except OSError:
            with open("{num}.png".format(num=num), "wb+") as f:
                f.write(content)

        num += 1

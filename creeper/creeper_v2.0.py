"""
    python v2.0版本
    主要爬取网通社经销社数据
    作者: xavier
    时间: 2017.12.13 (南京大屠杀纪念日)
"""
import requests
from bs4 import BeautifulSoup
import csv

import urllib
import gzip

def get_soup(url):
    r = requests.get(url, timeout=30)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'lxml')
    return soup

def get_ina_price(soup):
    div_ina_price = soup.find('div', {'class': 'ina_price'})
    div_ina_bt = div_ina_price.find('div', {'class': 'ina_bt'})
    ul = div_ina_bt.find('ul')
    header = []
    for li in ul:
        title = li.text
        header.append(title)


def main():
    """
        主函数
    """
    url = "http://auto.news18a.com/shanghai/"
    soup = get_soup(url)
    get_ina_price(soup)


if __name__ == '__main__':
    main()
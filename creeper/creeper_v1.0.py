"""
    python 爬虫
    爬虫对象: 网通社极趣社区
    作者: xavier
    时间: 2017/12/12
"""

import requests
from bs4 import BeautifulSoup
import csv

def configuration_bs(url):
    r = requests.get(url, timeout=30)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup

def get_web_image(soup):
    """
        获取web界面上的图片
    """
    div_class_ina_focus = soup.find_all('div', {'class': 'ina_focus'})[0]
    div_class_ina_silde = div_class_ina_focus.find('div', {'class': 'ina_silde'})

    div_class_ina_focusnr = div_class_ina_silde.find('div', {'class': 'ina_focusnr'})
    div_class_ina_focusnr_list = div_class_ina_focusnr.find_all('a')

    img_link_list = []
    for a in div_class_ina_focusnr_list:
        img = a.find('img')
        title = img['alt']
        img_link = img['data-original']
        html_link = img['src']
        img_link_list.append((title, img_link, html_link))

    return img_link_list

def get_ina_focus(img_link_list):
    header = ['标题', '图片链接', '跳转链接']
    with open('ina_focus.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        # print(img_link_list)
        for title, img_link, html_link in img_link_list:
            row_array = [title, img_link, html_link]
            writer.writerow(row_array)

def get_hot(soup):
    div_ina_hot = soup.find_all('div', {'class': 'ina_hot'})[0]
    div_ina_slide = div_ina_hot.find('div', {'class': 'ina_silde'})
    ul_list = div_ina_slide.find('ul')
    li_list = ul_list.find_all('li')
    ina_hot_list = []
    for li in li_list:

        a_tag = li.find('a')
        img_tag = li.find('img')

        title = a_tag['title']
        href = a_tag['href']
        img_link = img_tag['data-original']
        ina_hot_list.append((title, href, img_link))
    return ina_hot_list

def save_hot_list(ina_hot_list):
    header = ['标题', '图片地址', '图片链接']
    with open("ina_hot_list.csv", 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for title, href, img_link in ina_hot_list:
            row_array = [title, img_link, href]
            writer.writerow(row_array)


def get_ina_slide(soup):
    div_ina_slide = soup.find_all('div', {'class', 'ina_silde'})[5]
    div_ina_list = div_ina_slide.find('div', {'class', 'ina_list'})
    dl_list = div_ina_list.find_all('dl')

    story_list = []
    for dl in dl_list:
        dd_1 = dl.find_all('dd')[0]
        dd_2 = dl.find_all('dd')[1]
        dt = dl.find('dt')

        # dd_1 数据爬取
        div_ina_photo = dd_1.find('div',{'class': 'ina_photo'})
        div_ina_date = dd_1.find('div',{'class': 'ina_date'})

        ina_photo_a = div_ina_photo.find('a')
        ina_photo_a_img = ina_photo_a.find('img')

        user_info = ina_photo_a['href']
        user_photo = ina_photo_a_img['src']
        user_name = ina_photo_a.text.replace('\n', '')

        div_ina_date_time = div_ina_date.text

        # dd_2 数据爬取
        dd_2_h3 = dd_2.find('h3')
        div_dd_2_ina_list_jj = dd_2.find('div', {'class', 'ina_list_jj'})
        div_dd_2_ina_list_bottom = dd_2.find('div', {'class', 'ina_list_bottom'})

        dd_2_h3_a = dd_2_h3.find('a')
        jump_link = dd_2_h3_a['href']
        story_title = dd_2_h3_a['title']

        story_content = div_dd_2_ina_list_jj.text

        div_dd_2_ina_list_bottom_ina_label = div_dd_2_ina_list_bottom.find('div', {'class': 'ina_label'})
        div_dd_2_ina_list_bottom_ina_label_span = div_dd_2_ina_list_bottom_ina_label.find('span')
        story_tag = div_dd_2_ina_list_bottom_ina_label_span.text

        div_dd_2_ina_list_bottom_p = div_dd_2_ina_list_bottom.find('p')
        div_dd_2_ina_list_bottom_p_span_list = div_dd_2_ina_list_bottom_p.find_all('span')

        story_watching = div_dd_2_ina_list_bottom_p_span_list[0].text
        story_message = div_dd_2_ina_list_bottom_p_span_list[1].text
        story_good = div_dd_2_ina_list_bottom_p_span_list[2].text

        #dt 数据爬取
        dt_a = dt.find('a')
        dt_a_img = dt_a.find('img')
        story_cover = dt_a_img['src']

        story_list.append((user_name, user_photo, user_info, div_ina_date_time, story_cover, story_title, story_content, story_tag, story_watching, story_message, story_good, jump_link))

    return story_list

def save_story_list(story_list):
    header = [
        '用户名',
        '用户头像链接',
        '用户详情链接',
        '文章发布时间',
        '文章封面链接',
        '文章标题',
        '文章内容',
        '文章标签',
        '文章查看人数',
        '文章回复人数',
        '文章点赞人数',
        '文章跳转链接',
    ]
    with open('story_list.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for info in story_list:
            row_array = list(info)
            writer.writerow(row_array)


def main():
    """
        主函数
    """
    url = 'http://play.news18a.com/index.php'
    soup = configuration_bs(url)

    # 获取轮播图图片, 标题, 跳转界面链接
    # img_link_list = get_web_image(soup)
    # get_ina_focus(img_link_list)

    #获取热点图
    # ina_hot_list = get_hot(soup)
    # save_hot_list(ina_hot_list)

    #获取最新文章页面内容
    story_list = get_ina_slide(soup)
    save_story_list(story_list)





if __name__ == '__main__':
    main()
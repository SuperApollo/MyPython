import requests
from bs4 import BeautifulSoup
import os


# =================定义一个类解析和存储数据=============

class Spider:
    def savePageInfo(self, _url, _position):
        # 网站地址
        url = _url
        # 存储位置
        position = _position
        print('存储位置' + position)
        # 获取源码
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
        }
        html = requests.get(url, headers=headers).text
        print('获取源码成功')
        # soup = BeautifulSoup(html, 'lxml')
        items = BeautifulSoup(html, 'lxml').find('div', class_='article').find_all('div', class_='item')
        # 查找出所有相关节点
        # pics = soup.find_all('div', {'class': 'pic'})
        # infos = soup.find_all('div', {'class': 'info'})
        print('匹配' + str(len(items)) + '条')
        # 如果文件夹不存在，创建
        if not os.path.isdir(position):
            os.makedirs(position)

        i = 0
        for item in items:
            pic = item.find('div', class_='pic').find('a')
            print(pic)

            # for tag in pics:
            #     fp = open(position + '豆瓣电影排行.txt', 'wb')
            #     title = infos[i].a.get('title')
            #     img = tag.a.img.get('src')
            #     print(title)
            #     print(img)
            #     fp.write((str(title) + '\n').encode('utf-8'))
            #     fp.write((str(img) + '\n').encode('utf-8'))
            #     i += 1
            #     fp.close()


# ================爬豆瓣电影top250前20页==================

url = 'https://movie.douban.com/top250?start=0&filter='
spider = Spider()
position = 'F:\\ECopy\\ApolloWang\\Python\\douban\\'
spider.savePageInfo(url, position)

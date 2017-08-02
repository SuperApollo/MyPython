# 操作系统功能
import os
# 正则
import re

# 网络
import requests


# 定义一个类
class Spider:
    # 定义一个函数
    def savePageInfo(self, _url, _position, _regPic, _regName):
        # 要爬的网址
        url = _url
        # 本地地址
        position = _position
        print('本地存储位置：' + position)
        # 获取网页源代码
        html = requests.get(url).text
        print('获取网站源码成功...')
        # 图片地址正则
        regPic = _regPic
        # 图片名称正则
        regName = _regName
        pic_url = re.findall(regPic, html)
        name_str = re.findall(regName, html)
        print('匹配到' + str(len(pic_url)) + '条数据')
        print('name'+str(len(name_str))+'条')
        i = 0
        for each in pic_url:
            pic = requests.get(each)
            print('保存图片' + each)
            # 如果文件夹不存在，创建
            if not os.path.isdir(position):
                os.makedirs(position)
            name = name_str[i]
            fp = open(position + name + '.jpg', 'wb')
            fp.write(pic.content)
            fp.close()
            i += 1


# ==========================网页爬取图片====================
positon_end = ''
# 要爬的网址
# url = 'http://www.umei.cc/' + positon_end
# url = 'http://www.umei.cc/meinvtupian/xingganmeinv/' + positon_end
# url = 'https://tuchong.com/' + positon_end
# url = 'http://bbs.fengniao.com/forum/5025026.html/'

# 正则
# regX = r'src=(.*?\.jpg)'
# regX = re.compile(r'src="(.+?\.jpg)"')
regJpg = re.compile(r'data-lazyload-img-src="(.+?\.jpg\?.*)"')
# ==================正则含义====================================
# . 匹配任意除换行\n外的字符
# \d 数字 0-9
# \D 非数字
# \s 空白字符
# \S 非空白字符
# \w 单词字符
# \W 费单词字符
# * 匹配前一个字符0次或无限次
# + 匹配前一个字符1次或无限次
# ? 匹配前一个字符0次或1次
# 参数 url, 储存位置, 爬取的正则
spider = Spider()
# ==================获取poco人像前20页===========================
# for num in range(1, 20):
#     # 本地地址
#     position = 'F:\\ECopy\\ApolloWang\\Python\\poco_pic\\' + str(num) + '\\'
#     url = 'http://photo.poco.cn/vision.htx&p=' + str(num) + '&index_type=hot&tid=-1&gid=0#list'
#     spider.savePageInfo(url, position, regX)
# ==================获取5593879的所有图片=========================
# position = 'F:\\ECopy\\ApolloWang\\Python\\5593879_pic\\'
# url = 'http://photo.poco.cn/lastphoto-htx-id-5593879-p-0.xhtml'
# spider.savePageInfo(url, position, regJpg)
# ==================爬取图虫首页图片===============================
position = 'F:\\ECopy\\ApolloWang\\Python\\tuchong_pic\\'
url = 'https://tuchong.com/'
regPic = re.compile(r'data-lazy-url="(.+?\.jpg.*?)"')
regName = re.compile(r'<h3 class="event-title">(.*?)</h3>')
spider.savePageInfo(url, position, regPic, regName)

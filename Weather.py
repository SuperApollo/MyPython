import csv
import requests
from bs4 import BeautifulSoup
import xlsxwriter
import os

# 创建 Excel
workbook = xlsxwriter.Workbook('狗只在手，天气我有.xlsx')
# 创建 sheet
worksheet = workbook.add_worksheet('weather')
# 清空列及行
worksheet.set_column('A:A', 7)
worksheet.set_column('B:B', 7)
worksheet.set_column('C:C', 7)
worksheet.set_column('D:D', 7)
worksheet.set_column('E:E', 7)


# 写入 Excel 文件
def save_data(colom, content_list):
    colom_a = 'A' + colom
    colom_b = 'B' + colom
    colom_c = 'C' + colom
    colom_d = 'D' + colom
    colom_e = 'E' + colom
    # 城市
    worksheet.write(colom_a, content_list[0])
    # 日期
    worksheet.write(colom_b, content_list[1])
    # 天气
    worksheet.write(colom_c, content_list[2])
    # 最高温度
    worksheet.write(colom_d, content_list[3])
    # 最低温度
    worksheet.write(colom_e, content_list[4])


# 拼接 url
def get_url(city_name):
    url = 'http://www.weather.com.cn/weather/'
    with open('city.txt', 'r', encoding='UTF-8')as fs:
        lines = fs.readlines()
        for line in lines:
            if (city_name in line):
                code = line.split('=')[0].strip()
                return url + code + '.shtml'
    raise ValueError('invalid city name')


# 获取网页
def get_html(url):
    html = requests.get(url)
    html.encoding = 'utf-8'
    return html.text


# 获取数据
def get_data(html_text, city):
    final = []
    bs = BeautifulSoup(html_text, 'html.parser')
    body = bs.body
    data = body.find('div', {'id': '7d'})
    ul = data.find('ul')
    li = ul.find_all('li')

    for day in li:
        temp = [city]
        date = day.find('h1').string
        temp.append(date)
        inf = day.find_all('p')
        temp.append(inf[0].string)
        if inf[1].find('span') is None:
            temperature_highest = None
        else:
            temperature_highest = inf[1].find('span').string
            temperature_highest = temperature_highest.replace('C', '')
        temperature_lowest = inf[1].find('i').string
        temperature_lowest = temperature_lowest.replace('C', '')
        temp.append(temperature_highest)
        temp.append(temperature_lowest)
        final.append(temp)

    return final


# 写入 csv 文件
def write_data(data, name):
    file_name = name
    with open(file_name, 'a', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)


# 写入 csv 文件的第一行（标题）
def write_title(title, name):
    file_name = name
    # 加入newline=''为了防止出现空行
    with open(file_name, 'a', newline='')as f:
        f_csv = csv.writer(f)
        f_csv.writerow(title)


# 判断csv文件中是不包含某字符串
def contain_words(words, name):
    hasContains = False
    if os.path.exists(name):
        f = open(name, 'r')
        lines = f.readlines()
        for line in lines:
            for word in words:
                if word in line:
                    hasContains = True
                    break
    return hasContains


# 主函数
if __name__ == '__main__':
    cities = input('请狗只输入城市名，以空格隔开，例如 顺义 海淀: ').split(' ')
    if cities[0] != '':
        head = ['城市', '日期', '天气', '最高温度', '最低温度']
        if not contain_words(head, '狗只在手，天气我有.csv'):
            write_title(head, '狗只在手，天气我有.csv')
        colom = 2
        for city in cities:
            print('正在获取' + city + '的数据,狗只请稍等...')
            url = get_url(city)
            html_doc = get_html(url)
            print('获取' + city + '数据成功！')
            print('开始解析' + city + '数据,狗只请稍等...')
            result = get_data(html_doc, city)
            print('解析' + city + '数据成功！')
            print('开始写入文件...')
            write_data(result, '狗只在手，天气我有.csv')
            save_data('1', ['城市', '日期', '天气状况', '最高温度', '最低温度'])
            for day_list in result:
                save_data(('%d' % (colom)), day_list)
                colom += 1
            print('写入文件成功！')

        print('程序运行完毕，快去查看“狗只在手，天气我有”文件吧！')
    else:
        print('必须输入城市名哦！')
    workbook.close()

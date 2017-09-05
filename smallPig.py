# -*- coding: utf-8 -*-
'''
@author: Yalei Meng    E-mail: yaleimeng@sina.com
@license: (C) Copyright 2017, HUST Corporation Limited.
@desc:爬取某城市小猪短租的前300多条房源的基本信息。主要是描述、地址、价位，房屋图片链接，房东网名、照片、性别；
并写入csv表格。如果需要其他信息请根据实际需要修改。
@DateTime: Created on 2017/9/4，at 19:36
'''
from bs4 import BeautifulSoup
import requests as rq
import time
import csv
import codecs

  #从首页出发。目标是分析300个链接。根据数字规律构造网址的列表。
site =['http://gz.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i)) for i in range(1,15)]
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3192.0 Safari/537.36'
head = {'User-Agent':ua}

newUrls=set()
csvRows = []
# def updatePage(soup):
#     pages = soup.find_all('a',target='_self')  #从页脚获得新的页面链接。
#     for page in pages:                         #只把全新的页面加入到新页面集合。
#         if page['href'] not in newPages and page['href'] not in oldPages:
#             newPages.add(page['href'])
#     print(newPages)

def  getAllurls(web):
    r = rq.get(web, headers=head)
    soup = BeautifulSoup(r.text, 'html.parser')
    out = soup.find('ul', class_='pic_list clearfix').find_all('li')  # 这里是需要访问的单个元素网页。
    for var in out:
        url = var.find('a')['href']
        if url not in newUrls:
            newUrls.add(url)
            print(url)

def dealPage(myPage):
    r = rq.get(myPage)
    soup = BeautifulSoup(r.text, 'lxml')
    #print(soup)
    if soup.find('div', class_='member_pic').find('div')['class'] == ['member_ico1']:
        gender = 'female'
    else:
        gender = 'male'
    data ={
        'title'  :soup.find('div',{'class':'pho_info'}).find('em').text,
        'address':soup.find('div',class_='con_l').find('p')['title'],
        'roomPic':soup.find('div',class_='pho_show_big').find('img')['src'],
        'price':soup.find('div',class_='day_l').find('span').text,
        'owner':soup.find('div',class_='w_240').find('a')['title'],
        'gender': gender,
        'ownerPic': soup.find('div', class_='member_pic').find('a')['href'],
    }
    csvRows.append(data)
    print(data)

for st in site:             #从site每个页面分别请求，并添加url到newUrls。300个为止。
    getAllurls(st)
    time.sleep(1.5)
    if len(newUrls)>=300:
        break

for eve in newUrls:         #针对newUrls里面每个url,做详情页的爬取。
    dealPage(eve)
    time.sleep(1.5)

#把词典数据写入到csv文件。
print('字典列表的个数为%d'%len(csvRows))
rowHeader = ['title','address','roomPic','price','owner','gender','ownerPic']
with open('E:/romm.csv','w')as f:
    f.write(codecs.BOM_UTF8)
    f_csv = csv.DictWriter(f,rowHeader)
    f_csv.writeheader()
    f_csv.writerows(csvRows)

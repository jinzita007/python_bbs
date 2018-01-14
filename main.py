# -*- coding: utf-8 -*-
#---------------------------------------
#   程序：帖子爬虫
#   版本：0.1.5
#   作者：woaitianwen
#   日期：2018-1-10
#   语言：Python 3.6
#   操作：输入网址后就获取主题列表、然后进入帖子找作者、内容和发布时间
#---------------------------------------

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import mysql.connector

#连接mysql数据库
conn = mysql.connector.connect(user='root', password='root', database='bbs')
#使用cursor()方法获取操作游标
cur = conn.cursor()

#定义一个帖子的类
class Tieba:

    def __init__(self):

        baseurl = "http://www.deyi.com";
        self.baseurl = baseurl
        self.datas = []
        self.page = []
        self.pages = set()
        print("开始爬虫-------------------------------")

    #获取论坛的主题列表
    def get_home(self):
        url = self.baseurl
        html = urlopen(url)

        bsObj = BeautifulSoup(html, "lxml")
        # li = bsObj.find_all("li")
        # print(li)

        urls = bsObj.find_all("a", href=re.compile(r'^http://(www)+(.)+(deyi)+(.)+(/)+(thread)+(.*?)+(.html)'))
        #print(urls)

        url_list = []
        for item in urls:
            url_list.append(item['href'])
            # print("[*] 找到网址:", item['href'])
            # print("[*] 帖子标题：", item.text)
        # print(url_list)
        # 去除列表种重复的元素
        ls2 = list(set(url_list))

        # 获取URL的数量
        # print(len(ls2))
        # print(ls2)

        # 查找指定元素并删除
        index1 = 'http://www.deyi.com/thread-24488-1-1.html'  # 免责声明
        index2 = 'http://www.deyi.com/thread-2555-1-2.html'  # 版权声明
        index3 = 'http://www.deyi.com/thread--1-1.html'

        url_list_page = []
        for url_item in ls2:
            # print(url_item)
            if url_item not in (index1, index2,index3):
                url_list_page.append(url_item)
                self.pages.add(url_item)
                # print("[*] 找到网址的页面ID: ", url_item)
                # print(url_lists)

        # 获取page的ID
        url_lists = []
        for url_ii in url_list_page:
            #print(url_ii)
            newlist = re.search('(?<=thread-)\d+', url_ii).group()
            url_lists.append(newlist)
            #print(newlist)
        self.page = url_lists

    #获取论坛网站的翻页数量
    def get_url(self):
        self.get_home()
        page = self.page
        #print(page)

        for index in range(len(page)):

            try:
                #print("网站的页面ID: ", ll)
                #print("page页面ID：", page[index])

                response = urlopen('http://www.deyi.com/thread-' + str(page[index]) + '-1-1.html')

                bsObj = BeautifulSoup(response, "lxml")
                maxlength = bsObj.find("div", {"class": "pg"})
                #查找标题的元素
                title_find = bsObj.find("a",{"id":"thread_subject"})

                max_href = maxlength.find_all("a")
                #print(max_href)

                max_a_pattern = re.compile(r'http://www.deyi.com/thread-.*?-(\d+)-1.html')
                max_b = max_a_pattern.findall(str(max_href))
                # str转为int
                max_b = list(map(int, max_b))
                max_c = max(max_b)
                # 找最大的数值
                # print(max_c)
                # print('——————————————————————')
                # 默认页数为1
                page_number = 1
                # 用正则获取最大页数信息
                # 遍历每一页,获取页面的数量
                page_str = str(page[index])
                # 主题URL
                bbs_theme_url = 'http://www.deyi.com/thread-' + str(page[index]) + '-1-1.html'
                print("[*] 主题URL：", bbs_theme_url)
                # 主题标题
                title = title_find.text
                print("[*] 帖子标题：", title)
                # 主题查看数和主题回复数 reply_number
                # 查找hm的元素
                hm = bsObj.find("div", {"class": "hm"})
                # print(hm)
                hm = list(map(str.strip, hm.find_all(text=re.compile(r'\b\d+\b'))))
                # 主题查看数
                print("[*] 主题查看数：", hm[0])
                view_number = hm[0]
                # 主题回复数
                print("[*] 主题回复数：", hm[1])
                reply_number = hm[1]
                public_date = bsObj.find("em", {"id": re.compile('authorposton.*')})
                date = public_date.text.strip()
                public_date = re.compile(r'发表于')
                public_date = public_date.sub('', date)
                public_date = public_date.strip()

                print("[*] 主题时间：", public_date)

                # 主题ID
                titleId = page[index]

                # 保存主题列表
                cur.execute("INSERT INTO bbs_theme(titleId, url, title, reply_number, view_number, public_date) VALUES (%s, %s, %s, %s, %s, %s)", (titleId, bbs_theme_url, title, reply_number, view_number, public_date))
                # 返回执行execute()方法后影响的行数
                cur.rowcount
                conn.commit()

                while page_number <= max_c:

                    links = []
                    link = 'http://www.deyi.com/thread-' + page_str + '-' + str(page_number) + '-1.html'
                    # print(link)
                    links.append(link)
                    page_number = page_number + 1

                    # print("[*] 爬取第{}页：".format(page_number-1),links)
                    print("[*] URL: {}".format(link))
                    bbs_post_url = link
                    # print(bbs_post_url)

                    print("[*] 爬取页面ID：{} ".format(page[index]))

                    html = urlopen(link)
                    soup = BeautifulSoup(html, 'lxml')

                    print("[*] 爬取翻页：第{}页".format(page_number-1))
                    # 寻找'table'标签

                    links = soup.find_all("table", {"id": re.compile("pid.*")})
                    # 'table'标签的数量
                    # print("[*] 帖子标签：", len(links))
                    # print("[*] 标题：{}".soup.title)

                    for link in links:
                        res_data = {}
                        # 获取帖子的用户
                        soup = link.find("div", {"class": "authi"})
                        # 提取用户uid的url
                        uid_find  = soup.find("a", href=True)['href']
                        # pattern = '(\d+){2}'
                        # match = re.search(pattern, urlss)
                        # print(match.group())

                        lst = soup.text.strip()
                        # print("[*] 爬取第{}页：".format(page_number))
                        # return lst
                        print("[*] 帖子作者：", lst)
                        print("[*] 用户URL：", uid_find)
                        authorUrl = uid_find
                        pattern = '(\d+){2}'

                        match = re.search(pattern, uid_find)

                        print("[*] 用户UID：", match.group())
                        authorId = match.group()
                        # uid = uid_find.get('href')
                        # print("[*] 用户ID：", uid)

                        # 获取帖子内容
                        # 寻找'td'标签
                        try:
                            soup_post = link.find("td", {"class": "t_f"}).text.strip()
                            #print(soup_post)
                            # 正则表达式
                            dr = re.compile(
                                    r'\r|\n|\d{4}[-/]\d{2}[-/]\d{1,2}|\d{1,2}[:/]\d{1,2}|上传|下载附件|\d+\.*\d+|\(.*?\)|广 告.pcb{.*}|\n|',
                                    re.S)
                            # 正则的替换
                            dd = dr.sub('', soup_post)
                            # 移除空格
                            dd_s = dd.strip()
                            # return dd_s
                            print("[*] 帖子内容：",dd_s)

                            soup_date = link.find("em", {"id": re.compile('authorposton.*')})
                            date = soup_date.text.strip()
                            dr_date = re.compile(r'发表于')
                            dd_date = dr_date.sub('', date)
                            dd_date_s = dd_date.strip()
                            # return dd_date_s
                            # print(dd_date_s)
                            res_data['date'] = dd_date_s

                            print("[*] 发布时间：",dd_date_s)

                            print("[*] 爬取页面ID: {}".format(page[index]))

                            titleId = page[index]

                            # 保存到mysql数据库
                            # 执行SQL语句到数据库执行
                            cur.execute("INSERT INTO bbs_post(authorId, titleId, url, authorUrl, author, content, dates) VALUES (%s, %s ,%s, %s, %s, %s, %s)",(authorId, titleId, bbs_post_url, authorUrl, lst, dd_s, dd_date_s))
                            # 返回执行execute()方法后影响的行数
                            cur.rowcount
                            # 提交之后，再关闭cursor和连接
                            conn.commit()

                        except AttributeError:
                            pass

            except AttributeError:
                pass

baseTieba = Tieba()
baseTieba.get_url()


"""
利用BeautifulSoup，解析所有下载好的基准数据
"""
import os
import re
import json
from bs4 import BeautifulSoup
from bs4.element import Tag

date_list = []
date_set = set()
stock_sid_dic = {}
re_date = re.compile(r".*(201\d-\d\d-\d\d).*")
re_stock = re.compile(r".*\[(.*)\].*")

with open(r"C:\Users\Administrator\Desktop\dlstock_data\stockTypes.txt","r",encoding="utf-8")as f:
    for line in f:
        str_list = line.strip().split(",")
        stock_sid_dic[str_list[0]] = str_list[1]

f_write = open("2016-2018.csv", "w", encoding="utf-8")


def parse_html(filename):
    flag = True
    with open(r"C:\Users\Administrator\Desktop\fundamental\%s" % filename, "r", encoding="utf-8")as f_read:
        json_data = f_read.read()
        msg_list = json.loads(json_data)
        print(len(msg_list))
        i = 0
        for msg in msg_list:
            data = msg["data"]
            text_html = data.get("text/html", None)
            if text_html:
                soup = BeautifulSoup(text_html, "lxml")
                tbody = soup.find("tbody")
                contents = tbody.contents

                for content in contents:  # 循环的是那50条数据
                    if isinstance(content, Tag):
                        th_list = content.find_all("th")
                        td_list = content.find_all("td")
                        if len(th_list) == 2:
                            t_date = th_list[0].get_text().split()[0]
                            if t_date in date_set:
                                print("%s的数据重复" % t_date)
                                flag = False
                            if t_date not in date_list:
                                date_list.append(t_date)
                        if flag:
                            th_text = th_list[-1].get_text()
                            try:
                                g_stock = re_stock.search(th_text)
                                stock = g_stock.group(1)
                            except:
                                stock = "..."
                                print("股票名字有问题%s" % th_text)
                            sid = stock_sid_dic.get(stock, None)
                            td_texts = ""

                            for td in td_list:
                                td_text = td.get_text()
                                td_texts = td_texts + td_text + ","

                            td_texts = td_texts.rstrip(",")
                            if sid:
                                s_line = "".join([sid, ",", stock, ",", date_list[-1], ",", td_texts, "\n"])
                                f_write.write(s_line)
                            else:
                                print("我们没有%s这只股票"%stock)
            print(i)
            i += 1
        for item in date_list:
            date_set.add(item)
        print(date_list)


file_name_list = os.listdir(r"C:\Users\Administrator\Desktop\fundamental")
# file_name_list = os.listdir(r"C:\Users\Administrator\Desktop\xx")  # 测试用
for file_name in file_name_list:
    parse_html(file_name)
f_write.close()
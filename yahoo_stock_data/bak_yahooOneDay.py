# 每天爬取昨天的数据
# 现存问题：股票列表没有实时更新,改名数据和不改名数据都回去拿
import requests
from bs4 import BeautifulSoup
import datetime
import logging
import logging.config
import traceback
import random
import time
import os

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("downloadLog")

def loop_request(stock,timeout,log_ger):
    i = 0
    while 1:
        try:
            response = requests.get("https://finance.yahoo.com/quote/%s/history?guccounter=1"%(stock),timeout=timeout)
        except Exception:
            log_ger.error(traceback.format_exc())
            i += 1
            if i == 10:
                log_ger.info("%s download Fail!" % stock)
                break
            time.sleep(3)
        else:
            return response.text


def get_yahoo_stock_data(sid, stock, f_write, log_ger, yesterday, end_day):
    flag = False
    res = loop_request(stock, 5, log_ger)
    soup = BeautifulSoup(res,"html.parser")
    trs = soup.find_all("tr",attrs={"class": "BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)"})
    if trs:
        try:
            for tr in trs:
                tds = tr.children
                tr_text = ""
                for td in tds:
                    td_text = td.get_text()
                    if "," in td_text:
                        try:
                            td_text = datetime.datetime.strptime(td_text, "%b %d, %Y").date()
                            if td_text > end_day:
                                break
                            if td_text < yesterday:
                                log_ger.info("[%s,%s]download ok" % (sid, stock))
                                return
                            # if td_text == yesterday:
                            #     flag = True
                            td_text = str(td_text)
                        except:
                            td_text = td_text.replace(',', '')
                    tr_text += ''.join([td_text, ","])
                tr_text = tr_text.rstrip(",")
                f_write.write(''.join([sid, ",", stock, ",", tr_text, "\n"]))
                # if flag:
                #     log_ger.info("[%s,%s]download ok" % (sid, stock))
                #     return
        except:
            log_ger.error("[%s,%s] error" % (sid, stock))
            log_ger.error(traceback.format_exc())

# yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
yesterday = datetime.date(2018, 3, 28)
end_day = datetime.date(2018, 7, 9)
one_week_ago = yesterday - datetime.timedelta(days=6)
remove_file_name = "xx%s.csv" % one_week_ago
try:
    os.remove(remove_file_name)
    os.remove("download.log")
except Exception as e:
    logger.error(traceback.format_exc())
else:
    logger.info("%s 删除成功!")
f_write = open("%s.csv" % str(yesterday), "w", encoding="utf-8")
# with open("stockTypes.txt","r",encoding="utf-8")as f:
with open("stocktest","r",encoding="utf-8")as f:
    for line in f:
        stock, sid = line.strip().split(",")
        get_yahoo_stock_data(sid, stock, f_write, logger, yesterday, end_day)
        random_second = random.uniform(3.0, 6.0)
        time.sleep(random_second)
ss = ['ARGO', 'BHR', 'BKNG', 'CBRE', 'CLNY', 'CUR', 'SESN', 'EGC', 'SLS', 'HWC', 'EHC', 'JEF', 'STCN', 'NRC', 'CDMO', 'XAN', 'EQNR', 'EQNR', 'OXSQ', 'OSPN', 'WP', 'WELL', 'WYND']

f_write.close()
# [1] 25338
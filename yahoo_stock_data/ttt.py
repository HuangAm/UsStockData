import hashlib
import datetime

yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).date()

def get_file_md5(filename):
    myhash = hashlib.md5()
    with open(filename,"rb") as f:
        b = f.read()
        myhash.update(b)
    return myhash.hexdigest()

with open("/data/product/data_center/stock_file/over_%s" % str(yesterday),"w",encoding="utf-8")as f:
    file_md5 = get_file_md5("/data/product/data_center/stock_file/%s.csv" % str(yesterday))
    f.write(file_md5)

## UsStockData
雅虎财经美股历史数据，Quantopian的基准数据
### fundamental_data_v1
**功能**
- 爬取Quantopian的基准数据  

**使用方法**
- 打开Quantopian的研究模块的notebook页面，新建一个文件，把cell代码沾到新建文件的cell中(先不要运行)
- 启动tornado服务
- 在浏览器输入https://localhost:8889/data进行访问(好像是解决浏览器同源,反正没这一步没报错)
- 在浏览器终端运行js中的两个函数代码(如果没有Ipython对象，进入iframe指定的地址即可)

### fundamental_data_v2
**功能**
- 爬取Quantopian的基准数据  

**使用方法**
- 打开Quantopian的研究模块的notebook页面，将qunatopian_fund_study.ipynb上传，上传成功后打开该文件
- 把js代码贴到浏览器终端运行(如果没有Ipython对象，进入iframe指定的地址即可)
- 在浏览器中端运行`help()`按指示进行操作

### yahoo_stock_data
**功能**
- 爬取Yahoo的历史数据(每天的)

**使用方法**
- 运行脚本


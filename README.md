# 爬虫
爬去[得意生活](http://www.deyi.com/)用户、内容和发布时间存储到MySQL数据库中

该项目仅供研究学习一下

# 运行环境
python 3.6.4

### 运行依赖包
* BeautifulSoup
* mysql-connector

安装命令：
**1.安装BeautifulSoup4**

```
$ pip3 install BeautifulSoup4
```

**2.安装mysql**

```
$ pip3 install mysql-connector
```

**3.安装lxml**

```
$ pip3 install lxml
```

进入工程目录

```
$ cd python_bbs
```

修改mysql数据库配置[main.py]第17行中用户名和密码

```
conn = mysql.connector.connect(user='root', password='root', database='bbs')
```

把data.sql导入到mysql数据库

```
use bbs;
source data.sql;
```

运行启动脚本tieba.py立即开始抓取数据并存储到mysql中
```
python3 main.py
```
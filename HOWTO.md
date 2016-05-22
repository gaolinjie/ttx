HOWTO deploy on Linode
======================

###Build Ubuntu 12.10 on Linode and access the server
	$ ssh root@106.187.37.xxx
	# ssh to server
	# if encounter 'Host key verification failed', just delete ~/.ssh/known_hosts file

###Install Mysql
	$ apt-get update
	$ apt-get install mysql-server mysql-client

###Installing tools and dependencies
	$ apt-get install python-setuptools
	$ easy_install pip
	$ apt-get install git
	$ apt-get install nginx
	$ pip install supervisor

###Config Git
	$ ssh-keygen -t rsa -C "ttx@gmail.com"
	$ cat ~/.ssh/id_rsa.pub
	# copy and paste the RSA key to the Deploy keys setting
	$ git config --global user.name "ttx"  
	$ git config --global user.email ttx@gmail.com  

###Make directories for your app
	$ mkdir ~/www

###Pull in source code
	$ cd ~/www/
	$ git clone git@github.com:gaolinjie/ttx.git
	$ cd ttx

###Install web app required modules
	$ pip install -r requirements.txt

###Install python mysql
	$ easy_install -U distribute
	$ apt-get install libmysqld-dev libmysqlclient-dev
    $ apt-get install python-dev
	$ pip install mysql-python
	$ apt-get install python-MySQLdb

###Install PIL
	$ apt-get build-dep python-imaging
	$ apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev
	$ ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
	$ ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib
	$ ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib
	$ pip install http://effbot.org/downloads/Imaging-1.1.7.tar.gz
	# pip install -U PIL

###Install requests
	$ pip install requests

###Create database and then execute sql file in dbstructure/
	$ mysql -u root -p
	mysql> CREATE DATABASE ttx;
	mysql> GRANT ALL PRIVILEGES ON ttx.* TO 'ttx'@'localhost' IDENTIFIED BY 'ttx';
	mysql> exit
	$ mysql -u ttx -p --database=ttx < dbstructure/ttx.sql
	$ mysql -u ttx -p --database=ttx < dbstructure/data.sql

###Install Torndb
    $ pip install torndb

###Install Qiniu sdk
    $ pip install qiniu

###Install ghost.py on mac osx
	# Install qt and pyside follow http://qt-project.org/wiki/PySide_Binaries_MacOSX
	# pip install --pre Ghost.py

###Install pyquery
    apt-get install libxml2-dev libxslt-dev
    apt-get install python-dev python-setuptools
    # 如果内存为512mb，安装pyquery会内存不够，解决方法为下：
    # http://stackoverflow.com/questions/18334366/out-of-memory-issue-in-installing-packages-on-ubuntu-server
    $ dd if=/dev/zero of=/swapfile bs=1024 count=1024k
    $ mkswap /swapfile
    $ swapon /swapfile
    pip install pyquery
    $ swapoff -v /swapfile
    $ rm /swapfile

###Create symbolic links to conf files
	$ cd /etc/nginx
	$ rm nginx.conf
	$ ln -s ~/www/ttx/conf/nginx.conf nginx.conf
	$ cd
	$ ln -s ~/www/ttx/conf/supervisord.conf supervisord.conf  

###Create nginx user
	$ adduser --system --no-create-home --disabled-login --disabled-password --group nginx

###Create a logs directory:
	$ mkdir ~/logs

###Start Supervisor and Nginx
	$ supervisord
	$ /etc/init.d/nginx start

###Visit your public IP address and enjoy!

###Update your web app
	$ cd ~/www/ttx
	$ git pull

###Timed run scrapy use crontab
####1. 编写 cron.sh
	#! /bin/sh                     
	export PATH=$PATH:/usr/local/bin
	cd ~/www/ttx/ttxspider
	nohup scrapy crawl ttxspider >> ttxspider.log 2>&1 &
####2. 编辑 crontab 文件
	$ crontab -e
	# 插入命令 * */3 * * *  sh ~/www/ttx/ttxspider/cron.sh
####3. 开启 crontab log
	$ vi /etc/rsyslog.d/50-default.conf 
	$ service rsyslog  restart
	$ tail -f /var/log/cron.log
	# 查看 crontab 运行 log
####4. 启动、停止和重启 crontab 命令
	$ /etc/init.d/cron start
	$ /etc/init.d/cron stop
	$ /etc/init.d/cron restart
####5. 列出、删除 crontab 文件
	$ crontab -l
	# 列出 crontab 文件
	$ crontab -r
	# 删除 crontab 文件

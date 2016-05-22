#! /bin/sh                                                                                                                                            

export PATH=$PATH:/usr/local/bin

cd ~/www/ttx/ttxspider

nohup scrapy crawl ttxspider >> ttxspider.log 2>&1 &
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-19 15:39:03 元宵节
# @Author  : maixiaojie (tracywyj@gmail.com)
# @Link    : https://maixiaojie.github.io
# @Version : 1.0.0
# 
############文件下载器 python2.7########################
# 
# 本项目仅在python2.7下实验，下载8000+个视频，其他版本请灵活改动即可
# 本项目不维护其他版本python
# 
# 需要安装requests、progressbar、MySQLdb三个库
# 
# `pip install requests`
# `pip install progressbar`
# MySQLdb -- 如果不需要读取数据库，则不需要该库

import requests
import urllib
import os
import time
import progressbar
import MySQLdb

# 根据url获取文件名，需求不同，下面的表达式也不同，这块灵活改动
def getName(path):
	return path.split('/')[-1]

#下载文件
def download(url, dirpath):	
	# 配置你的文件请求相关的headers即可，这块灵活改动
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
		"Referer": "http://www.maiziedu.com/"
	}
	filename = getName(url)
	path = dirpath + '/' + filename
	r = requests.get(url, headers=headers, stream=True)
	chunk_size = 1024
	content_size = int(r.headers['content-length'])
	if r.status_code == 200:		
		print '[File Total Size]: %0.2f Mb' % (content_size /chunk_size / 1024)
		print '[File Name]: ' + filename
		with open(path, "wb") as file:
			widgets = ['Progress: ', progressbar.Percentage(), ' ',progressbar.Bar(marker='#', left='[', right=']'),' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
			pbar = progressbar.ProgressBar(widgets=widgets, maxval=content_size).start()
			for data in r.iter_content(chunk_size=chunk_size):
				if data:
					file.write(data)
					file.flush()
				pbar.update(len(data) + chunk_size)
			pbar.finish()

def main():
	# 下载的所有文件都放在该文件夹下，名称可自由修改，合法即可
	# 会先判断是否存在该文件夹，若不存在会创建文件夹
	path = "./video" 
	isExists = os.path.exists(path)
	if not isExists:
		os.makedirs(path)

	# 我这里的文件地址是从数据库中读取的
	# 你也可以灵活地改成从文件读取等其他方式
	db = MySQLdb.connect('ip:port', 'user', 'password', 'database',  charset='utf8')
	cursor = db.cursor()
	cursor.execute("SELECT video_url from lesson_detail limit 100 offset 0 ")
	rs = cursor.fetchall()
	cursor.close()
	db.close()

	# 遍历url集合，如果对应的文件本地已经存在，则跳过该文件下载
	for i, url in enumerate(rs):
		fileurl = ''.join(url)
		filename = getName(fileurl)
		filepath = path+'/'+filename
		isFileExists = os.path.exists(filepath)
		if isFileExists:
			print '[msg]: ' + filename + ' has been downloaded...'			
		else:
			print 'downloading ['+ str(i) +' ]' + fileurl
			download(fileurl, path)
			
	
main()
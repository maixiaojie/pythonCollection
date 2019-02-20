#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-16 15:43:36
# @Author  : maixiaojie (tracywyj@gmail.com)
# @Link    : https://yk.mcust.cn
# @Version : $Id$
import requests
import json
import codecs

#  ****************************************************
#  *python环境，目前2.7版本没问题，3版本暂未测试
#  *依赖库： requests  `pip install requests`	
#  *最后会生成一个json文件
#  ****************************************************
#   
# 极客时间官网，登录后--f12--Netword--任意点开该域名下的一个请求--Headers--Request Headers--Cookies
# 复制所有的cookies 
# https://time.geekbang.org/ 
cookies = "改成你的cookies"
# 专栏的id，修改成你要获取的专栏的id即可
# 如https://time.geekbang.org/column/154， 该专栏的id为154
id = '48'

class Tools(object):
	def __init__(self, cookies, columnid):
		super(Tools, self).__init__()
		self.cookies = cookies
		self.columnid = columnid
		self.headers = {
			'Cookie': self.cookies,
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 DID:3441301122:DID',
			'Referer': 'https://time.geekbang.org', 
			'Origin': 'https://time.geekbang.org',
			'Host': 'time.geekbang.org',
			'Content-Type': 'application/json'
		}
	def getall(self):
		headers = self.headers
		url = 'https://time.geekbang.org/serv/v1/my/products/all'
		r = response = requests.post(url, headers=headers)
		# print r.text
	# 获取专栏的文章列表
	def get_article_list(self):
		headers = self.headers
		url = 'https://time.geekbang.org/serv/v1/column/articles'
		payload = {'cid': self.columnid, 'order': 'earliest', 'prev': 0, 'sample': 'true', 'size': 200}
		r = response = requests.post(url, data=json.dumps(payload), headers=headers)
		res = r.json()
		code = res.get('code')
		if code >= 0:
			lists = res.get('data').get('list')
			ids_list = []
			for item in lists:
				ids_list.append(item.get('id'))
			return ids_list
		else:
			return []
	# 获取单个文章的数据
	def get_article_detail(self, article_id):
		headers = self.headers
		url = 'https://time.geekbang.org/serv/v1/article'
		payload = {'id': article_id, 'include_neighbors': 'false'}
		r = response = requests.post(url, data=json.dumps(payload), headers=headers)
		res = r.json()
		code = res.get('code')
		if code >= 0:
			# print 'id为'+ str(article_id)+'的文章数据获取成功'
			lists = res.get('data')
			article_dict = {}
			article_dict['id'] = res.get('data').get('id')
			article_dict['pid'] = res.get('data').get('cid')
			article_dict['article_title'] = res.get('data').get('article_title')
			article_dict['article_cover'] = res.get('data').get('article_cover')
			article_dict['audio_download_url'] = res.get('data').get('audio_download_url')
			article_dict['audio_url'] = res.get('data').get('audio_url')
			article_dict['audio_size'] = res.get('data').get('audio_size')
			article_dict['audio_time'] = res.get('data').get('audio_time')
			article_dict['mdhtml'] = res.get('data').get('article_content')			
			article_dict['ctime'] = res.get('data').get('article_ctime')
			with codecs.open('articles'+str(self.columnid)+".json", "a+", "utf-8") as fp:
				fp.write(json.dumps(article_dict,indent=4, ensure_ascii=False)+',\r\n')
		else:
			pass
			# print '获取失败'
	def main(self):
		ids = self.get_article_list()
		if len(ids) > 0:
			for id in ids:
				self.get_article_detail(id)


tool = Tools(cookies, id)
tool.main()
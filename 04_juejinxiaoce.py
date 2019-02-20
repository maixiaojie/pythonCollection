#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-16 15:43:36
# @Author  : maixiaojie (tracywyj@gmail.com)
# @Link    : https://yk.mcust.cn
# @Version : $Id$
import requests
import json
import codecs

cookies = ""
bookid = ""
token = ""
uid = ""
client_id = ""

class Tools(object):
	def __init__(self, cookies, bookid, token, uid, client_id):
		super(Tools, self).__init__()
		self.cookies = cookies
		self.token = token
		self.bookid = bookid
		self.uid = uid
		self.client_id = client_id
		self.headers = {
			'Cookie': self.cookies,
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 DID:3441301122:DID',
			'Referer': 'https://juejin.im', 
			'Origin': 'https://juejin.im',
			'Host': 'xiaoce-cache-api-ms.juejin.im',
			'Content-Type': 'application/json'
		}
	def getall(self):
		headers = self.headers
		url = "https://xiaoce-cache-api-ms.juejin.im/v1/get"
		payload = {'uid': '', 'client_id': '1548407371349', 'token': self.token, 'src': 'web', 'id': self.bookid}
		r = requests.get(url, params=payload, headers=headers)
		res = r.json()
		code = res.get('m')
		if(code == 'ok'):
			section = res.get('d').get('section')
			return section
		else:
			return []

	# 获取
	def get_article_detail(self, sectionid):
		headers = self.headers
		url = 'https://xiaoce-cache-api-ms.juejin.im/v1/getSection'
		payload = {'uid': self.uid, 'client_id': self.client_id, 'token': self.token, 'src': 'web', 'sectionId': sectionid}
		r = response = requests.get(url, params=payload, headers=headers)
		res = r.json()
		print res
		print r.url
		code = res.get('m')
		if(code == 'ok'):
			data = res.get('d')
			section_dict = {}
			section_dict['id'] = data.get('id')
			section_dict['pid'] = data.get('metaId')
			section_dict['article_title'] = data.get('title')
			section_dict['mdhtml'] = data.get('html')
			section_dict['mdtext'] = data.get('content')
			section_dict['createdAt'] = data.get('createdAt')
			with codecs.open('book-'+str(self.bookid)+".json", "a+", "utf-8") as fp:
				fp.write(json.dumps(section_dict,indent=4, ensure_ascii=False)+',\r\n')

	def main(self):
		ids = self.getall()
		if len(ids) > 0:
			for id in ids:
				self.get_article_detail(id)

tool = Tools(cookies, bookid, token, uid, client_id)
tool.main()
# tool.get_article_detail('5bdd0d83f265da615f76ba57')


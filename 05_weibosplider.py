#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-01 09:43:36
# @Author  : maixiaojie (tracywyj@gmail.com)
# @Link    : https://maixiaojie.github.io
# @Version : $Id$

import os
import requests
import json
import re
import math
import MySQLdb
import time
import datetime
import codecs
import logging

mylogger = logging.getLogger('mylogger')
mylogger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s- %(levelname)s - %(message)s')
fh = logging.FileHandler('logout.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

mylogger.addHandler(fh)

dbWB = MySQLdb.connect('ip:port', 'user', 'password', 'database',  charset='utf8')
cursorWB = dbWB.cursor()
cursorWB.execute('SET NAMES utf8mb4')
class Tool:
	removeImg = re.compile('<img.*?>')
	removeAddr = re.compile('<a.*?></a>')
	replaceLine = re.compile('<tr>|<div>|</div>|</p>')
	removeTag = re.compile('<.*?>')
	url_regex = re.compile('http://.*?/\w{7}') # http://t.cn/RdhOUUu
	s_regex = re.compile('u\w{3,4}') # u200b/u3000
	face_regex = re.compile('\[\w+\]') # 表情：[开心]
	#self是实例方法 cls是类方法
	@classmethod
	def replace(cls,x):
		x=re.sub(cls.removeImg,'',x)
		x=re.sub(cls.removeAddr,'',x)
		x=re.sub(cls.replaceLine,'',x)
		x=re.sub(cls.removeTag,'',x)
		x=re.sub(cls.url_regex,'',x)
		# x=re.sub(cls.s_regex,'',x)
		return x.strip() #去掉多余的空格
		# return x

class Weibo(object):
	def get_total(self,id,page):
		url = 'https://m.weibo.cn/api/container/getIndex?uid={}&type=uid&value={}&containerid=107603{}&page={}'.format(id,id,id,page)
		response = requests.get(url)
		print url
		ob_json = json.loads(response.text)
		# print ob_json
		status = ob_json.get('ok')
		# print status
		mylogger.info(status)
		if status == 1:
			totalData = ob_json.get('data').get('cardlistInfo').get('total')
			total_page = int(math.ceil(totalData / 10)) + 1
			mylogger.info('一共' + str(total_page) + '页微博...')
			mylogger.info('一共' + str(totalData) + '条微博...')
			sql = 'insert into wb_splider(`uid`, `splider_status`, `ctime`) values(%s, %s, %s)'
			dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			cursorWB.execute(sql, [id, '112', dt])
			dbWB.commit()
			# print '一共' + str(total_page) + '页微博...'
			# print '一共' + str(totalData) + '条微博...'
			return total_page
		else:
			mylogger.info(id + '的数据为空')
			# print '数据为空'
			# sql = 'insert into wb_splider(`uid`, `splider_status`) values(%s, %s)'
			# cursorWB.execute(sql, [id, '3'])
			return 0

	def get_weibo(self,id,page):
		url = 'https://m.weibo.cn/api/container/getIndex?uid={}&type=uid&value={}&containerid=107603{}&page={}'.format(id,id,id,page)
		response = requests.get(url)
		print url
		print '正在爬取...' + str(response.url)
		ob_json = json.loads(response.text)
		list_cards = ob_json.get('data').get('cards')
		mylogger.info('第' + str(page) + '页数据获取成功...')
		# print '第' + str(page) + '页数据获取成功...'
		return list_cards

	def write2file(self, data, filename):
		with codecs.open(filename, 'a+', 'utf-8') as f:
			f.write(data + '\r\n')

	def handle_cardlist(self, list_cards, uid):
		if list_cards != None:
			for card in list_cards:
				if card.get('card_type') == 9:
					wb_id = card.get('mblog').get('id')
					id = card.get('mblog').get('bid')
					source = card.get('mblog').get('source')
					reposts_count = card.get('mblog').get('reposts_count')
					comments_count = card.get('mblog').get('comments_count')
					attitudes_count = card.get('mblog').get('attitudes_count')
					text=card.get('mblog').get('text')
					pre_text = Tool.replace(text)
					retweeted_status = card.get('mblog').get('retweeted_status')
					created_at = card.get('mblog').get('created_at')
					# print pre_text
					if retweeted_status:
						is_retweeted = 1
					else:
						is_retweeted = 0
					sql = "insert into wb(`id`, `uid`, `wb_id`, `text`, `source`,`reposts_count`,`comments_count`,`attitudes_count`,`is_retweeted`,`created_at`, `origin_text`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
					try:
						self.write2file(pre_text, './userdata/'+uid+'.txt')
						row_count = cursorWB.execute(sql, [id, uid, wb_id, pre_text, source, reposts_count, comments_count, attitudes_count, is_retweeted, created_at, text])
					except BaseException as t:
						print t
						print wb_id
						mylogger.error(t)
					finally:
						
						pass

	def main(self,uid):
		total_sum = self.get_total(uid, 1)
		if total_sum > 10:
			total_sum = 10
		for i in range(total_sum):
			list_cards = self.get_weibo(uid,i+1)
			self.handle_cardlist(list_cards, uid)
		
		sql = 'insert into wb_splider(`uid`, `splider_status`, `ctime`) values(%s, %s, %s)'
		dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		if total_sum == 0:			
			cursorWB.execute(sql, [uid, '3', dt])
			mylogger.info(uid + ' total_sum = 0')
		else:
			cursorWB.execute(sql, [uid, '2', dt])
			mylogger.info(uid + ' total_sum != 0')
		dbWB.commit()
		# cursorWB.close()
		# dbWB.close()

if __name__ == '__main__':
	weibo=Weibo()
	# 6072592521  2401890571 1992968110 5195667944
	weibo.main('5195667944')
	
	# uid = sys.argv[1]
	# if uid != '':
	# 	weibo.main(uid)
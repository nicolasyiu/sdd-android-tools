#!/usr/bin/python
 # -*- coding: UTF-8 -*-
import os
import sys
import base64
import httplib
import urllib
import json
import time
import re

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
	reload(sys)
	sys.setdefaultencoding(default_encoding)

#新的抓取地址：http://a.app.qq.com/o/ajax/micro/AppDetail?pkgname=com.blsm.sft.fresh（直接返回json数据）
#应用宝抓取数据的url
myapp_api_url = {'host' : 'android.myapp.com' , 'app_detail' : '/myapp/detail.htm' }

#打印对象
def prn_obj(obj):
    print '\n '.join(['%s:%s' % item for item in obj.__dict__.items()])

class MyAppDetail(object):
	appPackage = None
	apkCode = 0
	apkVName = None
	appId = 0
	appName = None
	appCate = None
	iconUrl = None
	downUrl = None

	#构造方法
	def __init__(self,package_name=''):
		if package_name:
			self.app_detail(package_name)

	"""
	获取应用的详情
	"""
	def app_detail(self,package_name):
		url = myapp_api_url['app_detail']+"?"+urllib.urlencode({'apkName': package_name})
		headers = {}

		conn = httplib.HTTPConnection(myapp_api_url['host'])
		conn.request("GET", url)

		res = conn.getresponse()
		# print "\app_detail\t","GET\t",myapp_api_url['host']+url,"\n",res.status, res.reason

		#如果数据返回出错，那么return 空
		if res.status != 200:
			print "None"
			conn.close()
			return None

		data = res.read()

		conn.close()

		self.analysis_data(data)

	"""
	解析返回的数据
	"""
	def analysis_data(self,data):
		try:
			match = re.search(r"appDetailData = (.*?(\n.*){11})",data)
			if match:
				match_data = match.groups()[0]
				match_data = match_data.replace("orgame","\"orgame\"").replace("apkName","\"apkName\"").replace("apkCode","\"apkCode\"").replace("appId","\"appId\"").replace("appName","\"appName\"").replace("iconUrl","\"iconUrl\"").replace("appScore","\"appScore\"").replace("downTimes","\"downTimes\"").replace("downUrl","\"downUrl\"").replace("tipsUpDown","\"tipsUpDown\"")
				json_data = json.loads(match_data)
				self.appPackage = json_data['apkName']
				self.apkCode = json_data['apkCode']
				self.appId = json_data['appId']
				self.appName = json_data['appName']
				self.iconUrl = json_data['iconUrl']
				self.downUrl = json_data['downUrl']

			match_vname = re.search(r"<div class=\"det-othinfo-data\">V(.[^<>]*)</div>",data)
			if match_vname:
				self.apkVName = match_vname.groups()[0]

			match_cate = re.search(r"id=\"J_DetCate\">(.[^<>]*)</a>",data)
			if match_cate:
				self.appCate = match_cate.groups()[0]
		except Exception, e:
			print "analysis_data Exception",e

if len(sys.argv)>1:
	if len(sys.argv)>2 and sys.argv[1]=='download':
		app_detail = MyAppDetail(sys.argv[2])
		print app_detail.downUrl
	else:
		app_detail = MyAppDetail(sys.argv[1])
		prn_obj(app_detail)

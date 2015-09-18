#!/usr/bin/env python
 # -*- coding: UTF-8 -*- 
import os
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
	reload(sys)
	sys.setdefaultencoding(default_encoding)

#打印对象
def prn_obj(obj):
    print ', '.join(['%s:%s' % item for item in obj.__dict__.items()])

#解析存在兼职对的字符串
def analyze_key_value(xml_str):
	key_dict = {}
	pacakge_array = xml_str.split(' ')
	for pacakge_item in pacakge_array:
		item_array = pacakge_item.split('=')
		if len(item_array)!=2 :
			continue
		key_dict[item_array[0]] = item_array[1].replace('\'','').replace('\n','')
	return key_dict

#apk的信息
class ApkInfo(object):
	package_name = None
	versionCode = 0
	versionName = None

	app_name = None
	icon = None

	#构造方法
	def __init__(self,apk_path=None):
		if apk_path :
			infosList = os.popen("aapt d badging "+apk_path).readlines()
			self.loadInfo(infosList)

	#获取应用基本信息
	def loadInfo(self,infolist):
		global package_name
		for info in infolist:
			key_dict = analyze_key_value(info)
			if 'package' in info and 'versionCode=' in info:
				self.package_name = key_dict['name']
				self.versionCode = key_dict['versionCode']
				self.versionName = key_dict['versionName']
				continue

			if 'application' in info and 'label=' in info and 'icon=' in info :
				self.app_name = key_dict['label']
				self.icon = key_dict['icon']

			
#程序主逻辑开始
if len(sys.argv)>1 and '.apk' in  sys.argv[1]:
	#apk路径
	apk_path = sys.argv[1]

	#创建一个apkInfo对象
	apk_info = ApkInfo(apk_path)
	prn_obj(apk_info)















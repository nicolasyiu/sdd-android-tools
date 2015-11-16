#!/usr/bin/env python
 # -*- coding: UTF-8 -*-
import os
import sys
from apkinfo import ApkInfo
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
	reload(sys)
	sys.setdefaultencoding(default_encoding)

#打印对象
def prn_obj(obj):
    print ', '.join(['%s:%s' % item for item in obj.__dict__.items()])

#换行打印对象
def prn_obj2(obj):
    print '\n'.join(['%s\t%s' % item for item in obj.__dict__.items()])

#程序主逻辑开始
if len(sys.argv)>1 and '.apk' in  sys.argv[1]:
	#apk路径
	apk_path = sys.argv[1].replace(' ','\ ')
	#创建一个apkInfo对象
	apk_info = ApkInfo(apk_path)
	print '\n'+apk_info.contact_obj2(apk_info)

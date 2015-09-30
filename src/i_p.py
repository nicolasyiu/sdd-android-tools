#!/usr/bin/env python
 # -*- coding: UTF-8 -*-
import os
import sys
from apkinfo import ApkInfo
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
	reload(sys)
	sys.setdefaultencoding(default_encoding)

#程序主逻辑开始
if len(sys.argv)>1 and '.apk' in  sys.argv[1]:
    #apk路径
    apk_path = sys.argv[1].replace(' ','\ ')
    #创建一个apkInfo对象
    apk_info = ApkInfo(apk_path)
    print apk_info.packageName+","+apk_path

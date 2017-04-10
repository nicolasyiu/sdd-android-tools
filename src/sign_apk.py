#!/usr/bin/env python
# -*- coding: UTF-8 -*-   
import os
import sys
import pexpect
import apkinfo
import time

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

input_apk_path = sys.argv[1]
keystore_path = sys.argv[2]
pwd1 = sys.argv[3]
pwd2 = sys.argv[4]

apk_info = apkinfo.ApkInfo(input_apk_path)
output_apk_path = apk_info.appName + "_V" + apk_info.versionName + "_C" + apk_info.versionCode + "_" + apk_info.packageName + "_" + time.strftime(
    "%Y-%m-%d_%H%M%S", time.localtime())

jarsigner = pexpect.spawn(
    "jarsigner -tsa http://timestamp.digicert.com  -digestalg SHA1 -sigalg MD5withRSA -verbose -keystore "+keystore_path+" -signedjar " + output_apk_path + ".apk " + input_apk_path + " "+pwd1)
jarsigner.expect(".*:*")
jarsigner.sendline(pwd2)
jarsigner.expect(pexpect.EOF)

os.system("zipalign -f -v 4 " + output_apk_path + ".apk " + output_apk_path + "_zipaligned.apk")

#!/usr/bin/env python
# -*- coding: UTF-8 -*-   
import os
import sys
import string
import apkinfo

base_path = '';

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


# 替换文件内容
def replaceStr(filename, oldstr, newstr):
    with open(filename, "r") as f:
        d = f.read()
        d = d.replace(oldstr, newstr)
        f.close()
    with open(filename, "w") as fw:
        fw.write(d)
        fw.close()


# 列出所有文件
def listFile(file_path, package_orig, package_new):
    for parent, dirnames, filenames in os.walk(file_path):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        # for dirname in  dirnames:                       #输出文件夹信息
        # print  "#" + dirname

        for filename in filenames:  # 输出文件信息
            path = os.path.join(parent, filename)  # 输出文件路径信息
            if cmp(filename, "AndroidManifest.xml") == 0:
                replaceStr(path, "package=\"" + package_orig + "\"", "package=\"" + package_new + "\"");
                replaceStr(path, "android:name=\".", "android:name=\"" + package_orig + ".")
                print "" + path
            elif filename.endswith("smali"):
                replaceStr(path, package_orig + ".R", package_new + ".R");
                replaceStr(path, package_orig.replace(".", "/") + "/R", package_new.replace(".", "/") + "/R");
            # print "" + path

            elif filename.endswith("xml"):
                replaceStr(path, "http://schemas.android.com/apk/res/" + package_orig,
                           "http://schemas.android.com/apk/res/" + package_new);
            # print "" + path
            elif filename.endswith("yml"):
                replaceStr(path, "cur_package: " + package_orig, "cur_package: " + package_new);
                print "" + path
                # break


# 移动文件内容到合适的位置
def mvFiles(file_path, package_orig, package_new):
    dirname_array = package_new.replace(".", "/").split("/");
    dir_path = file_path + "/smali";
    for name in dirname_array:
        dir_path = dir_path + "/" + name
        os.system("mkdir " + dir_path);

    os.system("mv " + file_path + "/smali/" + package_orig.replace(".",
                                                                   "/") + "/R* " + file_path + "/smali/" + package_new.replace(
        ".", "/") + "/");


# 反编译包
def reverseApk(apk_path):
    os.system("apktool d " + apk_path)


# 程序主逻辑开始
if len(sys.argv) > 1 and '.apk' in sys.argv[1]:
    apk_path = sys.argv[1]
    path_array = apk_path.replace(".apk", "").split('/')
    file_path = path_array[len(path_array) - 1]
    package_new = sys.argv[2]

    apk_info = apkinfo.ApkInfo(apk_path)
    package_orig = apk_info.packageName

    reverseApk(apk_path)
    listFile(file_path, package_orig, package_new)
    mvFiles(file_path, package_orig, package_new)

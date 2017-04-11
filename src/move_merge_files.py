#!/usr/bin/env python
# -*- coding: UTF-8 -*-   
import os
import sys
import string
from xml.etree.ElementTree import ElementTree, Element, Comment

base_path = ''
xmlns_android = "http://schemas.android.com/apk/res/android"
xmlns_android_attrib = "{" + xmlns_android + "}"

# Extra项目的路径
extra_apk_path = sys.argv[1]
extra_file_path = extra_apk_path.replace(".apk", "")

# Target项目的路径
target_apk_path = sys.argv[2]
target_file_path = target_apk_path.replace(".apk", "")

# 存放各个id的键值
id_item_map = {'anim': '0x7f03ffff', 'array': '0x7f0affff', 'attr': '0x7f00ffff', 'bool': '0x7f08ffff',
               'color': '0x7f05ffff', 'dimen': '0x7f09ffff', 'drawable': '0x7f01ffff', 'id': '0x7f06ffff',
               'layout': '0x7f02ffff', 'raw': '0x7f04ffff', 'string': '0x7f06ffff', 'style': '0x7f07ffff'}

# id_item_map = {'anim':'0x7f03ffff','array':'0x7f0affff','attr':'0x7f00ffff','bool':'0x7f08ffff','color':'0x7f05ffff','dimen':'0x7f09ffff','drawable':'0x7f01ffff','id':'0x7f05ffff','layout':'0x7f02ffff','raw':'0x7f04ffff','string':'0x7f06ffff','style':'0x7f07ffff'}


# id_item_map = {'anim':'0x7f03ffff','array':'0x7f0affff','attr':'0x7f00ffff','bool':'0x7f08ffff','color':'0x7f05ffff','dimen':'0x7f09ffff','drawable':'0x7f01ffff','id':'0x7f06ffff','layout':'0x7f05ffff','raw':'0x7f04ffff','string':'0x7f04ffff','style':'0x7f03ffff'}


# target项目的包名
TARGET_PACKAGE_NAME = ""

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


# 查找项目的包名
def get_package_name_in_target():
    try:
        from xml.etree import ElementTree as ET
        manifest_parse = ET.parse(target_file_path + "/AndroidManifest.xml")
        manifest_root = manifest_parse.getroot()
        global TARGET_PACKAGE_NAME
        target_package_name = manifest_root.attrib['package']
        print "\n#### package name is :" + target_package_name
    except Exception, e:
        print "get_package_name_in_target " + str(e)


# 找出public.xml中drawable、layout、id、等的最大值
def find_max_value_in_target(file_path):
    try:
        from xml.etree import ElementTree as ET
        public_parse = ET.parse(file_path);
        items = public_parse.findall('public')
        for item in items:
            for key in id_item_map.keys():
                v_type = item.attrib['type']
                v_id = item.attrib['id']
                v_name = item.attrib['name']
                if cmp(key, v_type) == 0 and cmp(v_id, id_item_map[key]) > 0:
                    id_item_map[key] = item.attrib['id']

    except Exception, e:
        print "find_max_value Error " + str(e);


# 移动相应的文件到对应的目录下
def move_res_file_to_target():
    print "\n#### move_res_file_to_target..."
    # 移动hkc，资源文件
    os.system("mkdir -v " + target_file_path + "/smali")
    os.system("cp -R " + extra_file_path + "/smali/* " + target_file_path + "/smali/")

    # 移动extra资源代码
    os.system("rm -r " + extra_file_path + "/smali/" + TARGET_PACKAGE_NAME.replace(".", "/") + "/R.smali ")
    os.system("rm -r " + extra_file_path + "/smali/" + TARGET_PACKAGE_NAME.replace(".", "/") + "/R\$* ")
    os.system("cp -R " + extra_file_path + "/smali/" + TARGET_PACKAGE_NAME.replace(".",
                                                                                   "/") + "/* " + target_file_path + "/smali/" + TARGET_PACKAGE_NAME.replace(
        ".", "/") + "/")

    # 移动assets目录
    assets_file = os.listdir(extra_file_path + "/assets")
    os.system("mkdir -v " + target_file_path + "/assets/")
    for f in assets_file:
        if f.find("hkc_") == 0:
            os.system("cp " + extra_file_path + "/assets/" + f + " " + target_file_path + "/assets/" + f)

    # 移动libs/armeabi目录
    # armeabis_file = os.listdir(extra_file_path + "/lib/armeabi")
    # os.system("mkdir -v " + target_file_path + "/lib/armeabi/")
    # for f in armeabis_file:
    #     if f.find("libHkc") == 0:
    #         os.system("cp " + extra_file_path + "/lib/armeabi/" + f + " " + target_file_path + "/lib/armeabi/" + f)

    # 移动资源文件
    res_array = os.listdir(extra_file_path + "/res")
    from xml.etree import ElementTree as ET
    for res in res_array:
        # 在目标位置初始化好文件夹
        os.system("mkdir -v " + target_file_path + "/res/" + res)
        # 查询target项目对应的文件目录下有无需要移动的文件
        avaliable_files = os.listdir(extra_file_path + "/res/" + res)
        for f in avaliable_files:
            if f.find("strings.xml") == 0:
                extra_string = ET.parse(extra_file_path + "/res/values/strings.xml")
                extra_string_root = extra_string.getroot()
                string_items = extra_string_root.findall("string")

                target_string = ET.parse(extra_file_path + "/res/values/strings.xml")
                target_string_root = target_string.getroot()

                for item in string_items:
                    if not target_string_root.find("string[name="+item.attrib['name']+"]"):
                        target_string_root.append(item)

                target_string.write(target_file_path + "/res/values/strings.xml", "utf-8", True)

            else:
                os.system("cp " + extra_file_path + "/res/" + res + "/" + f + " " + target_file_path + "/res/" + res + "/" + f)


# 合并public xml
def merge_public_xml():
    try:
        from xml.etree import ElementTree as ET
        # 删除目标项目的public.xml文件
        public_parse = ET.parse(target_file_path + "/res/values/public.xml")
        public_root = public_parse.getroot()
        public_items = public_parse.findall("public")
        for item in public_items:
            v_type = item.attrib['type']
            v_name = item.attrib['name']
            if v_name.find("hkc_") == 0:
                public_root.remove(item)

        # Extra项目的hkc_res.xml文件
        print "\n#### move hkc_res xml..."
        assets_res_parse = ET.parse(target_file_path + "/assets/res.xml")
        res_items = assets_res_parse.findall("public")

        print "\n#### add public items..."
        modifyed_items = []
        for item in res_items:
            v_type = item.attrib['type']
            v_name = item.attrib['name']
            v_id = hex(int(id_item_map[v_type], 16) + 1)
            print "<public type=\"%s\" name=\"%s\" id=\"%s\">" % (v_type, v_name, v_id)
            item.attrib['id'] = v_id
            public_root.append(item)
            modifyed_items.append(item)
            id_item_map[v_type] = v_id

        public_parse.write(target_file_path + "/res/values/public.xml", "utf-8", True)

        # 修改Extra项目的hkc_res文件
        print "\n#### modify hkc_res items..."
        hkc_res_root = assets_res_parse.getroot()
        for item in res_items:
            v_type = item.attrib['type']
            v_name = item.attrib['name']
            if v_name.find("hkc_") == 0:
                hkc_res_root.remove(item)

        for item in modifyed_items:
            v_type = item.attrib['type']
            v_name = item.attrib['name']
            v_id = item.attrib['id']
            print "<public type=\"%s\" name=\"%s\" id=\"%s\">" % (v_type, v_name, v_id)
            hkc_res_root.append(item)

        assets_res_parse.write(target_file_path + "/assets/hkc_res.xml", "utf-8", True)

        print "\n#### add id items..."
        public_parse = ET.parse(target_file_path + "/res/values/public.xml")
        public_root = public_parse.getroot()
        public_items = public_parse.findall("public")

        id_parse = ET.parse(target_file_path + "/res/values/ids.xml")
        id_root = id_parse.getroot()
        id_items = id_parse.findall("item")

        # 查找ids中没有的public资源，
        map_added_public_item = {}
        for public_item in public_items:
            if_id_has_public = ''
            for id_item in id_items:
                if id_item.attrib['name'] == public_item.attrib['name']:
                    if_id_has_public = 'true'
                    break
            if if_id_has_public == '' and map_added_public_item.get(public_item.attrib['name'], '') == '':
                # print "move public item to id item:"+public_item.attrib['name']
                the_item = Element("item", {'type': 'id', 'name': public_item.attrib['name']});
                the_item.text = "false"
                empty_item = Comment("\r\n")
                id_root.append(empty_item)
                # id_root.append(the_item)
                map_added_public_item[public_item.attrib['name']] = 'true'

        id_parse.write(target_file_path + "/res/values/ids.xml", "utf-8", True)

        # 添加自定义的hkc资源
        id_parse = ET.parse(target_file_path + "/res/values/ids.xml")
        id_root = id_parse.getroot()
        id_items = id_parse.findall("item")

        for item in id_items:
            v_type = item.attrib['type']
            v_name = item.attrib['name']
            if v_name.find("hkc_") == 0:
                id_root.remove(item)

        for item in res_items:
            v_type = item.attrib['type']
            v_name = item.attrib['name']

            id_item = Element("item", {'type': 'id', 'name': v_name})
            item_string = "<item type=\"%s\" name=\"%s\">false</item>" % ("id", v_name)
            id_item.text = "false"
            empty_item = Comment("\r\n")
            print item_string
            item.attrib['id'] = v_id
            id_root.append(id_item)
            id_root.append(empty_item)

        id_parse.write(target_file_path + "/res/values/ids.xml", "utf-8", True)

    except Exception, e:
        print "merge_public_xml Error " + str(e);


# 修改styles.xml
def modify_target_styles_xml(style_v=''):
    try:
        from xml.etree import ElementTree as ET
        # 删除目标项目的public.xml文件
        public_parse = ET.parse(target_file_path + "/res/values" + style_v + "/styles.xml");
        public_root = public_parse.getroot()
        public_items = public_parse.findall("style")
        for item in public_items:
            if item.attrib.has_key("parent") <= 0:
                item.attrib['parent'] = ''
        public_parse.write(target_file_path + "/res/values" + style_v + "/styles.xml", "utf-8", True)
    except Exception, e:
        print "modify_target_styles_xml Error " + str(e);


# 获取extra项目所有的hkc-meta-data
def extra_pro_metas(extra_root):
    extra_metas = []
    for meta_data in extra_root.findall('./application/meta-data'):
        md_name = str(meta_data.attrib.get(xmlns_android_attrib + 'name'))
        md_value = str(meta_data.attrib.get(xmlns_android_attrib + 'value'))
        # 如果extra中包含hkc项目的meta-data，将所有的hkc item添加到这个数组中
        # if md_name.find('HKC_') == 0:
        extra_metas.append(meta_data)
        print "extra_meta_data\t", md_name + "\t", md_value
    return extra_metas


# 清除目标项目的meta-data
def clear_target_pro_meta(target_root, target_application):
    target_metas = target_root.findall('./application/meta-data')
    for meta_data in target_metas:
        md_name = str(meta_data.attrib.get(xmlns_android_attrib + 'name'))
        md_value = str(meta_data.attrib.get(xmlns_android_attrib + 'value'))
        # 如果target项目中包含hkc的item，那么要先
        # if md_name.find('HKC_') == 0:
        print "remove target meta\t", md_name + "\t", md_value
        target_application.remove(meta_data)


# 重新添加meta-data到target项目中
def readd_target_pro_meta(target_application, extra_hkc_metas):
    for extra_meta in extra_hkc_metas:
        md_name = str(extra_meta.attrib.get(xmlns_android_attrib + 'name'))
        md_value = str(extra_meta.attrib.get(xmlns_android_attrib + 'value'))
        target_application.append(extra_meta)
        print "add hkc meta to target\t", md_name + "\t", md_value


# 合并hkc-meta
def merge_hkc_meta(extra_root, target_root, target_application):
    print ''
    # 先查找所有的meta_data
    # for meta_data in extra_root.iter('meta-data'):
    extra_hkc_metas = extra_pro_metas(extra_root)

    # 遍历target项目的meta_data，如果包含有hkcitem，那么要将其删除
    clear_target_pro_meta(target_root, target_application)

    # 遍历extra中的hkc_meta_data,将他们全部添加到target项目中去
    readd_target_pro_meta(target_application, extra_hkc_metas)


# 获取extra项目的所有hkcactiviy
def extra_pro_activities(extra_root):
    extra_activitys = []
    for activity in extra_root.findall('./application/activity'):
        ac_name = str(activity.attrib.get(xmlns_android_attrib + 'name'))
        # if ac_name.find('com.hkc.') == 0:
        extra_activitys.append(activity)
        print "extra_activity\t", ac_name + "\t"
    return extra_activitys


# 清除目标项目的hkc activity 和main activity的标记
def clear_target_pro_activity(target_root, target_application):
    target_activitys = target_root.findall('./application/activity')
    for activity in target_activitys:
        ac_name = str(activity.attrib.get(xmlns_android_attrib + 'name'))
        # 如果target项目中包含hkc的item，那么要先
        if ac_name.find('com.hkc.') == 0:
            print "remove target activity\t", ac_name + "\t"
            target_application.remove(activity)
            continue
        # 如果包含有filter为MAIN和LAUNCHER的的activity，将其删除
        intent_filter = activity.find('intent-filter')
        actions = activity.findall('./intent-filter/action')
        categories = activity.findall('./intent-filter/category')

        # if len(actions) > 0 and len(categories) > 0:
        #     main_filter_index = 0
        #     main_action = None
        #     main_category = None
        #     for action in actions:
        #         if action.attrib[xmlns_android_attrib + 'name'] == 'android.intent.action.MAIN':
        #             main_filter_index = main_filter_index + 1
        #             main_action = action
        #     for category in categories:
        #         if category.attrib[xmlns_android_attrib + 'name'] == 'android.intent.category.LAUNCHER':
        #             main_filter_index = main_filter_index + 1
        #             main_category = category
        #     if main_filter_index >= 2:
        #         intent_filter.remove(main_action)
        #         intent_filter.remove(main_category)
        #         print "remove target main activity filter \t", main_action, "\t", main_category


# 重新添加hkc activity到target项目中
def readd_target_pro_activity(target_application, extra_hkc_activities):
    for activity in extra_hkc_activities:
        ac_name = str(activity.attrib.get(xmlns_android_attrib + 'name'))
        target_application.append(activity)
        print "add hkc activity to target\t", ac_name


# 合并hkc-meta
def merge_hkc_activity(extra_root, target_root, target_application):
    print ''
    # 查找所有的extra的所有hkc_activity
    extra_activitys = extra_pro_activities(extra_root)

    # 遍历target项目的activity，如果包含有hkcitem，那么要将其删除
    clear_target_pro_activity(target_root, target_application)

    # 合并activitys
    readd_target_pro_activity(target_application, extra_activitys)


# 获取extra项目的所有hkc service
def extra_pro_services(extra_root):
    extra_services = []
    for service in extra_root.findall('./application/service'):
        ac_name = str(service.attrib.get(xmlns_android_attrib + 'name'))
        # if ac_name.find('com.hkc.') == 0:
        extra_services.append(service)
        print "extra_service\t", ac_name + "\t"
    return extra_services


# 清除目标项目的service
def clear_target_pro_service(target_root, target_application):
    target_services = target_root.findall('./application/service')
    for service in target_services:
        sc_name = str(service.attrib.get(xmlns_android_attrib + 'name'))
        # 如果target项目中包含hkc的item，那么要先
        if sc_name.find('com.hkc.') == 0:
            print "remove target service\t", sc_name + "\t"
            target_application.remove(service)


# 重新添加hkc service到target项目中
def readd_target_pro_service(target_application, extra_hkc_services):
    for service in extra_hkc_services:
        sc_name = str(service.attrib.get(xmlns_android_attrib + 'name'))
        target_application.append(service)
        print "add hkc service to target\t", sc_name


# 合并service
def merge_hkc_services(extra_root, target_root, target_application):
    print ''
    # 查找所有的exta项目中的hkc service
    extra_hkc_services = extra_pro_services(extra_root)
    # 清除目标项目的service
    clear_target_pro_service(target_root, target_application)
    # 重新添加hkc_service 到目标项目
    readd_target_pro_service(target_application, extra_hkc_services)


# 合并extra项目的manifest到target项目
def merge_androidmanifest_xml():
    try:
        from xml.etree import ElementTree as ET
        ET.register_namespace('android', xmlns_android);
        # extra项目
        print extra_file_path + "/AndroidManifest.xml"
        extra_parse = ET.parse(extra_file_path + "/AndroidManifest.xml")
        extra_root = extra_parse.getroot()

        # target项目
        target_parse = ET.parse(target_file_path + "/AndroidManifest.xml")
        target_root = target_parse.getroot()
        target_application = target_root.find("application")

        # 合并两个项目的meta-data
        merge_hkc_meta(extra_root, target_root, target_application)

        # 合并两个项目的activity
        merge_hkc_activity(extra_root, target_root, target_application)

        # 合并两个项目的service
        merge_hkc_services(extra_root, target_root, target_application)

        target_parse.write(target_file_path + "/AndroidManifest.xml", "utf-8", True)

    except Exception, e:
        print "merge_androidmanifest_xml " + str(e)


# 重写生成app的图标
def redefine_app_icon():
    print "\n 重新定义图标: hkc_ic_launcher"
    try:
        from xml.etree import ElementTree as ET
        ET.register_namespace('android', xmlns_android);

        target_parse = ET.parse(target_file_path + "/AndroidManifest.xml")
        target_root = target_parse.getroot()
        target_application = target_root.find("application")
        target_application.attrib[xmlns_android_attrib + "icon"] = "@drawable/hkc_ic_launcher"

        target_parse.write(target_file_path + "/AndroidManifest.xml", "utf-8", True)
    except Exception, e:
        print "redefine_app_icon " + str(e)


# 重写生成app的名字
def redefine_app_name():
    print "\n 重新定义app_name"
    try:
        from xml.etree import ElementTree as ET
        ET.register_namespace('android', xmlns_android);

        # 首先获取extra项目的app_name
        extra_parse = ET.parse(extra_file_path + "/res/values/strings.xml")
        extra_root = extra_parse.getroot()
        extra_strings = extra_root.findall("string")
        extra_app_name = ''
        for string in extra_strings:
            if string.attrib['name'] == 'app_name':
                extra_app_name = string.text
                print "Extra 项目的名字\t" + extra_app_name
                break

        # 修改application的名字
        target_parse = ET.parse(target_file_path + "/AndroidManifest.xml")
        target_root = target_parse.getroot()
        target_application = target_root.find("application")
        orig_name = target_application.attrib[xmlns_android_attrib + "label"]
        print "Target 项目名字:\t" + orig_name
        if ('@' not in orig_name):
            target_application.attrib[xmlns_android_attrib + "label"] = extra_app_name
            print "新app的名字\t" + extra_app_name

        target_parse.write(target_file_path + "/AndroidManifest.xml", "utf-8", True)

        # 修改strings.xml的app的名字
        target_strings_parse = ET.parse(target_file_path + "/res/values/strings.xml")
        target_string_root = target_strings_parse.getroot()
        strings_item = target_string_root.findall("string")
        for string_i in strings_item:
            if orig_name.find(string_i.attrib['name']) == 8:
                print string_i.text + "=>" + extra_app_name
                string_i.text = extra_app_name

        target_strings_parse.write(target_file_path + "/res/values/strings.xml", "utf-8", True)

    except Exception, e:
        print "redefine_app_name " + str(e)


get_package_name_in_target()

find_max_value_in_target(target_file_path + "/res/values/public.xml")

try:
    move_res_file_to_target()
except Exception, e:
    print "move_res_file_to_target Error " + str(e)

try:
    merge_public_xml()
except Exception, e:
    print "merge_public_xml Error " + str(e)

try:
    modify_target_styles_xml()
    modify_target_styles_xml('-v14')
except Exception, e:
    print "modify_target_styles_xml Error " + str(e)

# redefine_app_icon()

# redefine_app_name()

merge_androidmanifest_xml()

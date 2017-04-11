#!/usr/bin/ruby
# coding: utf-8
require 'pathname'
root_path = Pathname.new(File.dirname(__FILE__)).realpath
require "#{root_path}/model/apk_info"
require "#{root_path}/model/change_apk"

apk_path = ARGV[0]
package_new = ARGV[1] #新包名

ChangeApk.new(apk_path,package_new).start

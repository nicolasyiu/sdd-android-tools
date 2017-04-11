#!/usr/bin/ruby
require 'pathname'
root_path = Pathname.new(File.dirname(__FILE__)).realpath
require "#{root_path}/model/apk_info"

apk_info = ApkInfo.new(ARGV[0])
puts apk_info.package_name + "," + ARGV[0]
#!/usr/bin/ruby
# coding: utf-8
require 'pathname'
require 'rexml/document'
root_path = Pathname.new(File.dirname(__FILE__)).realpath
require "#{root_path}/model/move_package"
require "#{root_path}/model/apk_info"
require "#{root_path}/model/change_apk"
require "#{root_path}/model/merge_xml"
require "#{root_path}/model/merge_apk"

MergeApk.new(ARGV[0], ARGV[1], ARGV[2]).start
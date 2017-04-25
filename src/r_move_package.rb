#!/usr/bin/ruby
# coding: utf-8
require 'pathname'
require 'rexml/document'
root_path = Pathname.new(File.dirname(__FILE__)).realpath
require "#{root_path}/model/move_package"

mv = MovePackage.new(ARGV[0])
mv.start(ARGV[1], ARGV[2])
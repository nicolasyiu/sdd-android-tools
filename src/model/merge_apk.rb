# coding: utf-8
class MergeApk

  attr_accessor :src_file_path
  attr_accessor :target_file_path

  attr_accessor :new_package

  def initialize(src_apk_path, target_apk_path, new_package)
    self.new_package = new_package
    ChangeApk.new(src_apk_path, self.new_package).start
    ChangeApk.new(target_apk_path, self.new_package).start
    self.src_file_path = src_apk_path.gsub(".apk", '')
    self.target_file_path = target_apk_path.gsub(".apk", '')
  end

  def start
    puts "start to merge files"
    self.merge_files(self.src_file_path)
  end

  def merge_files(src_path)
    Dir::entries(src_path).each do |filename|
      src_child_path = "#{src_path}/#{filename.gsub("$", "\\$")}"
      target_child_path = "#{src_child_path.gsub(Regexp.new("^#{self.src_file_path}"), self.target_file_path)}"
      if filename=='.' || filename=='..'
        next
      end
      if File.directory?(src_child_path)
        system("[ ! -d #{target_child_path} ] && mkdir #{target_child_path}")
        merge_files(src_child_path)
        next
      end

      #忽略友盟等信息的合并
      if src_child_path.include?("smali/u/aly") ||
          src_child_path.include?("smali/com/umeng") ||
          src_child_path.include?("smali/com/tencent/mm") ||
          src_child_path.include?("smali/android/support") ||
          src_child_path.include?("unknown/com/tencent/mm")
        next
      end

      if !File.exists?(target_child_path)
        system("cp #{src_child_path} #{target_child_path}")
      elsif src_child_path.include?('original/')
      elsif filename.end_with? '.xml'
        # elsif filename=='AndroidManifest.xml'
        MergeXml.new(src_child_path, target_child_path)
      else
      end
    end
  end
end
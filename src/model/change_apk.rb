# coding: utf-8
class ChangeApk
  attr_accessor :apk_path
  attr_accessor :unziped_path
  attr_accessor :old_package
  attr_accessor :new_package
  attr_accessor :apk_info

  def initialize(apk_path, new_package)
    self.apk_path = apk_path
    self.new_package = new_package
    self.unziped_path =self.apk_path.gsub(".apk", "").split('/').last
    self.apk_info = ApkInfo.new(apk_path)
  end

  def start
    system("apktool d #{self.apk_path}")
    content_replace(self.unziped_path, self.apk_info.package_name, self.new_package)
    mv_r_files(self.unziped_path,self.apk_info.package_name,self.new_package)
  end

  #指定路径的文件替换
  def content_replace(path, old_package, new_package)
    Dir::entries(path).each do |filename|
      child_path = path+"/"+filename
      if filename=='.' || filename=='..'
        next
      end
      if File.directory?(child_path)
        content_replace(child_path, old_package, new_package)
        next
      end
      if filename == "AndroidManifest.xml" && !child_path.include?('original')
        file_content_gsub(child_path, "package=\"#{old_package}\"", "package=\"#{new_package}\"")
        file_content_gsub(child_path, "getui.permission.GetuiService.#{old_package}", "getui.permission.GetuiService.#{new_package}")
        file_content_gsub(child_path, "android:authorities=\"downloads.#{old_package}\"", "android:authorities=\"downloads.#{new_package}\"")
        file_content_gsub(child_path, "android:name=\".", "android:name=\"#{old_package}.")
      elsif filename.end_with?("smali")
        file_content_gsub(child_path, "#{old_package}.R", "#{new_package}.R")
        file_content_gsub(child_path, "#{old_package.gsub(".", "/")}/R", "#{new_package.gsub(".", "/")}/R")
      elsif filename.end_with?("xml") && !child_path.include?('original/')
        file_content_gsub(child_path, "http://schemas.android.com/apk/res/#{old_package}",
                          "http://schemas.android.com/apk/res/#{new_package}")
      elsif filename.end_with?("yml")
        file_content_gsub(child_path, "cur_package: #{old_package}", "cur_package: #{new_package}");
      end

    end
  end

  #移动r文件
  def mv_r_files(file_path, old_package, new_package)
    dir_path = file_path + "/smali"
    new_package.gsub(".", "/").split("/").each do |name|
      dir_path = dir_path + "/" + name
      command = "mv #{file_path}/smali/#{old_package.gsub(".", "/")}/R* #{file_path}/smali/#{new_package.gsub( ".", "/")}/"
      system("mkdir " + dir_path)
      puts command
      system(command)
    end
  end

  private
  # 替换文件内容
  def file_content_gsub(filename, oldstr, newstr)
    #system("sed -i \"s/#{oldstr}/#{newstr}/g\" #{filename}")
    contents = []
    File.readlines(filename).each do |line|
      contents << line.gsub(oldstr, newstr)
    end

    File.open(filename, "w+") do |f|
      f.puts contents.join("")
      f.close
    end
  end
end
# coding: utf-8
class MovePackage
  attr_accessor :unziped_path


  def initialize(unziped_path)
    self.unziped_path = unziped_path
  end

  #特定的一些包的冲突的解决（比如两个apk都含有umeng，但版本不同，这时就需要移动下代码文件）
  def start(old_package, new_package)
    dir_path = "#{self.unziped_path}/smali"
    new_package.gsub(".", "/").split("/").each do |name|
      dir_path = "#{dir_path}/#{name}"
      system("mkdir #{dir_path}")
    end
    command = "mv #{self.unziped_path}/smali/#{old_package.gsub(".", "/")}/*  #{self.unziped_path}/smali/#{new_package.gsub(".", "/")}/"
    system(command)
    puts command
    content_replace(self.unziped_path, old_package, new_package)
  end


  #指定路径的文件替换
  def content_replace(path, old_package, new_package)
    Dir::entries(path).each do |filename|
      child_path = "#{path}/#{filename}"
      if filename=='.' || filename=='..'
        next
      end
      if File.directory?(child_path)
        content_replace(child_path, old_package, new_package)
        next
      end
      if !child_path.include?("AndroidManifest.xml")
        if filename.end_with?("smali")
          file_content_gsub(child_path, "#{old_package.gsub(".", "/")}/", "#{new_package.gsub(".", "/")}/")
        elsif filename.end_with?("xml")
          file_content_gsub(child_path, "#{old_package}.", "#{new_package}.")
        end
      end
    end
  end


  private
  # 替换文件内容
  def file_content_gsub(filename, oldstr, newstr)

    puts filename
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